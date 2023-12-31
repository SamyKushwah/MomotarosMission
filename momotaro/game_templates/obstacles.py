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
        # print("Button is pushed!")
        self.pushed = push

    def draw(self, screen):
        self.button_image = pygame.transform.scale(self.button_image, (self.__width, self.__height))
        self.__button_rect = self.button_image.get_rect()
        self.__button_rect.center = (self.__int_x, self.__int_y)
        screen.blit(self.button_image, (self.__int_x - (self.__width / 2), self.__int_y - (self.__height / 2)))


class ButtonObstacle():
    def __init__(self, button_position, fence_int_position, fence_final_position, x, y, fence_dimensions, level_num,
                 dog=False, dog_int_y=None):
        # super().__init__(x, y)
        self.dog_button_img = pygame.image.load("images/ObstacleButtonSprites/dog_symbol.png").convert_alpha()
        self.button_image = pygame.image.load("images/ObstacleButtonSprites/Button2.png").convert_alpha()

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
        if dog:
            self.type = "dog_button"
            self.__int_y_dog = dog_int_y
            self.__width_dog = int(self.dog_button_img.get_width() * self.scale_factor)
            self.__height_dog = int(self.dog_button_img.get_height() * self.scale_factor)
            self.__button_rect_dog = self.dog_button_img.get_rect(x=self.__int_x, y=self.__int_y_dog)

        self.velocity = (0, 0)
        self.fence_moving = False
        self.sound_playing = False

        # loading fence sound royalty free from evanto elements
        fence_path = "audio/fence.mp3"
        self.fence_sound = pygame.mixer.Sound(fence_path)
        self.fence_sound.set_volume(0.3)

    def is_pushed(self):
        return self.pushed

    def stop_fence_sound(self):
        self.fence_sound.stop()

    def get_rect(self):
        return self.__button_rect

    def set_pushed(self, push):
        self.pushed = push

    def draw(self, screen, momohealth):
        if self.type == "button":
            self.button_image = pygame.transform.scale(self.button_image, (self.__width, self.__height))
            self.__button_rect = self.button_image.get_rect()
            self.__button_rect.center = (self.__int_x, self.__int_y)
            screen.blit(self.button_image, (self.__int_x - (self.__width / 2), self.__int_y - (self.__height / 2)))
            if momohealth > 0:
                self.move_fence_to_new_pos()
            else:
                self.fence_sound.stop()
        elif self.type == "dog_button":
            self.dog_button_img = pygame.transform.scale(self.dog_button_img, (self.__width_dog, self.__height_dog))
            screen.blit(self.dog_button_img, (self.__int_x - (self.__width_dog / 2), self.__int_y_dog - (self.__height_dog / 2)))
        self.fence.draw(screen)

    def move_fence_to_new_pos(self):
        if self.is_pushed():
            if self.fence_velocity > 0:
                if self.fence.target[1] < self.fence.y:
                    self.fence.y -= self.fence_velocity
                    self.fence_moving = True
            else:
                if self.fence.target[1] > self.fence.y:
                    self.fence.y -= self.fence_velocity
                    self.fence_moving = True
        else:
            if self.fence_velocity > 0:
                if self.fence.initial[1] > self.fence.y:
                    self.fence.y += self.fence_velocity
                    self.fence_moving = True
            else:
                if self.fence.initial[1] < self.fence.y:
                    self.fence.y += self.fence_velocity
                    self.fence_moving = True

        # play the sound only once while the fence is moving
        # check whether sound is playing and only play if it is not
        if self.fence_moving and not self.sound_playing:
            self.fence_sound.play(loops=-1)
            self.sound_playing = True
        # stop playing sound when the gate reaches the top or bottom
        if self.fence.target[1] == self.fence.y or self.fence.initial[1] == self.fence.y:
            self.fence_sound.stop()
            self.sound_playing = False


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
        self.velocity = (0, 0)

    def draw(self, screen):
        self.fence_image = pygame.transform.scale(self.fence_image, (self.__width, self.__height))
        self.__fence_rect = self.fence_image.get_rect()
        self.__fence_rect.center = (self.x, self.y)
        screen.blit(self.fence_image, (self.x - (self.__width / 2), self.y - (self.__height / 2)))

    def get_rect(self):
        return self.__fence_rect


class ToriObstacle:
    def __init__(self, x, y, gate_num):
        self.gate_num = gate_num
        if gate_num == 1:
            self.tori_image = pygame.transform.scale((pygame.image.load("images/ObstacleButtonSprites/torigate1.png").convert_alpha()), (100, 100))
        else:
            self.tori_image = pygame.transform.scale((pygame.image.load("images/ObstacleButtonSprites/torigate2.png").convert_alpha()), (100, 100))
        self.x = x
        self.y = y

        # 'Pushed' for gate means activated -> ending level
        self.pushed = False
        self.type = "torigate"

    def draw(self, screen):
        screen.blit(self.tori_image, (self.x, self.y))

    def get_rect(self):
        return pygame.rect.Rect(((self.x, self.y), self.tori_image.get_size()))


class CoinObstacle:
    def __init__(self, x, y):
        self.coin_image = pygame.transform.scale(pygame.image.load("images/level_select_scene_UI/gold_coin.png").convert_alpha(), (92, 91))
        self.x = x
        self.y = y
        self.collected = False
        self.type = "coin"

    def draw(self, screen):
        screen.blit(self.coin_image, (self.x, self.y))

    def get_rect(self):
        return pygame.rect.Rect(((self.x, self.y), self.coin_image.get_size()))

class VaseObstacle:
    def __init__(self, x, y, spikes, duration):
        self.vase_image = pygame.transform.scale(
            pygame.image.load("images/ObstacleButtonSprites/vase.png").convert_alpha(), (45, 65))
        self.break_1 = pygame.transform.scale(
            pygame.image.load("images/ObstacleButtonSprites/vase_break_1.png").convert_alpha(), (45, 65))
        self.break_2 = pygame.transform.scale(
            pygame.image.load("images/ObstacleButtonSprites/vase_break_2.png").convert_alpha(), (45, 65))
        self.type = "vase"
        self.broken = 0
        self.hitbox = (50, 70)
        self.x = x
        self.y = y
        self.spikes = spikes
        self.velocity = (0, 0)
        self.duration = duration
        # vase break sound setup using royalty free mixkit
        break_path = "audio/break.mp3"
        self.break_sound = pygame.mixer.Sound(break_path)
        self.break_sound.set_volume(0.1)
    def get_rect(self):
        if self.broken:
            return pygame.rect.Rect(-5, -5, 0, 0)
        return pygame.rect.Rect(self.x, self.y, self.hitbox[0], self.hitbox[1])
    def draw(self, surface):
        if self.broken == 0:
            surface.blit(self.vase_image, (self.x, self.y))
        elif self.broken < self.duration - 5:
            surface.blit(self.break_2, (self.x, self.y))
        elif self.broken <= self.duration:
            surface.blit(self.break_1, (self.x, self.y))
        if self.broken == 1:
            self.spikes.active = True
        if self.broken > 0:
            self.broken -= 1
    def break_vase(self):
        if self.broken == 0:
            # play vase broken sound
            self.break_sound.play()
            self.broken = self.duration
            self.spikes.active = False
