#!/usr/bin/env python
import arrow
import os
import pprint

from flask import Flask, render_template
from flask_ask import Ask, statement, question

import secrets
from adafruit_io import AdafruitIO

app = Flask(__name__)
app.config['ASK_APPLICATION_ID'] = secrets.APPLICATION_ID
ask = Ask(app, '/')

VALID_ASPECTS = ['temperature', 'humidity']

aio = AdafruitIO(secrets.AIO_USERNAME, secrets.AIO_KEY, "weather-station")
# ------------------------------------------------------------------------------
@ask.intent('WeatherReport')
def weather_report(aspect):
    if aspect in VALID_ASPECTS:
        response = handle_generic(aspect)
    else:
        response = handle_unknown(aspect)

    return statement(response).simple_card('Weather Report', response)

def handle_generic(aspect):
    text = None
    now = arrow.now()

    data = aio.get_data(aspect, fields=['created_at'])
    if data.get('success', False):
        value = data['results'][0]['value']
        # "created_at": "2021-01-10T16:50:37.095Z"
        created_at = arrow.get(data['results'][0]['created_at'])
        data_age = now - created_at
        if data_age.total_seconds() > 60 * 5:
            text = render_template(F"{aspect}_old", value=value, age=created_at.humanize())
        else:
            text = render_template(aspect, value=value)
    else:
        text = render_template('error', feed=data['feed'], error_code=data['code'], error_msg=data['msg'])

    return text

def handle_unknown(aspect):
    return render_template('unknown', aspect=aspect)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Ask for various aspects of the weather.'
    return question(speech_text).reprompt(speech_text).simple_card('WeatherReport - Help', speech_text)

@ask.session_ended
def session_ended():
    return "{}", 200
# ------------------------------------------------------------------------------
# AWS Lambda Entry Point
def weather_handler(event, context):
    return ask.run_aws_lambda(event)
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # Allow setting request verification to FALSE for testing purposes.
    if 'ASK_VERIFY_REQUESTS' in os.environ:
            verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
            if verify == 'false':
                app.config['ASK_VERIFY_REQUESTS'] = False

    app.run(debug=True)
