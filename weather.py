#!/usr/bin/env python
import os

from flask import Flask, render_template
from flask_ask import Ask, statement, question

import secrets
from adafruit_io import AdafruitIO

app = Flask(__name__)
app.config['ASK_APPLICATION_ID'] = secrets.APPLICATION_ID

ask = Ask(app, '/')

@ask.intent('WeatherReport')
def weather_report(aspect):
    text = render_template('test', aspect=aspect)
    # text = F"You asked for the {aspect}."
    return statement(text).simple_card('Weather Report', text)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Ask for various aspects of the weather.'
    return question(speech_text).reprompt(speech_text).simple_card('WeatherReport - Help', speech_text)

@ask.session_ended
def session_ended():
    return "{}", 200

def weather_handler(event, context):
    return ask.run_aws_lambda(event)

if __name__ == '__main__':
    # Allow setting request verification to FALSE for testing purposes.
    if 'ASK_VERIFY_REQUESTS' in os.environ:
            verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
            if verify == 'false':
                app.config['ASK_VERIFY_REQUESTS'] = False

    # app.config['ASK_APPLICATION_ID'] = secrets.APPLICATION_ID
    app.run(debug=True)
