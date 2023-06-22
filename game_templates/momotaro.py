import pygame

class Momotaro:
    def __init__(self, spawn_position):
        self.position = spawn_position
        self.velocity = [0, 0]
        self.standing = False
        self.hitbox = (100, 140)
        self.gravity = 1
        self.health = 100
        self.attacking = False

        self.idle_image = None
        self.right_mvmnt_frames = None
        self.left_mvmnt_frames = None
        self.active_image = None

        self.frame_index = 0

        self.idle_image = pygame.transform.scale(pygame.image.load("images/MomotaroSprites/MomoStandingIdle.png"), (100, 150))

        self.right_mvmnt_frames = [pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkrightA.png"), (100, 150)),
                                   pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkrightB.png"), (100, 150))]

        self.left_mvmnt_frames = [pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkleftA.png"), (100, 150)),
                                  pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkleftB.png"), (100, 150))]

        self.left_attack_frames = [pygame.transform.scale(pygame.image.load("images/MomotaroSprites/MomoLiftKat(Left).png"), (100, 150)),
                                   pygame.transform.scale(pygame.image.load("images/MomotaroSprites/MomoStrike(Left).png"), (100, 150))]

    def update_movement(self):

        if not self.standing:
            self.velocity[1] += self.gravity

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.velocity[0] = 10
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            self.velocity[0] = -10
        else:
            self.velocity[0] = 0
        if keys[pygame.K_w]:
            if self.standing:
                self.velocity[1] = -20
                self.standing = False

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def check_collisions(self, collidables):
        pixel_margin = 30
        momotaro_rect = pygame.rect.Rect(self.position, self.hitbox)
        for collidable in collidables:
            collidable_rect = collidable.get_rect()
            if momotaro_rect.colliderect(collidable_rect):
                if (abs(momotaro_rect.left - collidable_rect.right) < pixel_margin) and not (abs(momotaro_rect.top - collidable_rect.bottom) < pixel_margin):
                    momotaro_rect.left = collidable_rect.right
                elif abs(momotaro_rect.right - collidable_rect.left) < pixel_margin and not abs(momotaro_rect.top - collidable_rect.bottom) < pixel_margin:
                    momotaro_rect.right = collidable_rect.left
                elif abs(momotaro_rect.top - collidable_rect.bottom) < pixel_margin:
                    momotaro_rect.top = collidable_rect.bottom
                    self.velocity[1] = 0
                elif abs(momotaro_rect.bottom - collidable_rect.top) < pixel_margin and not self.standing:
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










