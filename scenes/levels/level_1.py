from game_templates import level


def create_level(my_toolbox):
    level1 = level.Level(my_toolbox, 1, 5100, 5000, background="mountains")
    # add four walls
    level1.add_platform(position=(0, 0), dimensions=(71, 1080), facing_direction="right")  # left wall
    level1.add_platform((5100 - 70, 0), (70, 1080), facing_direction="left")  # right wall
    level1.add_platform((0, 1080 - 70), (1600, 70))  # bottom wall part 1
    level1.add_platform((0, 0), (5100, 140), facing_direction="down")               # top wall

    level1.add_platform((400, 800), (300, 50), facing_direction="up") #platform 1 for coin 1
    level1.add_platform((900, 690), (300, 50), facing_direction="up") #platform 2 for coin 1
    level1.add_obstacle(1080, 600, "coin")   # coin 1

    # gate leading to after the first coin
    level1.add_obstacle(1265, 1000, 'button', (1450, 760), (1450, 540), (200, 500))
    # block to cover off the gate top
    level1.add_platform((1350, 140), (215, 500), facing_direction="all")


    # platforming water section



    level1.add_obstacle(600, 980, "torigate") # end of the level marker

    return level1