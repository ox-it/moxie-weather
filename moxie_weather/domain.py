class Observation(object):

    """Name
    """
    name = ''

    """Temperature
    """
    temperature = 0

    """Wind speed
    """
    wind_speed = 0

    """Wind direction
    """
    wind_direction = ''

    """Pressure
    """
    pressure = 0

    """Outlook
    """
    outlook = None

    """Observed date
    """
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

    """Minimum temperature
    """
    min_temperature = 0

    """Maximum temperature
    """
    max_temperature = 0

    """Outlook
    """
    outlook = None

    """Observed date
    """
    observed_date = None