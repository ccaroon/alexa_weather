#!/usr/bin/env python

from __future__ import print_function
import requests

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
def get_temp():
    resp = requests.get("https://api.particle.io/v1/devices/230040001847343338333633/tempF?access_token=7b17fde278758834f69736682aedef21c8fb4cce")

    data = resp.json()
    tempF = round(data['result'], 1)

    return tempF

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
    tempF = get_temp()

    speech_output = "The current temperature is " + str(tempF) + " degrees."

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
    # t = get_temp()
    # print(t)

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
