from scenes.levels import level_1A
import pygame
from game_templates import controllable
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
            self.momotaro.poll_movement_2()
            self.momotaro.check_collision_demon(self.level.demon_list)
            self.momotaro.new_check_collision(self.level.rectangle_list)
            self.momotaro.check_collision_obstacle(self.level.obstacle_list)
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
                rectangle.movement(self.image, 2)
            else:
                self.level.rectangle_list.remove(rectangle.get_rect())
                self.level.demon_list.remove(rectangle)
        for rectangle in self.level.coin_list:
            #placeholder color
            pygame.draw.rect(self.image, (0,200,0), rectangle.get_rect())

        self.momotaro.draw_sprite(self.image)

        #draw rest of characters and objects