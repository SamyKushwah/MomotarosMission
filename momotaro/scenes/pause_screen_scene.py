import pygame
import sys
from momotaro.ui_templates import button
from momotaro.drivers import toolbox


def run(my_toolbox: toolbox.Toolbox, current_level):
    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/pause_screen/pause_screen_bkgnd.png").convert_alpha()
    background = pygame.transform.scale(background, (w, h))

    # load home button image
    home_img = pygame.Surface((400, 110), pygame.SRCALPHA)
    home_img.fill((255, 255, 255, 0))
    button_home = button.Button(home_img, text="Home")

    # load restart button image
    restart_img = pygame.Surface((610, 115), pygame.SRCALPHA)
    restart_img.fill((255, 255, 255, 0))
    button_restart = button.Button(restart_img, text="Restart")

    # load resume button image
    resume_img = pygame.Surface((575, 115), pygame.SRCALPHA)
    resume_img.fill((255, 255, 255, 0))
    button_resume = button.Button(resume_img, text="Resume")

    # draw the background
    scene_screen = pygame.surface.Surface((w, h))
    scene_screen.blit(background, (0, 0))

    # driver loop setup
    running = True
    while running:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check if the mouse was clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if button_home.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_selector"
                elif button_restart.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return current_level
                elif button_resume.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "resume"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"

        # draw the buttons with scaled position
        button_resume.draw(scene_screen, (w / 2, h * (6 / 13)), True)
        button_restart.draw(scene_screen, (w / 2, h * (8 / 13)), True)
        button_home.draw(scene_screen, (w / 2, h * (10 / 13)), True)

        # scene_screen.set_alpha(170)
        my_toolbox.draw_to_screen(scene_screen)
        pygame.display.flip()

        my_toolbox.clock.tick(60)