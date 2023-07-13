from momotaro.scenes.levels import level_1A, level_1, level_3
import pygame
from momotaro.game_templates import momotaro_player
from momotaro.scenes import pause_screen_scene, win_screen_scene, lose_screen_scene
from momotaro.ui_templates import button
import sys

'''
Purpose: The GameManager object contains level and player information and regularly updates and polls player 
            interactions with the environment provided by the level.
'''
# "Persistent State" Game Manager:
class GameManager:
    def __init__(self, my_toolbox, level):
        self.my_toolbox = my_toolbox
        self.level_complete = False
        self.momotaro = momotaro_player.Momotaro([300, 300])
        self.coins_collected = 0
        self.level_name = level
        match level:
            case "level_1A":
                self.level = level_1A.create_level(my_toolbox)
                self.controls = pygame.image.load("images/game_ui/controls2.png").convert_alpha()
            case "level_1":
                self.level = level_1.create_level(my_toolbox)
                self.controls = pygame.image.load("images/game_ui/controls.png").convert_alpha()
            case "level_3":
                self.level = level_3.create_level(my_toolbox)
                self.controls = pygame.image.load("images/game_ui/controls3.png").convert_alpha()

        self.image = pygame.surface.Surface((self.level.width, self.level.height))

        # Creating pause button
        pause_img = pygame.image.load("images/game_ui/pause_btn.png").convert_alpha()
        pause_img = pygame.transform.scale(pause_img, (90, 70))
        self.pause_btn = button.Button(pause_img)

        # Loading background image
        self.background = self.level.background
        # self.mountain_background = pygame.transform.scale(
            # pygame.image.load("images/backgrounds/level_1_bkgnd.png").convert_alpha(), (1920, 915))



    '''
    Purpose: While the GameManager object is running, the main gameplay loop for the corresponding level occurs
    '''
    def run(self):
        # run event handling for the level until lvl_complete == True or broken out of
        while not self.level_complete:
            # Poll events/user inputs
            events = pygame.event.get()
            for event in events:
                # Exiting the Game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # if clicking, can click on pause button
                    if self.pause_btn.is_clicked(
                            self.my_toolbox.adjusted_mouse_pos(event.pos)):  # if clicked pause button
                        return_st = pause_screen_scene.run(self.my_toolbox, self.level_name)
                        if return_st == "level_selector" or return_st == self.level_name:  # break out of running level
                            #print('restarting')
                            return return_st

                # if key pressing, can either be pausing or ending the game
                elif event.type == pygame.KEYDOWN:
                    # pause button pressed
                    if event.key == pygame.K_ESCAPE:
                        return_st = pause_screen_scene.run(self.my_toolbox, self.level_name)

                        # Poll pause scene next scene
                        if return_st == "level_selector" or return_st == self.level_name:  # break out of running level
                            #print('restarting')
                            return return_st
                    # up button pressed (W) at the tori gate, ending the level
                    if self.level.interactible_list["torigate"][0].is_pushed() and event.key == pygame.K_w:
                        win_return = win_screen_scene.run(self.my_toolbox, self.level_name, self.coins_collected)
                        self.update_save_file(self.level_name, self.coins_collected)
                        # Poll the win game scene next scene
                        if win_return == "level_selector" or win_return == self.level_name or win_return ==  "quit":
                            return win_return

            # Checking for if the game is over/failed (Momo dead or out of bounds)
            if self.momotaro.health <= 0 or self.momotaro.position[1] > 5000:
                lose_rt = lose_screen_scene.run(self.my_toolbox, self.level_name)

                # Poll next scene from lose screen
                if lose_rt == "level_selector" or lose_rt == self.level_name or lose_rt == "quit":
                    return lose_rt

            # If momotaro is pushed below a block, he dies
            if self.momotaro.standing_on:
                if self.momotaro.position[
                    1] + self.momotaro.get_rect().height // 2 > self.momotaro.standing_on.get_rect().top:
                    lose_rt = lose_screen_scene.run(self.my_toolbox, self.level_name)
                    if lose_rt == "level_selector" or lose_rt == self.level_name or lose_rt == "quit":
                        return lose_rt

            self.tick_physics()
            self.draw()

            self.my_toolbox.clock.tick(60)


    '''
    Purpose: Main physics checker and updater for gameplay cycle. Updates character and enemy collision, movement, and
                interaction with obstacles and with each other. Specific details on what's being updated belong within 
                the character methods.
    '''
    def tick_physics(self):
        for moving_platform in self.level.moving_platform_list:
            moving_platform.movement()
        self.momotaro.update_movement()
        self.momotaro.check_collisions(self.level.collidable_list)
        self.momotaro.check_collision_interactible(self.level.interactible_list, self)
        self.momotaro.check_damage(self.level.demon_list)
        self.momotaro.check_attacking(self.level.demon_list)
        #print(self.momotaro.position)
        for demon in self.level.demon_list:
            demon.update_movement(self.momotaro)
            demon.check_collisions(self.level.collidable_list)


    '''
    Purpose: Calls the draw function of each object and draws backgrounds
    '''
    def draw(self):
        view_surface = pygame.surface.Surface((1920, 1080))

        # Draw Background
        # self.image.fill((70, 70, 180))
        if self.momotaro.get_rect().centerx <= 960:
            positional = 0 - (960 / 200)
        elif self.momotaro.get_rect().centerx >= self.level.width - 960:
            positional = (self.level.width - 960) - ((self.level.width - 960) / 200) - 960
        else:
            positional = self.momotaro.get_rect().centerx - (self.momotaro.get_rect().centerx / 200) - 960

        # Main Background
        self.image.blit(self.background, (positional, 100))
        self.image.blit(self.background, (1920 + positional, 100))
        self.image.blit(self.controls, (170, 200))

        # Draw platforms
        for platform in self.level.platform_list:
            platform.draw_platform(self.image)
        for platform in self.level.moving_platform_list:
            platform.draw_platform(self.image)

        # Draw demons
        for demon in self.level.demon_list:
            if demon.health > 0:
                demon.draw(self.image)
            else:
                self.level.demon_list.remove(demon)

        # Draw obstacles
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

        # Draw momotaro
        self.momotaro.draw(self.image)

        if self.momotaro.get_rect().centerx <= 960:
            view_surface.blit(self.image, (0, 0))
        elif self.momotaro.get_rect().centerx >= self.level.width - 960:
            view_surface.blit(self.image, (-(self.level.width - 1920), 0))
        else:
            view_surface.blit(self.image, ((-self.momotaro.get_rect().centerx) + (1920 / 2), 0))

        # Draw Header
        self.level.header.draw_header(view_surface, self.momotaro.health, self.coins_collected)

        #self.pause_btn.draw(view_surface, (80, 65))
        self.my_toolbox.draw_to_screen(view_surface)
        pygame.display.update()

    """
    Purpose: Saves the number of coins collected upon level clear to update on the select screen
    """
    def update_save_file(self, level_name, coins_collected):
        # get current info from the save file
        with open("save_data/game_data", 'r') as file:
            level_coins = [line.rstrip() for line in file]

        # depending on which level you are currently on, update the information
        if level_name == "level_1":
            level_coins[0] = coins_collected
        elif level_name == "level_1A":
            level_coins[1] = coins_collected
        else:
            level_coins[2] = coins_collected

        with open("save_data/game_data", 'w') as file:
            [file.write(str(coin) + "\n") for coin in level_coins]
