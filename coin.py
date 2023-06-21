import pygame


class Coin:
    def __init__(self, x, y):
        self.coin_image = pygame.image.load("gold_coin.png")
        self.scale_factor = 1 / 5
        self.__width = int(self.coin_image.get_width() * self.scale_factor)
        self.__height = int(self.coin_image.get_height() * self.scale_factor)
        self.__int_x = x
        self.__int_y = y
        self.__coin_rect = self.coin_image.get_rect(x=x, y=y)
        self.collected = False

    def is_collected(self):
        return self.collected

    def get_coin_rect(self):
        return self.__coin_rect

    def set_collected(self, collect):
        self.collected = collect

    def draw_coin(self, screen):
        #self.__int_x = 400
        #self.__int_y = 768 - 300
        # new

        self.coin_rect = pygame.Rect(self.__int_x, self.__int_y, self.coin_image.get_width(),
                                           self.coin_image.get_height())
        self.coin_rect.scale_by_ip(self.scale_factor, self.scale_factor)
        self.coin_image = pygame.transform.scale(self.coin_image, (self.__width, self.__height))
        print(self.coin_image.get_height())
        #
        screen.blit(self.coin_image, (self.__int_x, self.__int_y))
        pygame.display.flip()
