import pygame
import sys
from ui_templates import button
from drivers import toolbox


def run(my_toolbox: toolbox.Toolbox, current_level):
    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/win_screen/win_screen.png")
    background = pygame.transform.scale(background, (w, h))

    # load home button image
    home_img = pygame.image.load("images/win_screen/home_btn.png")
    home_img = pygame.transform.scale(home_img, (w * (1 / 5), h * (1 / 14)))
    button_home = button.Button(home_img)

    # load restart button image
    restart_img = pygame.image.load("images/win_screen/restart_btn.png")
    restart_img = pygame.transform.scale(restart_img, (w * (1 / 3), h * (1 / 13)))
    button_restart = button.Button(restart_img)

    # load next button image
    next_img = pygame.image.load("images/win_screen/next_btn.png")
    next_img = pygame.transform.scale(next_img, (w * (1 / 5), h * (1 / 14)))
    button_next = button.Button(next_img)

    # driver loop setup
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            # Check if the mouse was clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if button_home.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_selector"
                elif button_restart.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return current_level
                # elif button_next.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                # return "level_2" if pressed if we make a level 2

        # draw the background and buttons with scaled position
        scene_screen = pygame.surface.Surface((w, h))
        scene_screen.blit(background, (0, 0))

        button_home.draw(scene_screen, (w * (1 / 7), h * (12 / 13)))
        button_restart.draw(scene_screen, (w * (1 / 2), h * (12 / 13)))
        button_next.draw(scene_screen, (w * (6 / 7), h * (12 / 13)))

        my_toolbox.draw_to_screen(scene_screen)

        pygame.display.flip()

        my_toolbox.clock.tick(60)
