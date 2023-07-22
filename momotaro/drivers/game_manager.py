from momotaro.scenes.levels import level_2, level_1, level_3
import pygame
from momotaro.game_templates import momotaro_player, pet_player
from momotaro.scenes import pause_screen_scene, win_screen_scene, lose_screen_scene
from momotaro.ui_templates import button
import sys
#from pygame import mixer
#pygame.mixer.init()

'''
Purpose: The GameManager object contains level and player information and regularly updates and polls player 
            interactions with the environment provided by the level.
'''


# "Persistent State" Game Manager:


class GameManager:

    def __init__(self, my_toolbox, level):
        self.my_toolbox = my_toolbox
        self.level_complete = False
        self.momotaro = None
        self.pet = None
        self.coins_collected = 0
        self.level_name = level
        match level:
            case "level_1":
                self.level, self.momotaro, self.pet = level_1.create_level(my_toolbox)
                self.controls_p1 = pygame.image.load("images/game_ui/controls_p1.png").convert_alpha()
                self.controls_p2 = pygame.image.load("images/game_ui/controls_p2.png").convert_alpha()

            case "level_2":
                self.level, self.momotaro, self.pet = level_2.create_level(my_toolbox)
                self.controls_p1 = pygame.image.load("images/game_ui/controls2_p1.png").convert_alpha()
                self.controls_p2 = pygame.image.load("images/game_ui/controls2_p2.png").convert_alpha()
                self.controls_p1 = pygame.transform.scale(self.controls_p1, (150, 100))
                self.controls_p2 = pygame.transform.scale(self.controls_p2, (150, 100))

            case "level_3":
                self.level, self.momotaro, self.pet = level_3.create_level(my_toolbox)
                self.controls_p1 = pygame.image.load("images/game_ui/controls3_p1.png").convert_alpha()
                self.controls_p2 = pygame.image.load("images/game_ui/controls3_p2.png").convert_alpha()

        self.image = pygame.surface.Surface((self.level.width, self.level.height))

        # win music setup using Shamisen Dance - By Steve Oxen Stinger 2
        win_path = "audio/win.mp3"
        self.win_sound = pygame.mixer.Sound(win_path)
        self.win_sound.set_volume(0.6)

        # lose music setup using Ninja Ambush - By Steve Oxen Stringer 2
        lose_path = "audio/lose.mp3"
        self.lose_sound = pygame.mixer.Sound(lose_path)
        self.lose_sound.set_volume(0.5)

        # Loading background image
        self.background = self.level.background
        # self.mountain_background = pygame.transform.scale(
        # pygame.image.load("images/backgrounds/level_1_bkgnd.png").convert_alpha(), (1920, 915))

        # Camera character locking
        self.camera_on_momotaro = True

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

                # if key pressing, can either be pausing, ending the game, or changing the camera view
                elif event.type == pygame.KEYDOWN:
                    # pause button pressed
                    if event.key == pygame.K_ESCAPE:
                        return_st = pause_screen_scene.run(self.my_toolbox, self.level_name)

                        # Poll pause scene next scene
                        if return_st == "level_selector" or return_st == self.level_name:  # break out of running level
                            # print('restarting')
                            return return_st

                    # changing the camera view
                    elif event.key == pygame.K_c:
                        self.camera_on_momotaro = not self.camera_on_momotaro

                    # both players at their gates and either pressed up to end the game
                    if self.level.interactible_list["torigate"][0].is_pushed() and self.level.interactible_list["torigate"][1].is_pushed() and \
                            (event.key == pygame.K_w or event.key == pygame.K_UP):
                        # add win sound
                        pygame.mixer.pause()
                        self.win_sound.play()
                        win_return = win_screen_scene.run(self.my_toolbox, self.level_name, self.coins_collected)
                        self.update_save_file(self.level_name, self.coins_collected)

                        # Poll the win game scene next scene
                        return win_return

            # Checking for if the game is over/failed (Momo dead or out of bounds)
            if self.momotaro.health <= 0 or self.momotaro.position[1] > 4000 or self.pet.health <= 0:
                pygame.mixer.pause()
                self.lose_sound.play()

                # only momotaro has different death animations, when the bird dies, use momotaro's oni death
                self.momotaro.death_type = "oni"

                lose_rt = self.play_death_animation()

                # Poll next scene from lose screen
                if lose_rt == "level_selector" or lose_rt == self.level_name or lose_rt == "quit":
                    return lose_rt

            # If momotaro is pushed below a block, he dies

            # If momotaro is pushed below a block, he dies

            if self.momotaro.standing and self.momotaro.standing_on != None:
                if self.momotaro.position[
                    1] + self.momotaro.get_rect().height // 2 > self.momotaro.standing_on.get_rect().top:
                    pygame.mixer.pause()
                    self.lose_sound.play()
                    self.momotaro.death_type = "crushed"
                    self.momotaro.health = 0
                    lose_rt = self.play_death_animation()
                    if lose_rt == "level_selector" or lose_rt == self.level_name or lose_rt == "quit":
                        return lose_rt

                if self.pet.standing and self.pet.standing_on != None:
                    if self.pet.position[
                        1] + self.pet.get_rect().height // 2 > self.pet.standing_on.get_rect().top:
                        self.momotaro.death_type = "crushed"
                        self.pet.health = 0
                        lose_rt = self.play_death_animation()
                        if lose_rt == "level_selector" or lose_rt == self.level_name or lose_rt == "quit":
                            return lose_rt

            self.tick_physics()
            val = self.draw()
            if val is not None:
                return val

            self.my_toolbox.clock.tick(60)

    '''
    Purpose: Main physics checker and updater for gameplay cycle. Updates character and enemy collision, movement, and
                interaction with obstacles and with each other. Specific details on what's being updated belong within 
                the character methods.
    '''

    def tick_physics(self):
        for moving_platform in self.level.moving_platform_list:
            moving_platform.movement()

        # Reset interactibles
        for interactible in self.level.interactible_list["button"]:
            interactible.set_pushed(False)

        self.momotaro.update_movement()
        self.momotaro.check_collisions(self.level.collidable_list)
        self.momotaro.check_collision_interactible(self.level.interactible_list, self)
        self.momotaro.check_damage(self.level.demon_list)
        self.momotaro.check_attacking(self.level.demon_list)

        self.pet.update_movement()
        self.pet.check_collisions(self.level.collidable_list)
        self.pet.check_collision_interactible(self.level.interactible_list, self)
        self.pet.check_damage(self.level.demon_list)

        #print(self.momotaro.position)
        for demon in self.level.demon_list:
            demon.update_movement(self.momotaro, self.pet)
            demon.check_collisions(self.level.collidable_list)

    '''
    Purpose: Calls the draw function of each object and draws backgrounds
    '''

    def draw(self):
        view_surface = pygame.surface.Surface((1920, 1080))

        # Draw Background
        if self.camera_on_momotaro:
            if self.momotaro.get_rect().centerx <= 960:
                positional = 0 - (960 / 200)
            elif self.momotaro.get_rect().centerx >= self.level.width - 960:
                positional = (self.level.width - 960) - ((self.level.width - 960) / 200) - 960
            else:
                positional = self.momotaro.get_rect().centerx - (self.momotaro.get_rect().centerx / 200) - 960
        else:
            if self.pet.get_rect().centerx <= 960:
                positional = 0 - (960 / 200)
            elif self.pet.get_rect().centerx >= self.level.width - 960:
                positional = (self.level.width - 960) - ((self.level.width - 960) / 200) - 960
            else:
                positional = self.pet.get_rect().centerx - (self.pet.get_rect().centerx / 200) - 960
        # Main Background
        self.image.blit(self.background, (positional, 100))
        self.image.blit(self.background, (1920 + positional, 100))

        if self.level_name == "level_1":
            self.image.blit(self.controls_p1, (120, 200))
            self.image.blit(self.controls_p2, (420, 200))

        if self.level_name == "level_2":
            self.image.blit(self.controls_p1, (100, 150))
            self.image.blit(self.controls_p2, (300, 150))

        # Draw platforms
        for platform in self.level.platform_list:
            platform.draw_platform(self.image)
        for platform in self.level.moving_platform_list:
            platform.draw_platform(self.image)
        for text in self.level.tutorial_text_list:
            text.draw(self.image, self.momotaro.position[0])

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
                    # self.level.coins_collected = 0
                    for coin in self.level.interactible_list[interactible_key]:
                        if not coin.collected:
                            coin.draw(self.image)

        # Draw players
        self.momotaro.draw(self.image)
        self.pet.draw(self.image)

        # camera centers on different player based on camera toggle C
        if self.camera_on_momotaro:
            if self.momotaro.get_rect().centerx <= 960:
                special_x = 0
            elif self.momotaro.get_rect().centerx >= self.level.width - 960:
                special_x = -(self.level.width - 1920)
            else:
                special_x = (-self.momotaro.get_rect().centerx) + (1920 / 2)
        else:
            if self.pet.get_rect().centerx <= 960:
                special_x = 0
            elif self.pet.get_rect().centerx >= self.level.width - 960:
                special_x = -(self.level.width - 1920)
            else:
                special_x = (-self.pet.get_rect().centerx) + (1920 / 2)

        view_surface.blit(self.image, (special_x, 0))

        # Draw Header
        self.level.header.draw_header(view_surface, self.momotaro.health, self.pet.health, self.coins_collected)

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
        elif level_name == "level_2":
            level_coins[1] = coins_collected
        else:
            level_coins[2] = coins_collected

        with open("save_data/game_data", 'w') as file:
            [file.write(str(coin) + "\n") for coin in level_coins]

    def play_death_animation(self):
        animation_delay = 50
        index = 0
        self.pet.velocity = [0, 0]
        # draw the background
        # scene_screen = pygame.surface.Surface((w, h))

        # driver loop setup
        running = True
        while running:

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

            if self.level_name == "level_1":
                self.image.blit(self.controls_p1, (120, 200))
                self.image.blit(self.controls_p2, (420, 200))

            if self.level_name == "level_2":
                self.image.blit(self.controls_p1, (100, 150))
                self.image.blit(self.controls_p2, (300, 150))


            # Draw platforms
            for platform in self.level.platform_list:
                platform.draw_platform(self.image)
            for platform in self.level.moving_platform_list:
                platform.draw_platform(self.image)
            for text in self.level.tutorial_text_list:
                text.draw(self.image, self.momotaro.position[0])

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
                        # self.level.coins_collected = 0
                        for coin in self.level.interactible_list[interactible_key]:
                            if not coin.collected:
                                coin.draw(self.image)

            # Draw players
            # self.pet.draw(self.image)
            # index = round(float(self.momotaro.frame_index) / float(animation_delay)

            if index > 2:
                return lose_screen_scene.run(self.my_toolbox, self.level_name)

            match self.momotaro.death_type:
                case "crushed":
                    self.momotaro.active_image = self.momotaro.death_crush_frames[index]
                    self.momotaro.frame_index += 1
                case "drown":
                    self.momotaro.active_image = self.momotaro.death_drown_frames[index]
                    self.momotaro.frame_index += 1
                case "oni":
                    self.momotaro.active_image = self.momotaro.death_oni_frames[index]
                    self.momotaro.frame_index += 1

            if self.momotaro.frame_index >= animation_delay:
                self.momotaro.frame_index = 0
                index += 1

            view_surface = pygame.surface.Surface((1920, 1080))

            self.image.blit(self.momotaro.active_image, self.momotaro.position)
            self.image.blit(self.pet.death_image, self.pet.position)

            if self.momotaro.get_rect().centerx <= 960:
                special_x = 0
            elif self.momotaro.get_rect().centerx >= self.level.width - 960:
                special_x = -(self.level.width - 1920)
            else:
                special_x = (-self.momotaro.get_rect().centerx) + (1920 / 2)

            view_surface.blit(self.image, (special_x, 0))

            # Draw Header
            self.level.header.draw_header(view_surface, self.momotaro.health, self.pet.health, self.coins_collected)

            # self.pause_btn.draw(view_surface, (80, 65))
            self.my_toolbox.draw_to_screen(view_surface)
            pygame.display.update()
