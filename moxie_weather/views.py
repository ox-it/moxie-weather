from flask import request

from moxie.core.views import ServiceView, accepts
from moxie.core.representations import HAL_JSON, JSON

from moxie_weather.services import WeatherService
from moxie_weather.representations import HALObservationRepresentation


class ObservationView(ServiceView):

    def handle_request(self):
        service = WeatherService.from_context()
        data = service.get_observation()
        self.attribution = service.get_attribution()
        return data

    @accepts(HAL_JSON, JSON)
    def as_hal_json(self, result):
        return HALObservationRepresentation(result, self.attribution, request.url_rule.endpoint).as_json()


class ForecastsView(ServiceView):
    pass