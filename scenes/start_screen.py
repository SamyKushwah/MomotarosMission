import pygame
def run_start_screen(screen):
    # load background image and scale it to fit in the screen window
    background = pygame.image.load("../images/start_screen.png")
    w, h = pygame.display.get_surface().get_size()
    background = pygame.transform.scale(background, (w, h))

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
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                background = pygame.transform.scale(background, event.size)

        # draw the background and title
        screen.blit(background, (0, 0))
        pygame.display.flip()


# background was created using the following images:
# https://craftpix.net/freebies/free-mountain-backgrounds-pixel-art/?num=1&count=58&sq=japanese%20mountain%20scene&pos=8
# https://pixabay.com/photos/pagoda-senso-ji-temple-asakusa-2405537/

# creating a resizeable screen
# https://stackoverflow.com/questions/62899967/how-to-make-my-pygame-game-window-resizeable
# https://stackoverflow.com/questions/36653519/how-do-i-get-the-size-width-x-height-of-my-pygame-window


