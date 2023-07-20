import pygame
import sys
import os
import pathlib
from momotaro.drivers import toolbox
from momotaro.drivers import game_manager
from momotaro.scenes import level_select_scene, title_menu_scene
from momotaro.ui_templates import screen_transition

'''
Purpose: Main driver/executable for the game. Based on the state passing in by each scene, the game will 
            transition between various states. 
'''
def main():
    my_toolbox = toolbox.Toolbox()

    pygame.mixer.init()

    next_state = "title_menu"

    os.chdir(pathlib.Path(__file__).parent.resolve().parent.resolve())

    pygame.display.set_caption('Momotaro\'s Mission')
    pygame.display.set_icon(pygame.image.load("images/MomotaroSprites/momotaroidle.png").convert_alpha())

    past_screen = None

    # background music setup using royalty free Fun In Kyoto - By Steve Oxen
    background_music_path = "audio/background_music.mp3"
    background_music = pygame.mixer.Sound(background_music_path)
    background_music.set_volume(0.3)
    background_music.play(loops=-1)

    # level 1 music setup using royalty free Shamisen Dance - By Steve Oxen
    level1_path = "audio/level1_music.mp3"
    level1_music = pygame.mixer.Sound(level1_path)
    level1_music.set_volume(0.2)

    # level 2 music setup using royalty free Misora (Traditional Japanese Music_03) from pixabay
    level2_path = "audio/level2_music.mp3"
    level2_music = pygame.mixer.Sound(level2_path)
    level2_music.set_volume(0.3)

    last_state = ""

    # driver loop
    running = True
    while running:
        # Close out of the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # next_state will be returned by each scene
        match next_state:
            case "title_menu":
                next_state, past_screen = title_menu_scene.run(my_toolbox)
                last_state = "title_menu"
            case "level_selector":
                # pygame.mixer.unpause()
                # bring user to the level selection page
                #print(last_state)
                if last_state != "title_menu":
                    #print("hi")
                    background_music.play()
                next_state = level_select_scene.run(my_toolbox, past_screen)
            case "quit":
                pygame.quit()
                sys.exit()

            case "level_1":
                pygame.mixer.pause()
                level1_music.play(loops=-1)
                my_game = game_manager.GameManager(my_toolbox, "level_1")
                next_state = my_game.run()
                level1_music.stop()
                last_state = "level1"
                pass  # todo
            case "level_2":
                # bring the user to level 2
                # brings user to our debug level for now
                pygame.mixer.pause()
                level2_music.play(loops=-1)
                my_game = game_manager.GameManager(my_toolbox, "level_1A")
                next_state = my_game.run()
                level2_music.stop()
                last_state = "level2"
                pass  # TODO
            case "level_1A":
                # brings user to our debug level for now
                my_game = game_manager.GameManager(my_toolbox, "level_1A")
                next_state = my_game.run()
            case "level_3":
                # bring the user to level 3
                my_game = game_manager.GameManager(my_toolbox, "level_3")
                next_state = my_game.run()
                pass  # TODO
            case "credits":
                # bring the user to the credits page
                pass  # TODO
            case "pause":
                # bring the user to the pause page
                # selection = pause_screen.run_pause_screen(screen)
                pass  # TODO
            case "resume":
                # resume current level (unused for now)
                pass  # TODO
            case "restart":
                # restart current level
                pass  # TODO
            case "level_complete":
                next_state = "level_selector"
            case "game_over":
                next_state = "level_selector"

        my_toolbox.clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()