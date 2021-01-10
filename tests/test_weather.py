import copy
import unittest
import weather
import secrets
import pprint
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
        "temperature": "temperature is currently \d+ degrees",
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

    def test_temperature(self):
        self.EVENT['request']['intent']['slots']['aspect']['value'] = "temperature"
        result = weather.weather_handler(self.EVENT, {})
        
        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            self.test_patterns['temperature']
        )

    def test_humidity(self):
        self.EVENT['request']['intent']['slots']['aspect']['value'] = "humidity"
        result = weather.weather_handler(self.EVENT, {})
        
        self.assertRegexpMatches(
            result['response']['outputSpeech']['text'],
            self.test_patterns['humidity']
        )

    # def test_incorrect_app_id(self):
    #     event = copy.deepcopy(self.EVENT)
    #     event['session']['application']['applicationId'] = "foo bar"
    #     with self.assertRaises(ValueError):
    #         weather.weather_handler(event, {})
