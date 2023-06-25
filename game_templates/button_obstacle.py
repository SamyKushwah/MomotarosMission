import pygame

class ButtonObstacle:
    def __init__(self, x, y):
        self.button_image = pygame.image.load("images/ObstacleButtonSprites/Button.png")
        #self.fence = pygame.image
        self.scale_factor = 0.5
        self.__width = int(self.button_image.get_width() * self.scale_factor)
        self.__height = int(self.button_image.get_height() * self.scale_factor)
        self.__int_x = x
        self.__int_y = y
        self.__button_rect = self.button_image.get_rect(x=x, y=y)
        self.pushed = False
        self.type = "button"

    def is_pushed(self):
        return self.pushed

    def get_rect(self):
        return self.__button_rect

    def set_pushed(self, push):
        print("Button is pushed!")
        self.pushed = push

    def draw(self, screen):
        self.button_image = pygame.transform.scale(self.button_image, (self.__width, self.__height))
        self.__button_rect = self.button_image.get_rect()
        self.__button_rect.center = (self.__int_x, self.__int_y)
        screen.blit(self.button_image, (self.__int_x - (self.__width / 2), self.__int_y - (self.__height / 2)))
