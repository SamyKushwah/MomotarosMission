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

        self.image = pygame.image.load("images/MomotaroSprites/MomoStandingIdle.png")
        self.idle_image = None
        self.right_mvmnt_frames = None
        self.left_mvmnt_frames = None
        self.frame_index = 0  # index used to loop through a list of animation sprites

        self.attacking_left = False
        self.attacking_right = False

    def poll_movement(self,event):
        if event.type == pygame.KEYDOWN:
            # print('keydown')

            if event.key == pygame.K_LEFT:
                self.keys_down += 1
                self.vel_x = -10
                # print('left')
                # self.friction = 0
                self.attacking_left = True
                self.attacking_right = False

            elif event.key == pygame.K_RIGHT:
                self.keys_down += 1
                self.vel_x = 10
                # print('right')
                # self.friction = 0
                self.attacking_left = False
                self.attacking_right = True

            if event.key == pygame.K_UP:
                if not self.is_jumping:
                    self.keys_down += 1
                    self.vel_y = -15
                    # print('up')
                    self.grav_on = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                # print('keyup')
                self.keys_down -= 1
                # self.friction = 5

                if self.keys_down == 0:
                    self.vel_x = 0
                elif self.keys_down < 0:
                    self.keys_down = 0
                    self.vel_x = 0

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
            wall = wall.get_rect()
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
        self.idle_image = pygame.image.load("images/MomotaroSprites/MomoStandingIdle.png")

        self.right_mvmnt_frames = [pygame.image.load("images/MomotaroSprites/momotarowalkrightA.png"),
                                   pygame.image.load("images/MomotaroSprites/momotarowalkrightB.png")]

        self.right_mvmnt_frames[0] = pygame.transform.scale(self.right_mvmnt_frames[0], (500, 550))
        self.right_mvmnt_frames[1] = pygame.transform.scale(self.right_mvmnt_frames[1], (500, 550))

        self.left_mvmnt_frames = [pygame.image.load("images/MomotaroSprites/momotarowalkleftA.png"),
                                  pygame.image.load("images/MomotaroSprites/momotarowalkleftB.png")]

        self.left_mvmnt_frames[0] = pygame.transform.scale(self.left_mvmnt_frames[0], (500, 550))
        self.left_mvmnt_frames[1] = pygame.transform.scale(self.left_mvmnt_frames[1], (500, 550))

        self.left_attack_frames = [pygame.image.load("images/MomotaroSprites/MomoLiftKat(Left).png"),
                              pygame.image.load("images/MomotaroSprites/MomoStrike(Left).png")]

        self.right_attack_frames = [pygame.image.load("images/MomotaroSprites/MomoLiftKat(Right).png"),
                                    pygame.image.load("images/MomotaroSprites/MomoStrike(Right).png")]

        self.x = 10  # Beginning X and Y where the character spawns (spawn in air)
        self.y = 768 - 600
        self.width = 500
        self.height = 500
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

        animation_delay = 8  # increase this number to change how fast the animation plays

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

        for demon in list_of_demons:
            if self.rect.colliderect(demon.get_rect()):
                if self.is_attacking:
                    demon.take_damage(damage)

                else:
                    self.take_damage(damage)

    def check_collision_coin(self, list_of_coins):
        for coin in list_of_coins:
            if self.rect.colliderect(coin.get_coin_rect()): #if collide w coin
                coin.set_collected(True) #make the coin be collected

    def check_collision_interactible(self, list_of_obstacles):
        for obstacle in list_of_obstacles:
            if self.rect.colliderect(obstacle.get_rect()):
                match obstacle.type:
                    case "button":
                        obstacle.set_pushed(True)

    def poll_attack(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                #print("h")
                self.is_attacking = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                self.is_attacking = False