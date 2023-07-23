import pygame
from pygame import mixer
mixer.init()


class Pet:
    def __init__(self, spawn_position):
        self.position = spawn_position
        self.velocity = [0.0, 0.0]
        self.standing = False
        self.hitbox = (35, 60)
        self.gravity = 0.8
        self.health = 50
        self.external_forces = [0, 0]
        self.standing_on = None
        self.moving_direction = "idle"
        self.last_direction = "left"
        self.jumped = False
        self.pet = "bird"
        self.digging = False

        self.iframes = 10
        self.switchdb = False


        self.active_image = None

        self.frame_index = 0


        # BIRD IMAGES ----------------------------------
        self.bird_idle_image = None
        self.right_bird_mvmnt_frames = None
        self.left_bird_mvmnt_frames = None

        self.left_flying = pygame.transform.scale(pygame.image.load("images/player2/flying_left.png").convert_alpha(),(40, 70))
        self.left_flapping = pygame.transform.scale(pygame.image.load("images/player2/flapping_left.png").convert_alpha(),(40, 70))

        self.right_flying = pygame.transform.scale(pygame.image.load("images/player2/flying_right.png").convert_alpha(),(40, 70))
        self.right_flapping = pygame.transform.scale(pygame.image.load("images/player2/flapping_right.png").convert_alpha(), (40, 70))


        self.right_bird_mvmnt_frames = [
            pygame.transform.scale(pygame.image.load("images/player2/walking_right_1.png").convert_alpha(), (30, 60)),
            pygame.transform.scale(pygame.image.load("images/player2/walking_right_2.png").convert_alpha(), (40, 60))]

        self.left_bird_mvmnt_frames = [
            pygame.transform.scale(pygame.image.load("images/player2/walking_left_1.png").convert_alpha(), (30, 60)),
            pygame.transform.scale(pygame.image.load("images/player2/walking_left_2.png").convert_alpha(), (35, 60))]

        self.bird_idle_image = self.right_bird_mvmnt_frames[0]

        self.bird_hurt_left_image = pygame.transform.rotate(self.right_bird_mvmnt_frames[0], 45)
        self.bird_hurt_right_image = pygame.transform.rotate(self.left_bird_mvmnt_frames[0], 45)

        self.bird_death_image = pygame.transform.scale(
            pygame.image.load("images/player2/bird_death.png").convert_alpha(), (50, 60))
        ##################

        # DOG IMAGES -------------------
        self.right_dog_mvmnt_frames = [
            pygame.transform.scale(pygame.image.load("images/player2/dog_walk_right_1.png").convert_alpha(), (60, 65)),
            pygame.transform.scale(pygame.image.load("images/player2/dog_walk_right_2.png").convert_alpha(), (60, 65))]

        self.left_dog_mvmnt_frames = [
            pygame.transform.scale(pygame.image.load("images/player2/dog_walk_left_1.png").convert_alpha(), (60, 65)),
            pygame.transform.scale(pygame.image.load("images/player2/dog_walk_left_2.png").convert_alpha(), (60, 65))]

        self.dog_idle_image_left = pygame.transform.scale(pygame.image.load("images/player2/dog_idle_left.png").convert_alpha(), (60, 65))
        self.dog_idle_image_right = pygame.transform.scale(pygame.image.load("images/player2/dog_idle_right.png").convert_alpha(), (60, 65))


        self.dog_hurt_left_image = pygame.transform.rotate(self.right_dog_mvmnt_frames[0], 45)
        self.dog_hurt_right_image = pygame.transform.rotate(self.left_dog_mvmnt_frames[0], 45)

        # SNIFFING
        self.right_dog_sniffing_mvmnt_frames = [
            pygame.transform.scale(pygame.image.load("images/player2/dog_sniffing_walk_right_1.png").convert_alpha(), (60, 65)),
            pygame.transform.scale(pygame.image.load("images/player2/dog_sniffing_walk_right_2.png").convert_alpha(), (60, 65))]

        self.left_dog_sniffing_mvmnt_frames = [
            pygame.transform.scale(pygame.image.load("images/player2/dog_sniffing_walk_left_1.png").convert_alpha(), (60, 65)),
            pygame.transform.scale(pygame.image.load("images/player2/dog_sniffing_walk_left_2.png").convert_alpha(), (60, 65))]

        self.dog_sniffing_idle_image_left = pygame.transform.scale(
            pygame.image.load("images/player2/dog_sniffing_idle_left.png").convert_alpha(), (60, 65))
        self.dog_sniffing_idle_image_right = pygame.transform.scale(
            pygame.image.load("images/player2/dog_sniffing_idle_right.png").convert_alpha(), (60, 65))

        self.dog_death_image = pygame.transform.scale(
            pygame.image.load("images/player2/dog_death.png").convert_alpha(), (60, 65))

        ##################

    def update_dog_movement(self):
        if not self.standing:
            self.velocity[1] += self.gravity

        if self.standing_on is not None:
            self.external_forces[0] += round(self.standing_on.velocity[0])
            self.external_forces[1] += round(self.standing_on.velocity[1])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            # add walking sound
            if self.velocity[0] < 0:
                self.velocity[0] += 0.2
            self.velocity[0] += 0.2
            self.moving_direction = "right"
            self.last_direction = "right"
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            # add walking sound
            if self.velocity[0] > 0:
                self.velocity[0] -= 0.2
            self.velocity[0] -= 0.2
            self.moving_direction = "left"
            self.last_direction = "left"
        else:
            self.moving_direction = "idle"
            self.velocity[0] = float(self.velocity[0]) - (self.velocity[0] * 0.2)
            if abs(self.velocity[0]) < 1:
                self.velocity[0] = 0

        if keys[pygame.K_UP]:
            # add sound of jumping here
            if self.standing:
                self.velocity[1] = -16 + (self.external_forces[1] / 2)
                self.velocity[0] += self.external_forces[0]
                self.standing = False

        if keys[pygame.K_PERIOD]:
            self.digging = True
        else:
            self.digging = False

        if self.velocity[0] > 10:
            self.velocity[0] = 10
        elif self.velocity[0] < -10:
            self.velocity[0] = -10

        if self.digging:
            if self.velocity[0] > 3:
                self.velocity[0] = 3
            elif self.velocity[0] < -3:
                self.velocity[0] = -3

        self.position[0] += self.velocity[0] + self.external_forces[0]
        self.position[1] += self.velocity[1] + self.external_forces[1]

    def update_bird_movement(self):
        if not self.standing:
            self.velocity[1] += self.gravity

        if self.standing_on is not None:
            self.external_forces[0] += round(self.standing_on.velocity[0])
            self.external_forces[1] += round(self.standing_on.velocity[1])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.velocity[0] += 0.3
            self.moving_direction = "right"
            self.last_direction = "right"
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.velocity[0] -= 0.3
            self.moving_direction = "left"
            self.last_direction = "left"
        else:
            self.moving_direction = "idle"
            self.velocity[0] = float(self.velocity[0]) - (self.velocity[0] * 0.2)
            if abs(self.velocity[0]) < 1:
                self.velocity[0] = 0

        if keys[pygame.K_UP]:
            # add sound of jumping here
            if not self.jumped:
                self.velocity[1] = -15 + (self.external_forces[1] / 2)
                self.velocity[0] += self.external_forces[0]
                self.standing = False
                self.jumped = True
        else:
            self.jumped = False

        if self.standing_on is not None:
            if self.velocity[0] > 6:
                self.velocity[0] = 6
            elif self.velocity[0] < -6:
                self.velocity[0] = -6
        else:
            if self.velocity[0] > 10:
                self.velocity[0] = 10
            elif self.velocity[0] < -10:
                self.velocity[0] = -10

        self.position[0] += self.velocity[0] + self.external_forces[0]
        self.position[1] += self.velocity[1] + self.external_forces[1]

    def switch(self):
        match self.pet:
            case "bird":
                self.pet = "dog"
            case "dog":
                self.pet = "bird"

    def update_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SLASH]:
            if not self.switchdb:
                self.switch()
                self.switchdb = True
        else:
            self.switchdb = False
        match self.pet:
            case "bird":
                self.update_bird_movement()
            case "dog":
                self.update_dog_movement()

    def check_collisions(self, collidables):
        pixel_margin = 30
        momotaro_rect = pygame.rect.Rect(self.position, self.hitbox)
        self.standing = False
        self.external_forces = [0, 0]
        for collidable in collidables:
            if collidable.type != "dog_button":
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

    def draw_bird(self, surface):
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
                    match self.last_direction:
                        case "right":
                            self.active_image = self.right_bird_mvmnt_frames[0]
                        case "left":
                            self.active_image = self.left_bird_mvmnt_frames[0]
            case "right":
                self.active_image = self.right_bird_mvmnt_frames[index]
                if self.standing:
                    self.frame_index += 1
            case "left":
                self.active_image = self.left_bird_mvmnt_frames[index]
                if self.standing:
                    self.frame_index += 1

        if self.frame_index >= animation_delay:
            self.frame_index = 0
        if self.standing_on is None:
            if self.jumped:
                match self.last_direction:
                    case "right":
                        self.active_image = self.right_flapping
                    case "left":
                        self.active_image = self.left_flapping
            else:
                match self.last_direction:
                    case "right":
                        self.active_image = self.right_flying
                    case "left":
                        self.active_image = self.left_flying

        surface.blit(self.active_image, self.position)

    def draw_dog(self, surface):
        if abs(self.velocity[0]) < 3:
            animation_delay = 8
        elif abs(self.velocity[0]) < 8:
            animation_delay = 6
        else:
            animation_delay = 4

        index = round(float(self.frame_index) / float(animation_delay))

        if index > 1:
            index = 1

        if not self.digging:
            match self.moving_direction:
                case "idle":
                    match self.last_direction:
                        case "right":
                            self.active_image = self.dog_idle_image_right
                        case "left":
                            self.active_image = self.dog_idle_image_left
                case "right":
                    self.active_image = self.right_dog_mvmnt_frames[index]
                    if self.standing:
                        self.frame_index += 1
                case "left":
                    self.active_image = self.left_dog_mvmnt_frames[index]
                    if self.standing:
                        self.frame_index += 1
        else:
            match self.moving_direction:
                case "idle":
                    match self.last_direction:
                        case "right":
                            self.active_image = self.dog_sniffing_idle_image_right
                        case "left":
                            self.active_image = self.dog_sniffing_idle_image_left
                case "right":
                    self.active_image = self.right_dog_sniffing_mvmnt_frames[index]
                    if self.standing:
                        self.frame_index += 1
                case "left":
                    self.active_image = self.left_dog_sniffing_mvmnt_frames[index]
                    if self.standing:
                        self.frame_index += 1
        if self.frame_index >= animation_delay:
            self.frame_index = 0

        surface.blit(self.active_image, self.position)

    def draw(self, surface):
        match self.pet:
            case "bird":
                self.draw_bird(surface)
            case "dog":
                self.draw_dog(surface)

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
                        except AttributeError:
                            pass
                        if obstacle.type == "dog_button":
                            if self.pet == "dog":
                                if self.digging:
                                    if self.get_rect().colliderect(obstacle.get_rect()):
                                        obstacle.type = "button"

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

    def draw_death(self, surface):
        match self.pet:
            case "bird":
                surface.blit(self.bird_death_image, self.position)
            case "dog":
                surface.blit(self.dog_death_image, self.position.)