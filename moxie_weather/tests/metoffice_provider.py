import unittest
from datetime import date

from moxie_weather.providers.metoffice import ApiWrapper


class MetOfficeObservationsProviderTest(unittest.TestCase):
    """
    Tests for MetOffice/Observations provider
    """

    def test_scrape_xml_daily_forecasts(self):
        with open('moxie_weather/tests/data/metoffice_forecast_daily.xml') as f:
            content = f.read()
            f.close()

        provider = ApiWrapper(None, None)
        result, location = provider.scrape_xml(content)

        self.assertEqual(location['name'], 'OXFORD')

        # 5 periods
        self.assertEqual(len(result), 5)
        first = result[date(year=2012, month=6, day=8)]
        self.assertIsNotNone(first)
        # 2 reps
        self.assertEqual(len(first), 2)
        self.assertEqual(first['Day']['U'], '2')