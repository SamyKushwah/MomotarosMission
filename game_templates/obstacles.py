import pygame

class Obstacle:
    def __init__(self, x, y):
        self.button_image = pygame.image.load("images/ObstacleButtonSprites/Button.png").convert_alpha()
        self.scale_factor = 1
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
        #print("Button is pushed!")
        self.pushed = push

    def draw(self, screen):
        self.button_image = pygame.transform.scale(self.button_image, (self.__width, self.__height))
        self.__button_rect = self.button_image.get_rect()
        self.__button_rect.center = (self.__int_x, self.__int_y)
        screen.blit(self.button_image, (self.__int_x - (self.__width / 2), self.__int_y - (self.__height / 2)))

class ButtonObstacle(Obstacle):
    def __init__(self, button_position, fence_int_position, fence_final_position, x, y, fence_dimensions):
        super().__init__(x, y)
        self.button_image = pygame.image.load("images/ObstacleButtonSprites/Button.png").convert_alpha()
        self.fence = Fence(fence_int_position, fence_final_position, fence_dimensions)
        self.scale_factor = 0.5
        self.__width = int(self.button_image.get_width() * self.scale_factor)
        self.__height = int(self.button_image.get_height() * self.scale_factor)
        self.__int_x = button_position[0]
        self.__int_y = button_position[1]
        self.__button_rect = self.button_image.get_rect(x=self.__int_x, y=self.__int_y)
        self.pushed = False
        self.fence_velocity = (self.fence.initial[1] - self.fence.target[1]) / abs(
            self.fence.initial[1] - self.fence.target[1])
        self.type = "button"
        self.velocity = (0,0)


    def is_pushed(self):
        return self.pushed

    def get_rect(self):
        return self.__button_rect

    def set_pushed(self, push):
        self.pushed = push

    def draw(self, screen):
        self.button_image = pygame.transform.scale(self.button_image, (self.__width, self.__height))
        self.__button_rect = self.button_image.get_rect()
        self.__button_rect.center = (self.__int_x, self.__int_y)
        screen.blit(self.button_image, (self.__int_x - (self.__width / 2), self.__int_y - (self.__height / 2)))
        self.move_fence_to_new_pos()
        self.fence.draw(screen)

    def move_fence_to_new_pos(self):
        if self.is_pushed():
            if self.fence_velocity > 0:
                if self.fence.target[1] < self.fence.y:
                    self.fence.y -= self.fence_velocity
            else:
                if self.fence.target[1] > self.fence.y:
                    self.fence.y -= self.fence_velocity
        else:
            if self.fence_velocity > 0:
                if self.fence.initial[1] > self.fence.y:
                    self.fence.y += self.fence_velocity
            else:
                if self.fence.initial[1] < self.fence.y:
                    self.fence.y += self.fence_velocity

class Fence:
    def __init__(self, fence_position, fence_ending_position, fence_dimensions):
        self.fence_image = pygame.image.load("images/ObstacleButtonSprites/WoodFence.png").convert_alpha()
        self.fence_image = pygame.transform.scale(self.fence_image, fence_dimensions)
        self.scale_factor = 1
        self.__width = int(self.fence_image.get_width() * self.scale_factor)
        self.__height = int(self.fence_image.get_height() * self.scale_factor)
        self.initial = fence_position
        self.target = fence_ending_position
        self.x = fence_position[0]
        self.y = fence_position[1]
        self.__fence_rect = self.fence_image.get_rect(x=self.x, y=self.y)
        self.type = "fence"
        self.velocity = (0,0)

    def draw(self, screen):
        self.fence_image = pygame.transform.scale(self.fence_image, (self.__width, self.__height))
        self.__fence_rect = self.fence_image.get_rect()
        self.__fence_rect.center = (self.x, self.y)
        screen.blit(self.fence_image, (self.x - (self.__width / 2), self.y - (self.__height / 2)))

    def get_rect(self):
        return self.__fence_rect

class ToriObstacle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.button_image = pygame.image.load("images/ObstacleButtonSprites/torigate.png").convert_alpha()
        self.scale_factor = 1
        self.__width = int(self.button_image.get_width() * self.scale_factor)
        self.__height = int(self.button_image.get_height() * self.scale_factor)
        self.__button_rect = self.button_image.get_rect(x=x, y=y)

        # 'Pushed' for gate means activated -> ending level
        self.pushed = False
        self.type = "torigate"

class CoinObstacle(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.button_image = pygame.image.load("images/level_select_scene_UI/gold_coin.png").convert_alpha()
        self.scale_factor = 1
        #self.__width = int(self.button_image.get_width() * self.scale_factor)
        #self.__height = int(self.button_image.get_height() * self.scale_factor)
        self.__width = 40
        self.__height = 80

        self.__button_rect = self.button_image.get_rect(x=x, y=y)

        # 'collected' for coin means activated -> collected
        self.collected = False
        self.type = "coin"