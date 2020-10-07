class Network:
    def __init__(self, addr, name, password):
        self._addr = addr
        self._name = name
        self._password = password

    @property
    def addr(self):
        return self._addr

    @property
    def name(self):
        return self._name

    @property
    def password(self):
        return self._password

    def __repr__(self):
        return f'Network({self.addr}, {self.name}, {self.password})'

    def __hash__(self):
        return self._addr.__hash__()

    def __eq__(self, other):
        return self._addr == other._addr


class Location:
    def __init__(self, lat, lon):
        self._lat = lat
        self._lon = lon

    @property
    def lat(self):
        return self._lat

    @property
    def lon(self):
        return self._lon
