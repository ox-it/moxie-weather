from flask import url_for, jsonify

from moxie.core.representations import HALRepresentation


class HALWeatherRepresentation(object):

    def __init__(self, observation, forecasts, attribution, last_updated, endpoint):
        self.observation = observation
        self.forecasts = forecasts
        self.attribution = attribution
        self.last_updated = last_updated
        self.endpoint = endpoint

    def as_dict(self):
        values = {}
        if self.observation:
            values['observation'] = self.observation.as_dict()
        else:
            values['observation'] = None
        values['forecasts'] = [f.as_dict() for f in self.forecasts]
        values['_attribution'] = self.attribution
        values['_last_updated'] = self.last_updated
        representation = HALRepresentation(values)
        representation.add_link('self', url_for(self.endpoint))
        return representation.as_dict()

    def as_json(self):
        return jsonify(self.as_dict())