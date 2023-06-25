from scenes.levels import level_1A
import pygame
from game_templates import momotaro
from scenes import pause_screen_scene, win_screen_scene, lose_screen_scene
from ui_templates import button
import sys


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
        w, h = self.level.width, self.level.height
        pause_img = pygame.image.load("images/game_ui/pause_btn.png")
        pause_img = pygame.transform.scale(pause_img, (90, 70))
        self.pause_btn = button.Button(pause_img)

        #self.mountain_background = pygame.transform.scale(
        #    pygame.image.load("images/backgrounds/mountains/parallax-mountain-bg.png"), (1920, 1080))
        #self.far_mountains = pygame.image.load("images/backgrounds/mountains/parallax-mountain-mountains.png")

    def run(self):
        # run event handling for the level until lvl_complete == True
        while not self.level_complete:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # if clicking
                    # need to put this code in whatever kevin did for how to win
                    # if win state reached then do this stuff
                    # for testing it just works with keys
                    '''pause_return = pause_screen_scene.run(self.my_toolbox)
                    if pause_return == "level_selector" or pause_return == "level_1":
                        return pause_return
                    if event.type == pygame.MOUSEBUTTONDOWN:  # change this to however the lose state is reached
                        lose_rt = lose_screen_scene.run(self.my_toolbox)
                        if lose_rt == "level_selector" or lose_rt == "level_1":
                            return lose_rt'''
                    if self.pause_btn.is_clicked(self.my_toolbox.adjusted_mouse_pos(event.pos)):  # if clicked pause button
                        return_st = pause_screen_scene.run(self.my_toolbox)
                        if return_st == "level_selector" or return_st == "level_1":  # break out of running level
                            return return_st
                        # in the fututre, should return someething like
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return_st = pause_screen_scene.run(self.my_toolbox)
                        if return_st == "level_selector" or return_st == "level_1":  # break out of running level
                            return return_st

            for moving_platform in self.level.moving_platform_list:
                moving_platform.movement()

            self.momotaro.update_movement()
            self.momotaro.check_collisions(self.level.collidable_list)
            self.momotaro.check_collision_interactible(self.level.interactible_list)

            self.momotaro.check_attacking(self.level.demon_list)

            for demon in self.level.demon_list:
                demon.update_movement(self.momotaro)
                demon.check_collisions(self.level.collidable_list)

            view_surface = pygame.surface.Surface((1920, 1080))

            self.draw()

            if self.momotaro.get_rect().centerx <= 960:
                view_surface.blit(self.image, (0, 0))
            elif self.momotaro.get_rect().centerx >= self.level.width - 960:
                view_surface.blit(self.image, (-(self.level.width - 1920), 0))
            else:
                view_surface.blit(self.image, ((-self.momotaro.get_rect().centerx) + (1920 / 2), 0))

            self.pause_btn.draw(view_surface, (80, 65))
            self.my_toolbox.draw_to_screen(view_surface)
            pygame.display.update()

            if self.level.interactible_list["torigate"][0].is_pushed():
                win_return = win_screen_scene.run(self.my_toolbox)
                if win_return == "level_selector" or win_return == "level_1":
                    return win_return
            elif self.momotaro.health <= 0:
                lose_rt = lose_screen_scene.run(self.my_toolbox)
                if lose_rt == "level_selector" or lose_rt == "level_1":
                    return lose_rt

            self.my_toolbox.clock.tick(60)

    def draw(self):
        self.image.fill((70, 70, 180))
        match self.level.background:
            case "cave":
                self.image.fill((20,20,30))
            case "mountains":
                if self.momotaro.get_rect().centerx <= 960:
                    positional = 0 - (self.momotaro.get_rect().centerx / 200)
                elif self.momotaro.get_rect().centerx >= self.level.width - 960:
                    positional = self.level.width - 1920 - (self.momotaro.get_rect().centerx / 200)
                else:
                    positional = self.momotaro.get_rect().centerx - (self.momotaro.get_rect().centerx / 200) - 960
                positional2 = self.momotaro.get_rect().centerx - (self.momotaro.get_rect().centerx / 30)
                # Main Background
                #self.image.blit(self.mountain_background, (positional, 0))
                #self.image.blit(self.mountain_background, (1920 + positional, 0))

                # Far Mountains
                #self.image.blit(self.far_mountains, (-544 + positional2, 850))
                #self.image.blit(self.far_mountains, (positional2, 850))
                #self.image.blit(self.far_mountains, (544 + positional2, 850))
        for platform in self.level.platform_list:
            platform.draw_platform(self.image)
        for platform in self.level.moving_platform_list:
            platform.draw_platform(self.image)
        for interactible_key in self.level.interactible_list.keys():
            for interactible in self.level.interactible_list[interactible_key]:
                interactible.draw(self.image)
        for demon in self.level.demon_list:
            if demon.health > 0:
                demon.draw(self.image)
            else:
                self.level.demon_list.remove(demon)
        for coin in self.level.coin_list:
            pygame.draw.rect(self.image, (0,200,0), coin.get_rect())

        self.momotaro.draw(self.image)