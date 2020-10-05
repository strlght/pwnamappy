import csv
from typing import Any, Callable
from pwnamappy.model import Location, Network


class CsvExporter:
    def __init__(self, stream: Callable[[], Any]):
        self._stream: Callable[[], Any] = stream

    def __call__(self, result):
        stream = self._stream()
        try:
            writer = csv.writer(stream)
            writer.writerow(
                ['Name', 'Password', 'BSSID', 'Latitude', 'Longitude'])
            for (network, location) in result.items():
                row = [network.name, network.password, network.addr]
                if location:
                    row.append(location.lat)
                    row.append(location.lon)
                else:
                    row.append('')
                    row.append('')
                writer.writerow(row)
        finally:
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
        ssid_idx = header.index('BSSID')
        lat_idx = header.index('Latitude')
        lon_idx = header.index('Longitude')
        for row in reader:
            if len(row) < 5:
                continue
            network = Network(
                row[ssid_idx], row[name_idx], row[password_idx])
            location = None
            try:
                location = Location(float(row[lat_idx]), float(row[lon_idx]))
            except ValueError:
                pass
            result[network] = location
        return result
