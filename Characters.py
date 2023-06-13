class Characters:#Samy

    def __init__(self, name, x, y):
        self._name = name
        self._x = x
        self._y = y

    @property
    def name(self):
        return self._name

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
