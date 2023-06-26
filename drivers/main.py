import pygame
import sys
import os
import toolbox
import game_manager
from scenes import level_select_scene, title_menu_scene

'''
Purpose: Main driver/executable for the game. Based on the state passing in by each scene, the game will 
            transition between various states. 
'''
def main():
    my_toolbox = toolbox.Toolbox()

    next_state = "title_menu"

    os.chdir("../")

    pygame.display.set_caption('Momotaro\'s Mission')
    pygame.display.set_icon(pygame.image.load("images/MomotaroSprites/momotaroidle.png").convert_alpha())

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
                next_state = title_menu_scene.run(my_toolbox)
            case "level_selector":
                # bring user to the level selection page
                next_state = level_select_scene.run(my_toolbox)
            case "quit":
                pygame.quit()
                sys.exit()

            case "level_1":
                # selection = ruhi_level1.run_level(screen)
                # selection = level_1_screen.run_level_1_screen(screen)
                my_game = game_manager.GameManager(my_toolbox, "level_1")
                next_state = my_game.run()
                pass  # todo
            case "level_2":
                # bring the user to level 2

                # brings user to our debug level for now
                my_game = game_manager.GameManager(my_toolbox, "level_1A")
                next_state = my_game.run()
                pass  # TODO
            case "level_1A":
                # brings user to our debug level for now
                my_game = game_manager.GameManager(my_toolbox, "level_1A")
                next_state = my_game.run()
            case "level_3":
                # bring the user to level 3
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