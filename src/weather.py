#!/usr/bin/env python

from __future__ import print_function
import requests

PARTICLE_API = "https://api.particle.io/v1/devices"
DEVICE_ID = "230040001847343338333633"
ACCESS_TOKEN = "7b17fde278758834f69736682aedef21c8fb4cce"

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

def get_tempF():
    tempF = get_particle_variable("tempF")
    return round(tempF, 1)
    
def get_rain_per_hour():
    rain = get_particle_variable("rainPerHour")
    return round(rain, 2)
    
def get_moon_illumination():
    percent = get_particle_variable("moonIllume")
    return round(percent,1)

# ---------------------------- Skill Stuffs ------------------------------------
def on_session_started(request, session):
    print("on_session_started")

def on_session_ended(request, session):
    print("on_session_ended")

def on_launch(request, session):
    print("on_launch")

def on_intent(request, session):

    intent = request['intent']
    intent_name = request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WeatherReport":
        return handle_weather(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_ended()
    else:
        raise ValueError("Invalid intent")

# ---------------------------- Handlers ------------------------------------
def handle_weather(intent, session):
    card_title = intent['name']
    tempF = get_tempF()
    rain  = get_rain_per_hour()
    moon  = get_moon_illumination()
    
    speech_output = "The current temperature is " + str(tempF) + " degrees."
    
    moon_statement = ""
    # New Moon = 0%
    if moon <= 0.5:
        moon_statement = "Looks like a New Moon."
    # Crescent < 50%
    elif moon > 0.5 and moon < 50.0:
        moon_statement = "We have a Crescent Moon tonight."
    # Quarter = 50%
    elif moon >= 50.0 and moon <= 50.9:
        moon_statement = "The Moon is One Quarter Illuminated."
    # Gibbous > 50%
    elif moon > 50.9 and moon <= 99.5:
        moon_statement = "We have a Gibbous Moon tonight."
    # Full = 100%
    elif moon > 99.5:
        moon_statement = "Beware the Full Moon."

    if rain >= 0.25:
        speech_output += " It looks like it's been raining."
        
    speech_output += " " + moon_statement

    return build_response(
        None,
        build_speechlet_response(card_title, speech_output, "", True)
    )

def handle_help():
    print("handle_help")

def handle_session_ended():
    card_title = "Session Ended"
    speech_output = "Thanks for using WCNC Weather"
    speechlet_response = build_speechlet_response(card_title, speech_output, None, True)

    return build_response({}, speechlet_response)


# ------------------------------ Lambda Main -----------------------------------
def weather_handler(event, context):

    if (event['session']['application']['applicationId'] != "amzn1.ask.skill.595fb06b-9e5b-481e-bfd1-c137e1d5023c"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started(event['request'], event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

# ---------------------------------- Main --------------------------------------
if __name__ == "__main__":
    event = {
        'request': {
            'type': "IntentRequest",
            'intent': {
                'name': "WeatherReport"
            }
        },
        'session': {
            'new': True,
            'application': {
                'applicationId': 'amzn1.ask.skill.595fb06b-9e5b-481e-bfd1-c137e1d5023c'
            }
        }
    }

    w = weather_handler(event, {})
    print(w)