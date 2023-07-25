import pygame
from pygame import mixer
pygame.mixer.init()


class Momotaro:
    def __init__(self, spawn_position):
        self.position = spawn_position
        self.velocity = [0.0, 0.0]
        self.standing = False
        self.hitbox = (50, 70)
        self.gravity = 1.15
        self.health = 100
        self.attacking = False
        self.external_forces = [0, 0]
        self.standing_on = None
        self.moving_direction = "idle"
        self.last_direction = "left"
        self.attacking_duration = 0
        self.charging_bounce = False

        self.charging = False
        self.attacking = False  # True if attack button is released
        self.attack_power = 0.1  # 0 - 1 decimal
        self.attack_damage = 75
        self.iframes = 0

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
        self.hurt_right_image = pygame.transform.rotate(self.left_mvmnt_frames[0], 325)

        self.swing_size = (400, 50)

        self.attack_swing_right_image = pygame.transform.scale(pygame.image.load("images/MomotaroSprites/swing.png").convert_alpha(),
                                                         (400, 50))
        self.attack_swing_left_image = pygame.transform.scale(pygame.image.load("images/MomotaroSprites/swing_left.png").convert_alpha(),
                                                         (400, 50))
        self.active_sweep_image = None

        self.death_crush_frames = [
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaro_crush1.png").convert_alpha(),
                                   (40, 70)),
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaro_crush2.png").convert_alpha(),
                                   (40, 70)),
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaro_crush3.png").convert_alpha(),
                                   (40, 70))]
        self.death_drown_frames = [
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaro_crush1.png").convert_alpha(),
                                   (40, 70)),
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaro_drown2.png").convert_alpha(),
                                   (40, 70)),
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaro_drown3.png").convert_alpha(),
                                   (40, 70))]
        self.death_oni_frames = [
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaro_crush1.png").convert_alpha(),
                                   (40, 70)),
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaro_oni2.png").convert_alpha(),
                                   (40, 70)),
            pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaro_oni3.png").convert_alpha(),
                                   (40, 70))]
        self.death_type = None

        # loading in coin collection audio from royalty free webpage mixkit
        coin_path = "audio/coin.mp3"
        self.coin_sound = pygame.mixer.Sound(coin_path)
        self.coin_sound.set_volume(0.5)

        # loading in strike audio from royalty free webpage mixkit
        strike_path = "audio/strike.mp3"
        self.strike_sound = pygame.mixer.Sound(strike_path)
        self.strike_sound.set_volume(0.35)

        # loading ouch sound from royalty free webpage mixkit
        ow_path = "audio/smack.mp3"
        self.ow_sound = pygame.mixer.Sound(ow_path)
        self.ow_sound.set_volume(0.35)

        # loading ouch sound from royalty free webpage mixkit
        demon_ow_path = "audio/deep_smack.mp3"
        self.demon_ow_sound = pygame.mixer.Sound(demon_ow_path)
        self.demon_ow_sound.set_volume(0.25)

    def update_movement(self):

        if self.iframes > 0:
            self.iframes -= 1

        if not self.standing:
            self.velocity[1] += self.gravity

        if self.standing_on is not None:
            self.external_forces[0] += round(self.standing_on.velocity[0])
            self.external_forces[1] += round(self.standing_on.velocity[1])
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            # add walking sound
            if not self.charging:
                if self.velocity[0] < 0:
                    self.velocity[0] += 0.2
                self.velocity[0] += 0.3
            else:
                self.velocity[0] += 0.05
            self.moving_direction = "right"
            self.last_direction = "right"
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            # add walking sound
            if not self.charging:
                if self.velocity[0] > 0:
                    self.velocity[0] -= 0.2
                self.velocity[0] -= 0.3
            else:
                self.velocity[0] -= 0.05
            self.moving_direction = "left"
            self.last_direction = "left"
        else:
            self.moving_direction = "idle"
            if self.standing_on is not None:
                self.velocity[0] = float(self.velocity[0]) - (self.velocity[0] * 0.3)
            else:
                self.velocity[0] = float(self.velocity[0]) - (self.velocity[0] * 0.035)
            if abs(self.velocity[0]) < 1:
                self.velocity[0] = 0

        if keys[pygame.K_w]:
            # add sound of jumping here
            if self.standing:
                self.velocity[1] = -23 + (self.external_forces[1] / 2)
                self.velocity[0] += self.external_forces[0]
                self.standing = False
        if self.attacking_duration <= 0:
            if keys[pygame.K_r]: # Momotaro is attacking
                if not self.charging:
                    self.attack_power = 0.1
                self.charging = True
                self.attacking = False
                if self.charging_bounce:
                    # self.charge_sound.play(-1)
                    pass  # TODO charging sound is very bad!
                self.charging_bounce = False
            elif not keys[pygame.K_r] and self.charging:
                self.attacking = True
                self.charging = False
                self.attacking_duration = 10
                self.strike_sound.play()
                self.charging_bounce = True
            else:
                self.charging = False
                self.attacking = False
                self.attacking_duration = 0
                self.attack_power = 0.1
                self.charging_bounce = True
        else:
            self.attacking_duration -= 1

        max = 10
        if self.charging and self.standing_on is not None:
            max = 2
        if self.velocity[0] > max:
            self.velocity[0] = max
        elif self.velocity[0] < -max:
            self.velocity[0] = -max

        if self.velocity[1] > 20:
            self.velocity[1] = 20
        self.position[0] += self.velocity[0] + self.external_forces[0]
        self.position[1] += self.velocity[1] + self.external_forces[1]

    def check_collisions(self, collidables):
        pixel_margin = 30
        momotaro_rect = pygame.rect.Rect(self.position, self.hitbox)
        self.standing = False
        self.external_forces = [0, 0]
        for collidable in collidables:
            if collidable.type != "dog_button":
                collidable_rect = collidable.get_rect()
                if momotaro_rect.colliderect(collidable_rect):
                    if collidable.type == "spikes":
                        if collidable.active:
                            self.health = 0
                            self.death_type = "oni"
                        else:
                            continue
                        return
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
                        # momotaro_rect.top = collidable_rect.bottom
                        self.velocity[1] = 3 + collidable.velocity[1]
                    elif abs(momotaro_rect.bottom - collidable_rect.top) < pixel_margin and not self.standing and \
                            self.velocity[1] >= 0:
                        momotaro_rect.bottom = collidable_rect.top
                        self.velocity[1] = 0
                        self.standing = True
                        self.standing_on = collidable
                    elif collidable_rect.top < momotaro_rect.centery < collidable_rect.bottom:
                        self.standing = True
                        self.standing_on = collidable

                        # if self.velocity[1] > 0:
                        #     #print("Clipping Warning! Teleporting up!")
                        #     momotaro_rect.bottom = collidable_rect.top
                        #     self.velocity[1] = 0
                        #     self.standing = True
                        # else:
                        #     #print("Clipping Warning! Teleporting down!")
                        #     momotaro_rect.top = collidable_rect.bottom
                        #     self.velocity[1] = 5

        if self.standing_on is not None:
            test_rect = pygame.rect.Rect((self.position[0] - 5, self.position[1] - 1),
                                         (self.hitbox[0] + 10, self.hitbox[1] + 10))
            if not test_rect.colliderect(self.standing_on.get_rect()):
                self.standing_on = None

            try:
                if self.standing_on.type == "water":
                    self.health = 0
                    self.death_type = "drown"
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

        if self.frame_index >= animation_delay:
            self.frame_index = 0

        if self.iframes > 0:
            match self.last_direction:
                case "left":
                    self.active_image = self.hurt_left_image
                case "right":
                    self.active_image = self.hurt_right_image

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

        surface.blit(self.active_image, self.position)

    def get_rect(self):
        return pygame.rect.Rect(self.position, self.hitbox)

    def check_collision_interactible(self, list_of_obstacles, obj):
        for obstacle_type in list_of_obstacles.keys():
            match obstacle_type:
                case "button":
                    for obstacle in list_of_obstacles[obstacle_type]:
                        if obstacle.type != "dog_button":
                            # print(self.standing_on)
                            try:
                                if self.standing_on.type == "button" and self.standing_on == obstacle:
                                    # print("hello")
                                    obstacle.set_pushed(True)
                            except AttributeError:
                                obstacle.set_pushed(False)
                case "torigate":
                    momo_center_x = self.get_rect().centerx
                    momo_center_y = self.get_rect().centery

                    obstacles = list_of_obstacles[obstacle_type]
                    momo_gate = None

                    for obstacle in obstacles:
                        if obstacle.gate_num == 1:
                            momo_gate = obstacle

                    gate_center_x = momo_gate.get_rect().centerx
                    gate_center_y = momo_gate.get_rect().centery

                    margin = 80
                    if (abs(momo_center_x - gate_center_x) < margin) and (abs(momo_center_y - gate_center_y) < margin):
                        momo_gate.pushed = True
                    else:  # fixed bug so now only when you are in gate range anf up you win
                        momo_gate.pushed = False

                case "coin":
                    for coin in list_of_obstacles[obstacle_type]:
                        if self.get_rect().colliderect(coin.get_rect()) and not coin.collected:
                            coin.collected = True
                            # play coin collected audio
                            self.coin_sound.play()
                            #print('coin collected')
                            obj.coins_collected += 1
                #case "fence":
                #    for fence in list_of_obstacles[obstacle_type]:
                #        if self.get_rect().colliderect(fence.get_rect()):

    def check_attacking(self, demon_list):
        if self.charging:
            if self.attack_power >= 0.4:
                self.attack_power = 0.4
                self.charging = False
                self.attacking = True
                self.attacking_duration = 10
                self.strike_sound.play()
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
                                if self.attack_power > 0.1:
                                    demon.velocity[0] += 30 * self.attack_power
                                    demon.velocity[1] += -30 * self.attack_power
                                demon.attacked = True
                                demon.iframes = 10 + 15 * self.attack_power
                                self.demon_ow_sound.play()

                        case "left":
                            if attack_rect_left.colliderect(demon.get_rect()):
                                demon.health -= (self.attack_damage * self.attack_power)
                                if self.attack_power > 0.1:
                                    demon.velocity[0] += -30 * self.attack_power
                                    demon.velocity[1] += -30 * self.attack_power
                                demon.attacked = True
                                demon.iframes = 10 + 15 * self.attack_power
                                self.demon_ow_sound.play()

    def hit(self, direction):
        if self.iframes <= 0:
            # add hit noise
            self.ow_sound.play()
            self.health -= 5
            self.iframes = 20
            match direction:
                case "left":
                    self.velocity[0] += -12
                    self.velocity[1] += -12
                    self.last_direction = "left"
                case "right":
                    self.velocity[0] += 12
                    self.velocity[1] += -12
                    self.last_direction = "right"