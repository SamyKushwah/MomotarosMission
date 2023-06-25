import pygame


class Demon:
    def __init__(self, x, y, health, max_move):
        self.demon_image = pygame.image.load("images/DemonSprites/DemonStand(Left).png")
        self.__height = 100
        self.__width = 100
        self.__int_x = x
        self.__int_y = y
        self.__health = health
        self.__max_move = max_move
        self.__demon_rect = self.demon_image.get_rect(x=x, y=y)
        self.__moving_right = True
        self.frame_index = 0
        self.idle_image = None
        self.right_mvmnt_frames = None
        self.left_mvmnt_frames = None
        self.scale_factor = 1 / 8
        self.__alive = True
        self.sprite_init()
        # pygame.surface.blit(self.demon_image, self.__demon_rect)

    def take_damage(self, damage_amount):
        self.__health -= damage_amount

    def is_alive(self):
        return self.__alive

    def get_rect(self):
        return self.__demon_rect

    def movement(self, screen, movement):
        if self.__health > 0 and self.__alive:
            if self.__demon_rect.x == self.__int_x - self.__max_move:
                self.__moving_right = True
            elif self.__demon_rect.x == self.__int_x + self.__max_move:
                self.__moving_right = False
            if self.__moving_right:
                self.__demon_rect.x += 1
            else:
                self.__demon_rect.x -= 1

            self.__demon_rect.update(self.__demon_rect)
            animation_delay = 10  # increase this number to change how fast the animation plays

            if self.__moving_right:
                if self.frame_index < animation_delay * 2:
                    index = self.frame_index // animation_delay
                    screen.blit(self.right_mvmnt_frames[index], (self.__demon_rect.x, self.__demon_rect.y))
                    self.frame_index += 1
                else:
                    self.frame_index = 0
                    index = self.frame_index // animation_delay
                    screen.blit(self.right_mvmnt_frames[index], (self.__demon_rect.x, self.__demon_rect.y))
                    self.frame_index += 1
            else:
                if self.frame_index < animation_delay * 2:
                    index = self.frame_index // animation_delay
                    screen.blit(self.left_mvmnt_frames[index], (self.__demon_rect.x, self.__demon_rect.y))
                    self.frame_index += 1
                else:
                    self.frame_index = 0
                    index = self.frame_index // animation_delay
                    screen.blit(self.left_mvmnt_frames[index], (self.__demon_rect.x, self.__demon_rect.y))
                    self.frame_index += 1
        else:
            self.__alive = False

    def sprite_init(self):

        # self.idle_image = pygame.image.load("./DemonSprites/MomoStandingIdle.png")

        self.left_mvmnt_frames = [pygame.image.load(
            "images/DemonSprites/DemonStand(Left).png"),
                                  pygame.image.load(
                                      "images/DemonSprites/DemonStrike(Left).png"),
                                  pygame.image.load(
                                      "images/DemonSprites/Demonlift(Left).png")]

        self.right_mvmnt_frames = [pygame.image.load(
            "images/DemonSprites/DemonStand(Right).png"),
                                   pygame.image.load(
                                       "images/DemonSprites/DemonStrike(Right).png"),
                                   pygame.image.load(
                                       "images/DemonSprites/Demonlift(Right).png")]

        self.rect = pygame.Rect(self.__int_x, self.__int_y, self.right_mvmnt_frames[0].get_width(),
                                self.right_mvmnt_frames[0].get_height())
        self.rect.scale_by_ip(self.scale_factor, self.scale_factor)

        # Scale the images

        for index in range(len(self.right_mvmnt_frames)):
            frame = self.right_mvmnt_frames[index]
            self.right_mvmnt_frames[index] = pygame.transform.scale(frame, (
                int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))

        for index in range(len(self.left_mvmnt_frames)):
            frame = self.left_mvmnt_frames[index]
            self.left_mvmnt_frames[index] = pygame.transform.scale(frame, (
                int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))