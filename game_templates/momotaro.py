import pygame

class Momotaro:
    def __init__(self, spawn_position):
        self.position = spawn_position
        self.velocity = [0, 0]
        self.standing = False
        self.hitbox = (50, 70)
        self.gravity = 1.3
        self.health = 100
        self.attacking = False
        self.external_forces = [0, 0]
        self.standing_on = None
        self.moving_direction = "idle"
        self.momentum = 0.1

        self.idle_image = None
        self.right_mvmnt_frames = None
        self.left_mvmnt_frames = None
        self.active_image = None

        self.frame_index = 0

        self.idle_image = pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotaroidle.png"), (40, 70))

        self.right_mvmnt_frames = [pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkrightA.png"), (60, 70)),
                                   pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkrightB.png"), (60, 70))]

        self.left_mvmnt_frames = [pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkleftA.png"), (60, 70)),
                                  pygame.transform.scale(pygame.image.load("images/MomotaroSprites/momotarowalkleftB.png"), (60, 70))]

        self.left_attack_frames = [pygame.transform.scale(pygame.image.load("images/MomotaroSprites/MomoLiftKat(Left).png"), (60, 70)),
                                   pygame.transform.scale(pygame.image.load("images/MomotaroSprites/MomoStrike(Left).png"), (60, 70))]

    def update_movement(self):

        if not self.standing:
            self.velocity[1] += self.gravity

        if self.standing_on is not None:
            self.external_forces[0] += round(self.standing_on.velocity[0])
            self.external_forces[1] += round(self.standing_on.velocity[1])

        self.velocity[0] = 0
        self.velocity[0] += self.external_forces[0]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and not keys[pygame.K_a]:
            self.velocity[0] += (5 + self.momentum)
            if not self.moving_direction == "right":
                self.momentum = 0.1
            else:
                self.momentum = self.momentum * 2
            self.moving_direction = "right"
        elif keys[pygame.K_a] and not keys[pygame.K_d]:
            self.velocity[0] -= (5 + self.momentum)
            if not self.moving_direction == "left":
                self.momentum = 0.1
            else:
                self.momentum = self.momentum * 2
            self.moving_direction = "left"
        else:
            self.moving_direction = "idle"
        if keys[pygame.K_w]:
            if self.standing:
                self.velocity[1] = -23
                self.standing = False

        if self.momentum > 7:
            self.momentum = 7

        print("momentum:", self.momentum)

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def check_collisions(self, collidables):
        pixel_margin = 30
        momotaro_rect = pygame.rect.Rect(self.position, self.hitbox)
        self.standing = False
        self.external_forces = [0, 0]
        for collidable in collidables:
            collidable_rect = collidable.get_rect()
            if momotaro_rect.colliderect(collidable_rect):
                if (abs(momotaro_rect.left - collidable_rect.right) < pixel_margin) and not abs(momotaro_rect.top - collidable_rect.bottom) < pixel_margin and not abs(momotaro_rect.bottom - collidable_rect.top) < pixel_margin:
                    momotaro_rect.left = collidable_rect.right
                elif abs(momotaro_rect.right - collidable_rect.left) < pixel_margin and not abs(momotaro_rect.top - collidable_rect.bottom) < pixel_margin and not abs(momotaro_rect.bottom - collidable_rect.top) < pixel_margin   :
                    momotaro_rect.right = collidable_rect.left
                elif abs(momotaro_rect.top - collidable_rect.bottom) < pixel_margin:
                    momotaro_rect.top = collidable_rect.bottom
                    self.velocity[1] = 0
                elif abs(momotaro_rect.bottom - collidable_rect.top) < pixel_margin and not self.standing and self.velocity[1] >= 0:
                    momotaro_rect.bottom = collidable_rect.top
                    self.velocity[1] = 0
                    self.standing = True
                    self.standing_on = collidable
                elif collidable_rect.top < momotaro_rect.centery < collidable_rect.bottom:
                    print("teleporting up!")
                    momotaro_rect.bottom = collidable_rect.top
                    self.velocity[1] = 0
                    self.standing = True

        if self.standing_on is not None:
            test_rect = pygame.rect.Rect((self.position[0] - 5, self.position[1] - 1), (self.hitbox[0] + 10, self.hitbox[1] + 10))
            if not test_rect.colliderect(self.standing_on.get_rect()):
                self.standing_on = None

        self.position[0] = momotaro_rect.x
        self.position[1] = momotaro_rect.y

    def draw(self, surface):
        animation_delay = 6
        if animation_delay < 4:
            animation_delay = 4

        index = round(float(self.frame_index) / float(animation_delay))

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

        if self.frame_index == animation_delay:
            self.frame_index = 0

        surface.blit(self.active_image, self.position)

    def get_rect(self):
        return pygame.rect.Rect(self.position, self.hitbox)

    def check_collision_interactible(self, list_of_obstacles):
        for obstacle_type in list_of_obstacles.keys():
            match obstacle_type:
                case "button":
                    pass
                    for obstacle in list_of_obstacles[obstacle_type]:
                        if self.get_rect().colliderect(obstacle.get_rect()):
                            pass
                # obstacle.set_pushed(True)
                case "torigate":
                    momo_center_x = self.get_rect().centerx
                    momo_center_y = self.get_rect().centery

                    obstacle = list_of_obstacles[obstacle_type][0]

                    gate_center_x = obstacle.get_rect().centerx
                    gate_center_y = obstacle.get_rect().centery

                    margin = 20
                    if (abs(momo_center_x - gate_center_x) < margin) and (abs(momo_center_y - gate_center_y) < margin):
                        obstacle.set_pushed(True)










