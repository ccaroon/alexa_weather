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
handler = sb.lambda_handler()
