class Observation(object):

    name = ''

    temperature = 0

    wind_speed = 0

    wind_direction = ''

    pressure = 0

    outlook = None

    observed_date = None

    def as_dict(self):
        return {'name': self.name,
                'temperature': self.temperature,
                'wind_speed': self.wind_speed,
                'wind_direction': self.wind_direction,
                'pressure': self.pressure,
                'outlook': self.outlook,
                'observed_date': self.observed_date}

    @staticmethod
    def from_dict(values):
        obs = Observation()
        obs.name = values['name']
        obs.temperature = values['temperature']
        obs.wind_speed = values['wind_speed']
        obs.wind_direction = values['wind_direction']
        obs.pressure = values['pressure']
        obs.outlook = values['outlook']
        obs.observed_date = values['observed_date']
        return obs


class Forecast(object):

    name = ''

    min_temperature = 0

    max_temperature = 0

    outlook = None

    observed_date = None

    def as_dict(self):
        return {'name': self.name,
                'min_temperature': self.min_temperature,
                'max_temperature': self.max_temperature,
                'outlook': self.outlook,
                'observed_date': self.observed_date}

    @staticmethod
    def from_dict(values):
        forecast = Forecast()
        forecast.name = values['name']
        forecast.min_temperature = values['min_temperature']
        forecast.max_temperature = values['max_temperature']
        forecast.outlook = values['outlook']
        forecast.observed_date = values['observed_date']
        return forecast