import pygame


class Coin:
    def __init__(self, x, y):
        self.coin_image = pygame.image.load("gold_coin.png")
        self.__height = 50
        self.__width = 50
        self.__int_x = x
        self.__int_y = y
        self.__coin_rect = self.coin_image.get_rect(x=x, y=y)
        self.scale_factor = 1 / 7
        self.collected = False

    def is_collected(self):
        return self.collected

    def get_coin_rect(self):
        return self.__coin_rect
