import pygame
from templates import button
import math

"""
    purpose: run the level select screen, displaying each level's progress and
             providing links to corresponding levels and credits page 
    author: Jessica Halvorsen <j.halvorsen@ufl.edu>

"""
def run_level_select_screen(screen):
    # load background image and scale it to fit in the screen window
    background = pygame.image.load("../images/level_select_screen/level_select_bkgnd.png")
    w, h = pygame.display.get_surface().get_size()
    background = pygame.transform.scale(background, (w, h))

    # load selection text and scale for screen size
    select_txt = pygame.image.load("../images/level_select_screen/level-title.png")
    select_txt = pygame.transform.scale(select_txt, (w / 2, h / 12))

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

    # load level information about coins from the save file
    with open("../game_data", 'r') as file:
        level_coins = [line.rstrip() for line in file]

    # decide which coin images correspond to each level
    level_coin_imgs = []
    for i in range(0, 3):
        temp = int(level_coins[i])
        if temp == 3:
            level_coin_imgs.append("3-gold-coins.png")
        elif temp == 2:
            level_coin_imgs.append("2-gold-coins.png")
        elif temp == 1:
            level_coin_imgs.append("1-gold-coins.png")
        elif temp == 0:
            level_coin_imgs.append("0-gold-coins.png")

    # load level coin images
    lvl_1_coin_img = pygame.image.load(f"../images/level_select_screen/{level_coin_imgs[0]}")
    lvl_1_coin_img = pygame.transform.scale(lvl_1_coin_img, (w / 5, h / 7))

    lvl_2_coin_img = pygame.image.load(f"../images/level_select_screen/{level_coin_imgs[1]}")
    lvl_2_coin_img = pygame.transform.scale(lvl_2_coin_img, (w / 5, h / 7))

    lvl_3_coin_img = pygame.image.load(f"../images/level_select_screen/{level_coin_imgs[2]}")
    lvl_3_coin_img = pygame.transform.scale(lvl_3_coin_img, (w / 5, h / 7))

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
                    return "level_1"
                elif button_2.is_clicked(event.pos):
                    return "level_2"
                elif button_3.is_clicked(event.pos):
                    return "level_3"
                elif credits_btn.is_clicked(event.pos):
                    return "credits"

            # if screen is resized rescale all buttons and images
            elif event.type == pygame.VIDEORESIZE:
                # resize screen and get new dimensions
                background = pygame.transform.scale(background, event.size)
                w, h = pygame.display.get_surface().get_size()

                # resize button images
                button_1_img = pygame.transform.scale(button_1_img, (h / 4, h / 4))
                button_1.image = button_1_img
                button_2_img = pygame.transform.scale(button_2_img, (h / 4, h / 4))
                button_2.image = button_2_img
                button_3_img = pygame.transform.scale(button_3_img, (h / 4, h / 4))
                button_3.image = button_3_img

                # resize text images
                credits_img = pygame.transform.scale(credits_img, (w / 6, h / 18))
                credits_btn.image = credits_img
                select_txt = pygame.transform.scale(select_txt, (w / 2, h / 12))

                # resize coin images
                lvl_1_coin_img = pygame.transform.scale(lvl_1_coin_img, (w / 5, h / 7))
                lvl_2_coin_img = pygame.transform.scale(lvl_2_coin_img, (w / 5, h / 7))
                lvl_3_coin_img = pygame.transform.scale(lvl_3_coin_img, (w / 5, h / 7))

        # draw the background and buttons with scaled position
        screen.blit(background, (0, 0))

        button_1.draw(screen, (w * (1.5 / 7), h * (4 / 5)))
        button_2.draw(screen, (w * (3.5 / 7), h * (7 / 10)))
        button_3.draw(screen, (w * (5.5 / 7), h * (7 / 9)))

        credits_btn.draw(screen, (w * (91 / 100), h * (97 / 100)))
        screen.blit(select_txt, (w * (1 / 100), h * (1 / 100)))

        screen.blit(lvl_1_coin_img, (w * (0.8 / 7), h * (5 / 6)))
        screen.blit(lvl_2_coin_img, (w * (2.8 / 7), h * (8.15 / 11)))
        screen.blit(lvl_3_coin_img, (w * (4.8 / 7), h * (8.15 / 10)))

        pygame.display.flip()