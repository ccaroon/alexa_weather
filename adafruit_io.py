import requests

class AdafruitIO:
    BASE_URL = "https://io.adafruit.com/api/v2"

    def __init__(self, username, api_key, group):
        self.__username   = username
        self.__key        = api_key
        self.__group_name = group

    def get_data(self, feed, **kwargs):
        feed_name = F"{self.__group_name}.{feed}"

        limit = kwargs.get('limit', 1)
        fields = ['value']
        fields.extend(kwargs.get('fields', []))
        include = ','.join(fields)
        url = F"{AdafruitIO.BASE_URL}/{self.__username}/feeds/{feed_name}/data?limit={limit}&include={include}"
        headers = {'X-AIO-Key': self.__key}

        resp = requests.get(url, headers=headers)

        if resp.status_code == 200:
            output = {
                "success": True,
                "results" : resp.json()
            }
        else:
            output = {
                "success": False,
                "code": resp.status_code,
                "feed": feed_name,
                "msg": resp.json()['error']
            }

        return (output)
