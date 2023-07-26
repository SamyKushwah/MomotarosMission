import pygame
from math import dist

'''
Purpose: Enemy object. Spawns at a specified location with a predetermined enemy detection range 
            (2-Dimensional). The Demons are subject to velocity changes and die on water. Demons take damage when hit
            by the sweep image from Momotaro's sword.
'''


class Demon:
    def __init__(self, spawn_position, detection_range):
        self.position = spawn_position
        self.velocity = [0, 0]
        self.standing = False
        self.hitbox = (100, 115)
        self.gravity = 1.3
        self.health = 100
        self.attacked = False
        self.detection_hitbox = detection_range
        self.attack_hitbox = (100, 100)
        self.external_forces = [0, 0]
        self.standing_on = None
        self.moving_direction = "idle"
        self.last_direction = "right"
        self.iframes = 10
        self.charge_frames = 0
        self.roar_activate = True

        # loading growl sound when demon attacks momotaro from royalty free webpage mixkit
        roar_path = "audio/roar.mp3"
        self.roar_sound = pygame.mixer.Sound(roar_path)
        self.roar_sound.set_volume(0.2)

        self.idle_left = pygame.transform.scale(
            pygame.image.load("images/DemonSprites/demon_idle_left.png").convert_alpha(), (100, 134))
        self.idle_right = pygame.transform.scale(
            pygame.image.load("images/DemonSprites/demon_idle_right.png").convert_alpha(), (100, 134))

        self.lift_left = pygame.transform.scale(
            pygame.image.load("images/DemonSprites/demon_lift_left.png").convert_alpha(), (116, 115))
        self.lift_right = pygame.transform.scale(
            pygame.image.load("images/DemonSprites/demon_lift_right.png").convert_alpha(), (116, 115))

        self.strike_left = pygame.transform.scale(
            pygame.image.load("images/DemonSprites/demon_strike_left.png").convert_alpha(), (139, 115))
        self.strike_right = pygame.transform.scale(
            pygame.image.load("images/DemonSprites/demon_strike_right.png").convert_alpha(), (139, 115))

        self.walk_right = [
            pygame.transform.scale(pygame.image.load("images/DemonSprites/demon_walk_right_1.png").convert_alpha(),
                                   (83, 115)),
            pygame.transform.scale(pygame.image.load("images/DemonSprites/demon_walk_right_2.png").convert_alpha(),
                                   (111, 115))]

        self.walk_left = [
            pygame.transform.scale(pygame.image.load("images/DemonSprites/demon_walk_left_1.png").convert_alpha(),
                                   (83, 115)),
            pygame.transform.scale(pygame.image.load("images/DemonSprites/demon_walk_left_2.png").convert_alpha(),
                                   (111, 115))]

        self.frame_index = 0
        self.active_image = 0

        self.health_holder = pygame.transform.scale(
            pygame.image.load("images/DemonSprites/health_holder.png").convert_alpha(), (120, 10))
        self.health_bar = pygame.transform.scale(pygame.image.load("images/DemonSprites/health.png").convert_alpha(),
                                                 (120, 8))

    '''
    Purpose: If Momotaro is within the demon's detection range, then it will start moving towards him. The movement
                also takes into account external velocity changes such as from getting hit by Momotaro or from
                being on a moving platform.
    '''

    def update_movement(self, momotaro, pet):
        # Demon subject to gravity
        if not self.standing:
            self.velocity[1] += self.gravity

        # Update moving platform velocities and die if on water
        if self.standing_on is not None:
            self.external_forces[0] += round(self.standing_on.velocity[0])
            self.external_forces[1] += round(self.standing_on.velocity[1])

            try:
                if self.standing_on.type == "water":
                    self.health = 0
            except AttributeError:
                pass

        # Check if either pet or Momotaro is within detection range
        detection_rect = pygame.rect.Rect((0, 0), self.detection_hitbox)
        detection_rect.center = self.get_rect().center

        if self.iframes <= 10:
            targets = []

            momotaro_rect = momotaro.get_rect()
            pet_rect = pet.get_rect()

            if detection_rect.colliderect(momotaro_rect):
                targets.append(momotaro)

            if detection_rect.colliderect(pet_rect):
                targets.append(pet)

            if len(targets) != 0:
                if self.roar_activate:
                    self.roar_activate = False
                dists = []
                for target in targets:
                    dists.append(dist(target.get_rect().center, detection_rect.center))

                target = targets[dists.index(min(dists))]

                target_Rect = target.get_rect()
                attack_rect = pygame.rect.Rect((0, 0), self.attack_hitbox)
                attack_rect.center = detection_rect.center
                if attack_rect.colliderect(target_Rect):
                    self.velocity[0] -= (self.velocity[0] * 0.3)
                    if detection_rect.centerx < target_Rect.centerx:
                        self.last_direction = "right"
                    else:
                        self.last_direction = "left"
                    if self.charge_frames == 0:
                        self.charge_frames = 25
                        self.moving_direction = "charging"
                    elif self.charge_frames <= 15:
                        if self.charge_frames == 15:
                            target.hit(self.last_direction)
                        self.moving_direction = "attacking"
                else:
                    self.charge_frames = 0
                    if detection_rect.centerx < target_Rect.centerx:
                        self.moving_direction = "right"
                        self.last_direction = "right"
                        self.velocity[0] += 0.8
                    else:
                        self.moving_direction = "left"
                        self.last_direction = "left"
                        self.velocity[0] -= 0.8
                    if detection_rect.centery - target_Rect.centery > 100:
                        if self.standing:
                            self.velocity[1] = -23 + (self.external_forces[1] / 2)
                            self.velocity[0] += self.external_forces[0]
                            self.standing = False
            else:
                self.roar_activate = True
                self.moving_direction = "idle"
                if abs(self.velocity[0]) < 1:
                    self.velocity[0] = 0
                self.velocity[0] -= (self.velocity[0] * 0.3)
        else:
            self.roar_activate = True
            self.moving_direction = self.last_direction

        # Limit max horizontal movement speed
        if self.velocity[0] > 6 and self.iframes == 0:
            self.velocity[0] = 6
        elif self.velocity[0] < -6 and self.iframes == 0:
            self.velocity[0] = -6

        # Update position with calculated velocity
        self.position[0] += self.velocity[0] + self.external_forces[0]
        self.position[1] += self.velocity[1] + self.external_forces[1]

        # Invincibility frames -- cannot be attacked too recently by Momotaro
        if self.iframes > 0:
            self.iframes -= 1
        elif self.iframes < 0:
            self.iframes = 0

        if self.charge_frames > 0:
            self.charge_frames -= 1

    '''
    Purpose: Allows the demon to stand on platforms and collide with walls
    '''

    def check_collisions(self, collidables):
        # Pixel margin is used as the amount of error between two sides of a rectangle colliding/overlapping
        pixel_margin = 30
        momotaro_rect = pygame.rect.Rect(self.position, self.hitbox)
        self.standing = False
        self.external_forces = [0, 0]
        for collidable in collidables:
            collidable_rect = collidable.get_rect()
            if momotaro_rect.colliderect(collidable_rect):
                # Colliding on the right side of the wall
                if (abs(momotaro_rect.left - collidable_rect.right) < pixel_margin) and not abs(
                        momotaro_rect.top - collidable_rect.bottom) < pixel_margin and not abs(
                    momotaro_rect.bottom - collidable_rect.top) < pixel_margin:
                    momotaro_rect.left = collidable_rect.right
                    self.velocity[0] += 3
                # Colliding on the left side of the wall
                elif abs(momotaro_rect.right - collidable_rect.left) < pixel_margin and not abs(
                        momotaro_rect.top - collidable_rect.bottom) < pixel_margin and not abs(
                    momotaro_rect.bottom - collidable_rect.top) < pixel_margin:
                    momotaro_rect.right = collidable_rect.left
                    self.velocity[0] += -3
                # Colliding on the bottom of a wall/ceiling
                elif abs(momotaro_rect.top - collidable_rect.bottom) < pixel_margin:
                    momotaro_rect.top = collidable_rect.bottom
                    self.velocity[1] = 3
                # Standing on a platform
                elif abs(momotaro_rect.bottom - collidable_rect.top) < pixel_margin and not self.standing and \
                        self.velocity[1] >= 0:
                    momotaro_rect.bottom = collidable_rect.top
                    self.velocity[1] = 0
                    self.standing = True
                    self.standing_on = collidable
                # Try to resolve getting pushed into a platform by teleporting up and out the platform
                elif abs(momotaro_rect.bottom - collidable_rect.top) < pixel_margin and not self.standing and \
                        self.velocity[1] >= 0:
                    momotaro_rect.bottom = collidable_rect.top
                    self.velocity[1] = 0
                    self.standing = True
                    self.standing_on = collidable
                elif collidable_rect.top < momotaro_rect.centery < collidable_rect.bottom:
                    self.standing = True
                    self.standing_on = collidable

        # Make standing_on = None if in the air
        if self.standing_on is not None:
            test_rect = pygame.rect.Rect((self.position[0] - 5, self.position[1] - 1),
                                         (self.hitbox[0] + 10, self.hitbox[1] + 10))
            if not test_rect.colliderect(self.standing_on.get_rect()):
                self.standing_on = None

        if self.standing and self.standing_on != None and self.position[
            1] + self.get_rect().height // 2 > self.standing_on.get_rect().top:
            self.health = 0

        self.position[0] = momotaro_rect.x
        self.position[1] = momotaro_rect.y

    '''
    Purpose: Draws the appropriate sprites and plays the corresponding animation with a set delay between frames. 
    '''

    def draw(self, surface):
        animation_delay = 15

        index = round(float(self.frame_index) / float(animation_delay))

        if index > 1:
            index = 1

        if self.velocity == [0, 0]:
            self.moving_direction = "idle"

        match self.moving_direction:
            case "idle":
                match self.last_direction:
                    case "left":
                        self.active_image = self.idle_left
                    case "right":
                        self.active_image = self.idle_right
            case "right":
                self.active_image = self.walk_right[index]
                if self.standing:
                    self.frame_index += 1
            case "left":
                self.active_image = self.walk_left[index]
                if self.standing:
                    self.frame_index += 1
            case "charging":
                match self.last_direction:
                    case "left":
                        self.active_image = self.lift_left
                    case "right":
                        self.active_image = self.lift_right
            case "attacking":
                match self.last_direction:
                    case "left":
                        self.active_image = self.strike_left
                    case "right":
                        self.active_image = self.strike_right

        if self.frame_index >= animation_delay:
            self.frame_index = 0

        image_rect = self.active_image.get_rect()
        image_rect.center = self.get_rect().center
        difference = self.active_image.get_height() - 115
        image_rect.y = image_rect.y - difference
        if self.moving_direction == "idle":
            image_rect.y += 10
        surface.blit(self.active_image, (image_rect.x, image_rect.y))
        surface.blit(pygame.transform.scale(self.health_bar, (
            self.health_bar.get_width() * abs(self.health) / 100, self.health_bar.get_height())), (
                         self.position[0] - (self.health_holder.get_width() / 2) + (self.active_image.get_width() / 2),
                         self.position[1] - 30))
        surface.blit(self.health_holder, (
            self.position[0] - (self.health_holder.get_width() / 2) + (self.active_image.get_width() / 2),
            self.position[1] - 30))

    def get_rect(self):
        return pygame.rect.Rect(self.position, self.hitbox)
