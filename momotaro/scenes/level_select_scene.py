import pygame
import sys
import os
import pathlib
from momotaro.ui_templates import button, screen_transition
from momotaro.drivers import toolbox

import math

"""
    purpose: run the level select screen, displaying each level's progress and
             providing links to corresponding levels and credits page 
    author: Jessica Halvorsen <j.halvorsen@ufl.edu>

"""


def run(my_toolbox: toolbox.Toolbox, past_screen):

    w, h = 1920, 1080

    # load level information about coins from the save file
    with open("save_data/game_data", 'r') as file:
        level_data = [line.rstrip() for line in file]

    # decide which coin images correspond to each level
    level_coin_imgs = []
    for i in range(0, 3):
        temp = int(level_data[i])
        # print(temp)
        if temp == 3:
            level_coin_imgs.append("3-gold-coins.png")
        elif temp == 2:
            level_coin_imgs.append("2-gold-coins.png")
        elif temp == 1:
            level_coin_imgs.append("1-gold-coins.png")
        elif temp == 0:
            level_coin_imgs.append("0-gold-coins.png")

    level_locks = []
    for i in range(3, 5):
        temp = level_data[i]
        if temp == "unlocked":
            level_locks.append("unlocked")
        elif temp == "locked":
            level_locks.append("locked")

    # load level 1 button info
    lvl_1_coin_img = pygame.image.load(f"images/level_select_scene_UI/{level_coin_imgs[0]}")
    lvl_1_coin_img = pygame.transform.scale(lvl_1_coin_img, (w / 5, h / 7))

    circle1_img = pygame.image.load("images/level_select_scene_UI/circle.png").convert_alpha()
    circle1_img = pygame.transform.scale(circle1_img, (h / 4, h / 4))

    button_1_img = pygame.Surface((75, 100), pygame.SRCALPHA)
    button_1_img.fill((255, 255, 255, 0))
    button_1 = button.Button(button_1_img, text="1")

    # load level 2 button info
    if level_locks[0] == "unlocked":
        lvl_2_coin_img = pygame.image.load(f"images/level_select_scene_UI/{level_coin_imgs[1]}")
        lvl_2_coin_img = pygame.transform.scale(lvl_2_coin_img, (w / 5, h / 7))

        circle2_img = circle1_img
        circle2_img = pygame.transform.scale(circle2_img, (h / 4, h / 4))

        button_2_img = pygame.Surface((100, 100), pygame.SRCALPHA)
        button_2_img.fill((255, 255, 255, 0))
        button_2 = button.Button(button_2_img, text="2")

    elif level_locks[0] == "locked":
        circle2_img = pygame.image.load("images/level_select_scene_UI/circle2_lock.png").convert_alpha()
        circle2_img = pygame.transform.scale(circle2_img, (h / 4, h / 4))

    # load level 3 info
    if level_locks[1] == "unlocked":
        lvl_3_coin_img = pygame.image.load(f"images/level_select_scene_UI/{level_coin_imgs[2]}")
        lvl_3_coin_img = pygame.transform.scale(lvl_3_coin_img, (w / 5, h / 7))

        circle3_img = circle1_img
        circle3_img = pygame.transform.scale(circle3_img, (h / 4, h / 4))

        button_3_img = pygame.Surface((100, 100), pygame.SRCALPHA)
        button_3_img.fill((255, 255, 255, 0))
        button_3 = button.Button(button_3_img, text="3")

    elif level_locks[1] == "locked":
        circle3_img = pygame.image.load("images/level_select_scene_UI/circle3_lock.png").convert_alpha()
        circle3_img = pygame.transform.scale(circle3_img, (h / 4, h / 4))

    # load background image and scale it to fit in the screen window
    background = pygame.image.load("images/level_select_scene_UI/level_select_background.png").convert_alpha()
    background = pygame.transform.scale(background, (w, h))

    # load selection text and scale for screen size
    select_txt = pygame.image.load("images/level_select_scene_UI/level-title.png").convert_alpha()
    select_txt = pygame.transform.scale(select_txt, (w / 2, h / 12))

    # load the credits button and scale to fit the screen
    credits_img = pygame.Surface((300, 55), pygame.SRCALPHA)
    credits_img.fill((255, 255, 255, 0))
    credits_btn = button.Button(credits_img, text="Credits", font_size=70)

    # draw the background and buttons with scaled position
    scene_screen = pygame.surface.Surface((w, h))
    scene_screen.blit(background, (0, 0))

    # driver loop setup
    running = True
    transition = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check if the mouse was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check which button was clicked
                if button_1.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_1", scene_screen
                elif level_locks[0] != "locked" and button_2.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_2", scene_screen
                elif level_locks[1] != "locked" and button_3.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "level_3", scene_screen
                elif credits_btn.is_clicked(my_toolbox.adjusted_mouse_pos(event.pos)):
                    return "credits", scene_screen

        credits_btn.draw(scene_screen, (w * (91 / 100), h * (96 / 100)), True)

        # draw the background and buttons with scaled position
        scene_screen.blit(select_txt, (w * (1 / 100), h * (1 / 100)))
        scene_screen.blit(circle1_img, (w * (1 / 7), h * (4 / 6)))
        scene_screen.blit(circle2_img, (w * (3 / 7), h * (6 / 10.5)))
        scene_screen.blit(circle3_img, (w * (5 / 7), h * (6 / 9.25)))

        # draw correct buttons for each level
        button_1.draw(scene_screen, (w * (1.5 / 7), h * (4 / 5)), True)
        scene_screen.blit(lvl_1_coin_img, (w * (0.8 / 7), h * (5 / 6)))
        if level_locks[0] != "locked":
            button_2.draw(scene_screen, (w * (3.5 / 7), h * (7 / 10)), True)
            scene_screen.blit(lvl_2_coin_img, (w * (2.8 / 7), h * (8.15 / 11)))
        if level_locks[1] != "locked":
            button_3.draw(scene_screen, (w * (5.5 / 7), h * (7 / 9)), True)
            scene_screen.blit(lvl_3_coin_img, (w * (4.8 / 7), h * (8.15 / 10)))

        # do the screen transition
        if transition:
            screen_transition.crossfade(past_screen, scene_screen, my_toolbox.screen, my_toolbox.clock, 10)
            transition = False

        my_toolbox.draw_to_screen(scene_screen)

        pygame.display.flip()

        my_toolbox.clock.tick(60)