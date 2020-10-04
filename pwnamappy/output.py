import csv


class CsvFormatter:
    def __init__(self, output):
        self._output = output

    def __call__(self, result):
        writer = csv.writer(self._output)
        writer.writerow(
            ['Name', 'Password', 'Addr', 'Latitude', 'Longitude'])
        for (network, location) in result.items():
            writer.writerow([network.name, network.password,
                             network.addr, location.lat, location.lon])
