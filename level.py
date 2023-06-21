import time

import pygame
import sys

import controllable
from controllable import Controllable

def main():
    pygame.init()
    level1 = Level(1,1000,700)
    level1.add_platform(0,600,1000,100)
    level1.add_platform(0,100,300,30)
    level1.add_platform(700, 500, 300, 30)
    level1.add_platform(300, 300, 300, 30)
    level1.add_platform(30, 450, 200, 30)
    level1.add_demon(100,501,100,50)
    level1.run()

    pygame.quit()
    sys.exit()

    # Set up the game window

class Level:
    def __init__(self, lvl_num, lvl_width, lvl_height):
        self.__width = lvl_width
        self.__height = lvl_height
        self.__lvl_num = lvl_num
        self.__screen = pygame.display.set_mode((lvl_width, lvl_height))
        self.__momotaro = controllable.Momotaro()
        self.__momotaro.sprites_init()
        #self.__animals = Animals()
        self.__platform_list = []
        self.__rectangle_list = []
        self.__wall_list = []
        self.__obstacle_list = []
        self.__coin_list = []
        self.__demon_list = []
        self.__coins_collected = 0
        self.__lvl_complete = False

    def run(self):
        clock = pygame.time.Clock()
        # run event handling for the level until lvl_complete == True
        while not self.__lvl_complete:
            self.__momotaro.poll_movement()
            self.__momotaro.new_check_collision(self.__rectangle_list)
            self.draw()
            pygame.display.update()
            clock.tick(60)

    def draw(self):
        self.__screen.fill((0, 0, 0))
        self.__momotaro.draw_sprite(self.__screen)
        for rectangle in self.__platform_list:
            #placeholder color
            rectangle.draw_platform(self.__screen)
        for rectangle in self.__obstacle_list:
            #placeholder color
            pygame.draw.rect(self.__screen, (0,200,0), rectangle.get_rect())
        for rectangle in self.__demon_list:
            rectangle.movement(self.__screen,2)
        for rectangle in self.__coin_list:
            #placeholder color
            pygame.draw.rect(self.__screen, (0,200,0), rectangle.get_rect())

        #draw rest of characters and objects

    def get_screen(self):
        return self.__screen

    def get_lvl_num(self):
        return self.__lvl_num

    def add_platform(self,x,y,height,width):
        temp_platform = Platform(x,y,height,width)
        self.__platform_list.append(temp_platform)
        self.__rectangle_list.append(temp_platform.get_rect())

    def add_demon(self,x,y,health,movement):
        temp_demon = Demon(x,y,health,movement)
        self.__demon_list.append(temp_demon)
    #def add_demon(self,x,y)
    #def add_obstacle(self,x,y)
    #def add_coin(self,x,y)

class Platform:
    def __init__(self, x, y, width, height):
        self.__height = height
        self.__width = width
        self.__x = x
        self.__y = y
        self.__rect = pygame.Rect(x,y,width,height)

    def get_rect(self):
        return self.__rect

    def draw_platform(self,screen):
        platform_image = pygame.image.load("platform.png")
        platform_image = pygame.transform.scale(platform_image, (self.__width,self.__height))
        screen.blit(platform_image, (self.__x, self.__y))

'''class Wall:
    def __init__(self, x, y, width, height):
        self.__height = height
        self.__width = width
        self.__x = x
        self.__y = y
        self.__rect = pygame.Rect(x,y,width,height)
        self.__wall_image = pygame.image.load("wall.png")

    def get_rect(self):
        return self.__rect

    def draw_wall(self,screen):
        wall_image = pygame.image.load("wall.png")
        wall_x = 1024 - 50
        wall_y = 0
        screen.blit(wall_image, (wall_x, wall_y))'''


class Demon:
    def __init__(self, x, y, health, max_move):
        self.demon_image = pygame.image.load("player.png")
        self.__height = 100
        self.__width = 100
        self.__int_x = x
        self.__int_y = y
        self.__health = health
        self.__max_move = max_move
        self.__demon_rect = self.demon_image.get_rect(x=x, y=y)
        self.__moving_right = True
        self.frame_index = 0
        self.idle_image = None
        self.right_mvmnt_frames = None
        self.left_mvmnt_frames = None
        self.scale_factor = 1 / 5
        self.sprite_init()
        #pygame.surface.blit(self.demon_image, self.__demon_rect)

    def movement(self, screen,movement):
        if self.__health > 0:
            if self.__demon_rect.x == self.__int_x - self.__max_move:
                self.__moving_right = True
            elif self.__demon_rect.x == self.__int_x + self.__max_move:
                self.__moving_right = False
            if self.__moving_right:
                self.__demon_rect.x += 1
            else:
                self.__demon_rect.x -= 1

        self.__demon_rect.update(self.__demon_rect)
        animation_delay = 10  # increase this number to change how fast the animation plays

        if self.__moving_right:
            if self.frame_index < animation_delay * 2:
                index = self.frame_index // animation_delay
                screen.blit(self.right_mvmnt_frames[index], (self.__demon_rect.x, self.__demon_rect.y))
                self.frame_index += 1
            else:
                self.frame_index = 0
                index = self.frame_index // animation_delay
                screen.blit(self.right_mvmnt_frames[index], (self.__demon_rect.x, self.__demon_rect.y))
                self.frame_index += 1
        else:
            if self.frame_index < animation_delay * 2:
                index = self.frame_index // animation_delay
                screen.blit(self.left_mvmnt_frames[index], (self.__demon_rect.x, self.__demon_rect.y))
                self.frame_index += 1
            else:
                self.frame_index = 0
                index = self.frame_index // animation_delay
                screen.blit(self.left_mvmnt_frames[index], (self.__demon_rect.x, self.__demon_rect.y))
                self.frame_index += 1


    def sprite_init(self):

        #self.idle_image = pygame.image.load("./DemonSprites/MomoStandingIdle.png")

        self.left_mvmnt_frames = [pygame.image.load("./DemonSprites/DemonStand(Left).png"),
                                   pygame.image.load("./DemonSprites/DemonStrike(Left).png"),
                                  pygame.image.load("./DemonSprites/Demonlift(Left).png")]

        self.right_mvmnt_frames = [pygame.image.load("./DemonSprites/DemonStand(Right).png"),
                                  pygame.image.load("./DemonSprites/DemonStrike(Right).png"),
                                  pygame.image.load("./DemonSprites/Demonlift(Right).png")]

        self.rect = pygame.Rect(self.__int_x, self.__int_y, self.__width, self.__height)
        self.rect.scale_by_ip(self.scale_factor, self.scale_factor)

        # Scale the images

        for index in range(len(self.right_mvmnt_frames)):
            frame = self.right_mvmnt_frames[index]
            self.right_mvmnt_frames[index] = pygame.transform.scale(frame, (
                int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))

        for index in range(len(self.left_mvmnt_frames)):
            frame = self.left_mvmnt_frames[index]
            self.left_mvmnt_frames[index] = pygame.transform.scale(frame, (
                int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))

if __name__ == "__main__":
    main()

