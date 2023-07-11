import pygame
from pygame import mixer
mixer.init()


class Momotaro:
    def __init__(self, spawn_position):
        self.position = spawn_position
        self.velocity = [0.0, 0.0]
        self.standing = False
        self.hitbox = (50, 70)
        self.gravity = 1.3
        self.health = 100
        self.attacking = False
        self.external_forces = [0, 0]
        self.standing_on = None
        self.moving_direction = "idle"
        self.last_direction = "left"
        self.attacking_duration = 0

        self.charging = False
        self.attacking = False  # True if attack button is released
        self.attack_power = 0.1  # 0 - 1 decimal
        self.attack_damage = 100
        self.iframes = 10

        self.idle_image = None
        self.right_mvmnt_frames = None
        self.left_mvmnt_frames = None
        self.active_image = None

        self.frame_index = 0

        self.idle_image = pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaroidle.png").convert_alpha(), (40, 70))

        self.right_mvmnt_frames = [
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkrightA.png").convert_alpha(), (60, 70)),
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkrightB.png").convert_alpha(), (60, 70))]

        self.left_mvmnt_frames = [
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkleftA.png").convert_alpha(), (60, 70)),
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkleftB.png").convert_alpha(), (60, 70))]

        self.left_attack_frames = [
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/MomoLiftKat(Left).png").convert_alpha(), (60, 70)),
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/MomoStrike(Left).png").convert_alpha(), (60, 70))]

        self.attacking_left_image = pygame.transform.scale(
            pygame.image.load("images/MomotaroSprites/MomoStrike(Left).png").convert_alpha(), (60, 70))
        self.attacking_right_image = pygame.transform.scale(
            pygame.image.load("images/MomotaroSprites/MomoStrike(Right).png").convert_alpha(), (60, 70))

        self.charging_left_image = pygame.transform.scale(
            pygame.image.load("images/MomotaroSprites/MomoStandingSide(Left).png").convert_alpha(), (60, 70))
        self.charging_right_image = pygame.transform.scale(
            pygame.image.load("images/MomotaroSprites/MomoStandSide(Right).png").convert_alpha(), (60, 70))

        self.hurt_left_image = pygame.transform.rotate(self.right_mvmnt_frames[0], 45)
        self.hurt_right_image = pygame.transform.rotate(self.left_mvmnt_frames[0], 45)

        self.swing_size = (400, 50)

        self.attack_swing_right_image = pygame.transform.scale(pygame.image.load("images/MomotaroSprites/swing.png").convert_alpha(),
                                                         (400, 50))
        self.attack_swing_left_image = pygame.transform.scale(pygame.image.load("images/MomotaroSprites/swing_left.png").convert_alpha(),
                                                         (400, 50))
        self.active_sweep_image = None

    def update_movement(self):

        if not self.standing:
            self.velocity[1] += self.gravity

        if self.standing_on is not None:
            self.external_forces[0] += round(self.standing_on.velocity[0])
            self.external_forces[1] += round(self.standing_on.velocity[1])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            # add walking sound
            if self.velocity[0] < 0:
                self.velocity[0] += 0.3
            self.velocity[0] += 0.3
            self.moving_direction = "right"
            self.last_direction = "right"
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            # add walking sound
            if self.velocity[0] > 0:
                self.velocity[0] -= 0.3
            self.velocity[0] -= 0.3
            self.moving_direction = "left"
            self.last_direction = "left"
        else:
            self.moving_direction = "idle"
            self.velocity[0] = float(self.velocity[0]) - (self.velocity[0] * 0.1)
            if abs(self.velocity[0]) < 1:
                self.velocity[0] = 0

        if keys[pygame.K_w]:
            # add sound of jumping here
            if self.standing:
                self.velocity[1] = -23 + (self.external_forces[1] / 2)
                self.velocity[0] += self.external_forces[0]
                self.standing = False

        if self.attacking_duration <= 0:
            if keys[pygame.K_p]:
                if not self.charging:
                    self.attack_power = 0.1
                self.charging = True
                self.attacking = False
            elif not keys[pygame.K_p] and self.charging:
                self.attacking = True
                self.charging = False
                self.attacking_duration = 10
            else:
                self.charging = False
                self.attacking = False
                self.attacking_duration = 0
                self.attack_power = 0.1
        else:
            self.attacking_duration -= 1

        if self.velocity[0] > 15:
            self.velocity[0] = 15
        elif self.velocity[0] < -15:
            self.velocity[0] = -15

        self.position[0] += self.velocity[0] + self.external_forces[0]
        self.position[1] += self.velocity[1] + self.external_forces[1]

    def check_collisions(self, collidables):
        pixel_margin = 30
        momotaro_rect = pygame.rect.Rect(self.position, self.hitbox)
        self.standing = False
        self.external_forces = [0, 0]
        for collidable in collidables:
            collidable_rect = collidable.get_rect()
            if momotaro_rect.colliderect(collidable_rect):
                if (abs(momotaro_rect.left - collidable_rect.right) < pixel_margin) and not abs(
                        momotaro_rect.top - collidable_rect.bottom) < pixel_margin and not abs(
                        momotaro_rect.bottom - collidable_rect.top) < pixel_margin:
                    momotaro_rect.left = collidable_rect.right
                    self.velocity[0] += 3
                elif abs(momotaro_rect.right - collidable_rect.left) < pixel_margin and not abs(
                        momotaro_rect.top - collidable_rect.bottom) < pixel_margin and not abs(
                        momotaro_rect.bottom - collidable_rect.top) < pixel_margin:
                    momotaro_rect.right = collidable_rect.left
                    self.velocity[0] += -3
                elif abs(momotaro_rect.top - collidable_rect.bottom) < pixel_margin:
                    #momotaro_rect.top = collidable_rect.bottom
                    self.velocity[1] = 3 + collidable.velocity[1]
                elif abs(momotaro_rect.bottom - collidable_rect.top) < pixel_margin and not self.standing and \
                        self.velocity[1] >= 0:
                    momotaro_rect.bottom = collidable_rect.top
                    self.velocity[1] = 0
                    self.standing = True
                    self.standing_on = collidable
                elif collidable_rect.top < momotaro_rect.centery < collidable_rect.bottom:
                    if self.velocity[1] > 0:
                        #print("Clipping Warning! Teleporting up!")
                        momotaro_rect.bottom = collidable_rect.top
                        self.velocity[1] = 0
                        self.standing = True
                    else:
                        #print("Clipping Warning! Teleporting down!")
                        momotaro_rect.top = collidable_rect.bottom
                        self.velocity[1] = 5

        if self.standing_on is not None:
            test_rect = pygame.rect.Rect((self.position[0] - 5, self.position[1] - 1),
                                         (self.hitbox[0] + 10, self.hitbox[1] + 10))
            if not test_rect.colliderect(self.standing_on.get_rect()):
                self.standing_on = None

            try:
                if self.standing_on.type == "water":
                    self.health = 0
            except AttributeError:
                pass

        self.position[0] = momotaro_rect.x
        self.position[1] = momotaro_rect.y

    def draw(self, surface):
        if abs(self.velocity[0]) < 3:
            animation_delay = 8
        elif abs(self.velocity[0]) < 8:
            animation_delay = 6
        else:
            animation_delay = 4

        index = round(float(self.frame_index) / float(animation_delay))

        if index > 1:
            index = 1

        match self.moving_direction:
            case "idle":
                    self.active_image = self.idle_image
            case "right":
                self.active_image = self.right_mvmnt_frames[index]
                if self.standing:
                    self.frame_index += 1
            case "left":
                self.active_image = self.left_mvmnt_frames[index]
                if self.standing:
                    self.frame_index += 1

        match self.last_direction:
            case "right":
                if self.charging:
                    self.active_image = self.charging_right_image
                elif self.attacking:
                    self.active_image = self.attacking_right_image
                    surface.blit(self.active_sweep_image, (self.get_rect().right, self.get_rect().top + 6))
            case "left":
                if self.charging:
                    self.active_image = self.charging_left_image
                elif self.attacking:
                    self.active_image = self.attacking_left_image
                    surface.blit(self.active_sweep_image, (
                        self.get_rect().left - self.active_sweep_image.get_size()[0], self.get_rect().top + 6))

        if self.frame_index >= animation_delay:
            self.frame_index = 0

        surface.blit(self.active_image, self.position)

    def get_rect(self):
        return pygame.rect.Rect(self.position, self.hitbox)

    def check_collision_interactible(self, list_of_obstacles, obj):
        for obstacle_type in list_of_obstacles.keys():
            match obstacle_type:
                case "button":
                    for obstacle in list_of_obstacles[obstacle_type]:
                        #print(self.standing_on)
                        try:
                            if self.standing_on.type == "button" and self.standing_on == obstacle:
                                #print("hello")
                                obstacle.set_pushed(True)
                            else:
                                #print("bye")
                                obstacle.set_pushed(False)
                        except AttributeError:
                            obstacle.set_pushed(False)
                case "torigate":
                    momo_center_x = self.get_rect().centerx
                    momo_center_y = self.get_rect().centery

                    obstacle = list_of_obstacles[obstacle_type][0]

                    gate_center_x = obstacle.get_rect().centerx
                    gate_center_y = obstacle.get_rect().centery

                    margin = 80
                    if (abs(momo_center_x - gate_center_x) < margin) and (abs(momo_center_y - gate_center_y) < margin):
                        obstacle.set_pushed(True)
                    else:  # fixed bug so now only when you are in gate range anf up you win
                        obstacle.set_pushed(False)

                case "coin":
                    for coin in list_of_obstacles[obstacle_type]:
                        if self.get_rect().colliderect(coin.get_rect()) and not coin.collected:
                            coin.collected = True
                            #print('coin collected')
                            obj.coins_collected += 1

                #case "fence":
                #    for fence in list_of_obstacles[obstacle_type]:
                #        if self.get_rect().colliderect(fence.get_rect()):






    def check_attacking(self, demon_list):
        if self.charging:
            if self.attack_power >= 1:
                self.attack_power = 1
            else:
                self.attack_power += 0.01

        if self.attacking:
            sweep_size = ((self.swing_size[0] * self.attack_power), (self.swing_size[1]))
            match self.last_direction:
                case "left":
                    self.active_sweep_image = pygame.transform.scale(self.attack_swing_left_image, sweep_size)
                case "right":
                    self.active_sweep_image = pygame.transform.scale(self.attack_swing_right_image, sweep_size)

            attack_rect_right = pygame.rect.Rect((self.get_rect().right, self.get_rect().top + 30), sweep_size)
            attack_rect_left = pygame.rect.Rect(
                (self.get_rect().left - self.active_sweep_image.get_size()[0], self.get_rect().top + 30), sweep_size)

            for demon in demon_list:
                if demon.iframes <= 0:
                    match self.last_direction:
                        case "right":
                            if attack_rect_right.colliderect(demon.get_rect()):
                                demon.health -= (self.attack_damage * self.attack_power)
                                demon.velocity[0] += 100
                                demon.velocity[1] += -15
                                demon.attacked = True
                                demon.iframes = 20
                        case "left":
                            if attack_rect_left.colliderect(demon.get_rect()):
                                demon.health -= (self.attack_damage * self.attack_power)
                                demon.velocity[0] += -100
                                demon.velocity[1] += -15
                                demon.attacked = True
                                demon.iframes = 20

            #self.attack_power = 0

    def check_damage(self, demon_list):
        if self.iframes <= 0:
            for demon in demon_list:
                if self.get_rect().colliderect(demon.get_rect()):
                    self.health -= 5
                    momotaro_rect = self.get_rect()
                    collidable_rect = demon.get_rect()
                    self.iframes = 20
                    if abs(momotaro_rect.left - collidable_rect.right) < abs(momotaro_rect.right - collidable_rect.left):
                        self.velocity[0] += 6
                        self.velocity[1] += -12
                    else:
                        self.velocity[0] += -6
                        self.velocity[1] += -12
        else:
            self.iframes -= 1
