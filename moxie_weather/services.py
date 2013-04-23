import logging
import json

from moxie.core.service import Service
from moxie.core.kv import kv_store

from moxie_weather.domain import Observation


logger = logging.getLogger(__name__)

KEY_OBSERVATION = 'obs'


class WeatherService(Service):

    def __init__(self, providers=None):
        self.provider = self._import_provider(providers.items()[0])

    def import_observation(self):
        observation = self.provider.import_observation()
        kv_store.set(KEY_OBSERVATION, json.dumps(observation.as_dict()))

    def get_observation(self):
        obs = kv_store.get(KEY_OBSERVATION)
        return Observation.from_dict(json.loads(obs))

    def get_attribution(self):
        """Returns a dictionary containing attribution data
        """
        return self.provider.ATTRIBUTION
