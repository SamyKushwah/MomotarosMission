import pygame
from momotaro.drivers import toolbox


def run(my_toolbox: toolbox.Toolbox):
    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/backgrounds/title_screen_bkgnd.png").convert_alpha()
    background = pygame.transform.scale(background, (w, h))

    # load title image
    title_img = pygame.image.load("images/title_screen_scene_UI/main-title.png").convert_alpha()
    title_img = pygame.transform.scale(title_img, (1300, 400))
    # w * (1 / 2), h * (1 / 4)

    # driver loop setup
    running = True
    while running:
        scene_screen = pygame.surface.Surface((w, h))
        scene_screen.blit(background, (0, 0))
        title_img_location = ((w - title_img.get_size()[0]) / 2, 100)
        scene_screen.blit(title_img, title_img_location)
        my_toolbox.draw_to_screen(scene_screen)


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", scene_screen
            # Check if the mouse was clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    my_toolbox.fullscreen()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                # Screen was clicked somewhere
                return "level_selector", scene_screen


        # draw the background and title
        my_toolbox.clock.tick(60)

