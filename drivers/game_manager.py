from scenes.levels import level_1A
import pygame
from game_templates import controllable
from scenes import pause_screen_scene, win_screen_scene, lose_screen_scene
import sys
from ui_templates import button


class GameManager:
    def __init__(self, my_toolbox, level):
        self.my_toolbox = my_toolbox
        self.level_complete = False
        self.momotaro = controllable.Momotaro()
        self.momotaro.sprites_init()
        self.coins_collected = 0
        match level:
            case "level_1A":
                self.level = level_1A.create_level(my_toolbox)

        self.image = pygame.surface.Surface((self.level.width, self.level.height))

        # Creating pause button
        pause_img = pygame.image.load("images/game_ui/pause_btn.png")
        pause_img = pygame.transform.scale(pause_img, (90, 70))
        self.pause_btn = button.Button(pause_img)

    def run(self):
        # run event handling for the level until lvl_complete == True
        while not self.level_complete:
            events = pygame.event.get()
            for event in events:
                self.momotaro.poll_movement(event)
                self.momotaro.poll_attack(event)
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

            self.momotaro.poll_movement_2()
            self.momotaro.check_collision_demon(self.level.demon_list)
            self.momotaro.new_check_collision(self.level.collidable_list)
            self.momotaro.check_collision_interactible(self.level.interactible_list)
            self.draw()
            view_surface = pygame.surface.Surface((1920, 1080))
            if self.momotaro.rect.centerx <= 960:
                view_surface.blit(self.image, (0, 0))
            elif self.momotaro.rect.centerx >= self.level.width - 960:
                view_surface.blit(self.image, (-(self.level.width - 1920), 0))
            else:
                view_surface.blit(self.image, ((-self.momotaro.rect.centerx) + (1920 / 2), 0))
            self.level.header.draw_header(view_surface, self.momotaro.get_health(), self.coins_collected)
            self.my_toolbox.draw_to_screen(view_surface)
            self.pause_btn.draw(view_surface, (50, 15))
            pygame.display.update()
            self.my_toolbox.clock.tick(60)

    def draw(self):
        view_surface = pygame.surface.Surface((1920, 1080))
        self.image.fill((70, 70, 180))
        for platform in self.level.platform_list:
            platform.draw_platform(self.image)
        for platform in self.level.moving_platform_list:
            platform.movement()
            platform.draw_platform(self.image)
        for interactible in self.level.interactible_list:
            interactible.draw(self.image)
        for demon in self.level.demon_list:
            if demon.is_alive():
                demon.movement(self.image, 2)
            else:
                self.level.demon_list.remove(demon)
        for coin in self.level.coin_list:
            pygame.draw.rect(self.image, (0, 200, 0), coin.get_rect())

        self.momotaro.draw_sprite(self.image)
