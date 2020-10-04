import requests
from pwnamappy.model import Network
from pwnamappy.model import Location

WIGGLE_NETWORK_DETAIL_URL = 'https://api.wigle.net/api/v2/network/detail'


class ThrottleException(Exception):
    def __repr__(self):
        return "Got throttled :("


class ApiKeyException(Exception):
    def __repr__(self):
        return "Invalid API key :("


class WiggleMapper(object):
    def __init__(self, key: str):
        auth_pair = key.split(':')
        self._username = auth_pair[0]
        self._password = auth_pair[1]

    def __call__(self, net: Network):
        auth = requests.auth.HTTPBasicAuth(self._username, self._password)
        params: dict = {'netid': net.addr}
        r = requests.get(WIGGLE_NETWORK_DETAIL_URL, params=params, auth=auth)
        if r.status_code == 401:
            raise ApiKeyException()
        response_json: dict = r.json()
        if response_json['success'] and len(response_json['results']) > 0:
            result_json = response_json['results'][0]
            lat = result_json['trilat']
            lon = result_json['trilong']
            return Location(lat, lon)
        elif response_json['message'] == 'too many queries today.':
            raise ThrottleException()
        return None
