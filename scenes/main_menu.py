import pygame
from templates import button

pygame.font.init()


def run_main_menu(screen, clock, high_score):
    # main menu elements setup
    middle = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    background = pygame.image.load("images/background_menu.jpg")
    background = pygame.transform.scale(background, (1024, 768))

    test_image = pygame.Surface([200, 100])
    test_image.fill('azure')

    play_button = button.Button(test_image, 'Comic Sans MS', 70, "Play")

    font = pygame.font.SysFont("Comic Sans MS", 100)
    text_color = (234, 114, 110)
    title_top = font.render("Momotaro's", False, text_color)
    title_bottom = font.render("Mission", False, text_color)

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
        screen.blit(background, (0, 0))
        screen.blit(title_top, (middle.x - (title_top.get_rect().width / 2), middle.y - title_top.get_rect().height - 100))
        screen.blit(title_bottom, (middle.x - (title_bottom.get_rect().width / 2), middle.y + 75))

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

