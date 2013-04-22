from flask import Blueprint, request
from flask.helpers import make_response

from moxie.core.representations import HALRepresentation
from .views import ForecastsView, ObservationView


def create_blueprint(blueprint_name, conf):
    weather_blueprint = Blueprint(blueprint_name, __name__, **conf)

    weather_blueprint.add_url_rule('/', view_func=get_routes)
    weather_blueprint.add_url_rule('/observation',
                                   view_func=ObservationView.as_view('observation'))
    weather_blueprint.add_url_rule('/forecast',
                                   view_func=ForecastsView.as_view('forecast'))
    return weather_blueprint


def get_routes():
    path = request.path
    representation = HALRepresentation({})
    representation.add_curie('hl', 'http://moxie-weather.readthedocs.org/en/latest/http_api/weather.html#{rel}')
    representation.add_link('self', '{bp}'.format(bp=path))
    representation.add_link('hl:observation', '{bp}observation'.format(bp=path), title='Observation')
    representation.add_link('hl:forecast', '{bp}forecast'.format(bp=path), title='Forecast')
    response = make_response(representation.as_json(), 200)
    response.headers['Content-Type'] = "application/json"
    return response
