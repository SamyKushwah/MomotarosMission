import pygame
import sys
from drivers import toolbox
import drivers

pygame.font.init()


class Button(pygame.sprite.Sprite):
    button_font = pygame.font.SysFont('Comic Sans MS', 30)

    my_toolbox = toolbox.Toolbox()
    # loading the font
    font_path = "snapitc.ttf"
    font_size = 135
    snapitc_font = pygame.font.Font(font_path, font_size)

    def __init__(self, image, font=font_path, lwd=None, text=None):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.lwd = lwd
        self.text = text
        self.image = image
        self.rect = self.image.get_rect()

        self.hover = False
        self.mous_pos = None

    def draw(self, surface, location, highlight = False):
        self.rect.center = location
        surface.blit(self.image, self.rect)

        text_surface = None
        if self.font is not None and self.text is not None:
            my_font = pygame.font.Font("drivers/" + self.font, self.font_size)
            text_surface = my_font.render(self.text, False, (195, 52, 39))  # red - 195, 52, 39
            text_rect = text_surface.get_rect()  # Set text_rect center
            text_rect.center = location
            surface.blit(text_surface, text_rect)
            if highlight:
                mouse_temp = pygame.mouse.get_pos()
                mouse_pos = self.my_toolbox.adjusted_mouse_pos(mouse_temp)
                # mouse_pos = pygame.mouse.get_pos()
                # print(self.rect)
                # print(text_rect)
                self.hover = self.rect.collidepoint(mouse_pos)
                # print(mouse_pos)
                if self.hover:
                    # print(location)
                    # Create a shadow effect for the text
                    shadow_offset = 2  # Offset for the shadow
                    shadow_color = (0, 0, 0)  # Shadow color (black in this example)
                    shadow_pos = (location[0] + shadow_offset, location[1] + shadow_offset)
                    my_font = pygame.font.Font("drivers/" + self.font_path, self.font_size)
                    text_surface = my_font.render(self.text, True, shadow_color)
                    text_rect = text_surface.get_rect()  # Set text_rect center
                    text_rect.center = shadow_pos
                    surface.blit(text_surface, text_rect)
                # print(self.hover)
                # text_surface = my_font.render(self.text, False, (0, 0, 0))
                # text_yellow_rect = text_surface.get_rect()
                # text_rect_prnt = text_yellow_rect if self.hover else text_rect
                '''if self.hover and mouse_pos == self.mouse_pos:
                    self.count += 1
                    if self.count > 10:
                        self.kill()
                else:
                    self.count = 0'''
                # self.mouse_pos = mouse_pos
                # surface.blit(text_surface, text_rect_prnt)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
