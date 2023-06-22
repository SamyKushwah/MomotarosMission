'''import pygame

class PushBlockObstacle:
    def __init__(self, x, y):
        self.block_image = pygame.image.load("images/ObstacleButtonSprites/PushBlock.png")
        self.scale_factor = 0.5
        self.__width = int(self.block_image.get_width() * self.scale_factor)
        self.__height = int(self.block_image.get_height() * self.scale_factor)
        self.__int_x = x
        self.__int_y = y
        self.__block_rect = self.block_image.get_rect(x=x, y=y)
        self.type = "block"

    def get_rect(self):
        return self.__block_rect

    def move(self,min_x, max_x,direction, list_of_walls):
        for wall in list_of_walls:
            if self.rect.colliderect(wall):
        amount_to_move = 1
        if max_x < self.__block_rect.x + amount_to_move * direction < min_x:
            self.__block_rect.x += amount_to_move * direction
            self.__block_rect.update(self.__block_rect)

    def draw(self, screen):
        self.block_image = pygame.transform.scale(self.block_image, (self.__width, self.__height))
        self.__block_rect = self.block_image.get_rect()
        self.__block_rect.center = (self.__int_x, self.__int_y)
        screen.blit(self.block_image, (self.__int_x - (self.__width / 2), self.__int_y - (self.__height / 2)))'''
