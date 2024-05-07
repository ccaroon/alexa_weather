#!/usr/bin/env python
import arrow

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model.ui import SimpleCard

from adafruit_io import AdafruitIO
import secrets
import version

VALID_ASPECTS = ['temperature', 'humidity']

SPEECH_TEMPLATES = {
    "error": "{feed} error. {error_code}. {error_msg}.",
    "unknown": "The weather station does not know anything about {aspect}.",
    "humidity": "The relative humidity is currently {value} percent.",
    "humidity_old": "The relative humidity was {value} percent {age}.",
    "temperature": "The temperature is currently {value} degrees.",
    "temperature_old": "The temperature was {value} degrees {age}."
}

sb = SkillBuilder()
aio = AdafruitIO(secrets.AIO_USERNAME, secrets.AIO_KEY, "weather-station")
# ------------------------------------------------------------------------------
# LaunchRequest Handler
# ------------------------------------------------------------------------------
@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    speech_text = f"Welcome to The Weather Station Version {version.VERSION}"

    handler_input.response_builder.speak(
        speech_text
    ).set_card(
        SimpleCard("Weather Station", speech_text)
    ).set_should_end_session(False)
    
    return handler_input.response_builder.response
# ------------------------------------------------------------------------------
# WeatherReport Intent Handler
# ------------------------------------------------------------------------------
@sb.request_handler(can_handle_func=is_intent_name("WeatherReport"))
def weather_report_handler(handler_input):
    intent = handler_input.request_envelope.request.intent
    aspect = intent.slots.get("aspect").value
    
    if aspect in VALID_ASPECTS:
        speech_text = request_weather_data(aspect)
    else:
        template = SPEECH_TEMPLATES.get("unknown")
        tmpl_data = {
            "aspect": aspect
        }
        speech_text = template.format_map(tmpl_data)

    handler_input.response_builder.speak(
        speech_text
    ).set_card(
        SimpleCard("Weather Station", speech_text)
    ).set_should_end_session(True)
    
    return handler_input.response_builder.response
# ------------------------------------------------------------------------------
def request_weather_data(aspect):
    text = None
    now = arrow.now()

    data = aio.get_data(aspect, fields=['created_at'])
    if data.get('success', False):
        value = data['results'][0]['value']
        # "created_at": "2021-01-10T16:50:37.095Z"
        created_at = arrow.get(data['results'][0]['created_at'])
        data_age = now - created_at
        if data_age.total_seconds() > 60 * 5:
            template = SPEECH_TEMPLATES.get(f"{aspect}_old")
            tmpl_data = {
                "value": value,
                "age": created_at.humanize()
            }
            text = template.format_map(tmpl_data)
        else:
            template = SPEECH_TEMPLATES.get(aspect)
            tmpl_data = {
                "value": value
            }
            text = template.format_map(tmpl_data)
    else:
        template = SPEECH_TEMPLATES["error"]
        tmp_data = {
            "feed": data["feed"],
            "error_code": data["code"],
            "error_msg": data["msg"]
        }
        text = template.format_map(tmp_data)

    return text
# ------------------------------------------------------------------------------
# HelpIntent Handler
# ------------------------------------------------------------------------------
@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    help_text = f"The Weather Station can report the following: {','.join(VALID_ASPECTS)}."
    ask_text = "Ask me to 'get the temperature'."

    handler_input.response_builder.speak(
        help_text
    ).ask(ask_text).set_card(
        SimpleCard("Weather Station", help_text)
    )
    
    return handler_input.response_builder.response
# ------------------------------------------------------------------------------
# Cancel/Stop Handler
# ------------------------------------------------------------------------------
@sb.request_handler(
    can_handle_func=lambda handler_input :
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    speech_text = "Thanks for using the Weather Station. Goodbye!"

    handler_input.response_builder.speak(
        speech_text
    ).set_card(
        SimpleCard("Weather Station", speech_text)
    ).set_should_end_session(True)
    
    return handler_input.response_builder.response
# ------------------------------------------------------------------------------
# Session End Handler
# ------------------------------------------------------------------------------
@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    # Any cleanup logic goes here
    return handler_input.response_builder.response
# ------------------------------------------------------------------------------
# Session End Handler
# ------------------------------------------------------------------------------
@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    # Log the exception in CloudWatch Logs
    print(exception)

    speech_text = "Sorry, I didn't get it. Can you please say it again!!"
    handler_input.response_builder.speak(speech_text).ask(speech_text)
    return handler_input.response_builder.response
# ------------------------------------------------------------------------------
# Create Lambda Handler
# ------------------------------------------------------------------------------
handler = sb.lambda_handler()
