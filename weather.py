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
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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

def handle_weather(intent, session):

    card_title = intent['name']
    tempF = get_temp()
    
    speech_output = "The current temperature is " + str(tempF) + " degrees."

    return build_response(
        None, 
        build_speechlet_response(card_title, speech_output, "", True)
    )

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
    if intent_name == "WhatsTheTemperature":
        return handle_weather(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_ended()
    else:
        raise ValueError("Invalid intent")

def handle_help():
    pass

def handle_session_ended():
    card_title = "Session Ended"
    speech_output = "Thanks for using WCNC Weather"
    speechlet_response = build_speechlet_response(card_title, speech_output, None, True)

    return build_response({}, speechlet_response)


# --------------------------------- Main ---------------------------------------
def weather_handler(event, context):
    # TODO: input skill id
    # if (event['session']['application']['applicationId'] != "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started(event['request'], event['session'])


    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

    
if __name__ == "__main__":
    # t = get_temp()
    # print(t)

    event = {
        'request': {
            'type': "IntentRequest",
            'intent': {
                'name': "WhatsTheTemperature"
            }
        },
        'session': {
            'new': True
        }
    }
    
    w = weather_handler(event, {})
    print(w)
