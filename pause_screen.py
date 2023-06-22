import pygame
import sys
from ui_templates import button
from drivers import toolbox


def run(my_toolbox: toolbox.Toolbox):
    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/pause_screen/pause_screen_bkgnd.png")
    background = pygame.transform.scale(background, (w, h))

    # load home button image
    home_img = pygame.image.load("images/pause_screen/home_btn.png")
    home_img = pygame.transform.scale(home_img, (w * (1 / 4), h * (1 / 13)))
    button_home = button.Button(home_img)

    #load restart button image
    restart_img = pygame.image.load("images/pause_screen/restart_btn.png")
    restart_img = pygame.transform.scale(restart_img, (w * (1 / 3), h * (1 / 12)))
    button_restart = button.Button(restart_img)

    #load resume button image
    resume_img = pygame.image.load("images/pause_screen/resume_btn.png")
    resume_img = pygame.transform.scale(resume_img, (w * (1 / 3), h * (1 / 12)))
    button_resume = button.Button(resume_img)

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
                elif button_resume.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "resume"
                elif button_restart.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_1"

        # draw the background and buttons with scaled position
        scene_screen = pygame.surface.Surface((w, h))
        scene_screen.blit(background, (0, 0))

        button_resume.draw(scene_screen, (w / 2, h * (6 / 13)))
        button_restart.draw(scene_screen, (w / 2, h * (8 / 13)))
        button_home.draw(scene_screen, (w / 2, h * (10 / 13)))

        my_toolbox.draw_to_screen(scene_screen)

        pygame.display.flip()

        my_toolbox.clock.tick(60)
