import pygame

pygame.font.init()


class Button(pygame.sprite.Sprite):
    button_font = pygame.font.SysFont('Comic Sans MS', 30)

    def __init__(self, image, font=None, lwd=None, text=None):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.lwd = lwd
        self.text = text
        self.image = image
        self.rect = self.image.get_rect()

    def draw(self, surface, location):
        rect = self.image.get_rect()
        rect.center = location
        self.rect = rect
        surface.blit(self.image, rect)

        if self.font is not None and self.text is not None:
            my_font = pygame.font.SysFont(self.font, self.lwd)
            text_surface = my_font.render(self.text, False, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = location
            surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite
# https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
