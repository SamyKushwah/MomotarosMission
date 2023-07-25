import pygame
from momotaro.ui_templates import button, screen_transition
from momotaro.drivers import toolbox


def run(my_toolbox: toolbox.Toolbox, current_level, past_screen):
    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/backgrounds/lose_screen_bkgnd.png").convert_alpha()
    background = pygame.transform.scale(background, (w, h))

    # load home button image
    home_img = pygame.Surface((400, 110), pygame.SRCALPHA)
    home_img.fill((255, 255, 255, 0))
    button_home = button.Button(home_img, text="Home", font_size=100)

    # load restart button image
    restart_img = pygame.Surface((610, 115), pygame.SRCALPHA)
    restart_img.fill((255, 255, 255, 0))
    button_restart = button.Button(restart_img, text="Restart", font_size=100)

    # draw the background
    scene_screen = pygame.surface.Surface((w, h))
    scene_screen.blit(background, (0, 0))



    # driver loop setup
    running = True
    transition = True
    while running:

        # draw buttons with scaled position
        button_home.draw(scene_screen, (1030, h * (12 / 13)), True)
        button_restart.draw(scene_screen, (1570, h * (12 / 13)), True)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "quit", scene_screen
            # Check if the mouse was clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if button_home.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_selector", scene_screen
                elif button_restart.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return current_level, scene_screen

        # do the screen transition
        if transition:
            screen_transition.crossfade(past_screen, scene_screen, my_toolbox.screen, my_toolbox.clock, 10)
            transition = False

        my_toolbox.draw_to_screen(scene_screen)
        pygame.display.flip()

        my_toolbox.clock.tick(60)

