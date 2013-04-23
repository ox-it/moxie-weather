from celery.utils.log import get_task_logger

from moxie import create_app
from moxie.worker import celery

from moxie_weather.services import WeatherService

logger = get_task_logger(__name__)

BLUEPRINT_NAME = 'weather'


@celery.task
def import_weather_observation():
    app = create_app()
    with app.blueprint_context(BLUEPRINT_NAME):
        service = WeatherService.from_context()
        service.import_observation()


@celery.task
def import_weather_forecasts():
    app = create_app()
    with app.blueprint_context(BLUEPRINT_NAME):
        service = WeatherService.from_context()
        service.import_forecasts()