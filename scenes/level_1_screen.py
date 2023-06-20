import pygame
from templates import button
def run_level_1_screen(screen):
    # load background image and scale it to fit in the screen window
    background = pygame.image.load("../images/level_1/MomotaroStandingWalking.png")
    w, h = pygame.display.get_surface().get_size()
    background = pygame.transform.scale(background, (w, h))
    screen.fill((255, 255, 255))

    # load pause image and create a button from it
    pause_img = pygame.image.load("../images/level_1/pause_btn.png")
    pause_img = pygame.transform.scale(pause_img, (w / 4, h / 4))
    pause_btn = button.Button(pause_img)

    # driver loop setup
    running = True
    dt = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            # Check if the mouse was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check which button was clicked
                if pause_btn.is_clicked(event.pos):
                    return "pause"

            # if screen is resized rescale all buttons and images
            elif event.type == pygame.VIDEORESIZE:
                # resize screen and get new dimensions
                background = pygame.transform.scale(background, event.size)
                w, h = pygame.display.get_surface().get_size()

                # resize button images
                pause_img = pygame.transform.scale(pause_img, (w / 4, h / 4))
                pause_btn.image = pause_img

        # draw the background and title
        screen.blit(background, (0, 0))
        pause_btn.draw(screen, (w * (1.5 / 7), h * (4 / 5)))
        pygame.display.flip()