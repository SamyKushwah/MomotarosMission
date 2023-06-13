class Characters:#Samy

    def __init__(self, name, x, y, char_speed):
        #might need a velocity x and velocity y to update x and y pos
        #self._x += self._vel_x
        self._name = name
        self._x = x
        self._y = y
        self._char_speed = char_speed

    @property
    def name(self):
        return self._name

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def char_speed(self):
        return self._char_speed

    def move_left(self):
        self._x -= self._char_speed
        #mvoing left is decreasing the x position

    def move_right(self):
        self._x += self._char_speed

    def move_up(self):
        self._y -= self._char_speed
        #subtracting bc top left corner is 0,0 so up is closer to 0 and down is adding to 0

    def move_down(self):
        self._y += self._char_speed