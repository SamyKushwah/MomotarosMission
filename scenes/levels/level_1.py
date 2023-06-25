from game_templates import level


def create_level(my_toolbox):
    level1 = level.Level(my_toolbox, 1, 5100, 5000, background="cave")
    # add four walls
    level1.add_platform(position=(0, 0), dimensions=(71, 1080), facing_direction="right")  # left wall
    level1.add_platform((5100 - 70, 0), (70, 1080), facing_direction="left")  # right wall
    level1.add_platform((0, 1080 - 70), (1500, 70))  # bottom wall
    level1.add_platform((0, 0), (5100, 140), facing_direction="down")               # top wall


    level1.add_obstacle(600, 980, "torigate")



    return level1