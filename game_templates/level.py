import pygame
import math

from game_templates import demon, obstacles


class Level:
    def __init__(self, my_toolbox, level_num, level_width, level_height, background = "cave"):
        self.width = level_width
        self.height = level_height
        self.level_num = level_num
        self.collidable_list = []
        self.platform_list = []
        self.moving_platform_list = []
        self.interactible_list = {}
        self.demon_list = []
        self.background = background
        self.header = Header()

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

    def add_obstacle(self, x, y, type):
        match type:
            case "button":
                temp_obstacle = obstacles.ButtonObstacle(x, y)
                try:
                    self.interactible_list["button"] += [temp_obstacle]
                except KeyError:
                    self.interactible_list["button"] = [temp_obstacle]

            case "torigate":
                temp_obs = obstacles.ToriObstacle(x, y)
                try:
                    self.interactible_list["torigate"] += [temp_obs]
                except KeyError:
                    self.interactible_list["torigate"] = [temp_obs]

            case "coin":
                temp_obs = obstacles.CoinObstacle(x, y)
                try:
                    self.interactible_list["coin"] += [temp_obs]
                except KeyError:
                    self.interactible_list["coin"] = [temp_obs]


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
                BL = pygame.image.load("images/tiles/stone/Stone(MM).png").convert()
                BM = pygame.image.load("images/tiles/stone/Stone(MM).png").convert()
                BR = pygame.image.load("images/tiles/stone/Stone(MM).png").convert()
                ML = pygame.image.load("images/tiles/stone/Stone(MM).png").convert()
                MM = pygame.image.load("images/tiles/stone/Stone(MM).png").convert()
                MR = pygame.image.load("images/tiles/stone/Stone(MM).png").convert()
                TL = pygame.image.load("images/tiles/stone/Stone(MM).png").convert()
                TM = pygame.image.load("images/tiles/stone/Stone(MM).png").convert()
                TR = pygame.image.load("images/tiles/stone/Stone(MM).png").convert()
                match facing_direction:
                    case "all":
                        BL = pygame.image.load("images/tiles/stone/Stone(BL).png").convert()
                        BM = pygame.image.load("images/tiles/stone/Stone(BM).png").convert()
                        BR = pygame.image.load("images/tiles/stone/Stone(BR).png").convert()
                        ML = pygame.image.load("images/tiles/stone/Stone(ML).png").convert()
                        MM = pygame.image.load("images/tiles/stone/Stone(MM).png").convert()
                        MR = pygame.image.load("images/tiles/stone/Stone(MR).png").convert()
                        TL = pygame.image.load("images/tiles/stone/Stone(TL).png").convert()
                        TM = pygame.image.load("images/tiles/stone/Stone(TM).png").convert()
                        TR = pygame.image.load("images/tiles/stone/Stone(TR).png").convert()
                    case "up":
                        TM = pygame.image.load("images/tiles/stone/Stone(TM).png").convert()
                        if corners:
                            TL = pygame.image.load("images/tiles/stone/Stone(TL).png").convert()
                            TR = pygame.image.load("images/tiles/stone/Stone(TR).png").convert()
                        else:
                            TL = pygame.image.load("images/tiles/stone/Stone(TM).png").convert()
                            TR = pygame.image.load("images/tiles/stone/Stone(TM).png").convert()
                    case "down":
                        BM = pygame.image.load("images/tiles/stone/Stone(BM).png").convert()
                        if corners:
                            BL = pygame.image.load("images/tiles/stone/Stone(BL).png").convert()
                            BR = pygame.image.load("images/tiles/stone/Stone(BR).png").convert()
                        else:
                            BL = pygame.image.load("images/tiles/stone/Stone(BM).png").convert()
                            BR = pygame.image.load("images/tiles/stone/Stone(BM).png").convert()
                    case "left":
                        ML = pygame.image.load("images/tiles/stone/Stone(ML).png").convert()
                        if corners:
                            BL = pygame.image.load("images/tiles/stone/Stone(BL).png").convert()
                            TL = pygame.image.load("images/tiles/stone/Stone(TL).png").convert()
                        else:
                            BL = pygame.image.load("images/tiles/stone/Stone(ML).png").convert()
                            TL = pygame.image.load("images/tiles/stone/Stone(ML).png").convert()
                    case "right":
                        MR = pygame.image.load("images/tiles/stone/Stone(MR).png").convert()
                        if corners:
                            BR = pygame.image.load("images/tiles/stone/Stone(BR).png").convert()
                            TR = pygame.image.load("images/tiles/stone/Stone(TR).png").convert()
                        else:
                            BR = pygame.image.load("images/tiles/stone/Stone(MR).png").convert()
                            TR = pygame.image.load("images/tiles/stone/Stone(MR).png").convert()

            case "water":
                BL = pygame.image.load("images/tiles/watertile.png").convert()
                BM = pygame.image.load("images/tiles/watertile.png").convert()
                BR = pygame.image.load("images/tiles/watertile.png").convert()
                ML = pygame.image.load("images/tiles/watertile.png").convert()
                MM = pygame.image.load("images/tiles/watertile.png").convert()
                MR = pygame.image.load("images/tiles/watertile.png").convert()
                TL = pygame.image.load("images/tiles/watertile.png").convert()
                TM = pygame.image.load("images/tiles/watertile.png").convert()
                TR = pygame.image.load("images/tiles/watertile.png").convert()

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
        self.__moving_down = True
        self.max_speed = max_speed
        self.initial = position
        self.target = target
        self.middle = [(self.initial[0] + self.target[0]) // 2, (self.initial[1] + self.target[1]) // 2]
        print("middle:", self.middle[0])

    def movement(self):
        moved = [self.x - self.initial[0] + 1, self.y - self.initial[1] + 1]
        moved_middle = [self.middle[0] - self.initial[0], self.middle[1] - self.initial[1]]
        moved_target = [self.target[0] - self.initial[0], self.target[1] - self.initial[1]]

        if self.target[0] != self.initial[0]:
            x_progress = moved[0] / moved_target[0]

            if self.x < self.middle[0]:
                speed_x = (moved[0] / moved_middle[0]) * self.max_speed + 1
            else:
                speed_x = (1 - ((moved[0] - moved_middle[0]) / (moved_target[0] - moved_middle[0]))) * self.max_speed + 1
            speed_x = min(round(speed_x), self.max_speed)

            if self.__moving_right:
                self.x += speed_x
                self.velocity[0] = speed_x
            else:
                self.x -= speed_x
                self.velocity[0] = -speed_x

            if self.x > self.target[0]:
                self.__moving_right = False
            elif self.x < self.initial[0]:
                self.__moving_right = True

            last_y = self.y
            self.y = self.initial[1] + (moved_target[1] * x_progress)
            self.velocity[1] = self.y - last_y

        elif self.target[1] != self.initial[1]:
            if self.y < self.middle[1]:
                speed_y = (moved[1] / moved_middle[1]) * self.max_speed + 1
            else:
                speed_y = (1 - ((moved[1] - moved_middle[1]) / (moved_target[1] - moved_middle[1]))) * self.max_speed + 1
            speed_y = min(round(speed_y), self.max_speed)

            if self.__moving_down:
                self.y += speed_y
                self.velocity[1] = speed_y
            else:
                self.y -= speed_y
                self.velocity[1] = -speed_y

            if self.y > self.target[1]:
                self.__moving_down = False
            elif self.y < self.initial[1]:
                self.__moving_down = True

class Header:
    def __init__(self):
        # load the images
        self.health_front = pygame.image.load("images/level_1/HealthBarFront.png")
        self.health_back = pygame.image.load("images/level_1/HealthBarBack.png")
        self.header = pygame.image.load("images/level_1/header.png")
        self.coin_back = pygame.image.load("images/level_1/CoinBarBack.png")
        self.zero = pygame.image.load("images/level_1/zero.png")
        self.one = pygame.image.load("images/level_1/one.png")
        self.two = pygame.image.load("images/level_1/two.png")
        self.three = pygame.image.load("images/level_1/three.png")
        self.player_1_txt = pygame.image.load("images/level_1/player_one_txt.png")
        self.player_2_txt = pygame.image.load("images/level_1/player_two_txt.png")
        self.momo = pygame.image.load("images/MomotaroSprites/MomoStandingIdle.png")

        # scale images
        self.health_front = pygame.transform.scale(self.health_front, (225, 30))
        self.health_back = pygame.transform.scale(self.health_back, (300, 65))
        self.header = pygame.transform.scale(self.header, (1000, 100))
        self.coin_back = pygame.transform.scale(self.coin_back, (140, 65))
        self.zero = pygame.transform.scale(self.zero, (125, 65))
        self.one = pygame.transform.scale(self.one, (125, 65))
        self.two = pygame.transform.scale(self.two, (125, 65))
        self.three = pygame.transform.scale(self.three, (125, 65))
        self.player_1_txt = pygame.transform.scale(self.player_1_txt, (145, 50))
        # self.player_2_txt = pygame.transform.scale(self.player_2_txt, (145, 50))
        self.momo = pygame.transform.scale(self.momo, (50, 80))

    def draw_header(self, surface, health, coins):
        # draw images to the screen
        surface.blit(self.header, (460, 0))
        surface.blit(self.player_1_txt, (570, 30))
        surface.blit(self.momo, (745, 10))

        surface.blit(self.health_back, (850, 15))
        health_len = 225 * (health / 100)
        self.health_front = pygame.transform.scale(self.health_front, (health_len, 30))
        surface.blit(self.health_front, (908.5, 32))

        surface.blit(self.coin_back, (1200, 15))

        if coins == 0:
            surface.blit(self.zero, (1200, 15))
        elif coins == 1:
            surface.blit(self.one, (1200, 15))
        elif coins == 2:
            surface.blit(self.two, (1200, 15))
        else:
            surface.blit(self.three, (1200, 15))

        # surface.blit(self.player_2_txt, (1230, 30))