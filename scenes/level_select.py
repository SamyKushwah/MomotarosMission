import pygame
from templates import button
import math

"""
    purpose: run the level select screen, displaying each level's progress and
             providing links to corresponding levels and credits page 
    author: Jessica Halvorsen <j.halvorsen@ufl.edu>

"""

"""
def draw_coins(screen, level_coins, gold, silver):
    for i in range(0, 2):
        curr_num = int(level_coins[i])
        if curr_num >= 1:
    # print first gold coin for the current level
"""

def run_level_select_screen(screen):
    # load background image and scale it to fit in the screen window
    background = pygame.image.load("../images/level_select_screen/level-no-circle.png")
    w, h = pygame.display.get_surface().get_size()
    background = pygame.transform.scale(background, (w, h))

    # load the level buttons for level 1-3 and scale to fit on current screen size
    button_1_img = pygame.image.load("../images/level_select_screen/circle1.png")
    button_1_img = pygame.transform.scale(button_1_img, (h / 4, h / 4))
    button_1 = button.Button(button_1_img)

    button_2_img = pygame.image.load("../images/level_select_screen/circle2.png")
    button_2_img = pygame.transform.scale(button_2_img, (h / 4, h / 4))
    button_2 = button.Button(button_2_img)

    button_3_img = pygame.image.load("../images/level_select_screen/circle3.png")
    button_3_img = pygame.transform.scale(button_3_img, (h / 4, h / 4))
    button_3 = button.Button(button_3_img)

    # load the credits button and scale to fit the screen
    credits_img = pygame.image.load("../images/level_select_screen/credits.png")
    credits_img = pygame.transform.scale(credits_img, (w / 6, h / 18))
    credits_btn = button.Button(credits_img)

    # TODO: decide how we want to do the coins being gold/silver
    # load level information about coins from the save file
    with open("../game_data", 'r') as file:
        level_coins = [line.rstrip() for line in file]

    # load gold and silver coin images
    gold_3_img = pygame.image.load("../images/level_select_screen/3-gold-coins.png")
    gold_3_img = pygame.transform.scale(gold_3_img, (w / 5, h / 7))

    gold_0_img = pygame.image.load("../images/level_select_screen/3-silver-coins.png")
    gold_0_img = pygame.transform.scale(gold_0_img, (w / 5, h / 7))

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
                if button_1.is_clicked(event.pos):
                    # button 1 was clicked, go to level one
                    return "level_1"
                elif button_2.is_clicked(event.pos):
                    # button 2 was clicked, go to level two
                    return "level_2"
                elif button_3.is_clicked(event.pos):
                    # button 3 was clicked, go to level three
                    return "level_3"
                elif credits_btn.is_clicked(event.pos):
                    # credits button was clicked, go to credits page
                    return "credits"
            # if screen is resized rescale all buttons and images
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                background = pygame.transform.scale(background, event.size)
                w, h = pygame.display.get_surface().get_size()
                button_1_img = pygame.transform.scale(button_1_img, (h / 4, h / 4))
                button_1.image = button_1_img
                button_2_img = pygame.transform.scale(button_2_img, (h / 4, h / 4))
                button_2.image = button_2_img
                button_3_img = pygame.transform.scale(button_3_img, (h / 4, h / 4))
                button_3.image = button_3_img
                credits_img = pygame.transform.scale(credits_img, (w / 6, h / 18))
                credits_btn.image = credits_img
                # draw correct color coin in the correct location
                gold_3_img = pygame.transform.scale(gold_3_img, (w / 5, h / 7))
                gold_0_img = pygame.transform.scale(gold_0_img, (w / 5, h / 7))
                # coin_gold_img = pygame.transform.scale(coin_gold_img, (h / 12, h / 12))
                # coin_silver_img = pygame.transform.scale(coin_silver_img, (h / 12, h / 12))
                break

        # draw the background and buttons with scaled position
        screen.blit(background, (0, 0))
        button_1.draw(screen, (w * (1.5 / 7), h * (4 / 5)))
        button_2.draw(screen, (w * (3.5 / 7), h * (7 / 10)))
        button_3.draw(screen, (w * (5.5 / 7), h * (7 / 9)))
        credits_btn.draw(screen, (w * 0.90, h * 0.95))
        screen.blit(gold_3_img, (w * (0.8 / 7), h * (5 / 6)))
        screen.blit(gold_0_img, (w * (2.8 / 7), h * (8.15 / 11)))
        pygame.display.flip()



# screen was designed by editing royalty-free images found here:
# cherry blossom: https://pixabay.com/photos/cherry-blossom-flower-plant-nature-3285200/
# tori gate: https://pixabay.com/photos/miyajima-gate-tori-547290/
# mountain lake: https://pixabay.com/photos/mount-fuji-japan-mountains-landmark-395047/
# buddha: https://pixabay.com/photos/buddha-buddha-statue-spiritual-4014365/

