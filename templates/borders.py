class Borders:
    def __init__(self):
        self.rect = None
        self.collide_type = None

    def __int__(self, rect, collide_type):
        self.rect = rect
        self.collide_type = collide_type