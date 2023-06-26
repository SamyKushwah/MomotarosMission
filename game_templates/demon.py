import pygame

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

        self.idle_image = pygame.transform.scale(pygame.image.load("images/DemonSprites/DemonStanding.png").convert_alpha(), (70, 100))

        self.right_mvmnt_frames = [pygame.transform.scale(pygame.image.load("images/DemonSprites/DemonStand(Right).png").convert_alpha(), (45, 100)),
                                   pygame.transform.scale(pygame.image.load("images/DemonSprites/Demonlift(Right).png").convert_alpha(), (70, 100))]

        self.left_mvmnt_frames = [pygame.transform.scale(pygame.image.load("images/DemonSprites/DemonStand(Left).png").convert_alpha(), (45, 100)),
                                   pygame.transform.scale(pygame.image.load("images/DemonSprites/Demonlift(Left).png").convert_alpha(), (70, 100))]
        self.frame_index = 0
        self.active_image = 0

    def update_movement(self, momotaro):

        if not self.standing:
            self.velocity[1] += self.gravity

        if self.standing_on is not None:
            self.external_forces[0] += round(self.standing_on.velocity[0])
            self.external_forces[1] += round(self.standing_on.velocity[1])

        detection_rect = pygame.rect.Rect((0, 0), self.detection_hitbox)
        detection_rect.center = self.get_rect().center
        momotaro_rect = momotaro.get_rect()
        if detection_rect.colliderect(momotaro_rect):
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
            self.moving_direction = "idle"
            self.velocity[0] = float(self.velocity[0]) - (self.velocity[0] * 0.05)
            if abs(self.velocity[0]) < 1:
                self.velocity[0] = 0

        if self.velocity[0] > 12:
            self.velocity[0] = 12
        elif self.velocity[0] < -12:
            self.velocity[0] = -12

        self.position[0] += self.velocity[0] + self.external_forces[0]
        self.position[1] += self.velocity[1] + self.external_forces[1]

        if self.iframes > 0:
            self.iframes -= 1

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
                    momotaro_rect.top = collidable_rect.bottom
                    self.velocity[1] = 3
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

        surface.blit(self.active_image, self.position)

    def get_rect(self):
        return pygame.rect.Rect(self.position, self.hitbox)
