import pygame
from momotaro.ui_templates import button, screen_transition
from momotaro.drivers import toolbox

"""
    purpose: run the controls screen, provide button to go back to the pause page
    author: Samradhi Kushwah <skushwah@ufl.edu>

"""

def run(my_toolbox: toolbox.Toolbox, past_screen):

    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/backgrounds/controls_bkgnd.png").convert_alpha()
    background = pygame.transform.scale(background, (w, h))

    # create the back button
    back = pygame.Surface((300, 100), pygame.SRCALPHA)
    back.fill((255, 255, 255, 0))
    button_back = button.Button(back, text="Back", font_size=60)

    # draw the background
    scene_screen = pygame.surface.Surface((w, h))
    scene_screen.blit(background, (0, 0))

    # driver loop setup
    running = True
    transition = True
    while running:

        # draw buttons with scaled position
        button_back.draw(scene_screen, (120, 50), True)

        for event in [pygame.event.wait()] + pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", scene_screen
            # Check if the mouse was clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # back button and fade
                if button_back.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "back", scene_screen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    my_toolbox.fullscreen()

        # do the screen transition
        if transition:
            screen_transition.crossfade(past_screen, scene_screen, my_toolbox.screen, my_toolbox.clock, 10)
            transition = False

        my_toolbox.draw_to_screen(scene_screen)
        pygame.display.flip()

        my_toolbox.clock.tick(60)