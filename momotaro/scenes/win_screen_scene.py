import pygame
import sys
from momotaro.ui_templates import button
from momotaro.drivers import toolbox


def run(my_toolbox: toolbox.Toolbox, current_level, coins):
    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    if coins == 0:
        background = pygame.image.load("images/win_screen/win_screen_0.png").convert_alpha()
    elif coins == 1:
        background = pygame.image.load("images/win_screen/win_screen_1.png").convert_alpha()
    elif coins == 2:
        background = pygame.image.load("images/win_screen/win_screen_2.png").convert_alpha()
    else:
        background = pygame.image.load("images/win_screen/win_screen_3.png").convert_alpha()

    background = pygame.transform.scale(background, (w, h))

    # load home button image
    home_img = pygame.Surface((400, 110), pygame.SRCALPHA)
    home_img.fill((255, 255, 255, 0))
    button_home = button.Button(home_img, text="Home")

    # load restart button image
    restart_img = pygame.Surface((610, 115), pygame.SRCALPHA)
    restart_img.fill((255, 255, 255, 0))
    button_restart = button.Button(restart_img, text="Restart")

    # load next button image if not on last level (level 3)
    if current_level != "level_3":
        next_img = pygame.Surface((400, 105), pygame.SRCALPHA)
        next_img.fill((255, 255, 255, 0))
        button_next = button.Button(next_img, text="Next")

    # draw the background and buttons with scaled position
    scene_screen = pygame.surface.Surface((w, h))
    scene_screen.blit(background, (0, 0))



    # driver loop setup
    running = True
    while running:

        button_home.draw(scene_screen, (w * (1 / 7), h * (12 / 13)), True)
        button_restart.draw(scene_screen, (w * (1 / 2), h * (12 / 13)), True)
        if current_level != "level_3":
            button_next.draw(scene_screen, (w * (6 / 7), h * (12 / 13)), True)

        my_toolbox.draw_to_screen(scene_screen)

        pygame.display.flip()

        my_toolbox.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            # Check if the mouse was clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if button_home.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_selector"
                elif button_restart.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return current_level
                elif current_level != "level_3" and button_next.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    if current_level == "level_1":
                        return "level_2"
                    elif current_level == "level_2":
                        return "level_3"


        my_toolbox.clock.tick(60)