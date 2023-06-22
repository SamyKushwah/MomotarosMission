import time

from scenes.levels import level_1A
import pygame
from game_templates import controllable
from ui_templates import button
from scenes import pause_screen
import sys


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
        w, h = self.level.width, self.level.height
        #scene_screen = pygame.surface.Surface((w, h))
        pause_img = pygame.image.load("images/pause_btn.png")
        pause_img = pygame.transform.scale(pause_img, (w * (1 / 40), h * (1 / 40)))
        #pause_btn = button.Button(pause_img)
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
                elif event.type == pygame.MOUSEBUTTONDOWN: #if clicking
                    if self.pause_btn.is_clicked(self.my_toolbox.adjusted_mouse_pos(event.pos)): #if clicked pause button
                        return_st = pause_screen.run(self.my_toolbox)
                        if return_st is "level_selector" or return_st is "level_1": #break out of running level
                            return return_st
                        #in the fututre, should return someething like
            self.momotaro.poll_movement_2()
            self.momotaro.check_collision_demon(self.level.demon_list)
            self.momotaro.new_check_collision(self.level.rectangle_list)
            self.momotaro.check_collision_obstacle(self.level.obstacle_list)
            #
            self.momotaro.check_collision_coin(self.level.coin_list)
            #
            self.draw()
            view_surface = pygame.surface.Surface((1920, 1080))
            if self.momotaro.rect.centerx <= 960:
                view_surface.blit(self.image, (0, 0))
            elif self.momotaro.rect.centerx >= self.level.width - 960:
                view_surface.blit(self.image, (-(self.level.width - 1920), 0))
            else:
                view_surface.blit(self.image, ((-self.momotaro.rect.centerx) + (1920 / 2), 0))
            self.my_toolbox.draw_to_screen(view_surface)
            pygame.display.update()
            self.my_toolbox.clock.tick(60)

    def draw(self):
        self.image.fill((70, 70, 180))
        for rectangle in self.level.platform_list:
            rectangle.draw_platform(self.image)
        for rectangle in self.level.obstacle_list:
            #placeholder color
            #pygame.draw.rect(self.image, (0,200,0), rectangle.get_rect())
            rectangle.draw(self.image)
        for rectangle in self.level.demon_list:
            if rectangle.is_alive():
                rectangle.movement(self.image,2)
            else:
                self.level.rectangle_list.remove(rectangle.get_rect())
                self.level.demon_list.remove(rectangle)
        #
        for coin in self.level.coin_list:
            if not coin.is_collected(): #while the coin has not been collected draw the coin
                coin.draw_coin(self.image)
            else: #otherwise, increase the coin count
                self.level.coin_list.remove(coin) #removing coin from the list
                self.coins_collected += 1
        #
        self.pause_btn.draw(self.image, (100, 100))
        self.momotaro.draw_sprite(self.image)

        #draw rest of characters and objects