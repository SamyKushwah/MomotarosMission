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

        self.iframes = 10

        self.idle_image = None
        self.right_mvmnt_frames = None
        self.left_mvmnt_frames = None
        self.active_image = None

        self.frame_index = 0


        self.left_flying = pygame.transform.scale(pygame.image.load("images/player2/flying_left.png").convert_alpha(),(40, 70))
        self.left_flapping = pygame.transform.scale(pygame.image.load("images/player2/flapping_left.png").convert_alpha(),(40, 70))

        self.right_flying = pygame.transform.scale(pygame.image.load("images/player2/flying_right.png").convert_alpha(),(40, 70))
        self.right_flapping = pygame.transform.scale(pygame.image.load("images/player2/flapping_right.png").convert_alpha(), (40, 70))


        self.right_mvmnt_frames = [
            pygame.transform.scale(pygame.image.load("images/player2/walking_right_1.png").convert_alpha(), (30, 60)),
            pygame.transform.scale(pygame.image.load("images/player2/walking_right_2.png").convert_alpha(), (40, 60))]

        self.left_mvmnt_frames = [
            pygame.transform.scale(pygame.image.load("images/player2/walking_left_1.png").convert_alpha(), (30, 60)),
            pygame.transform.scale(pygame.image.load("images/player2/walking_left_2.png").convert_alpha(), (35, 60))]

        self.idle_image = self.right_mvmnt_frames[0]

        self.hurt_left_image = pygame.transform.rotate(self.right_mvmnt_frames[0], 45)
        self.hurt_right_image = pygame.transform.rotate(self.left_mvmnt_frames[0], 45)

        self.death_image = pygame.transform.scale(pygame.image.load("images/player2/death.png").convert_alpha(),
                                                  (40, 60))


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
            if self.velocity[0] > 15:
                self.velocity[0] = 15
            elif self.velocity[0] < -15:
                self.velocity[0] = -15

        self.position[0] += self.velocity[0] + self.external_forces[0]
        self.position[1] += self.velocity[1] + self.external_forces[1]


    def update_movement(self):
        match self.pet:
            case "bird":
                self.update_bird_movement()


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
                    self.standing = True
                    self.standing_on = collidable

                    #if self.velocity[1] > 0:
                    #    #print("Clipping Warning! Teleporting up!")
                    #    momotaro_rect.bottom = collidable_rect.top
                    #    self.velocity[1] = 0
                    #    self.standing = True
                    #else:
                    #    #print("Clipping Warning! Teleporting down!")
                    #    momotaro_rect.top = collidable_rect.bottom
                    #    self.velocity[1] = 5

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
                            self.active_image = self.right_mvmnt_frames[0]
                        case "left":
                            self.active_image = self.left_mvmnt_frames[0]
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

    def draw(self, surface):
        match self.pet:
            case "bird":
                self.draw_bird(surface)

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

                case "torigate":
                    center_x = self.get_rect().centerx
                    center_y = self.get_rect().centery

                    obstacles = list_of_obstacles[obstacle_type]
                    pet_gate = None

                    for obstacle in obstacles:
                        if obstacle.gate_num == 2:
                            pet_gate = obstacle

                    gate_center_x = pet_gate.get_rect().centerx
                    gate_center_y = pet_gate.get_rect().centery

                    margin = 80
                    if (abs(center_x - gate_center_x) < margin) and (abs(center_y - gate_center_y) < margin):
                        pet_gate.set_pushed(True)
                    else:  # fixed bug so now only when you are in gate range anf up you win
                        pet_gate.set_pushed(False)

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