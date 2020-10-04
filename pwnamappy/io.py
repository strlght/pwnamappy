import csv
from pwnamappy.model import Location, Network


class CsvExporter:
    def __init__(self, stream):
        self._stream = stream

    def __call__(self, result):
        writer = csv.writer(self._stream)
        writer.writerow(
            ['Name', 'Password', 'SSID', 'Latitude', 'Longitude'])
        for (network, location) in result.items():
            writer.writerow([network.name, network.password,
                             network.addr, location.lat, location.lon])


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
        for line in reader:
            network = Network(
                line[ssid_idx], line[name_idx], line[password_idx])
            location = Location(float(line[lat_idx]), float(line[lon_idx]))
            result[network] = location
        return result
