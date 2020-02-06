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

    # test_patterns = {
    #     'humidity': "relative humidity .*\d.\d percent",
    #     "moon_phase": "new moon|crescent|quarter|gibbous|full moon",
    #     "pressure": "pressure .*\d.\d inches of mercury",
    #     "rainfall": "no significant rainfall|\d.\d inches",
    #     "temperature": "temperature .*\d.\d degrees",
    #     "wind": "wind .*\d.\d miles per hour"
    # }

    # def setUp(self):
    #     print("setup")
    #
    # def tearDown(self):
    #     print("teardown")

    def test_something(self):
        self.EVENT['request']['intent']['slots']['aspect']['value'] = "something"
        result = weather.weather_handler(self.EVENT, {})

        # pprint.pprint(result)
        self.assertEqual(result['response']['outputSpeech']['text'], "You asked for the something.")
        # self.assertRegexpMatches(
        #     result['response']['outputSpeech']['text'],
        #     self.test_patterns['humidity']
        # )

    # def test_incorrect_app_id(self):
    #     event = copy.deepcopy(self.EVENT)
    #     event['session']['application']['applicationId'] = "foo bar"
    #     with self.assertRaises(ValueError):
    #         weather.weather_handler(event, {})
