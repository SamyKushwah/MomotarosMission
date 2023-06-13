import pygame
from templates import button

pygame.font.init()


def run_main_menu(screen, clock, high_score):
    # main menu elements setup
    middle = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    test_image = pygame.Surface([100, 50])
    test_image.fill('azure')

    play_button = button.Button(test_image, 'Comic Sans MS', 100, "Play")

    # driver loop setup
    running = True
    dt = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            # Check if the mouse was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click was on the button
                if play_button.is_clicked(event.pos):
                    # The button was clicked
                    return "play"

        # fill the background
        screen.fill("aquamarine4")

        # draw the play button
        play_button.draw(screen, middle)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-independent physics.
        dt = clock.tick(60) / 1000

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            return "quit"

# https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection

