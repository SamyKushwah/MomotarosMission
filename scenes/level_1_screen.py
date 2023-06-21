import pygame
from templates import button, level
def run_level_1_screen(screen):
    # load background image and scale it to fit in the screen window
    background = pygame.image.load("../images/level_1/level_1_bkgnd.png")
    w, h = pygame.display.get_surface().get_size()
    background = pygame.transform.scale(background, (w, h))

    # load pause image and create a button from it
    pause_img = pygame.image.load("../images/level_1/pause_btn.png")
    pause_img = pygame.transform.scale(pause_img, (w / 20, h / 20))
    pause_btn = button.Button(pause_img)

    # load the walls and create Wall objects with them
    top_wall_img = pygame.image.load("../images/level_1/top_wall.png")
    top_wall_img = pygame.transform.scale(top_wall_img, (w, h / 16))
    top_wall = level.Wall(top_wall_img)

    bottom_wall_img = pygame.image.load("../images/level_1/bottom_wall.png")
    bottom_wall_img = pygame.transform.scale(bottom_wall_img, (w, h / 16))
    bottom_wall = level.Wall(bottom_wall_img)

    left_wall_img = pygame.image.load("../images/level_1/left_wall.png")
    left_wall_img = pygame.transform.scale(left_wall_img, (h / 16, h))
    left_wall = level.Wall(left_wall_img)

    right_wall_img = pygame.image.load("../images/level_1/right_wall.png")
    right_wall_img = pygame.transform.scale(right_wall_img, (h / 16, h))
    right_wall = level.Wall(right_wall_img)

    # load the platforms and create Platform objects with them
    plat_1_1_img = pygame.image.load("../images/level_1/big_box.png")
    plat_1_1_img = pygame.transform.scale(plat_1_1_img, (w / 4, h / 4))
    plat_1_1 = level.Platform(plat_1_1_img)

    plat_1_2_img = pygame.image.load("../images/level_1/small_box.png")
    plat_1_2_img = pygame.transform.scale(plat_1_2_img, (w / 5, h / 5))
    plat_1_2 = level.Platform(plat_1_2_img)

    plat_2_1_img = pygame.image.load("../images/level_1/blk_2-1.png")
    plat_2_1_img = pygame.transform.scale(plat_2_1_img, (w / 4, h / 4))
    plat_2_1 = level.Platform(plat_2_1_img)

    plat_2_2_img = pygame.image.load("../images/level_1/blk_2-2.png")
    plat_2_2_img = pygame.transform.scale(plat_2_2_img, (w / 5, h / 5))
    plat_2_2 = level.Platform(plat_2_2_img)

    plat_2_3_img = pygame.image.load("../images/level_1/blk_2-3.png")
    plat_2_3_img = pygame.transform.scale(plat_2_3_img, (w / 7, h / 7))
    plat_2_3 = level.Platform(plat_2_3_img)

    plat_2_4_img = pygame.image.load("../images/level_1/blk_2-4.png")
    plat_2_4_img = pygame.transform.scale(plat_2_4_img, (w / 4.5, h / 15))
    plat_2_4 = level.Platform(plat_2_4_img)

    plat_3_1_img = pygame.image.load("../images/level_1/blk_3-1.png")
    plat_3_1_img = pygame.transform.scale(plat_3_1_img, (w / 2, h / 15))
    plat_3_1 = level.Platform(plat_3_1_img)

    plat_3_2_img = pygame.image.load("../images/level_1/blk_3-2.png")
    plat_3_2_img = pygame.transform.scale(plat_3_2_img, (w / 3,  h / 8))
    plat_3_2 = level.Platform(plat_3_2_img)

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
                pause_img = pygame.transform.scale(pause_img, (w / 20, h / 20))
                pause_btn.image = pause_img

                # resize wall images
                top_wall_img = pygame.transform.scale(top_wall_img, (w, h / 16))
                top_wall.image = top_wall_img

                bottom_wall_img = pygame.transform.scale(bottom_wall_img, (w, h / 16))
                bottom_wall.image = bottom_wall_img

                left_wall_img = pygame.transform.scale(left_wall_img, (h / 16, h))
                left_wall.image = left_wall_img

                right_wall_img = pygame.transform.scale(right_wall_img, (h / 16, h))
                right_wall.image = right_wall_img

                plat_1_1_img = pygame.transform.scale(plat_1_1_img, (w / 4, h / 4))
                plat_1_1.image = plat_1_1_img

                plat_1_2_img = pygame.transform.scale(plat_1_2_img, (w / 5, h / 5))
                plat_1_2.image = plat_1_2_img

                plat_2_1_img = pygame.transform.scale(plat_2_1_img, (w / 4, h / 4))
                plat_2_1.image = plat_2_1_img

                plat_2_2_img = pygame.transform.scale(plat_2_2_img, (w / 5, h / 5))
                plat_2_2.image = plat_2_2_img

                plat_2_3_img = pygame.transform.scale(plat_2_3_img, (w / 7, h / 7))
                plat_2_3.image = plat_2_3_img

                plat_2_4_img = pygame.transform.scale(plat_2_4_img, (w / 4.5, h / 15))
                plat_2_4.image = plat_2_4_img

                plat_3_1_img = pygame.transform.scale(plat_3_1_img, (w / 2, h / 15))
                plat_3_1.image = plat_3_1_img

                plat_3_2_img = pygame.transform.scale(plat_3_2_img, (w / 3, h / 8))
                plat_3_2.image = plat_3_2_img

        # draw the background and title
        screen.blit(background, (0, 0))
        pause_btn.draw(screen, (w * (6.6 / 7), h * (0.5 / 7)))

        # draw the walls
        top_wall.draw_wall(screen, (w / 2, 0))
        bottom_wall.draw_wall(screen, (w / 2, h))
        left_wall.draw_wall(screen, (0, h / 2))
        right_wall.draw_wall(screen, (w, h / 2))

        # draw the platforms
        plat_1_1.draw_platform(screen, (w * (6.25 / 7), h * (6.25 / 7)))
        plat_1_2.draw_platform(screen, (w * (4.8 / 7), h * (6.65 / 7)))

        plat_2_1.draw_platform(screen, (w * (0.68 / 7), h * (4 / 7)))
        plat_2_2.draw_platform(screen, (w * (2.23 / 7), h * (4.17 / 7)))
        plat_2_3.draw_platform(screen, (w * (3.34 / 7), h * (3.965 / 7)))
        plat_2_4.draw_platform(screen, (w * (4.53 / 7), h * (3.695 / 7)))

        plat_3_1.draw_platform(screen, (w * (3.1 / 7), h * (2 / 7)))
        plat_3_2.draw_platform(screen, (w * (5.85 / 7), h * (1.79 / 7)))     # 5.8

        pygame.display.flip()