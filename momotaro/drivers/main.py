import pygame
import sys
import os
import pathlib
from momotaro.drivers import toolbox
from momotaro.drivers import game_manager
from momotaro.scenes import level_select_scene, title_menu_scene, credits_scene
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
    level1_music.set_volume(0.1)

    # level 2 music setup using royalty free Misora (Traditional Japanese Music_03) from pixabay
    level2_path = "audio/level2_music.mp3"
    level2_music = pygame.mixer.Sound(level2_path)
    level2_music.set_volume(0.08)

    # level 3 music setup using royalty free Koto (Traditional Japanese Music_01) from pixabay
    level3_path = "audio/level3_music.mp3"
    level3_music = pygame.mixer.Sound(level3_path)
    level3_music.set_volume(0.1)

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
                # bring user to the level selection page
                if last_state != "title_menu":
                    background_music.play()
                next_state, past_screen = level_select_scene.run(my_toolbox, past_screen)

            case "level_1":
                pygame.mixer.pause()
                level1_music.play(loops=-1)
                my_game = game_manager.GameManager(my_toolbox, "level_1", past_screen)
                next_state, past_screen = my_game.run()
                level1_music.stop()
                last_state = "level1"
                pass  # todo

            case "level_2":
                # bring the user to level 2
                pygame.mixer.pause()
                level2_music.play(loops=-1)
                my_game = game_manager.GameManager(my_toolbox, "level_2", past_screen)
                next_state, past_screen = my_game.run()
                level2_music.stop()
                last_state = "level2"
                pass  # TODO

            case "level_3":
                # bring the user to level 3
                pygame.mixer.pause()
                level3_music.play(loops=-1)
                my_game = game_manager.GameManager(my_toolbox, "level_3")
                next_state = my_game.run()
                level3_music.stop()
                last_state = "level3"
                pass  # TODO

            case "credits":
                # bring the user to the credits page
                next_state, past_screen = credits_scene.run(my_toolbox, past_screen)

            case "level_complete":
                next_state = "level_selector"

            case "game_over":
                next_state = "level_selector"

            case "quit":
                pygame.quit()
                sys.exit()

        my_toolbox.clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()