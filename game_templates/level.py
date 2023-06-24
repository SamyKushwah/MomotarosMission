import pygame
import sys
import math
import os

from game_templates import demon, button_obstacle, controllable


class Level:
    def __init__(self, my_toolbox, level_num, level_width, level_height):
        self.width = level_width
        self.height = level_height
        self.level_num = level_num

        self.collidable_list = []
        self.platform_list = []
        self.moving_platform_list = []
        self.interactible_list = []
        self.coin_list = []
        self.demon_list = []
        self.header = Header()

    def add_platform(self, position, dimensions, platform_type="stone", facing_direction="all", corners=False):
        temp_platform = Platform(position, dimensions, platform_type, facing_direction, corners)
        print("Adding platform", temp_platform.get_rect())
        self.platform_list.append(temp_platform)
        self.collidable_list.append(temp_platform)

    def add_moving_platform(self, position, dimensions, movement_amount, platform_type="stone", facing_direction="all",
                            corners=False):
        temp_platform = MovingPlatform(position, dimensions, movement_amount, platform_type, facing_direction, corners)
        print("Adding platform", temp_platform.get_rect())
        self.moving_platform_list.append(temp_platform)
        self.collidable_list.append(temp_platform)

    def add_demon(self, x, y, health, movement):
        temp_demon = demon.Demon(x, y, health, movement)
        self.demon_list.append(temp_demon)
        print("adding rect:", temp_demon.get_rect())

    def add_obstacle(self, x, y, type):
        match type:
            case "button":
                temp_obstacle = button_obstacle.ButtonObstacle(x, y)
                self.interactible_list.append(temp_obstacle)

class Platform:
    def __init__(self, position, dimensions, platform_type="stone", facing_direction="all", corners=False):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.x = position[0]
        self.y = position[1]
        self.image = pygame.surface.Surface(dimensions)
        match platform_type:
            case "stone":
                BL = pygame.image.load("images/tiles/stone/Stone(MM).png")
                BM = pygame.image.load("images/tiles/stone/Stone(MM).png")
                BR = pygame.image.load("images/tiles/stone/Stone(MM).png")
                ML = pygame.image.load("images/tiles/stone/Stone(MM).png")
                MM = pygame.image.load("images/tiles/stone/Stone(MM).png")
                MR = pygame.image.load("images/tiles/stone/Stone(MM).png")
                TL = pygame.image.load("images/tiles/stone/Stone(MM).png")
                TM = pygame.image.load("images/tiles/stone/Stone(MM).png")
                TR = pygame.image.load("images/tiles/stone/Stone(MM).png")
                match facing_direction:
                    case "all":
                        BL = pygame.image.load("images/tiles/stone/Stone(BL).png")
                        BM = pygame.image.load("images/tiles/stone/Stone(BM).png")
                        BR = pygame.image.load("images/tiles/stone/Stone(BR).png")
                        ML = pygame.image.load("images/tiles/stone/Stone(ML).png")
                        MM = pygame.image.load("images/tiles/stone/Stone(MM).png")
                        MR = pygame.image.load("images/tiles/stone/Stone(MR).png")
                        TL = pygame.image.load("images/tiles/stone/Stone(TL).png")
                        TM = pygame.image.load("images/tiles/stone/Stone(TM).png")
                        TR = pygame.image.load("images/tiles/stone/Stone(TR).png")
                    case "up":
                        TM = pygame.image.load("images/tiles/stone/Stone(TM).png")
                        if corners:
                            TL = pygame.image.load("images/tiles/stone/Stone(TL).png")
                            TR = pygame.image.load("images/tiles/stone/Stone(TR).png")
                        else:
                            TL = pygame.image.load("images/tiles/stone/Stone(TM).png")
                            TR = pygame.image.load("images/tiles/stone/Stone(TM).png")
                    case "down":
                        BM = pygame.image.load("images/tiles/stone/Stone(BM).png")
                        if corners:
                            BL = pygame.image.load("images/tiles/stone/Stone(BL).png")
                            BR = pygame.image.load("images/tiles/stone/Stone(BR).png")
                        else:
                            BL = pygame.image.load("images/tiles/stone/Stone(BM).png")
                            BR = pygame.image.load("images/tiles/stone/Stone(BM).png")
                    case "left":
                        ML = pygame.image.load("images/tiles/stone/Stone(ML).png")
                        if corners:
                            BL = pygame.image.load("images/tiles/stone/Stone(BL).png")
                            TL = pygame.image.load("images/tiles/stone/Stone(TL).png")
                        else:
                            BL = pygame.image.load("images/tiles/stone/Stone(ML).png")
                            TL = pygame.image.load("images/tiles/stone/Stone(ML).png")
                    case "right":
                        MR = pygame.image.load("images/tiles/stone/Stone(MR).png")
                        if corners:
                            BR = pygame.image.load("images/tiles/stone/Stone(BR).png")
                            TR = pygame.image.load("images/tiles/stone/Stone(TR).png")
                        else:
                            BR = pygame.image.load("images/tiles/stone/Stone(MR).png")
                            TR = pygame.image.load("images/tiles/stone/Stone(MR).png")

            case "water":
                BL = pygame.image.load("images/tiles/watertile.png")
                BM = pygame.image.load("images/tiles/watertile.png")
                BR = pygame.image.load("images/tiles/watertile.png")
                ML = pygame.image.load("images/tiles/watertile.png")
                MM = pygame.image.load("images/tiles/watertile.png")
                MR = pygame.image.load("images/tiles/watertile.png")
                TL = pygame.image.load("images/tiles/watertile.png")
                TM = pygame.image.load("images/tiles/watertile.png")
                TR = pygame.image.load("images/tiles/watertile.png")

        BL = pygame.transform.scale(BL, (70, 70))
        BM = pygame.transform.scale(BM, (70, 70))
        BR = pygame.transform.scale(BR, (70, 70))
        ML = pygame.transform.scale(ML, (70, 70))
        MM = pygame.transform.scale(MM, (70, 70))
        MR = pygame.transform.scale(MR, (70, 70))
        TL = pygame.transform.scale(TL, (70, 70))
        TM = pygame.transform.scale(TM, (70, 70))
        TR = pygame.transform.scale(TR, (70, 70))

        tile_width = int(MM.get_size()[0])
        tile_height = int(MM.get_size()[1])
        tiles_wide = int(math.ceil(self.width / (tile_width - 0)))
        tiles_high = int(math.ceil(self.height / (tile_height - 0)))

        for column in range(0, tiles_wide):
            if column == 0:
                self.image.blit(TL, (tile_width * column, 0))
            elif column == tiles_wide - 1:
                self.image.blit(TR, (self.width - tile_width, 0))
            else:
                self.image.blit(TM, (tile_width * column, 0))

        for row in range(1, tiles_high - 1):
            for column in range(0, tiles_wide):
                if column == 0:
                    self.image.blit(ML, (tile_width * column, tile_height * row))
                elif column == tiles_wide - 1:
                    self.image.blit(MR, (self.width - tile_width, tile_height * row))
                else:
                    self.image.blit(MM, (tile_width * column, tile_height * row))
        if tiles_high > 1:
            for column in range(0, tiles_wide):
                if column == 0:
                    self.image.blit(BL, (tile_width * column, self.height - tile_height))
                elif column == tiles_wide - 1:
                    self.image.blit(BR, (self.width - tile_width, self.height - tile_height))
                else:
                    self.image.blit(BM, (tile_width * column, self.height - tile_height))

    def get_rect(self):
        return pygame.rect.Rect((self.x, self.y), (self.width, self.height))

    def draw_platform(self, surface):
        surface.blit(self.image, (self.x, self.y))

class MovingPlatform(Platform):
    def __init__(self, position, dimensions, velocity, platform_type, facing_direction="all", corners=False):
        super().__init__(position, dimensions, platform_type, facing_direction, corners)
        self.__int_x = position[0]
        self.__int_y = position[1]
        self.__moving_right = True
        self.vel = velocity

    def movement(self):
        if self.x == self.__int_x - self.vel:
            self.__moving_right = True
        elif self.x == self.__int_x + self.vel:
            self.__moving_right = False
        if self.__moving_right:
            self.x += 1
        else:
            self.x -= 1
        self.get_rect().update(self.get_rect())

class Header:
    def __init__(self):
        # load the images
        self.health_front = pygame.image.load("images/HealthBarFront.png")
        self.health_back = pygame.image.load("images/HealthBarBack.png")
        self.header = pygame.image.load("images/header.png")
    def draw_header(self, surface):
        # scale images
        self.health_front = pygame.transform.scale(self.health_front, (225, 30))
        self.health_back = pygame.transform.scale(self.health_back, (300, 65))
        self.header = pygame.transform.scale(self.header, (1600, 100))

        surface.blit(self.header, (150, 0))
        surface.blit(self.health_back, (300, 10))
        surface.blit(self.health_front, (358.5, 27))





