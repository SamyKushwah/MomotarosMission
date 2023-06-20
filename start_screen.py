import pygame
def run_start_screen(screen):
    # load background image and scale it to fit in the screen window
    background = pygame.image.load("../images/start_screen/start_screen_bkgnd.png")
    w, h = pygame.display.get_surface().get_size()
    background = pygame.transform.scale(background, (w, h))

    # load title image
    title_img = pygame.image.load("../images/start_screen/main-title.png")
    title_img = pygame.transform.scale(title_img, (w * (3 / 4), h / 4))

    # driver loop setup
    running = True
    dt = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            # Check if the mouse was clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Screen was clicked somewhere
                return "play"

            # if screen is resized
            elif event.type == pygame.VIDEORESIZE:
                # resize screen and get new dimensions
                background = pygame.transform.scale(background, event.size)
                w, h = pygame.display.get_surface().get_size()

                # resize title image
                title_img = pygame.transform.scale(title_img, (w * (3 / 4), h / 4))

        # draw the background and title
        screen.blit(background, (0, 0))

        loc = (w - title_img.get_size()[0]) / 2
        screen.blit(title_img, (loc, h / 8))

        pygame.display.flip()

