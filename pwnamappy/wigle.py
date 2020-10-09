import base64
import requests
from pwnamappy.model import Network
from pwnamappy.model import Location

_wigle_network_detail_url = 'https://api.wigle.net/api/v2/network/detail'


class ThrottleException(Exception):
    def __repr__(self):
        return 'Got throttled :('


class ApiKeyException(Exception):
    def __repr__(self):
        return 'Invalid API key :('


class WigleMapper:
    def __init__(self, key: str):
        if ':' not in key:
            key = base64.decodebytes(key.encode()).decode()
        auth_pair = key.split(':')
        self._username = auth_pair[0]
        self._password = auth_pair[1]

    def __call__(self, net: Network):
        auth = requests.auth.HTTPBasicAuth(self._username, self._password)
        params: dict = {'netid': net.addr}
        response = requests.get(
            _wigle_network_detail_url, params=params, auth=auth)
        if response.status_code == 401:
            raise ApiKeyException()
        response_json: dict = response.json()
        if response_json['success'] and len(response_json['results']) > 0:
            result_json = response_json['results'][0]
            lat = result_json['trilat']
            lon = result_json['trilong']
            if lat == 0.0 and lon == 0.0:
                return None
            return Location(lat, lon)
        if response_json['message'] == 'too many queries today.':
            raise ThrottleException()
        return None
