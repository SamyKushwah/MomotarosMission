import pygame
class Screen:
# width, height, backgroung image, windowcaption,
    def __init__(self, w, h, bkd_img, caption):
        self._w = w
        self._h = h
        self._bkdimg = bkd_img
        self._cap = caption

    @property
    def width(self):
        return self._w

    @property
    def height(self):
        return self._h

    @property
    def get_bkd(self):
        return self._bkdimg

    def set_caption(self): #changes the window caption on the top left of the window
        pygame.display.set_caption(self._cap)

    def load_bck_img(self): #loads the background image
        pygame.image.load(self._bkdimg)
        pygame.transform.scale(self._bkdimg, self._w, self._h)

