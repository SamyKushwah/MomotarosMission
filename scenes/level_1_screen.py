import pygame
from templates import button
def run_level_1_screen(screen):
    # load background image and scale it to fit in the screen window
    background = pygame.image.load("../images/MomotaroStandingWalking.png")
    screen.fill((255, 255, 255))
    background = pygame.transform.scale(background, (1024, 768))

    # driver loop setup
    running = True
    dt = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            """
            # Check if the mouse was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check which button was clicked
                if button_1.is_clicked(event.pos):
                    # button 1 was clicked, go to level one
                    return "level_1"
                elif button_2.is_clicked(event.pos):
                    # button 2 was clicked, go to level two
                    return "level_2"
                elif button_3.is_clicked(event.pos):
                    # button 3 was clicked, go to level three
                    return "level_3"
"""
        # draw the background and title
        screen.blit(background, (0, 0))
        pygame.display.flip()


