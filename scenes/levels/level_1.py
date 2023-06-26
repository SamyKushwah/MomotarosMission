from game_templates import level


def create_level(my_toolbox):
    level1 = level.Level(my_toolbox, 1, 5100, 5000, background="mountains")
    level1.load_water_img()
    level1.load_stone_imgs()

    # add four walls
    level1.add_platform(position=(0, 0), dimensions=(71, 1080), facing_direction="right")       # left wall
    level1.add_platform((5100 - 70, 0), (70, 1080), facing_direction="left")                    # right wall
    level1.add_platform((0, 1080 - 70), (1700, 70))                                             # bottom wall part 1
    level1.add_platform((0, 0), (5100, 140), facing_direction="down")                           # top wall

    # fix the corners
    level1.add_platform((-10, 70), (70, 70), facing_direction=None)
    level1.add_platform((5040, 70), (70, 70), facing_direction=None)
    level1.add_platform((-10, 1080 - 70), (70, 70), facing_direction=None)
    level1.add_platform((5040, 1080 - 70), (70, 70), facing_direction=None)

    # add platforms
    level1.add_platform((400, 800), (300, 50), facing_direction="up")               # platform 1 for coin 1
    level1.add_platform((900, 690), (300, 50), facing_direction="up")               # platform 2 for coin 1
    level1.add_obstacle(1080, 600, "coin")                                          # coin 1

    # gate leading to after the first coin
    level1.add_obstacle(1265, 1000, 'button', fence_initial=(1450, 780), fence_final=(1450, 540), fence_dimensions=(200, 500))

    # block to cover off the gate top
    level1.add_platform((1350, 130), (215, 500), facing_direction="all")


    # platforming water section
    level1.add_platform((1700, 1080 - 70 + 5), (500, 70), platform_type="water")
    level1.add_platform((2200, 1010), (200, 70), facing_direction="up")
    level1.add_platform((2400, 1080 - 70 + 5), (500, 70), platform_type="water")
    level1.add_platform((2900, 810), (2200, 270), facing_direction="up")

    level1.add_moving_platform((1750, 850), (250, 70), 5, (2000, 850))
    level1.add_moving_platform((2450, 850), (250, 70), 5, (2600, 850))

    # gate ending water platforming
    level1.add_obstacle(3060, 800, "button", fence_initial=(3300, 620), fence_final=(3300, 400), fence_dimensions=(150, 400))


    # Demon fight pit section
    level1.add_demon([4120, 780], (800,500))
    level1.add_moving_platform((3400, 400), (275, 50), 10, (4000, 650))
    level1.add_moving_platform((4200, 650), (175, 50), 10, (4600, 300))

    level1.add_platform((4800, 300), (200, 50), facing_direction="up")
    level1.add_obstacle(4900, 250, 'coin')


    # over water platforming - 3rd coin segment
    level1.add_platform((2800, 400), (600, 50), facing_direction="up")
    level1.add_platform((2200, 400), (400, 50), facing_direction='up')

    level1.add_demon([2400, 380], (100,100))
    level1.add_obstacle(2400, 200, 'coin')

    level1.add_platform((1560, 400), (350,50), facing_direction="up")
    level1.add_obstacle(1650, 380, "torigate") # end of the level marker

    return level1