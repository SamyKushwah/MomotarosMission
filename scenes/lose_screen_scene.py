import pygame
import sys
from ui_templates import button
from drivers import toolbox


def run(my_toolbox: toolbox.Toolbox):
    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/lose_screen/lose_screen.png")
    background = pygame.transform.scale(background, (w, h))

    # load home button image
    home_img = pygame.image.load("images/lose_screen/home_btn.png")
    home_img = pygame.transform.scale(home_img, (w * (1 / 5), h * (1 / 14)))
    button_home = button.Button(home_img)

    # load restart button image
    restart_img = pygame.image.load("images/lose_screen/restart_btn.png")
    restart_img = pygame.transform.scale(restart_img, (w * (1 / 3), h * (1 / 13)))
    button_restart = button.Button(restart_img)

    # draw the background and buttons with scaled position
    scene_screen = pygame.surface.Surface((w, h))
    scene_screen.blit(background, (0, 0))

    button_home.draw(scene_screen, (w * (1 / 4), h * (12 / 13)))
    button_restart.draw(scene_screen, (w * (3 / 4), h * (12 / 13)))

    my_toolbox.draw_to_screen(scene_screen)

    pygame.display.flip()

    # driver loop setup
    running = True
    while running:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            # Check if the mouse was clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if button_home.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_selector"
                elif button_restart.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_1"



        my_toolbox.clock.tick(60)
