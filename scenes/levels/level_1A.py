from game_templates import level


def create_level(my_toolbox):
    level1 = level.Level(my_toolbox, 1, 5100, 5000, background="mountains")
    # add four walls
    level1.add_platform(position=(0, 0), dimensions=(71, 1080), facing_direction="right")               # left wall
    level1.add_platform((5100 - 70, 0), (70, 1080), facing_direction="left")        # right wall
    level1.add_platform((0, 1080 - 70), (1200, 70))                                 # bottom wall
    level1.add_platform((1200, 1080 - 70), (1000, 70), platform_type="water")       # water section 1
    level1.add_platform((2200, 1080 - 70), (700, 70))                               # bottom wall cont.
    level1.add_platform((2900, 1080 - 70), (700, 70), platform_type="water")        # water section 2
    level1.add_platform((3600, 1080 - 70), (1900, 70))                              # bottom wall cont.
    level1.add_platform((0, 0), (5100, 140), facing_direction="down")               # top wall

    # add platforms throughout
    level1.add_moving_platform((500, 900), (300, 50), 5, (1200, 700), facing_direction="up")               # set 1
    level1.add_platform((250, 600), (300, 50), facing_direction="up")
    level1.add_platform((600, 400), (150, 50), facing_direction="up")

    level1.add_platform((2700, 800), (300, 50), facing_direction="up")              # set 2
    level1.add_platform((3000, 650), (250, 50), facing_direction="up")
    level1.add_platform((3250, 500), (200, 50), facing_direction="up")
    level1.add_platform((3450, 350), (150, 50), facing_direction="up")


    # add moving platforms
    level1.add_moving_platform((4000, 400), (100, 80), 30, (4000, 800))
    level1.add_moving_platform((4200, 400), (275, 50), 20, (4500, 800))

    # add demons
    level1.add_demon([4000, 300], 300)
    level1.add_demon([3325, 400], 300)

    # add tori gate obstacle
    level1.add_obstacle(600, 500, "torigate")

    #c oins
    level1.add_obstacle(600, 900, "coin")

    # de
    #level1.add_obstacle(500, 600, "button")
    return level1
