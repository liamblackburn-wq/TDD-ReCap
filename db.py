class Duties:
    def __init__(self, name, description):
        self.name = name
        self._description = description

    def equals(self, duty2):
        return self.name == duty2.name

    def description(self):
        return self._description


def call_database():
    pass