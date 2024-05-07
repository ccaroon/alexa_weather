import arrow
import json
import unittest
import unittest.mock

from ask_sdk_model.slot import Slot
from ask_sdk_model.intent import Intent
from ask_sdk_model.intent_request import IntentRequest
from ask_sdk_model.launch_request import LaunchRequest
from ask_sdk_model.session_ended_request import SessionEndedRequest
from ask_sdk_model.request_envelope import RequestEnvelope
from ask_sdk_core.handler_input import HandlerInput

import weather_station

from mocks import MockResponse

class TestWeatherStation(unittest.TestCase):
    SLOTS = {
        "temperature": Slot(name="aspect", value="temperature"),
        "humidity": Slot(name="aspect", value="humidity"),
        "unknown": Slot(name="aspect", value="giant fish frog")
    }

    test_patterns = {
        'humidity': r"humidity is currently \d+ percent",
        'humidity_old': r"humidity was \d+ percent \d+ (minutes|hours|days|weeks|months) ago",

        "temperature": r"temperature is currently \d+ degrees",
        "temperature_old": r"temperature was \d+ degrees \d+ (minutes|hours|days|weeks|months) ago",

        "unknown": "does not know anything about giant fish frog"
    }


    def __build_handler_input(self, aspect):
        intent = Intent(
            "WeatherReport",
            slots={
                "aspect": self.SLOTS.get(aspect)
            }
        )
        request = IntentRequest(intent=intent)
        handler_input = HandlerInput(
            RequestEnvelope(request=request)
        )
        return handler_input


    def test_launch_request(self):
        handler_input = HandlerInput(
            RequestEnvelope(request=LaunchRequest())
        )

        result = weather_station.launch_request_handler(handler_input)
        self.assertRegex(
            result.output_speech.ssml,
            r"Welcome to The Weather Station Version \d\.\d\.\d"
        )


    def test_help_request(self):
        intent = Intent(
            "AMAZON.HelpIntent"
        )
        request = IntentRequest(intent=intent)
        handler_input = HandlerInput(
            RequestEnvelope(request=request)
        )

        result = weather_station.help_intent_handler(handler_input)
        self.assertRegex(
            result.output_speech.ssml,
            "The Weather Station can report the following:"
        )


    def test_cancel_stop_request(self):
        intent = Intent(
            "AMAZON.CancelIntent"
        )
        request = IntentRequest(intent=intent)
        handler_input = HandlerInput(
            RequestEnvelope(request=request)
        )

        result = weather_station.cancel_and_stop_intent_handler(handler_input)
        self.assertRegex(
            result.output_speech.ssml,
            "Thanks for using the Weather Station. Goodbye!"
        )


    def test_session_ended_handler(self):
        handler_input = HandlerInput(
            RequestEnvelope(request=SessionEndedRequest())
        )

        result = weather_station.session_ended_request_handler(handler_input)
        self.assertIsNone(result.output_speech)


    def test_unknown(self):
        handler_input = self.__build_handler_input("unknown")
        result = weather_station.weather_report_handler(handler_input)

        self.assertRegex(
            result.output_speech.ssml,
            self.test_patterns['unknown']
        )


    def test_all_exception_handler(self):
        handler_input = self.__build_handler_input("humidity")
        result = weather_station.all_exception_handler(handler_input, RuntimeError("Frog Blast the Vent Core!"))

        self.assertRegex(
            result.output_speech.ssml,
            "Sorry, I didn't get it. Can you please say it again!!"
        )


    @unittest.mock.patch('requests.get')
    def test_temperature(self, mock_get):
        resp_content = [{
            'value': 42,
            'created_at': arrow.now().format('YYYY-MM-DDTHH:mm:ss.SSSZ'),
        }]
        mock_get.return_value = MockResponse(status=200, content=json.dumps(resp_content))

        handler_input = self.__build_handler_input("temperature")
        result = weather_station.weather_report_handler(handler_input)

        self.assertRegex(
            result.output_speech.ssml,
            self.test_patterns['temperature']
        )


    @unittest.mock.patch('requests.get')
    def test_temperature_old_data(self, mock_get):
        resp_content = [{
            'value': 42,
            'created_at': arrow.now().shift(minutes=-7).format('YYYY-MM-DDTHH:mm:ss.SSSZ'),
        }]
        mock_get.return_value = MockResponse(status=200, content=json.dumps(resp_content))

        handler_input = self.__build_handler_input("temperature")
        result = weather_station.weather_report_handler(handler_input)

        self.assertRegex(
            result.output_speech.ssml,
            self.test_patterns['temperature_old']
        )


    @unittest.mock.patch('requests.get')
    def test_humidity(self, mock_get):
        resp_content = [{
            'value': 65,
            'created_at': arrow.now().format('YYYY-MM-DDTHH:mm:ss.SSSZ'),
        }]
        mock_get.return_value = MockResponse(status=200, content=json.dumps(resp_content))

        handler_input = self.__build_handler_input("humidity")
        result = weather_station.weather_report_handler(handler_input)

        self.assertRegex(
            result.output_speech.ssml,
            self.test_patterns['humidity']
        )


    @unittest.mock.patch('requests.get')
    def test_humidity(self, mock_get):
        resp_content = [{
            'value': 65,
            'created_at': arrow.now().shift(days=-2).format('YYYY-MM-DDTHH:mm:ss.SSSZ'),
        }]
        mock_get.return_value = MockResponse(status=200, content=json.dumps(resp_content))

        handler_input = self.__build_handler_input("humidity")
        result = weather_station.weather_report_handler(handler_input)

        self.assertRegex(
            result.output_speech.ssml,
            self.test_patterns['humidity_old']
        )


    @unittest.mock.patch('requests.get')
    def test_error(self, mock_get):
        resp_content = {
            'error': "AIO is down for maintenance"
        }
        mock_get.return_value = MockResponse(status=500, content=json.dumps(resp_content))

        handler_input = self.__build_handler_input("temperature")
        result = weather_station.weather_report_handler(handler_input)

        self.assertRegex(
            result.output_speech.ssml,
            F"weather-station.temperature error. 500. {resp_content['error']}"
        )
