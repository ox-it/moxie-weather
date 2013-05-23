Weather endpoint
================

Endpoint to search and retrieve information about graduate courses. Follows specification of Moxie.

.. http:get:: /weather

    Get weather information

    **Example request**:

    .. sourcecode:: http

		GET /weather HTTP/1.1
		Host: api.m.ox.ac.uk
		Accept: application/json

    **Example response as JSON**:

    .. sourcecode:: http
    
        HTTP/1.1 200 OK
        Content-Type: application/json

        {
          "_last_updated": "2013-04-23T14:50:58.174414",
          "_links": {
            "self": {
              "href": "/weather/"
            }
          },
          "observation": {
            "wind_speed": 9,
            "pressure": 1021,
            "name": "BENSON",
            "outlook_icon": "gc",
            "wind_direction": "WSW",
            "outlook_description": "Cloudy",
            "observed_date": "2013-04-23T13:00:00",
            "temperature": 16.7
          },
          "_attribution": {
            "url": "http://www.metoffice.gov.uk/",
            "title": "MetOffice"
          },
          "forecasts": [
            {
              "name": "OXFORD",
              "outlook_icon": "si",
              "max_temperature": 17.0,
              "outlook_description": "Partly cloudy",
              "min_temperature": 9.0,
              "observed_date": "2013-04-23T00:00:00"
            },
            [...]
          ]
        }

    `outlook_icon` can have the following values:

    * `unk`: Unknown
    * `cs`: Clear night
    * `s`: Sunny day
    * `pc`: Partly cloudy (night)
    * `si`: Partly cloudy
    * `m`: Mist
    * `f`: Fog
    * `gc`: Cloudy / Overcast
    * `lrs`: Light rain shower
    * `d`: Drizzle
    * `lr`: Light rain
    * `hr`: Heavy rain shower
    * `h`: Hail shower
    * `lsn`: Light snow shower
    * `hsn`: Heavy snow shower
    * `tsh`: Thunder shower
    * `tst`: Thunder

    :statuscode 200: resource found
    :statuscode 503: service not available
