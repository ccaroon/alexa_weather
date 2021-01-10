import arrow
import copy
import json
import unittest
import mock

import weather
import secrets

from mocks import MockResponse

class TestWeather(unittest.TestCase):
    EVENT = {
        'request': {
            'type': "IntentRequest",
            'intent': {
                'name': "WeatherReport",
                'slots': {
                    'aspect': {
                        'name': 'aspect',
                        'value': None
                    }
                }
            }
        },
        'session': {
            'new': True,
            'application': {
                'applicationId': secrets.APPLICATION_ID
            }
        }
    }

    test_patterns = {
        'humidity': "humidity is currently \d+ percent",
        'humidity_old': "humidity was \d+ percent \d+ (minutes|hours|days|weeks|months) ago",

        "temperature": "temperature is currently \d+ degrees",
        "temperature_old": "temperature was \d+ degrees \d+ (minutes|hours|days|weeks|months) ago",
    }

    # def setUp(self):
    #     print("setup")
    #
    # def tearDown(self):
    #     print("teardown")


    def test_unknown(self):
        self.EVENT['request']['intent']['slots']['aspect']['value'] = "giant frog fish"
        result = weather.weather_handler(self.EVENT, {})
        self.assertEqual(result['response']['outputSpeech']['text'], "The weather station does not know anything about giant frog fish.")

    @mock.patch('requests.get')
    def test_temperature(self, mock_get):
        resp_content = [{
            'value': 42,
            'created_at': arrow.now().format('YYYY-MM-DDTHH:mm:ss.SSSZ'),
        }]
        mock_get.return_value = MockResponse(status=200, content=json.dumps(resp_content))

        self.EVENT['request']['intent']['slots']['aspect']['value'] = "temperature"
        result = weather.weather_handler(self.EVENT, {})

        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            self.test_patterns['temperature']
        )

    @mock.patch('requests.get')
    def test_temperature_old_data(self, mock_get):
        resp_content = [{
            'value': 42,
            'created_at': arrow.now().shift(minutes=-7).format('YYYY-MM-DDTHH:mm:ss.SSSZ'),
        }]
        mock_get.return_value = MockResponse(status=200, content=json.dumps(resp_content))

        self.EVENT['request']['intent']['slots']['aspect']['value'] = "temperature"
        result = weather.weather_handler(self.EVENT, {})

        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            self.test_patterns['temperature_old']
        )

    @mock.patch('requests.get')
    def test_humidity(self, mock_get):
        resp_content = [{
            'value': 65,
            'created_at': arrow.now().format('YYYY-MM-DDTHH:mm:ss.SSSZ'),
        }]
        mock_get.return_value = MockResponse(status=200, content=json.dumps(resp_content))

        self.EVENT['request']['intent']['slots']['aspect']['value'] = "humidity"
        result = weather.weather_handler(self.EVENT, {})

        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            self.test_patterns['humidity']
        )

    @mock.patch('requests.get')
    def test_humidity(self, mock_get):
        resp_content = [{
            'value': 65,
            'created_at': arrow.now().shift(days=-2).format('YYYY-MM-DDTHH:mm:ss.SSSZ'),
        }]
        mock_get.return_value = MockResponse(status=200, content=json.dumps(resp_content))

        self.EVENT['request']['intent']['slots']['aspect']['value'] = "humidity"
        result = weather.weather_handler(self.EVENT, {})

        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            self.test_patterns['humidity_old']
        )

    @mock.patch('requests.get')
    def test_error(self, mock_get):
        resp_content = {
            'error': "AIO is down for maintenance"
        }
        mock_get.return_value = MockResponse(status=500, content=json.dumps(resp_content))

        self.EVENT['request']['intent']['slots']['aspect']['value'] = "temperature"
        result = weather.weather_handler(self.EVENT, {})

        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            F"weather-station.temperature error. 500. {resp_content['error']}"
        )







#
