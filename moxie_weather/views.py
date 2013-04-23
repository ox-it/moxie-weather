from flask import request

from moxie.core.views import ServiceView, accepts
from moxie.core.representations import HAL_JSON, JSON

from moxie_weather.services import WeatherService
from moxie_weather.representations import HALWeatherRepresentation


class WeatherView(ServiceView):

    def handle_request(self):
        service = WeatherService.from_context()
        self.observation = service.get_observation()
        self.forecasts = service.get_forecasts()
        self.attribution = service.get_attribution()
        self.last_updated = service.get_last_updated()
        return None

    @accepts(HAL_JSON, JSON)
    def as_hal_json(self, result):
        return HALWeatherRepresentation(self.observation, self.forecasts, self.attribution,
                                        self.last_updated, request.url_rule.endpoint).as_json()