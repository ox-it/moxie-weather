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