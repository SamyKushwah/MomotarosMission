import pygame
import math

from momotaro.game_templates import demon, obstacles, pet_player

from momotaro.ui_templates import tutorial


class Level:
    def __init__(self, my_toolbox, level_num, level_width, level_height, background="cave"):
        self.width = level_width
        self.height = level_height
        self.level_num = level_num
        self.collidable_list = []
        self.platform_list = []
        self.moving_platform_list = []
        self.tutorial_text_list = []
        self.interactible_list = {}
        self.demon_list = []
        self.spikes_list = []
        self.type = background
        self.pet_image = None
        if background == "mountains":
            self.background = pygame.transform.scale(
                pygame.image.load("images/backgrounds/level_1_bkgnd.png").convert_alpha(), (1920, 1080))
            self.header = Header("mountains")
        elif background == "cave":
            self.background = pygame.transform.scale(
                pygame.image.load("images/backgrounds/level_2_bkgnd.png").convert_alpha(), (1920, 1080))
            self.header = Header("cave")
        elif background == "bamboo":
            self.background = pygame.transform.scale(
                pygame.image.load("images/backgrounds/level_3_bkgnd.png").convert_alpha(), (1920, 1080))
            self.header = Header("bamboo")

        self.stone_imgs = []
        self.water_img = None
        self.spike_img = None

    def add_spikes(self, position, dimensions, vase_position, facing_direction="all", corners=False, duration=100):
        temp_platform = Platform(position, dimensions, self.stone_imgs, self.water_img, self.spike_img, "spikes",
                                 facing_direction, corners)
        self.platform_list.append(temp_platform)
        self.collidable_list.append(temp_platform)
        self.add_obstacle(vase_position[0], vase_position[1], "spike_vase", spikes=temp_platform, duration=duration)

    def add_platform(self, position, dimensions, platform_type="stone", facing_direction="all", corners=False):
        temp_platform = Platform(position, dimensions, self.stone_imgs, self.water_img, self.spike_img, platform_type, facing_direction,
                                 corners)
        self.platform_list.append(temp_platform)
        self.collidable_list.append(temp_platform)

    def add_moving_platform(self, position, dimensions, max_speed, target, platform_type="stone",
                            facing_direction="all",
                            corners=False):
        temp_platform = MovingPlatform(position, dimensions, max_speed, target, self.stone_imgs, self.water_img, self.spike_img,
                                       platform_type, facing_direction, corners)
        self.moving_platform_list.append(temp_platform)
        self.collidable_list.append(temp_platform)

    def add_demon(self, spawn_position, detection_range):
        temp_demon = demon.Demon(spawn_position, detection_range)
        self.demon_list.append(temp_demon)

    def add_obstacle(self, x, y, type, fence_initial=None, fence_final=None, fence_dimensions=None, gate_num=None, spikes=None, duration=100, dog_y=None):
        match type:
            case "button":
                temp_obstacle = obstacles.ButtonObstacle((x, y), fence_initial, fence_final, x, y, fence_dimensions,
                                                         self.level_num)
                try:
                    self.interactible_list["button"] += [temp_obstacle]
                except KeyError:
                    self.interactible_list["button"] = [temp_obstacle]

                self.collidable_list.append(temp_obstacle)

                temp_obstacle = temp_obstacle.fence
                try:
                    self.interactible_list["fence"] += [temp_obstacle]
                except KeyError:
                    self.interactible_list["fence"] = [temp_obstacle]

                self.collidable_list.append(temp_obstacle)

            case "torigate":
                temp_obs = obstacles.ToriObstacle(x, y, gate_num)
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
            case "dog_button":
                temp_obstacle = obstacles.ButtonObstacle((x, y), fence_initial, fence_final, x, y, fence_dimensions,
                                                         self.level_num, dog=True, dog_int_y=dog_y)
                try:
                    self.interactible_list["button"] += [temp_obstacle]
                except KeyError:
                    self.interactible_list["button"] = [temp_obstacle]

                self.collidable_list.append(temp_obstacle)

                temp_obstacle = temp_obstacle.fence
                try:
                    self.interactible_list["fence"] += [temp_obstacle]
                except KeyError:
                    self.interactible_list["fence"] = [temp_obstacle]

                self.collidable_list.append(temp_obstacle)
            case "spike_vase":
                temp_obstacle = obstacles.VaseObstacle(x, y, spikes, duration)
                try:
                    self.interactible_list["vase"] += [temp_obstacle]
                except KeyError:
                    self.interactible_list["vase"] = [temp_obstacle]
                self.collidable_list.append(temp_obstacle)

    def add_tutorial_text(self, x, y, x_min, x_max, y_min,y_max, dimensions, text, font_size=30):
        temp_text = tutorial.TutorialText((x, y), x_min, x_max,y_min, y_max, dimensions=dimensions, text=text,
                                              font_size=font_size)
        self.tutorial_text_list.append(temp_text)

    def load_stone_imgs(self):
        if self.type == "mountains":
            self.stone_imgs.append(pygame.image.load("images/tiles/stone/Stone(BL).png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone/Stone(BM).png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone/Stone(BR).png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone/Stone(ML).png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone/Stone(MM).png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone/Stone(MR).png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone/Stone(TL).png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone/Stone(TM).png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone/Stone(TR).png").convert_alpha())
        elif self.type == "cave":
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_2/stone2_BL.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_2/stone2_BM.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_2/stone2_BR.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_2/stone2_ML.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_2/stone2_MM.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_2/stone2_MR.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_2/stone2_TL.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_2/stone2_TM.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_2/stone2_TR.png").convert_alpha())
        elif self.type == "bamboo":
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_3/stone3_BL.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_3/stone3_BM.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_3/stone3_BR.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_3/stone3_ML.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_3/stone3_MM.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_3/stone3_MR.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_3/stone3_TL.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_3/stone3_TM.png").convert_alpha())
            self.stone_imgs.append(pygame.image.load("images/tiles/stone_3/stone3_TR.png").convert_alpha())

    def load_water_img(self):
        self.water_img = pygame.image.load("images/tiles/watertile.png").convert_alpha()
        self.spike_img = pygame.image.load("images/ObstacleButtonSprites/spikes.png").convert_alpha()


class Platform:
    def __init__(self, position, dimensions, stone_imgs, water_img, spike_img, platform_type, facing_direction, corners=False):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.x = position[0]
        self.y = position[1]
        self.image = pygame.surface.Surface(dimensions, pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.velocity = [0, 0]
        self.type = platform_type
        self.active = True
        match platform_type:
            case "stone":
                BL = stone_imgs[4]
                BM = stone_imgs[4]
                BR = stone_imgs[4]
                ML = stone_imgs[4]
                MM = stone_imgs[4]
                MR = stone_imgs[4]
                TL = stone_imgs[4]
                TM = stone_imgs[4]
                TR = stone_imgs[4]
                match facing_direction:
                    case "all":
                        BL = stone_imgs[0]
                        BM = stone_imgs[1]
                        BR = stone_imgs[2]
                        ML = stone_imgs[3]
                        MM = stone_imgs[4]
                        MR = stone_imgs[5]
                        TL = stone_imgs[6]
                        TM = stone_imgs[7]
                        TR = stone_imgs[8]
                    case "up":
                        TM = stone_imgs[7]
                        if corners:
                            TL = stone_imgs[6]
                            TR = stone_imgs[8]
                        else:
                            TL = TM
                            TR = TM
                    case "down":
                        BM = stone_imgs[1]
                        if corners:
                            BL = stone_imgs[0]
                            BR = stone_imgs[2]
                        else:
                            BL = BM
                            BR = BM
                    case "left":
                        ML = stone_imgs[3]
                        if corners:
                            BL = stone_imgs[0]
                            TL = stone_imgs[6]
                        else:
                            BL = ML
                            TL = ML
                    case "right":
                        MR = stone_imgs[5]
                        if corners:
                            BR = stone_imgs[2]
                            TR = stone_imgs[4]
                        else:
                            BR = MR
                            TR = MR

            case "water":
                BL = water_img
                BM = water_img
                BR = water_img
                ML = water_img
                MM = water_img
                MR = water_img
                TL = water_img
                TM = water_img
                TR = water_img
            case "spikes":
                BL = spike_img
                BM = spike_img
                BR = spike_img
                ML = spike_img
                MM = spike_img
                MR = spike_img
                TL = spike_img
                TM = spike_img
                TR = spike_img

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
        if self.active:
            surface.blit(self.image, (self.x, self.y))
        else:
            temp_image = self.image.copy()
            temp_image.set_alpha(20)
            surface.blit(temp_image, (self.x, self.y))


class MovingPlatform(Platform):
    def __init__(self, position, dimensions, max_speed, target, stone_imgs, water_img, spike_img, platform_type,
                 facing_direction="all", corners=False):
        super().__init__(position, dimensions, stone_imgs, water_img, spike_img, platform_type, facing_direction, corners)
        self.__int_x = position[0]
        self.__int_y = position[1]
        self.__moving_right = True
        self.__moving_down = True
        self.max_speed = max_speed
        self.initial = position
        self.target = target
        self.middle = [(self.initial[0] + self.target[0]) // 2, (self.initial[1] + self.target[1]) // 2]
        # print("middle:", self.middle[0])

    def movement(self):
        moved = [self.x - self.initial[0] + 1, self.y - self.initial[1] + 1]
        moved_middle = [self.middle[0] - self.initial[0], self.middle[1] - self.initial[1]]
        moved_target = [self.target[0] - self.initial[0], self.target[1] - self.initial[1]]

        if self.target[0] != self.initial[0]:
            # print('move x')
            x_progress = moved[0] / moved_target[0]

            if self.x < self.middle[0]:
                speed_x = (moved[0] / moved_middle[0]) * self.max_speed + 1
            else:
                speed_x = (1 - (
                            (moved[0] - moved_middle[0]) / (moved_target[0] - moved_middle[0]))) * self.max_speed + 1
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
                speed_y = (1 - (
                            (moved[1] - moved_middle[1]) / (moved_target[1] - moved_middle[1]))) * self.max_speed + 1
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
    def __init__(self, level_type):
        # load the images
        self.health_front = pygame.image.load("images/game_ui/HealthBarFront.png").convert_alpha()
        if level_type == "mountains":
            self.health_back = pygame.image.load("images/game_ui/HealthBarBack.png").convert_alpha()
            self.header = pygame.image.load("images/game_ui/header.png").convert_alpha()
            self.coin_back = pygame.image.load("images/game_ui/CoinBarBack.png").convert_alpha()
        elif level_type == "cave":
            self.health_back = pygame.image.load("images/game_ui/HealthBarBack2.png").convert_alpha()
            self.header = pygame.image.load("images/game_ui/header2.png").convert_alpha()
            self.coin_back = pygame.image.load("images/game_ui/CoinBarBack2.png").convert_alpha()
        elif level_type == "bamboo":
            self.health_back = pygame.image.load("images/game_ui/HealthBarBack3.png").convert_alpha()
            self.header = pygame.image.load("images/game_ui/header3.png").convert_alpha()
            self.coin_back = pygame.image.load("images/game_ui/CoinBarBack3.png").convert_alpha()

        self.zero = pygame.image.load("images/game_ui/zero.png").convert_alpha()
        self.one = pygame.image.load("images/game_ui/one.png").convert_alpha()
        self.two = pygame.image.load("images/game_ui/two.png").convert_alpha()
        self.three = pygame.image.load("images/game_ui/three.png").convert_alpha()
        self.player_1_txt = pygame.image.load("images/game_ui/player_one_txt.png").convert_alpha()
        self.player_2_txt = pygame.image.load("images/game_ui/player_two_txt.png").convert_alpha()
        self.momo = pygame.image.load("images/MomotaroSprites/momotaroidle.png").convert_alpha()
        self.bird = pygame.image.load("images/player2/bird.png").convert_alpha()
        self.dog = pygame.image.load("images/player2/dog_idle_right.png").convert_alpha()
        self.monkey = pygame.image.load("images/player2/monkey_idle_right.png").convert_alpha()

        # scale images
        self.health_front = pygame.transform.scale(self.health_front, (225, 30))
        self.health_back = pygame.transform.scale(self.health_back, (300, 65))
        self.header = pygame.transform.scale(self.header, (2200, 100))
        self.coin_back = pygame.transform.scale(self.coin_back, (140, 65))
        self.zero = pygame.transform.scale(self.zero, (125, 65))
        self.one = pygame.transform.scale(self.one, (125, 65))
        self.two = pygame.transform.scale(self.two, (125, 65))
        self.three = pygame.transform.scale(self.three, (125, 65))
        self.player_1_txt = pygame.transform.scale(self.player_1_txt, (200, 40))
        self.player_2_txt = pygame.transform.scale(self.player_2_txt, (200, 40))
        self.momo = pygame.transform.scale(self.momo, (50, 80))
        self.bird = pygame.transform.scale(self.bird, (60, 80))
        self.dog = pygame.transform.scale(self.dog, (60, 80))
        self.monkey = pygame.transform.scale(self.monkey, (60, 80))

    def draw_header(self, surface, momo_health, pet_health, coins, pet):

        # draw images to the screen
        surface.blit(self.header, (-200, 0))
        surface.blit(self.player_1_txt, (210, 30))
        surface.blit(self.momo, (435, 10))

        surface.blit(self.health_back, (540, 15))
        health_len = 225 * (momo_health / 100)

        self.health_front = pygame.transform.scale(self.health_front, (health_len, 30))
        surface.blit(self.health_front, (598.5, 32))

        surface.blit(self.coin_back, (890, 15))

        if coins == 0:
            surface.blit(self.zero, (900, 15))
        elif coins == 1:
            surface.blit(self.one, (900, 15))
        elif coins == 2:
            surface.blit(self.two, (900, 15))
        else:
            surface.blit(self.three, (900, 15))

        surface.blit(self.player_2_txt, (1080, 30))
        if pet == "bird":
            surface.blit(self.bird, (1305, 10))
        elif pet == "dog":
            surface.blit(self.dog, (1305, 10))
        elif pet == "monkey":
            surface.blit(self.monkey, (1305, 10))

        surface.blit(self.health_back, (1410, 15))
        health_len = 225 * (pet_health / 50)
        self.health_front = pygame.transform.scale(self.health_front, (health_len, 30))
        surface.blit(self.health_front, (1468.5, 32))
