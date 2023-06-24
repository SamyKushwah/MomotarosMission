import pygame


class Demon:
<<<<<<< Updated upstream
=======
    def __init__(self, spawn_position, detection_range):
        self.position = spawn_position
        self.velocity = [0,0]
        self.standing = False
        self.hitbox = (70, 80)
        self.gravity = 1.3
        self.health = 100
        self.detection_range = detection_range

        self.idle_image = pygame.transform.scale(pygame.image.load("images/DemonSprites/DemonStanding.png"), (70, 100))

        self.right_mvmnt_frames = [pygame.transform.scale(pygame.image.load("images/DemonSprites/DemonStand(Right).png"), (45, 100)),
                                   pygame.transform.scale(pygame.image.load("images/DemonSprites/Demonlift(Right).png"), (70, 100))]

        self.left_mvmnt_frames = [pygame.transform.scale(pygame.image.load("images/DemonSprites/DemonStand(Left).png"), (45, 100)),
                                   pygame.transform.scale(pygame.image.load("images/DemonSprites/Demonlift(Left).png"), (70, 100))]

        self.frame_index = 0

        self.active_image = 0

    def update_movement(self, momo):
        momo_pos = momo.position        # [300, 300]

        if not self.standing:
            self.velocity[1] += self.gravity

        if dist(self.position, momo_pos) <= self.detection_range:
            if (momo_pos[0] - self.position[0]) < 0:        # momo to the left of oni
                self.velocity[0] = -6
            else:       # momo to the right of the oni
                self.velocity[0] = 6
        else:
            self.velocity[0] = 0

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def check_collisions(self, collidables):
        pixel_margin = 30
        momotaro_rect = pygame.rect.Rect(self.position, self.hitbox)
        self.standing = False
        for collidable in collidables:
            collidable_rect = collidable.get_rect()
            if momotaro_rect.colliderect(collidable_rect):
                if (abs(momotaro_rect.left - collidable_rect.right) < pixel_margin) and not abs(
                        momotaro_rect.top - collidable_rect.bottom) < pixel_margin and not abs(
                        momotaro_rect.bottom - collidable_rect.top) < pixel_margin:
                    momotaro_rect.left = collidable_rect.right
                elif abs(momotaro_rect.right - collidable_rect.left) < pixel_margin and not abs(
                        momotaro_rect.top - collidable_rect.bottom) < pixel_margin and not abs(
                        momotaro_rect.bottom - collidable_rect.top) < pixel_margin:
                    momotaro_rect.right = collidable_rect.left
                elif abs(momotaro_rect.top - collidable_rect.bottom) < pixel_margin:
                    momotaro_rect.top = collidable_rect.bottom
                    self.velocity[1] = 0
                elif abs(momotaro_rect.bottom - collidable_rect.top) < pixel_margin and not self.standing:
                    momotaro_rect.bottom = collidable_rect.top
                    self.velocity[1] = 0
                    self.standing = True
                elif collidable_rect.top < momotaro_rect.centery < collidable_rect.bottom:
                    print("teleporting up!")
                    momotaro_rect.bottom = collidable_rect.top
                    self.velocity[1] = 0
                    self.standing = True
        self.position[0] = momotaro_rect.x
        self.position[1] = momotaro_rect.y

    def draw(self, surface):
        animation_delay = 16

        index = round(float(self.frame_index) / float(animation_delay))

        if self.velocity[0] == 0:
            self.active_image = self.idle_image
        elif self.velocity[0] > 0:
            self.active_image = self.right_mvmnt_frames[index]
            self.frame_index += 1
        elif self.velocity[0] < 0:
            self.active_image = self.left_mvmnt_frames[index]
            self.frame_index += 1

        if self.frame_index == animation_delay:
            self.frame_index = 0

        surface.blit(self.active_image, self.position)

    def get_rect(self):
        return pygame.rect.Rect(self.position, self.hitbox)






    '''
>>>>>>> Stashed changes
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

