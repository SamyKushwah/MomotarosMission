import pygame

'''
Purpose: Enemy object in Momotaro. Spawn at a specified location with a predetermined enemy detection range 
            (2-Dimensional). The Demons are subject to velocity changes and die on water. Demons take damage when hit
            by the sweep image from Momotaro's sword.
'''
class Demon:
    def __init__(self, spawn_position, detection_range):
        self.position = spawn_position
        self.velocity = [0,0]
        self.standing = False
        self.hitbox = (60, 100)
        self.gravity = 1.3
        self.health = 100
        self.attacked = False
        self.detection_hitbox = detection_range
        self.external_forces = [0, 0]
        self.standing_on = None
        self.moving_direction = "idle"
        self.iframes = 10
        #self.in_detect_range = False

        self.idle_image = pygame.transform.scale(pygame.image.load("images/DemonSprites/DemonStanding.png").convert_alpha(), (70, 100))

        self.right_mvmnt_frames = [pygame.transform.scale(pygame.image.load("images/DemonSprites/DemonStand(Right).png").convert_alpha(), (45, 100)),
                                   pygame.transform.scale(pygame.image.load("images/DemonSprites/Demonlift(Right).png").convert_alpha(), (70, 100))]

        self.left_mvmnt_frames = [pygame.transform.scale(pygame.image.load("images/DemonSprites/DemonStand(Left).png").convert_alpha(), (45, 100)),
                                   pygame.transform.scale(pygame.image.load("images/DemonSprites/Demonlift(Left).png").convert_alpha(), (70, 100))]
        self.frame_index = 0
        self.active_image = 0

    '''
    Purpose: If Momotaro is within the demon's detection range, then it will start moving towards him. The movement
                also takes into account external velocity changes such as from getting hit by Momotaro or from
                being on a moving platform.
    '''
    def update_movement(self, momotaro):
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

        # Check if Momotaro is within detection range
        detection_rect = pygame.rect.Rect((0, 0), self.detection_hitbox)
        detection_rect.center = self.get_rect().center
        momotaro_rect = momotaro.get_rect()
        if detection_rect.colliderect(momotaro_rect):
            #self.in_detect_range = True
            if detection_rect.centerx < momotaro_rect.centerx:
                self.moving_direction = "right"
                self.velocity[0] += 0.2
            else:
                self.moving_direction = "left"
                self.velocity[0] -= 0.2
            if detection_rect.centery - momotaro_rect.centery > 100:
                if self.standing:
                    self.velocity[1] = -23 + (self.external_forces[1] / 2)
                    self.velocity[0] += self.external_forces[0]
                    self.standing = False
        else:
            #self.in_detect_range = False
            self.moving_direction = "idle"
            self.velocity[0] = float(self.velocity[0]) - (self.velocity[0] * 0.05)
            if abs(self.velocity[0]) < 1:
                self.velocity[0] = 0

        # Limit max horizontal movement speed
        if self.velocity[0] > 12:
            self.velocity[0] = 12
        elif self.velocity[0] < -12:
            self.velocity[0] = -12

        # Update position with calculated velocity
        self.position[0] += self.velocity[0] + self.external_forces[0]
        self.position[1] += self.velocity[1] + self.external_forces[1]

        # Invincibility frames -- cannot be attacked too recently by Momotaro
        if self.iframes > 0:
            self.iframes -= 1

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

        # Make standing_on = None if in the air
        if self.standing_on is not None:
            test_rect = pygame.rect.Rect((self.position[0] - 5, self.position[1] - 1),
                                         (self.hitbox[0] + 10, self.hitbox[1] + 10))
            if not test_rect.colliderect(self.standing_on.get_rect()):
                self.standing_on = None

        self.position[0] = momotaro_rect.x
        self.position[1] = momotaro_rect.y

    '''
    Purpose: Draws the appropriate sprites and plays the corresponding animation with a set delay between frames. 
    '''
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

        surface.blit(self.active_image, self.position)

    def get_rect(self):
        return pygame.rect.Rect(self.position, self.hitbox)
