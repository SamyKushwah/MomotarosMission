from Characters import Characters #Samy


class momotaro(Characters):
    def __init__(self, name, x, y, health, coins=0):
        super().__init__(name, x, y)
        self._health = health
        self._coins = coins

    @property
    def health(self):
        return self._health

    @property
    def coins(self):
        return self._coins
