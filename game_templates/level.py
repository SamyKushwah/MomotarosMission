import pygame
import math

from game_templates import demon, button_obstacle


class Level:
    def __init__(self, my_toolbox, level_num, level_width, level_height, background = "cave"):
        self.width = level_width
        self.height = level_height
        self.level_num = level_num

        self.collidable_list = []
        self.platform_list = []
        self.moving_platform_list = []
        self.interactible_list = {}
        self.coin_list = []
        self.demon_list = []
        self.background = background

    def add_platform(self, position, dimensions, platform_type = "stone", facing_direction="all", corners=False):
        temp_platform = Platform(platform_type = platform_type, position = position, dimensions = dimensions, facing_direction = facing_direction, corners = corners)
        self.platform_list.append(temp_platform)
        self.collidable_list.append(temp_platform)

    def add_moving_platform(self, position, dimensions, max_speed, target, platform_type="stone",
                            facing_direction="all",
                            corners=False):
        temp_platform = MovingPlatform(position, dimensions, max_speed, target, platform_type, facing_direction,
                                       corners)
        print("Adding platform", temp_platform.get_rect())
        self.moving_platform_list.append(temp_platform)
        self.collidable_list.append(temp_platform)

    def add_demon(self, spawn_position, detection_range):
        temp_demon = demon.Demon(spawn_position, detection_range)
        self.demon_list.append(temp_demon)
        #print("adding rect:", temp_demon.get_rect())

    def add_obstacle(self, x, y, type):
        match type:
            case "button":
                temp_obstacle = button_obstacle.ButtonObstacle(x, y)
                try:
                    self.interactible_list["button"] += [temp_obstacle]
                except KeyError:
                    self.interactible_list["button"] = [temp_obstacle]

            case "torigate":
                temp_obs = button_obstacle.ToriObstacle(x, y)
                try:
                    self.interactible_list["torigate"] += [temp_obs]
                except KeyError:
                    self.interactible_list["torigate"] = [temp_obs]


class Platform:
    def __init__(self, position, dimensions, platform_type, facing_direction, corners=False):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.x = position[0]
        self.y = position[1]
        self.image = pygame.surface.Surface(dimensions)
        self.velocity = [0, 0]
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
    def __init__(self, position, dimensions, max_speed, target, platform_type, facing_direction="all", corners=False):
        super().__init__(position, dimensions, platform_type, facing_direction, corners)
        self.__int_x = position[0]
        self.__int_y = position[1]
        self.__moving_right = True
        self.max_speed = max_speed
        self.initial = position[0]
        self.target = target
        self.middle = int(self.initial + ((target - self.initial) / 2.0))
        print("middle:",self.middle)

    def movement(self):
        moved = (self.x - self.initial) + 1
        moved_middle = self.middle - self.initial
        moved_target = self.target - self.initial
        if self.x < self.middle:
            speed = ((moved / moved_middle) * self.max_speed) + 1
        else:
            speed = (1 - ((moved - moved_middle) / (moved_target - moved_middle))) * self.max_speed + 1
        speed = round(speed)
        if speed > self.max_speed:
            speed = self.max_speed
        if self.__moving_right:
            self.x = self.x + speed
            self.velocity[0] = speed
        else:
            self.x = self.x - speed
            self.velocity[0] = -speed
        if self.x > self.target:
            self.__moving_right = False
        elif self.x < self.initial:
            self.__moving_right = True
