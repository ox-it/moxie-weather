import logging
import requests
from requests import RequestException
from lxml import etree
from datetime import datetime, date, time

from moxie_weather.domain import Forecast, Observation

logger = logging.getLogger(__name__)


METOFFICE_OUTLOOK_CHOICES = (
    ('NA', 'unk'),
    (0, 'cs'),
    (1, 's'),
    (2, 'pc'),     # night
    (3, 'si'),
    (4, 'unk'),    # DUST ??
    (5, 'm'),
    (6, 'f'),
    (7, 'gc'),     # Medium-level cloud
    (8, 'gc'),     # Low-level cloud
    (9, 'lrs'),    # night
    (10, 'lrs'),
    (11, 'd'),
    (12, 'lr'),
    (13, 'hr'),   # Heavy rain shower (night)??
    (14, 'hr'),   # Heavy rain shower (day)??
    (15, 'hr'),
    (16, 'hr'),   # Sleet shower (night)??
    (17, 'hr'),   # Sleet shower (day)??
    (18, 'hr'),   # Sleet??
    (19, 'h'),   # Hail shower (night)
    (20, 'h'),   # Hail shower (day)
    (21, 'h'),   # Hail
    (22, 'lsn'),   # Light snow shower (night)
    (23, 'lsn'),   # Light snow shower (day)
    (24, 'lsn'),   # Light snow
    (25, 'hsn'),   # Heavy snow shower (night)
    (26, 'hsn'),   # Heavy snow shower (day)
    (27, 'hsn'),   # Heavy snow
    (28, 'tsh'),   # Thundery shower (night)
    (29, 'tsh'),   # Thundery shower (day)
    (30, 'tst'),   # Thunder storm
    (31, 'tst'),   # Tropical storm
    (32, 'unk'),   # NOT USED?
    (33, 'h'),   # Haze
    )


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
            outlooks = dict(METOFFICE_OUTLOOK_CHOICES)
            forecast.outlook = outlooks[int(f['Day']['W'])]
            forecast.observed_date = datetime.combine(fc, time(hour=0))
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
        observation.observed_date = str(datetime.combine(latest_day,
                    time(int(latest_hour)/60)))
        outlooks = dict(METOFFICE_OUTLOOK_CHOICES)
        observation.outlook = outlooks[int(latest['W'])]
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