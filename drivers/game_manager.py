from scenes.levels import level_1A
import pygame
from game_templates import momotaro
from scenes import pause_screen_scene, win_screen_scene, lose_screen_scene
from ui_templates import button
import sys


# "Persistent State" Game Manager:
class GameManager:
    def __init__(self, my_toolbox, level):
        self.my_toolbox = my_toolbox
        self.level_complete = False
        self.momotaro = momotaro.Momotaro([300, 300])
        self.coins_collected = 0
        match level:
            case "level_1A":
                self.level = level_1A.create_level(my_toolbox)

        self.image = pygame.surface.Surface((self.level.width, self.level.height))

        # Creating pause button
        pause_img = pygame.image.load("images/game_ui/pause_btn.png").convert_alpha()
        pause_img = pygame.transform.scale(pause_img, (90, 70))
        self.pause_btn = button.Button(pause_img)

        self.mountain_background = pygame.transform.scale(
            pygame.image.load("images/backgrounds/level_1_bkgnd_lightest.png").convert_alpha(), (1920, 915))
        # self.far_mountains = pygame.image.load("images/backgrounds/mountains/parallax-mountain-mountains-reduced.png").convert_alpha()

    def run(self):
        # run event handling for the level until lvl_complete == True
        while not self.level_complete:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # if clicking
                    if self.pause_btn.is_clicked(
                            self.my_toolbox.adjusted_mouse_pos(event.pos)):  # if clicked pause button
                        return_st = pause_screen_scene.run(self.my_toolbox)
                        if return_st == "level_selector" or return_st == "level_1":  # break out of running level
                            return return_st
                        # in the fututre, should return someething like
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return_st = pause_screen_scene.run(self.my_toolbox)
                        if return_st == "level_selector" or return_st == "level_1":  # break out of running level
                            return return_st
                if self.level.interactible_list["torigate"][0].is_pushed():
                    win_return = win_screen_scene.run(self.my_toolbox)
                    if win_return == "level_selector" or win_return == "level_1":
                        return win_return
                elif self.momotaro.health <= 0:
                    lose_rt = lose_screen_scene.run(self.my_toolbox)
                    if lose_rt == "level_selector" or lose_rt == "level_1" or lose_rt == "quit":
                        return lose_rt

            self.tick_physics()
            self.draw()

            self.my_toolbox.clock.tick(60)

    def tick_physics(self):
        for moving_platform in self.level.moving_platform_list:
            moving_platform.movement()
        self.momotaro.update_movement()
        self.momotaro.check_collisions(self.level.collidable_list)
        self.momotaro.check_collision_interactible(self.level.interactible_list, self)
        self.momotaro.check_damage(self.level.demon_list)
        self.momotaro.check_attacking(self.level.demon_list)
        for demon in self.level.demon_list:
            demon.update_movement(self.momotaro)
            demon.check_collisions(self.level.collidable_list)

    def draw(self):
        view_surface = pygame.surface.Surface((1920, 1080))

        self.image.fill((70, 70, 180))
        match self.level.background:
            case "cave":
                self.image.fill((20, 20, 30))
            case "mountains":
                if self.momotaro.get_rect().centerx <= 960:
                    positional = 0 - (960 / 200)
                elif self.momotaro.get_rect().centerx >= self.level.width - 960:
                    positional = (self.level.width - 960) - ((self.level.width - 960) / 200) - 960
                else:
                    positional = self.momotaro.get_rect().centerx - (self.momotaro.get_rect().centerx / 200) - 960
                # Main Background
                self.image.blit(self.mountain_background, (positional, 100))
                self.image.blit(self.mountain_background, (1920 + positional, 100))

                # Far Mountains
                # self.image.blit(self.far_mountains, (-544 + positional, 850))
                # self.image.blit(self.far_mountains, (positional, 850))
                # self.image.blit(self.far_mountains, (544 + positional, 850))
        for platform in self.level.platform_list:
            platform.draw_platform(self.image)
        for platform in self.level.moving_platform_list:
            platform.draw_platform(self.image)
        for demon in self.level.demon_list:
            if demon.health > 0:
                demon.draw(self.image)
            else:
                self.level.demon_list.remove(demon)
        for interactible_key in self.level.interactible_list.keys():
            match interactible_key:
                case "button":
                    for obstacle in self.level.interactible_list[interactible_key]:
                        obstacle.draw(self.image)
                case "torigate":
                    for obstacle in self.level.interactible_list[interactible_key]:
                        obstacle.draw(self.image)
                case "coin":
                    #self.level.coins_collected = 0
                    for coin in self.level.interactible_list[interactible_key]:
                        if not coin.collected:
                            coin.draw(self.image)

        self.momotaro.draw(self.image)

        if self.momotaro.get_rect().centerx <= 960:
            view_surface.blit(self.image, (0, 0))
        elif self.momotaro.get_rect().centerx >= self.level.width - 960:
            view_surface.blit(self.image, (-(self.level.width - 1920), 0))
        else:
            view_surface.blit(self.image, ((-self.momotaro.get_rect().centerx) + (1920 / 2), 0))

        self.level.header.draw_header(view_surface, self.momotaro.health, self.coins_collected)

        # self.pause_btn.draw(view_surface, (80, 65))
        self.my_toolbox.draw_to_screen(view_surface)
        pygame.display.update()
