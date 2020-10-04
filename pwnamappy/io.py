import csv
from typing import Any, Callable
from pwnamappy.model import Location, Network


class CsvExporter:
    def __init__(self, stream: Callable[[], Any]):
        self._stream: Callable[[], Any] = stream

    def __call__(self, result):
        stream = self._stream()
        writer = csv.writer(stream)
        writer.writerow(
            ['Name', 'Password', 'SSID', 'Latitude', 'Longitude'])
        for (network, location) in result.items():
            writer.writerow([network.name, network.password,
                             network.addr, location.lat, location.lon])
        stream.close()


class CsvImporter:
    def __init__(self, stream):
        self._stream = stream

    def __call__(self):
        result = {}
        reader = csv.reader(self._stream)
        header = reader.__next__()
        name_idx = header.index('Name')
        password_idx = header.index('Password')
        ssid_idx = header.index('SSID')
        lat_idx = header.index('Latitude')
        lon_idx = header.index('Longitude')
        for row in reader:
            if len(row) < 5:
                continue
            network = Network(
                row[ssid_idx], row[name_idx], row[password_idx])
            location = Location(float(row[lat_idx]), float(row[lon_idx]))
            result[network] = location
        return result
