import random


class Services:
    def __init__(self):
        self.name = ''
        self.description = ''
        self.hours = ''
        self.url = ''
        self.phones = ''
        self.coordinates = ''
        self.map = ''

    def make_hash(self):
        new_hash = "%032x" % random.getrandbits(128)
        return new_hash

    def make_map(self):
        hash_ = self.make_hash()

        address = 'static/cash/' + hash_ + '.png'
        with open(address, mode='wb') as file:
            file.write(self.map)
        self.map = hash_ + '.png'
