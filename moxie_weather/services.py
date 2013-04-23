import logging
import json

from moxie.core.service import Service
from moxie.core.kv import kv_store

from moxie_weather.domain import Observation, Forecast


logger = logging.getLogger(__name__)

KEY_OBSERVATION = 'obs'
KEY_FORECASTS = 'forecasts'


class WeatherService(Service):

    def __init__(self, providers=None):
        self.provider = self._import_provider(providers.items()[0])

    def import_observation(self):
        observation = self.provider.import_observation()
        kv_store.set(KEY_OBSERVATION, json.dumps(observation.as_dict()))

    def import_forecasts(self):
        forecasts = self.provider.import_forecasts()
        data = json.dumps([forecast.as_dict() for forecast in forecasts])
        kv_store.set(KEY_FORECASTS, data)

    def get_observation(self):
        obs = kv_store.get(KEY_OBSERVATION)
        return Observation.from_dict(json.loads(obs))

    def get_forecasts(self):
        data = kv_store.get(KEY_FORECASTS)
        forecasts = json.loads(data)
        return [Forecast.from_dict(rs) for rs in forecasts]

    def get_attribution(self):
        """Returns a dictionary containing attribution data
        """
        return self.provider.ATTRIBUTION