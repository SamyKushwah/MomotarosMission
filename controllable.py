import pygame


class Controllable:
    gravity = 1  # Adjust number to change how fast he falls

    def __init__(self):
        self.x = 10  # Beginning X and Y where the character spawns (spawn in air)
        self.y = 768 - 350
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = True
        self.grav_on = True
        # self.friction = 0
        self.keys_down = 0

        # basic sprite info
        self.scale_factor = 1 / 5  # Used to scale the image and rectangle of the character
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.image = pygame.image.load("player.png")
        self.idle_image = None
        self.right_mvmnt_frames = None
        self.left_mvmnt_frames = None
        self.frame_index = 0  # index used to loop through a list of animation sprites

    def poll_movement(self,event):
        #events = pygame.event.get()

        '''
        if len(events) == 0 and self.vel_x != 0:
            if self.vel_x > 0:
                self.vel_x += -1
            else:
                self.vel_x += 1'''
        #for event in events:
        if event.type == pygame.KEYDOWN:
            # print('keydown')
            self.keys_down += 1
            if event.key == pygame.K_LEFT:
                self.vel_x = -20
                # print('left')
                # self.friction = 0
            elif event.key == pygame.K_RIGHT:
                self.vel_x = 20
                # print('right')
                # self.friction = 0

            if event.key == pygame.K_UP:
                if not self.is_jumping:
                    self.vel_y = -20
                    # print('up')
                    self.grav_on = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                # print('keyup')
                self.keys_down -= 1
                # self.friction = 5

                if self.keys_down == 0:
                    self.vel_x = 0

            '''
            elif event.type == pygame.KEYUP:
                if self.vel_x != 0 and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    if self.vel_x > 0:
                        self.vel_x += -20
                    else:
                        self.vel_x += 20

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.vel_x = 0
        if self.friction:
            if self.vel_x > 0:
                self.vel_x += -1 * self.friction
            else:
                self.vel_x += self.friction'''
    def poll_movement_2(self):
        if self.grav_on:
            self.vel_y += Controllable.gravity

        # Update player position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.rect.update(self.rect)

        if self.vel_y != 0:
            self.is_jumping = True
        else:
            self.is_jumping = False

        # Check for collision and print character in another function

    def new_check_collision(self, list_of_walls):
        pixel_margin = 30
        for wall in list_of_walls:
            # print(wall.bottom)
            # print(self.rect.bottom)
            # print(self.is_jumping)
            if self.rect.colliderect(wall):
                # Check which two sides of the rectangles are touching

                if abs(self.rect.left - wall.right) < pixel_margin and not (
                        abs(self.rect.top - wall.bottom) < pixel_margin):
                    self.rect.left = wall.right
                elif abs(self.rect.right - wall.left) < pixel_margin and not (
                        abs(self.rect.top - wall.bottom) < pixel_margin):
                    self.rect.right = wall.left
                elif abs(self.rect.top - wall.bottom) < pixel_margin:
                    self.rect.top = wall.bottom
                    self.vel_y = 0
                elif abs(self.rect.bottom - wall.top) < pixel_margin and self.is_jumping:
                    self.rect.bottom = wall.top
                    self.vel_y = 0
                    self.is_jumping = False
                    self.grav_on = False
            else:
                self.grav_on = True



    def draw_sprite(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update()


class Momotaro(Controllable):
    def sprites_init(self):
        self.is_attacking = False
        self.attacking_left = False
        self.attacking_right = False
        self.health = 100
        self.idle_image = pygame.image.load("./MomotaroSprites/MomoStandingIdle.png")

        self.right_mvmnt_frames = [pygame.image.load("./MomotaroSprites/MomoWalkingbl(Right).png"),
                                   pygame.image.load("./MomotaroSprites/MomoWalkingfl(Right).png")]

        self.left_mvmnt_frames = [pygame.image.load("./MomotaroSprites/MomoWalkingbl(Left).png"),
                                  pygame.image.load("./MomotaroSprites/MomoWalkingfl(Left).png")]

        self.left_attack_frames = [pygame.image.load("./MomotaroSprites/MomoLiftKat(Left).png"),
                              pygame.image.load("./MomotaroSprites/MomoStrike(Left).png")]

        self.right_attack_frames = [pygame.image.load("./MomotaroSprites/MomoLiftKat(Right).png"),
                                 pygame.image.load("./MomotaroSprites/MomoStrike(Right).png")]

        self.x = 10  # Beginning X and Y where the character spawns (spawn in air)
        self.y = 768 - 600
        self.width = 411
        self.height = 542
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.scale_by_ip(self.scale_factor, self.scale_factor)

        # Scale the images
        self.idle_image = pygame.transform.scale(self.idle_image, (
        int(self.idle_image.get_width() * self.scale_factor), int(self.idle_image.get_height() * self.scale_factor)))

        for index in range(len(self.right_mvmnt_frames)):
            frame = self.right_mvmnt_frames[index]
            self.right_mvmnt_frames[index] = pygame.transform.scale(frame, (
            int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))

        for index in range(len(self.left_mvmnt_frames)):
            frame = self.left_mvmnt_frames[index]
            self.left_mvmnt_frames[index] = pygame.transform.scale(frame, (
                int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))

        for index in range(len(self.left_attack_frames)):
            frame = self.left_attack_frames[index]
            self.left_attack_frames[index] = pygame.transform.scale(frame, (
                int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))

        for index in range(len(self.right_attack_frames)):
            frame = self.right_attack_frames[index]
            self.right_attack_frames[index] = pygame.transform.scale(frame, (
                int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))

    def draw_sprite(self, screen):
        # print(self.vel_x)
        # print(self.rect.x)
        # print(self.idle_image.get_height())
        # screen.blit(self.idle_image, (self.rect.x, self.rect.y))

        animation_delay = 4  # increase this number to change how fast the animation plays

        if self.attacking_left and self.is_attacking:
            if self.frame_index < animation_delay * 2:
                index = self.frame_index // animation_delay
                screen.blit(self.left_attack_frames[index], (self.rect.x, self.rect.y))
                self.frame_index += 1
            else:
                self.frame_index = 0
                index = self.frame_index // animation_delay
                screen.blit(self.left_attack_frames[index], (self.rect.x, self.rect.y))
                self.frame_index += 1
        elif self.attacking_right and self.is_attacking:
            if self.frame_index < animation_delay * 2:
                index = self.frame_index // animation_delay
                screen.blit(self.right_attack_frames[index], (self.rect.x, self.rect.y))
                self.frame_index += 1
            else:
                self.frame_index = 0
                index = self.frame_index // animation_delay
                screen.blit(self.right_attack_frames[index], (self.rect.x, self.rect.y))
                self.frame_index += 1
        elif self.vel_x == 0:
            screen.blit(self.idle_image, (self.rect.x, self.rect.y))
        elif self.vel_x > 0:
            if self.frame_index < animation_delay * 2:
                index = self.frame_index // animation_delay
                screen.blit(self.right_mvmnt_frames[index], (self.rect.x, self.rect.y))
                self.frame_index += 1
            else:
                self.frame_index = 0
                index = self.frame_index // animation_delay
                screen.blit(self.right_mvmnt_frames[index], (self.rect.x, self.rect.y))
                self.frame_index += 1

        elif self.vel_x < 0:
            if self.frame_index < animation_delay * 2:
                index = self.frame_index // animation_delay
                screen.blit(self.left_mvmnt_frames[index], (self.rect.x, self.rect.y))
                self.frame_index += 1
            else:
                self.frame_index = 0
                index = self.frame_index // animation_delay
                screen.blit(self.left_mvmnt_frames[index], (self.rect.x, self.rect.y))
                self.frame_index += 1

    def take_damage(self,damage):
        self.health -= damage

    def check_collision_demon(self, list_of_demons):
        damage = 100
        pixel_margin = 30


        for demon in list_of_demons:
            if self.rect.colliderect(demon.get_rect()):
                wall = demon.get_rect()
                if abs(self.rect.left - wall.right) < pixel_margin and not (
                        abs(self.rect.top - wall.bottom) < pixel_margin):
                    self.attacking_left = True
                    self.attacking_right = False
                elif abs(self.rect.right - wall.left) < pixel_margin and not (
                        abs(self.rect.top - wall.bottom) < pixel_margin):
                    self.attacking_right = True
                    self.attacking_left = False

                if self.is_attacking:
                    demon.take_damage(damage)

                else:
                    self.take_damage(damage)

    def poll_attack(self,events):
        #events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    print("h")
                    self.is_attacking = True


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.is_attacking = False

class Bird(Controllable):
    def poll_movement(self, events):
        #events = pygame.event.get()

        '''
        if len(events) == 0 and self.vel_x != 0:
            if self.vel_x > 0:
                self.vel_x += -1
            else:
                self.vel_x += 1'''
        for event in events:
            if event.type == pygame.KEYDOWN:
                # print('keydown')
                if event.key == pygame.K_a:
                    self.keys_down += 1
                    self.vel_x = -20
                    # print('left')
                    # self.friction = 0
                elif event.key == pygame.K_d:
                    self.keys_down += 1
                    self.vel_x = 20
                    # print('right')
                    # self.friction = 0

                if event.key == pygame.K_w:
                    #if not self.is_jumping:
                        self.keys_down += 1
                        self.vel_y = -15
                        # print('up')
                        self.grav_on = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w:
                    # print('keyup')
                    self.keys_down -= 1
                    # self.friction = 5

                    if self.keys_down == 0:
                        self.vel_x = 0

            '''
            elif event.type == pygame.KEYUP:
                if self.vel_x != 0 and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    if self.vel_x > 0:
                        self.vel_x += -20
                    else:
                        self.vel_x += 20

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.vel_x = 0
        if self.friction:
            if self.vel_x > 0:
                self.vel_x += -1 * self.friction
            else:
                self.vel_x += self.friction'''

        if self.grav_on:
            self.vel_y += Controllable.gravity

        # Update player position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.rect.update(self.rect)

        if self.vel_y != 0:
            self.is_jumping = True
        else:
            self.is_jumping = False