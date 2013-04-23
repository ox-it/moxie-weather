import logging
import json
from datetime import datetime

from moxie.core.service import Service
from moxie.core.kv import kv_store

from moxie_weather.domain import Observation, Forecast


logger = logging.getLogger(__name__)

KEY_OBSERVATION = 'observation'
KEY_FORECASTS = 'forecasts'
KEY_UPDATED = 'last_updated'


class WeatherService(Service):

    def __init__(self, providers=None, service_key='weather'):
        """Weather service
        :param providers: list of providers to be used
        :param service_key: identifier of the service, mainly used when storing data
        """
        self.provider = self._import_provider(providers.items()[0])
        self.service_key = service_key

    def import_observation(self):
        """Import observation data from provider
        """
        observation = self.provider.import_observation()
        kv_store.set(self._get_key(KEY_OBSERVATION), json.dumps(observation.as_dict()))
        self._set_last_updated()

    def import_forecasts(self):
        """Import forecasts data from provider
        """
        forecasts = self.provider.import_forecasts()
        data = json.dumps([forecast.as_dict() for forecast in forecasts])
        kv_store.set(self._get_key(KEY_FORECASTS), data)
        self._set_last_updated()

    def get_observation(self):
        """Get observation data from storage
        :return: Observation domain object
        """
        obs = kv_store.get(self._get_key(KEY_OBSERVATION))
        return Observation.from_dict(json.loads(obs))

    def get_forecasts(self):
        """Get forecasts data from storage
        :return: list of Forecast domain object
        """
        data = kv_store.get(self._get_key(KEY_FORECASTS))
        forecasts = json.loads(data)
        return [Forecast.from_dict(rs) for rs in forecasts]

    def get_attribution(self):
        """Returns a dictionary containing attribution data
        """
        return self.provider.ATTRIBUTION

    def get_last_updated(self):
        """Get date of last update
        """
        return kv_store.get(self._get_key(KEY_UPDATED))

    def _get_key(self, key):
        """Get key used in kv store
        :param key: key to format
        :return: key formatted
        """
        return "{app}_{key}".format(app=self.service_key, key=key)

    def _set_last_updated(self):
        """Set the last updated date to now
        """
        kv_store.set(self._get_key(KEY_UPDATED), datetime.now())
