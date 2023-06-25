import pygame
from drivers import toolbox


def run(my_toolbox: toolbox.Toolbox):
    w, h = 1920, 1080

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/title_screen_scene_UI/title_screen_background.png")
    background = pygame.transform.scale(background, (w, h))

    # load title image
    title_img = pygame.image.load("images/title_screen_scene_UI/main-title.png")
    title_img = pygame.transform.scale(title_img, (w * (1 / 2), h * (1 / 4)))

    # driver loop setup
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            # Check if the mouse was clicked
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                # Screen was clicked somewhere
                return "level_selector"

        # draw the background and title
        scene_screen = pygame.surface.Surface((w, h))
        scene_screen.blit(background, (0, 0))
        title_img_location = ((w - title_img.get_size()[0]) / 2, 0)
        scene_screen.blit(title_img, title_img_location)
        my_toolbox.draw_to_screen(scene_screen)

        my_toolbox.clock.tick(60)

        pygame.display.flip()
