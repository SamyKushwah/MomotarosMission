import pygame
import sys

"""
    synopsis: script for displaying the main menu screen at the beginning of the game
    author: Jessica Halvorsen <j.halvorsen@ufl.edu> 
"""
def display_screen(screen):
    # load background image and scale to fit inside screen
    background = pygame.image.load("background_menu.jpg")
    background = pygame.transform.scale(background, (1024, 768))    # TODO change to use screen class

    # initialize font data for title
    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 200)
    text_color = (234, 114, 110)
    title_top = font.render("Momotaro's", False, text_color)
    title_bottom = font.render("Mission", False, text_color)

    # initialize button info    # TODO change to use screen class and button class
    button_color = (0, 0, 0)
    button_size = (400, 100)
    button_pos = (300, 450)

    # continue checking for events and update screen with title, background
    # and button info
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # draw rectangle button depending on hovering or not
        screen.blit(background, (0, 0))
        screen.blit(title_top, (120, 120))
        screen.blit(title_bottom, (250, 250))
        pygame.draw.rect(screen, button_color, (button_pos, button_size))
        pygame.display.update()
