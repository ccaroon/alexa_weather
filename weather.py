#!/usr/bin/env python

from __future__ import print_function
import requests

PARTICLE_API = "https://api.particle.io/v1/devices"
DEVICE_ID = "230040001847343338333633"
ACCESS_TOKEN = "7b17fde278758834f69736682aedef21c8fb4cce"
APPLICATION_ID = "amzn1.ask.skill.595fb06b-9e5b-481e-bfd1-c137e1d5023c"

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# ----------------------- Do some REAL work ------------------------------------
def get_particle_variable(name):
    resp = requests.get("%s/%s/%s?access_token=%s" % (PARTICLE_API, DEVICE_ID, name, ACCESS_TOKEN))

    if resp.raise_for_status() == None:
        data = resp.json()

    if data['error'] != None:
        raise ValueError("Failed to retrieve value for %s: %s" % (name, data['error']))

    return(data['result'])

def get_humidity():
    humidity = get_particle_variable("humidity")
    return round(humidity, 1)

def get_tempF():
    tempF = get_particle_variable("tempF")
    # My weather station's temperature is currently off by around 9 degrees b/c it
    # does not get enough airflow. I'll just correct it here for now until I can
    # figure out how to solve the airflow issue
    tempF -= 9.0
    return round(tempF, 1)

def get_pressure():
    # Pascals
    pressure_pa = get_particle_variable("pressurePa")
    
    # Convert to Inches of Mercury
    pressure_inhg = pressure_pa * 0.0002953

    return round(pressure_inhg, 1)

def get_rain_per_hour():
    rain = get_particle_variable("rainPerHour")
    return round(rain, 2)
    
def get_rain_per_day():
    rain = get_particle_variable("rainPerDay")
    return round(rain, 2)

def get_moon_illumination():
    percent = get_particle_variable("moonIllume")
    return round(percent,1)

# ---------------------------- Skill Stuffs ------------------------------------
def on_session_started(request, session):
    pass

def on_session_ended(request, session):
    pass

def on_launch(request, session):
    pass

def on_intent(request, session):

    intent = request['intent']
    intent_name = request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WeatherReport":
        return handle_weather_report(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_ended()
    else:
        raise ValueError("Invalid intent")

# ---------------------------- Handlers ------------------------------------
def handle_weather_report(intent, session):
    card_title = intent['name']

    aspect = intent['slots']['aspect']['value']

    speech_output = ""
    if aspect == "humidity":
        speech_output = handle_humidity()
    elif aspect == "moon phase":
        speech_output = handle_moon_phase()
    elif aspect == "pressure":
        speech_output = handle_pressure()
    elif aspect == "rainfall":
        speech_output = handle_rainfall()
    elif aspect == "temperature":
        speech_output = handle_temperature()
    elif aspect == "weather":
        speech_output = handle_weather()
    else:
        speech_output = "The WeatherStation does not know anything about " + str(aspect)

    return build_response(
        None,
        build_speechlet_response(card_title, speech_output, "", True)
    )

def handle_humidity():
    humidity = get_humidity()
    humidity_stmt = "The relative humidity is currently %0.1f percent." % (humidity)
    return humidity_stmt

# TODO: Add ability to determine Waxing and Waning
def handle_moon_phase():
    moon = get_moon_illumination()

    illume_stmt = "at %0.1f percent illumination." % (moon)

    moon_statement = ""
    # New Moon = 0%
    if moon <= 0.5:
        moon_statement += "Looks like a New Moon."
    # Crescent < 50%
    elif moon > 0.5 and moon < 50.0:
        moon_statement += "The Moon is Crescent " + illume_stmt
    # Quarter = 50%
    elif moon >= 50.0 and moon <= 50.9:
        moon_statement += "The Moon is One Quarter Illuminated."
    # Gibbous > 50%
    elif moon > 50.9 and moon <= 99.5:
        moon_statement += "The Moon is Gibbous " + illume_stmt
    # Full = 100%
    elif moon > 99.5:
        moon_statement += "Beware the Full Moon."

    return moon_statement

# TODO: Add ability to determine Rising for Falling
def handle_pressure():
    pressure = get_pressure()
    pressure_stmt = "The pressure is currently at %0.1f inches of mercury." % (pressure)
    return (pressure_stmt)

def handle_rainfall():
    rain_h = get_rain_per_hour()
    rain_d = get_rain_per_day()

    if rain_h < 0.25:
        rain_statement = "There has been no rainfall in the last hour."
    else:
        rain_statement = "It has rained %0.2f inches in the last hour." % (rain_h)

    if rain_d >= 0.25:
        rain_statement += " Today's total rain accumulation is %0.2f inches." % (rain_d)

    return rain_statement

def handle_temperature():
    tempF = get_tempF()

    temperature_statement = "The temperature is currently %0.1f degrees." % (tempF)

    return temperature_statement

# Report ALL aspects of the weather
def handle_weather():
    # Temperature
    weather_statement = handle_temperature()

    # Rainfall
    rain_h = get_rain_per_hour()
    if rain_h >= 0.25:
        weather_statement += " It looks like it's been raining."
        
    rain_d = get_rain_per_day()
    if rain_d >= 0.25:
        weather_statement += " Total rain accumulation is %0.2f inches." % (rain_d)
    
    # Humidity
    weather_statement += " " + handle_humidity()
    
    # Pressure
    weather_statement += " " + handle_pressure()

    # Moon
    weather_statement += " " + handle_moon_phase()

    return (weather_statement)

def handle_help():
    print("handle_help")

def handle_session_ended():
    card_title = "Session Ended"
    speech_output = "Thanks for using WCNC Weather"
    speechlet_response = build_speechlet_response(card_title, speech_output, None, True)

    return build_response({}, speechlet_response)


# ------------------------------ Lambda Main -----------------------------------
def weather_handler(event, context):

    if (event['session']['application']['applicationId'] != APPLICATION_ID):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started(event['request'], event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
