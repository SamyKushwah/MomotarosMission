import pygame
import sys
from ui_templates import button
from drivers import toolbox


def run(my_toolbox: toolbox.Toolbox, current_level):
    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/pause_screen/pause_screen_bkgnd.png").convert_alpha()
    background = pygame.transform.scale(background, (w, h))

    # load home button image
    home_img = pygame.Surface((400, 110), pygame.SRCALPHA)
    home_img.fill((255, 255, 255, 0))
    #home_img = pygame.image.load("images/pause_screen/home_btn.png")
    #home_img = pygame.transform.scale(home_img, (w * (1 / 4), h * (1 / 13)))
    button_home = button.Button(home_img, lwd=2, text="Home")

    """home_highlight = pygame.image.load("images/pause_screen/homehighlight.png")
    home_highlight = pygame.transform.scale(home_highlight, (w * (1 / 4), h * (1 / 13)))
    home_highlight_bt = button.Button(home_highlight)"""

    #load restart button image
    #restart_img = pygame.image.load("images/pause_screen/restart_btn.png")
    #restart_img = pygame.transform.scale(restart_img, (w * (1 / 3), h * (1 / 12)))
    restart_img = pygame.Surface((610, 115), pygame.SRCALPHA)
    restart_img.fill((255, 255, 255, 0))
    button_restart = button.Button(restart_img, lwd=2, text="Restart")

    #load resume button image
    #resume_img = pygame.image.load("images/pause_screen/resume_btn.png")
    #resume_img = pygame.transform.scale(resume_img, (w * (1 / 3), h * (1 / 12)))
    resume_img = pygame.Surface((575, 115), pygame.SRCALPHA)
    resume_img.fill((255, 255, 255, 0))
    button_resume = button.Button(resume_img, lwd=2, text="Resume")

    scene_screen = pygame.surface.Surface((w, h))
    scene_screen.blit(background, (0, 0))
    #scene_screen.set_alpha(170)

    #highlight = False

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
                    #print('returning current level')
                    #print(current_level)
                    return current_level
                elif button_resume.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "resume"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"


        # draw the background and buttons with scaled position

        button_resume.draw(scene_screen, (w / 2, h * (6 / 13)), True)
        button_restart.draw(scene_screen, (w / 2, h * (8 / 13)), True)
        button_home.draw(scene_screen, (w / 2, h * (10 / 13)), True)

        #scene_screen.set_alpha(170)
        my_toolbox.draw_to_screen(scene_screen)
        pygame.display.flip()