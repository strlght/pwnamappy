import csv
import requests
from pwnamappy.model import Network

WPA_SEC_RETRIEVE_URL = 'https://wpa-sec.stanev.org/?api&dl=1'


def _convert_to_mac_address(addr):
    return ':'.join(addr[i:i + 2] for i in range(0, len(addr), 2))


def _extract_nets_from_strings(values):
    csv_reader = csv.reader(values, delimiter=':')
    processed = set()
    nets = []
    for row in csv_reader:
        if len(row) != 4:
            continue
        raw_addr = row[0]
        if raw_addr in processed:
            continue
        processed.add(raw_addr)
        addr: str = _convert_to_mac_address(raw_addr)
        name: str = row[2]
        password: str = row[3]
        nets.append(Network(addr, name, password))
    return nets


class ApiRetriever:
    def __init__(self, key):
        self._key = key

    def __call__(self):
        cookies = {'key': self._key}
        response = requests.get(WPA_SEC_RETRIEVE_URL, cookies=cookies)
        keys = response.text.split('\n')[::-1]
        return _extract_nets_from_strings(keys)


class FileRetriever:
    def __init__(self, input_stream):
        self._input_steam = input_stream

    def __call__(self):
        return _extract_nets_from_strings(self._input_steam.readlines()[::-1])
