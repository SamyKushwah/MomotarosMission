from game_templates import level


def create_level(my_toolbox):
    level1 = level.Level(my_toolbox, 1, 5100, 5000)

    # add four walls
    level1.add_platform((0, 0), (71, 1080), facing_direction="right")               # left wall
    level1.add_platform((5100 - 70, 0), (70, 1080), facing_direction="left")        # right wall
    level1.add_platform((0, 1080 - 70), (1200, 70))                                 # bottom wall
    level1.add_platform((1200, 1080 - 70), (1000, 70), platform_type="water")       # water section 1
    level1.add_platform((2200, 1080 - 70), (700, 70))                               # bottom wall cont.
    level1.add_platform((2900, 1080 - 70), (700, 70), platform_type="water")        # water section 2
    level1.add_platform((3600, 1080 - 70), (1900, 70))                              # bottom wall cont.
    level1.add_platform((0, 0), (5100, 100), facing_direction="down")               # top wall

    # fix corners of walls
    level1.add_platform((-10, 70), (70, 70), facing_direction=None)
    level1.add_platform((5040, 70), (70, 70), facing_direction=None)
    level1.add_platform((-10, 1080 - 70), (70, 70), facing_direction=None)
    level1.add_platform((5040, 1080 - 70), (70, 70), facing_direction=None)

    # add platforms throughout
    level1.add_platform((500, 800), (300, 50), facing_direction="up")               # set 1
    level1.add_platform((250, 600), (300, 50), facing_direction="up")
    level1.add_platform((600, 400), (150, 50), facing_direction="up")

    level1.add_platform((2700, 800), (300, 50), facing_direction="up")              # set 2
    level1.add_platform((3000, 650), (250, 50), facing_direction="up")
    level1.add_platform((3250, 500), (200, 50), facing_direction="up")
    level1.add_platform((3450, 350), (150, 50), facing_direction="up")

    # add moving platforms
    level1.add_moving_platform((3900, 600), (275, 50), 50)
    level1.add_moving_platform((4200, 400), (275, 50), 70)
    level1.add_moving_platform((4200, 800), (275, 50), 30)
    level1.add_moving_platform((4500, 600), (275, 50), 40)

    # add demons
    level1.add_demon(400, 500, 1000, 135)           # demon 1
    level1.add_demon(3325, 400, 1000, 75)           # demon 2

    level1.add_demon(4000, 500, 1000, 100)          # demon 3
    level1.add_demon(4300, 300, 1000, 60)          # demon 4
    level1.add_demon(4600, 500, 1000, 80)

    # level1.add_obstacle(500, 600, "button")
    return level1
