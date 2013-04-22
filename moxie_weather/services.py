import logging

from moxie.core.service import Service
from moxie.core.kv import kv_store


logger = logging.getLogger(__name__)


class WeatherService(Service):

    def __init__(self, providers=None):
        self.provider = self._import_provider(providers.items()[0])

    def import_observation(self):
        observation = self.provider.import_observation()

    def get_observation(self):
        return self.provider.import_observation()


    def search(self, query, medium):
        """Search in provider
        :param query: query
        :param medium: medium (email, tel)
        :return: list of domain objects
        """
        return self.searcher.search(query, medium)