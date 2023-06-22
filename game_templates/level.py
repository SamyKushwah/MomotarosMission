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
        self.interactible_list = []
        self.coin_list = []
        self.demon_list = []

    def add_platform(self, platform_type, position, dimensions, facing_direction="all", corners=False):
        temp_platform = Platform(platform_type, position, dimensions, facing_direction, corners)
        print("Adding platform", temp_platform.get_rect())
        self.platform_list.append(temp_platform)
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
    def __init__(self, platform_type, position, dimensions, facing_direction="all", corners=False):
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
