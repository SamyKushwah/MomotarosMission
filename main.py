import pygame
from pygame.locals import *


# Accompanying script imports


def main():
    pygame.init()
    pygame.display.set_caption("Debug Main Menu")
    clock = pygame.time.Clock()

    # Do we want the screen to be adjustable?
    # Do we want to enforce a minimum screen resolution? (to prevent our graphics from dying if the window is scaled too small)
    # What resolution do we want?

    # Screen constants - can also be made into an object with the following attributes
    min_width = 1024
    min_height = 768
    screen_flags = 0
    screen = pygame.display.set_mode((min_width, min_height), screen_flags)

    # To ask: is it ok to have the screen as a global variable or how can we make the screen object passable into the
    # other scripts that we will use? Will we need to pass the screen object into every class constructor
    # (OOP approach) or into every function call (functional approach)?a

    # Debugging menu to test player movement
    running = True
    selected_level = None
    player = Controllable()
    while running:


        if selected_level == 1:
            screen.fill((0, 0, 0))
            collidables = []
            collidables.append(load_debug_level(screen))
            collidables.append(load_platform(screen))

            player.poll_movement()
            player.check_collision(collidables)
            player.draw_sprite(screen)

        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_1:
                        selected_level = 1
            draw_main_menu(screen)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


def draw_main_menu(screen):
    menu_font = pygame.font.Font(None, 40)
    title = menu_font.render("Main Menu", True, (255, 255, 255))
    screen.blit(title, (350, 100))


def load_debug_level(screen):
    # Load a ground platform
    ground_image = pygame.image.load("ground.png")
    ground_x = 0
    ground_y = 768 - 200

    screen.blit(ground_image, (ground_x, ground_y))

    return pygame.Rect(ground_x, ground_y, 1024, 200)

def load_platform(screen):
    platform_image = pygame.image.load("platform.png")
    platform_x = 724
    platform_y = 768 - 400

    screen.blit(platform_image, (platform_x, platform_y))

    return pygame.Rect(platform_x, platform_y, 300, 50)


class Borders:
    def __init__(self):
        self.rect = None
        self.collide_type = None

    def __int__(self, rect, collide_type):
        self.rect = rect
        self.collide_type = collide_type

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

        self.image = pygame.image.load("player.png")

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

        if self.is_jumping:
            self.vel_y += Controllable.gravity

        # Update player position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.rect.update(self.rect)

        # Check for collision and print character in another function

    def check_collision(self, list_of_walls):
        for wall in list_of_walls:
            print(self.rect.bottom)
            if self.rect.colliderect(wall):
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


    def draw_sprite(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update()


if __name__ == "__main__":
    main()
