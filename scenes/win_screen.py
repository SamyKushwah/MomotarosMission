import pygame
from templates import button

def run_win_screen(screen):
    # load background image and scale it to fit in the screen window
    background = pygame.image.load("../images/win_screen/win_screen.png")
    w, h = pygame.display.get_surface().get_size()
    background = pygame.transform.scale(background, (w, h))

    # load home, restart, and next buttons - scale to background size
    home_img = pygame.image.load("../images/win_screen/home_btn.png")
    home_img = pygame.transform.scale(home_img, (w / 5, h / 14))
    home_btn = button.Button(home_img)

    restart_img =pygame.image.load("../images/win_screen/restart_btn.png")
    restart_img = pygame.transform.scale(restart_img, (w / 3, h / 13))
    restart_btn = button.Button(restart_img)

    next_img = pygame.image.load("../images/win_screen/next_btn.png")
    next_img = pygame.transform.scale(next_img, (w / 5, h / 14))
    next_btn = button.Button(next_img)

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
                if next_btn.is_clicked(event.pos):
                    return "next"
                elif restart_btn.is_clicked(event.pos):
                    return "restart"
                elif home_btn.is_clicked(event.pos):
                    return "home"

            # if screen is resized rescale all buttons and images
            elif event.type == pygame.VIDEORESIZE:
                # resize screen and get new dimensions
                background = pygame.transform.scale(background, event.size)
                w, h = pygame.display.get_surface().get_size()

                # resize button images
                home_img = pygame.transform.scale(home_img, (w / 5, h / 14))
                home_btn.image = home_img
                restart_img = pygame.transform.scale(restart_img, (w / 3, h / 13))
                restart_btn.image = restart_img
                next_img = pygame.transform.scale(next_img, (w / 5, h / 14))
                next_btn.image = next_img

        # draw the background and buttons with scaled position
        screen.blit(background, (0, 0))

        home_btn.draw(screen, (w * (1 / 7), h * (12 / 13)))
        restart_btn.draw(screen, (w * (1 / 2), h * (12 / 13)))
        next_btn.draw(screen, (w * (6 / 7), h * (12 / 13)))

        pygame.display.flip()
