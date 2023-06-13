import pygame


class Controllable:
    gravity = 1

    def __init__(self):
        x = 10
        y = 768 - 350
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = True

        # basic sprite info
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.image = pygame.image.load("images/player.png")

    def poll_movement(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.vel_x = -20
                    print('left')
                elif event.key == pygame.K_RIGHT:
                    self.vel_x = 20
                    print('right')
                    
                if event.key == pygame.K_UP:
                    if not self.is_jumping:
                        self.vel_y = -20
                        print('up')
                        self.is_jumping = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.vel_x = 0

        self.vel_y += Controllable.gravity

        # Update player position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.rect.update(self.rect)

        # Check for collision and print character in another function

    def check_collision(self, list_of_walls):
        for pair in list_of_walls:
            wall = pair[0]
            wall_type = pair[1]
            print(self.rect.bottom)

            if self.rect.colliderect(wall):
                if wall_type == "Wall":
                    if self.vel_x > 0:
                        self.rect.right = wall.left
                    elif self.vel_x < 0:
                        self.rect.left = wall.right
                    else:
                        if self.vel_y > 0:
                            print('bruh')
                            self.rect.bottom = wall.top
                            self.vel_y = 0
                            self.is_jumping = False
                        elif self.vel_y < 0:
                            self.rect.top = wall.bottom
                            self.vel_y = 0
                elif wall_type == "Floor":
                    if self.vel_y > 0:
                        print('bruh')
                        self.rect.bottom = wall.top
                        self.vel_y = 0
                        self.is_jumping = False
                    elif self.vel_y < 0:
                        self.rect.top = wall.bottom
                        self.vel_y = 0

    def draw_sprite(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update()