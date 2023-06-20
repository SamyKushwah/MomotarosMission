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
    player = Momotaro()
    player.sprites_init()
    while running:


        if selected_level == 1:
            screen.fill((0, 0, 0))
            collidables = []
            collidables.append(load_debug_level(screen))
            collidables.append(load_platform(screen))
            collidables.append(load_wall(screen))

            player.poll_movement()
            player.new_check_collision(collidables)
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
    platform_x = 524
    platform_y = 768 - 380

    screen.blit(platform_image, (platform_x, platform_y))

    return pygame.Rect(platform_x, platform_y, 300, 50)

def load_wall(screen):
    wall_image = pygame.image.load("wall.png")
    wall_x = 1024-50
    wall_y = 0

    screen.blit(wall_image, (wall_x, wall_y))

    return pygame.Rect(wall_x, wall_y, 50, 568)




class Controllable:
    gravity = 1         # Adjust number to change how fast he falls

    def __init__(self):
        self.x = 10          # Beginning X and Y where the character spawns (spawn in air)
        self.y = 768 - 350
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = True
        self.grav_on = True

        #self.friction = 0
        self.keys_down = 0

        # basic sprite info
        self.scale_factor = 1/5  # Used to scale the image and rectangle of the character
        self.width = 100
        self.height = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.image = pygame.image.load("player.png")
        self.idle_image = None
        self.right_mvmnt_frames = None
        self.left_mvmnt_frames = None
        self.frame_index = 0 #index used to loop through a list of animation sprites

    def poll_movement(self):
        events = pygame.event.get()

        '''
        if len(events) == 0 and self.vel_x != 0:
            if self.vel_x > 0:
                self.vel_x += -1
            else:
                self.vel_x += 1'''
        for event in events:
            if event.type == pygame.KEYDOWN:
                #print('keydown')
                self.keys_down += 1
                if event.key == pygame.K_LEFT:
                    self.vel_x = -20
                    #print('left')
                    #self.friction = 0
                elif event.key == pygame.K_RIGHT:
                    self.vel_x = 20
                    #print('right')
                    #self.friction = 0

                if event.key == pygame.K_UP:
                    if not self.is_jumping:
                        self.vel_y = -20
                        #print('up')
                        self.grav_on = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                    #print('keyup')
                    self.keys_down -= 1
                    #self.friction = 5

                    if self.keys_down == 0:
                        self.vel_x = 0

            '''
            elif event.type == pygame.KEYUP:
                if self.vel_x != 0 and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    if self.vel_x > 0:
                        self.vel_x += -20
                    else:
                        self.vel_x += 20
                    
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.vel_x = 0
        if self.friction:
            if self.vel_x > 0:
                self.vel_x += -1 * self.friction
            else:
                self.vel_x += self.friction'''

        if self.grav_on:
            self.vel_y += Controllable.gravity

        # Update player position
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.rect.update(self.rect)

        if self.vel_y != 0:
            self.is_jumping = True
        else:
            self.is_jumping = False

        # Check for collision and print character in another function

    def new_check_collision(self, list_of_walls):
        pixel_margin = 25
        for wall in list_of_walls:
            #print(wall.bottom)
            #print(self.rect.bottom)
            #print(self.is_jumping)
            if self.rect.colliderect(wall):
                 # Check which two sides of the rectangles are touching

                if abs(self.rect.left - wall.right) < pixel_margin and not (abs(self.rect.top - wall.bottom) < pixel_margin):
                    self.rect.left = wall.right
                elif abs(self.rect.right - wall.left) < pixel_margin and not (abs(self.rect.top - wall.bottom) < pixel_margin):
                    self.rect.right = wall.left
                elif abs(self.rect.top - wall.bottom) < pixel_margin:
                    self.rect.top = wall.bottom
                    self.vel_y = 0
                elif abs(self.rect.bottom - wall.top) < pixel_margin and self.is_jumping:
                    self.rect.bottom = wall.top
                    self.vel_y = 0
                    self.is_jumping = False
                    self.grav_on = False
            else:
                self.grav_on = True


    ''' Old code - not used anymore
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
                        self.vel_y = 0'''

    def draw_sprite(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update()

class Momotaro(Controllable):
    def sprites_init(self):
        self.idle_image = pygame.image.load("./MomotaroSprites/MomoStandingIdle.png")

        self.right_mvmnt_frames = [pygame.image.load("./MomotaroSprites/MomoWalkingbl(Right).png"), pygame.image.load("./MomotaroSprites/MomoWalkingfl(Right).png")]

        self.left_mvmnt_frames = [pygame.image.load("./MomotaroSprites/MomoWalkingbl(Left).png"), pygame.image.load("./MomotaroSprites/MomoWalkingfl(Left).png")]

        self.x = 10  # Beginning X and Y where the character spawns (spawn in air)
        self.y = 768 - 600
        self.width = 411
        self.height = 542
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.scale_by_ip(self.scale_factor, self.scale_factor)

        # Scale the images
        self.idle_image = pygame.transform.scale(self.idle_image, (int(self.idle_image.get_width() * self.scale_factor), int(self.idle_image.get_height() * self.scale_factor)))

        for index in range(len(self.right_mvmnt_frames)):
            frame = self.right_mvmnt_frames[index]
            self.right_mvmnt_frames[index] = pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))

        for index in range(len(self.left_mvmnt_frames)):
            frame = self.left_mvmnt_frames[index]
            self.left_mvmnt_frames[index] = pygame.transform.scale(frame, (
            int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))

    def draw_sprite(self, screen):
        #print(self.vel_x)
        #print(self.rect.x)
        #print(self.idle_image.get_height())
        #screen.blit(self.idle_image, (self.rect.x, self.rect.y))
        if self.vel_x == 0:
            screen.blit(self.idle_image, (self.rect.x, self.rect.y))
        elif self.vel_x > 0:
            screen.blit(self.right_mvmnt_frames[self.frame_index],(self.rect.x, self.rect.y))
            self.frame_index += 1
            self.frame_index %= 2
        elif self.vel_x < 0:
            screen.blit(self.left_mvmnt_frames[self.frame_index],(self.rect.x, self.rect.y))
            self.frame_index += 1
            self.frame_index %= 2

        pygame.display.update()

if __name__ == "__main__":
    main()
