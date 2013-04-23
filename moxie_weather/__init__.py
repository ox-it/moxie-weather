from flask import Blueprint

from .views import WeatherView


def create_blueprint(blueprint_name, conf):
    weather_blueprint = Blueprint(blueprint_name, __name__, **conf)
    weather_blueprint.add_url_rule('/', view_func=WeatherView.as_view('weather'))
    return weather_blueprint