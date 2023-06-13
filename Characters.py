class Characters:

    def __init__(self, name, coins=0):
        self._name = name
        self._coins = coins

    @property
    def name(self):
        return self._name

    @property
    def coins(self):
        return self._coins
