import logging
import requests
from requests import RequestException
from lxml import etree
from datetime import datetime, date, time

from moxie_weather.domain import Forecast, Observation

logger = logging.getLogger(__name__)


# from http://www.metoffice.gov.uk/media/pdf/3/0/DataPoint_API_reference.pdf
# tuple with icon and description
METOFFICE_OUTLOOK = {
    'NA': ('unk', 'Unknown'),
    0: ('cs', 'Clear night'),
    1: ('s', 'Sunny day'),
    2: ('pc', 'Partly cloudy'),     # night
    3: ('si', 'Partly cloudy'),
    4: ('unk', 'Unknown'),
    5: ('m', 'Mist'),
    6: ('f', 'Fog'),
    7: ('gc', 'Cloudy'),
    8: ('gc', 'Overcast'),
    9: ('lrs', 'Light rain shower'),    # night
    10: ('lrs', 'Light rain shower'),
    11: ('d', 'Drizzle'),
    12: ('lr', 'Light rain'),
    13: ('hr', 'Heavy rain shower'),    # night
    14: ('hr', 'Heavy rain shower'),
    15: ('hr', 'Heavy rain'),
    16: ('hr', 'Sleet shower'),     # night
    17: ('hr', 'Sleet shower'),
    18: ('hr', 'Sleet'),
    19: ('h', 'Hail shower'),       # night
    20: ('h', 'Hail shower'),
    21: ('h', 'Hail'),
    22: ('lsn', 'Light snow shower'),   # night
    23: ('lsn', 'Light snow shower'),
    24: ('lsn', 'Light snow'),
    25: ('hsn', 'Heavy snow shower'),   # night
    26: ('hsn', 'Heavy snow shower'),
    27: ('hsn', 'Heavy snow'),
    28: ('tsh', 'Thunder shower'),   # night
    29: ('tsh', 'Thunder shower'),
    30: ('tst', 'Thunder'),
}


class MetOfficeProvider(object):
    """
    Scrapes MetOffice DataPoint / observations API
    Documentation is available at: http://www.metoffice.gov.uk/public/ddc/datasets-documentation.html#DailyForecast
    TODO: this class should be splitted in two (observations and forecasts).
    """

    ATTRIBUTION = {
        'title': 'MetOffice',
        'url': 'http://www.metoffice.gov.uk/'
    }

    def __init__(self, url, api_key, forecasts_location_id, observations_location_id):
        self.api = ApiWrapper(url, api_key)
        self.forecasts_location_id = forecasts_location_id
        self.observations_location_id = observations_location_id

    def import_forecasts(self):
        forecasts, location = self.api.get_daily_forecasts_by_location(self.forecasts_location_id)
        for fc in forecasts:
            f = forecasts[fc]
            forecast = Forecast()
            forecast.name = location['name']
            forecast.min_temperature = float(f['Night']['Nm'])
            forecast.max_temperature = float(f['Day']['Dm'])
            outlook = METOFFICE_OUTLOOK[int(f['Day']['W'])]
            forecast.outlook_icon = outlook[0]
            forecast.outlook_description = outlook[1]
            forecast.observed_date = datetime.combine(fc, time(hour=0)).isoformat()
            yield forecast

    def import_observation(self):
        observations, location = self.api.get_observations_by_location(self.observations_location_id)
        latest_day = sorted(observations)[-1]
        latest_hour = sorted(observations[latest_day], key=lambda x: int(x))[-1]
        latest = observations[latest_day][latest_hour]
        observation = Observation()
        observation.name = location['name']
        observation.temperature = float(latest['T'])
        observation.wind_speed = int(latest['S'])
        observation.wind_direction = latest['D']
        observation.pressure = int(latest['P'])
        observation.observed_date = datetime.combine(latest_day,
                    time(int(latest_hour)/60)).isoformat()
        outlook = METOFFICE_OUTLOOK[int(latest['W'])]
        observation.outlook_icon = outlook[0]
        observation.outlook_description = outlook[1]
        return observation


class ApiWrapper(object):
    """
    Scrape the XML API
    """

    FORECAST_FRAGMENT_URL = '/wxfcs/all/xml'

    OBSERVATIONS_FRAGMENT_URL = '/wxobs/all/xml'

    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key

    def get_daily_forecasts_by_location(self, location_id):
        url = '{0}/{1}?res=daily'.format(self.FORECAST_FRAGMENT_URL, location_id)
        content = self.do_request(url)
        return self.scrape_xml(content)

    def get_observations_by_location(self, location_id):
        url = '{0}/{1}?res=hourly'.format(
            self.OBSERVATIONS_FRAGMENT_URL,
            location_id,
        )
        content = self.do_request(url)
        return self.scrape_xml(content)

    def do_request(self, fragment):
        """Do a request to the API
        :param fragment: fragment URL to use
        :return: content as string or None
        """
        try:
            response = requests.get('{host}{fragment}&key={key}'.format(host=self.host,
                                                                        fragment=fragment, key=self.api_key))
        except RequestException:
            logger.warning('Error requesting MetOffice', exc_info=True)
            return None
        else:
            return response.content

    def scrape_xml(self, content):
        """Scrape XML from MetOffice DataPoint API.
        Can be used to parse Forecasts/Daily, Forecasts/3hourly, Observations
        Returns a list of representations, information about the location
        """
        xml = etree.fromstring(content)
        location = xml.find('.//Location')
        l = {}
        for k in location.attrib:
            l[k] = location.attrib[k]
        periods = xml.findall('.//Period')
        p = {}
        for period in periods:
            date_val = period.get('value')
            date_parsed = date(year=int(date_val[0:4]),
                month=int(date_val[5:7]), day=int(date_val[8:10]))
            p[date_parsed] = {}
            reps = period.findall('.//Rep')
            for rep in reps:
                # rep.txt represents the number of minutes since midnight
                p[date_parsed][rep.text] = {}
                # set of attributes depends on type forecasts vs. observations,
                # but also if it's a forecast for the day or night (e.g. min temperature is
                # only available for a night forecast...
                for k in rep.attrib:
                    p[date_parsed][rep.text][k] = rep.attrib[k]
        return p, l