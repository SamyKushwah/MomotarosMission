import pygame
import sys
pygame.font.init()
from drivers import toolbox
import drivers


class Button(pygame.sprite.Sprite):
    my_toolbox = toolbox.Toolbox()
    #loading the font
    font_path = "snapitc.ttf"
    font_size = 135
    snapitc_font = pygame.font.Font(font_path, font_size)

    def __init__(self, image, font=font_path, lwd=None, text=None):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.lwd = lwd
        self.text = text
        self.image1 = image
        #self.original_image = image.convert_alpha()
        #self.image = self.original_image
        self.rect = self.image1.get_rect()
        #self.hover_image = self.image.convert_alpha().copy()
        #self.hover_image = self.hover_image.fill()
        #pygame.draw.rect(self.hover_image, (255, 255, 0), self.hover_image.get_rect(), 6)
        self.hover = False
        self.mouse_pos = None

    def draw(self, surface, location, highlight=False):
        #x, y = location
        #self.rect.centerx, self.rect.centery = location

        #rect = self.image1.get_rect()
        self.rect.center = location
        #self.rect = rect
        surface.blit(self.image1, self.rect)
        '''if highlight:
            home_highlight = pygame.image.load("images/pause_screen/homehighlight.png")
            home_highlight = pygame.transform.scale(home_highlight, (self.rect.width, self.rect.height))
            surface.blit(self.image, home_highlight.get_rect())'''
        """if highlight:
            mouse_pos = pygame.mouse.get_pos()
            self.hover = self.rect.collidepoint(mouse_pos)
            print(self.hover)
            self.image = self.hover_image if self.hover else self.original_image
            '''if self.hover and mouse_pos == self.mouse_pos:
                self.count += 1
                if self.count > 10:
                    self.kill()
            else:
                self.count = 0'''
            self.mouse_pos = mouse_pos
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(self.hover_image, (0, 0, 0), self.hover_image.get_rect(), 6)"""
        text_surface = None
        if self.font is not None and self.text is not None:
            my_font = pygame.font.Font("drivers/" + self.font, self.font_size)
            text_surface = my_font.render(self.text, False, (195, 52, 39)) #red - 195, 52, 39
            text_rect = text_surface.get_rect()  # Set text_rect center
            text_rect.center = location
            surface.blit(text_surface, text_rect)
            if highlight:
                mouse_temp = pygame.mouse.get_pos()
                mouse_pos = self.my_toolbox.adjusted_mouse_pos(mouse_temp)
                #mouse_pos = pygame.mouse.get_pos()
                #print(self.rect)
                #print(text_rect)
                self.hover = self.rect.collidepoint(mouse_pos)
                #print(mouse_pos)
                if self.hover:
                    #print(location)
                    # Create a shadow effect for the text
                    shadow_offset = 2  # Offset for the shadow
                    shadow_color = (0, 0, 0)  # Shadow color (black in this example)
                    shadow_pos = (location[0] + shadow_offset, location[1] + shadow_offset)
                    my_font = pygame.font.Font("drivers/" + self.font_path, self.font_size)
                    text_surface = my_font.render(self.text, True, shadow_color)
                    text_rect = text_surface.get_rect()  # Set text_rect center
                    text_rect.center = shadow_pos
                    surface.blit(text_surface, text_rect)
                #print(self.hover)
                #text_surface = my_font.render(self.text, False, (0, 0, 0))
                #text_yellow_rect = text_surface.get_rect()
                #text_rect_prnt = text_yellow_rect if self.hover else text_rect
                '''if self.hover and mouse_pos == self.mouse_pos:
                    self.count += 1
                    if self.count > 10:
                        self.kill()
                else:
                    self.count = 0'''
                #self.mouse_pos = mouse_pos
                #surface.blit(text_surface, text_rect_prnt)


    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
