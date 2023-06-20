import time

import pygame
import sys
from controllable import Controllable

def main():
    pygame.init()
    level1 = Level(1,1000,700)
    level1.add_platform(0,600,1000,100)
    level1.add_platform(0,100,300,30)
    level1.add_platform(700, 500, 300, 30)
    #level1.add_platform(300, 300, 300, 30)
    #level1.add_platform(30, 450, 200, 30)
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
        self.__momotaro = Controllable()
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
            #placeholder color
            pygame.draw.rect(self.__screen, (0,200,0), rectangle.get_rect())
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


"""class Demon:
    def __init__(self, x, y, health, max_move):
        demon_image = pygame.image.load("your/path/to/character.png")
        self.__int_x = x
        self.__int_y = y
        self.__health = health
        self.__max_move = max_move
        self.__demon_rect = demon_image.get_rect(x=x, y=y)
        pygame.surface.blit(demon_image, self.__demon_rect)

    def movement(self, max_x, max_y):
        while self.__health > 0:"""
            

if __name__ == "__main__":
    main()
