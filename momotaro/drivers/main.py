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

    next_state = "title_menu"

    os.chdir(pathlib.Path(__file__).parent.resolve().parent.resolve())

    pygame.display.set_caption('Momotaro\'s Mission')
    pygame.display.set_icon(pygame.image.load("images/MomotaroSprites/momotaroidle.png").convert_alpha())

    past_screen = None

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

            case "level_selector":
                # bring user to the level selection page
                next_state = level_select_scene.run(my_toolbox, past_screen)

            case "quit":
                pygame.quit()
                sys.exit()

            case "level_1":
                # bring the user to level 2
                my_game = game_manager.GameManager(my_toolbox, "level_1")
                next_state = my_game.run()
                pass  # todo

            case "level_2":
                # bring the user to level 2
                my_game = game_manager.GameManager(my_toolbox, "level_2")
                next_state = my_game.run()
                pass  # TODO

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