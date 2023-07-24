import pygame
import sys
from ui_templates import button, screen_transition
from drivers import toolbox


def run(my_toolbox: toolbox.Toolbox, current_level, past_screen):
    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/backgrounds/pause_screen_bkgnd.png").convert_alpha()
    background = pygame.transform.scale(background, (w, h))

    # load home button image
    home_img = pygame.Surface((400, 106), pygame.SRCALPHA)
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

    # load controls button image
    controls_img = pygame.Surface((647, 103), pygame.SRCALPHA)
    controls_img.fill((255, 255, 255, 0))
    button_controls = button.Button(controls_img, text="Controls")

    # draw the background
    scene_screen = pygame.surface.Surface((w, h))
    scene_screen.blit(background, (0, 0))

    # driver loop setup
    running = True
    transition = True
    while running:
        for event in [pygame.event.wait()]+pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check if the mouse was clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if button_home.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_selector", scene_screen
                elif button_restart.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return current_level, scene_screen
                elif button_controls.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "controls", scene_screen
                elif button_resume.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "resume", scene_screen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume", scene_screen

        # draw the buttons with scaled position
        button_resume.draw(scene_screen, (w / 2, h * (5.5 / 13)), True)
        button_restart.draw(scene_screen, (w / 2, h * (7.5 / 13)), True)
        button_home.draw(scene_screen, (w / 2, h * (9.5 / 13)), True)
        button_controls.draw(scene_screen,(w / 2, h * (11.5 / 13)), True)

        # do the screen transition
        if transition:
            screen_transition.crossfade(past_screen, scene_screen, my_toolbox.screen, my_toolbox.clock, 10)
            transition = False

        my_toolbox.draw_to_screen(scene_screen)
        pygame.display.flip()

        my_toolbox.clock.tick(60)