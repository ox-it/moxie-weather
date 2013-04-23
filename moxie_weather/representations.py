from flask import url_for, jsonify

from moxie.core.representations import HALRepresentation


class HALObservationRepresentation(object):

    def __init__(self, observation, attribution, endpoint):
        self.observation = observation
        self.attribution = attribution
        self.endpoint = endpoint

    def as_dict(self):
        values = self.observation.as_dict()
        values['_attribution'] = self.attribution
        representation = HALRepresentation(values)
        representation.add_link('self', url_for(self.endpoint))
        return representation.as_dict()

    def as_json(self):
        return jsonify(self.as_dict())