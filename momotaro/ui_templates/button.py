import pygame
import sys
from momotaro.drivers import toolbox
import momotaro.drivers

pygame.font.init()


class Button(pygame.sprite.Sprite):
    my_toolbox = toolbox.Toolbox()

    # loading the font
    font_path = "snapitc.ttf"
    #font_size = 135

    def __init__(self, image, font=font_path, lwd=None, text=None, font_size=135):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.lwd = lwd
        self.text = text
        self.image = image
        self.rect = self.image.get_rect()
        self.font_size = font_size
        self.hover = False
        self.mous_pos = None

        # lose music setup using Ninja Ambush - By Steve Oxen Stringer 2
        sound_path = "audio/menu_select.mp3"
        self.sound = pygame.mixer.Sound(sound_path)
        self.sound.set_volume(0.6)

    def draw(self, surface, location, highlight=False):
        # drawing button
        self.rect.center = location
        surface.blit(self.image, self.rect)

        # text_surface = None
        if self.font is not None and self.text is not None:
            # creating red text
            my_font = pygame.font.Font("drivers/" + self.font, self.font_size)
            text_surface = my_font.render(self.text, False, (195, 52, 39))  # red - 195, 52, 39
            text_rect = text_surface.get_rect()  # Set text_rect center
            text_rect.center = location
            surface.blit(text_surface, text_rect)
            if highlight:
                # seeing if cursor is hovering on button
                mouse_temp = pygame.mouse.get_pos()
                mouse_pos = self.my_toolbox.adjusted_mouse_pos(mouse_temp)
                self.hover = self.rect.collidepoint(mouse_pos)
                if self.hover:
                    # create a different color for cursor text
                    shadow_offset = 0
                    shadow_color = (0, 0, 0)  # Text color (black)
                    shadow_pos = (location[0] + shadow_offset, location[1] + shadow_offset)
                    # creating black text
                    my_font = pygame.font.Font("drivers/" + self.font_path, self.font_size)
                    text_surface = my_font.render(self.text, True, shadow_color)
                    text_rect = text_surface.get_rect()  # Set text_rect center
                    text_rect.center = shadow_pos
                    surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.sound.play()
        return self.rect.collidepoint(mouse_pos)

# https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame