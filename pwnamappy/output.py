import csv


class CsvFormatter(object):
    def __init__(self, output):
        self._output = output

    def __call__(self, result):
        writer = csv.writer(self._output)
        writer.writerow(
            ['Name', 'Password', 'Addr', 'Latitude', 'Longitude'])
        for (k, v) in result.items():
            writer.writerow([k.name, k.password, k.addr, v.lat, v.lon])
