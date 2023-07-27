import pygame
import sys
from momotaro.drivers import toolbox
import momotaro.drivers

pygame.font.init()


class TutorialText(pygame.sprite.Sprite):
    my_toolbox = toolbox.Toolbox()

    # loading the font
    font_path = "snapitc.ttf"
    #font_size = 135

    def __init__(self, location, x_min, x_max, y_min = 0, y_max = 1080, dimensions = (100,100), font=font_path, lwd=None, text=None, font_size=30):
        pygame.sprite.Sprite.__init__(self)
        self.done = False
        self.y_min = y_min
        self.y_max = y_max
        self.location = location
        self.x_min = x_min
        self.x_max = x_max
        self.font = font
        self.lwd = lwd
        self.text = text
        self.dimensions = dimensions
        #self.rect = self.image.get_rect()
        self.font_size = font_size
        self.my_font = pygame.font.Font("drivers/" + self.font, self.font_size)
        self.text_surface = self.my_font.render(self.text, False, (195, 52, 39))  # red - 195, 52, 39
        self.text_rect = self.text_surface.get_rect()  # Set text_rect center
        self.text_rect.center = location

    def draw(self, surface, curr_x, curr_y, curr_x_2, curr_y_2):
        if self.font is not None and self.text is not None:
            # creating red text
            '''if curr_x > self.x_max and self.y_min < curr_y < self.y_max:
                self.done = True'''
            if not self.done and self.x_min < curr_x < self.x_max and self.y_min < curr_y < self.y_max or self.x_min < curr_x_2 < self.x_max and self.y_min < curr_y_2 < self.y_max:
                surface.blit(self.text_surface, self.text_rect)

# https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame