from flask import url_for, jsonify

from moxie.core.representations import HALRepresentation


class HALObservationRepresentation(object):

    def __init__(self, observation, endpoint):
        self.observation = observation
        self.endpoint = endpoint

    def as_dict(self):
        representation = HALRepresentation(self.observation.as_dict())
        representation.add_link('self', url_for(self.endpoint))
        return representation.as_dict()

    def as_json(self):
        return jsonify(self.as_dict())