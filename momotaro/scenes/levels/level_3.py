from momotaro.game_templates import level
from momotaro.game_templates import momotaro_player, pet_player


def create_level(my_toolbox):
    level3 = level.Level(my_toolbox, 3, 5100, 5000, background="cave")
    level3.load_water_img()
    level3.load_stone_imgs()

    # add four walls
    level3.add_platform(position=(0, 0), dimensions=(71, 1080), facing_direction="right")        # left wall
    level3.add_platform((5100 - 70, 0), (70, 1080), facing_direction="left")                     # right wall
    level3.add_platform((0, 0), (5100, 140), facing_direction="down")                            # top wall
    level3.add_platform((0, 1080 - 69), (300, 70))
    level3.add_platform((350, 1080 - 69), (300, 70))                                            # bottom wall section 1
    level3.add_platform((650, 1080 - 69), (350, 70))
    level3.add_platform((1000, 1080 - 69), (200, 70))                                           # bottom wall section 3
    level3.add_platform((1200, 1080 - 69), (3900, 70))                                           # bottom wall section 3
    # 3030

    # fix the corners
    level3.add_platform((-10, 70), (70, 70), facing_direction=None)
    level3.add_platform((5040, 70), (70, 70), facing_direction=None)
    level3.add_platform((-10, 1080 - 70), (70, 70), facing_direction=None)
    level3.add_platform((5040, 1080 - 70), (70, 70), facing_direction=None)

    # add moving platforms throughout
    level3.add_moving_platform((350, 525), (100, 50), 2, (350, 700), facing_direction="up")    # first water section
    level3.add_moving_platform((500, 300), (100, 50), 2, (500, 525), facing_direction="up")
    level3.add_moving_platform((850, 300), (100, 50), 2, (850, 775), facing_direction="up")

    level3.add_moving_platform((-2000, 0), (2000, 800), 0.75, (0, 0), facing_direction="up")
    #over water at top for momotaro
    level3.add_moving_platform((2750, 350), (100, 35), 2, (3150, 350), facing_direction="up")
    level3.add_moving_platform((3700, 350), (100, 35), 2, (4100, 350), facing_direction="up")

    # add regular platforms
    level3.add_platform((50, 750), (1800 - 40, 50), facing_direction="up")
    #level3.add_platform((1050, 750), (1000, 140), facing_direction="up")# first section (top)
    #level3.add_platform((50, 300), (250, 200), facing_direction=None)
    level3.add_platform((650, 300), (100, 450), facing_direction=None)
    level3.add_platform((1100, 140), (100, 500), facing_direction=None)
    level3.add_platform((1200, 600), (150, 50), facing_direction="up")
    level3.add_platform((1550, 450), (150, 50), facing_direction="up")
    level3.add_platform((1200, 300), (150, 50), facing_direction="up")
    level3.add_platform((1700, 300), (100, 450), facing_direction="up")

    level3.add_platform((2000, 70), (50, 450 + 50 + 330), facing_direction=None)
    level3.add_platform((2450, 400), (50, 450 + 50), facing_direction=None)
    level3.add_platform((2450 - 150, 700), (150, 50), facing_direction="up")
    level3.add_platform((2050, 800), (150, 50), facing_direction="up")
    level3.add_platform((2050, 600), (150, 50), facing_direction="up")
    level3.add_platform((2450 - 150, 450), (150, 50), facing_direction="up")
    level3.add_platform((2050, 400), (150, 50), facing_direction="up")
    level3.add_platform((2450, 400), (2450, 70), facing_direction="up")

    level3.add_platform((2750, 800), (750, 70), facing_direction="up")
    level3.add_platform((2750 + 750 - 200, 675), (200, 35), facing_direction="up")
    level3.add_platform((2450 + 50, 575), (50, 70), facing_direction="up")
    level3.add_platform((2450 + 50, 575), (50, 70), facing_direction="up")
    level3.add_platform((3500, 400), (70, 450 + 20), facing_direction="up")

    level3.add_platform((3850, 850), (300, 50), facing_direction="up")
    level3.add_platform((4300, 400), (100, 425), facing_direction=None)

    #level3.add_platform((4700, 400), (100, 500), facing_direction="up")


    # add water sections
    level3.add_platform((300, 1080 - 70), (200, 70), platform_type="water")  # water section 1 (bottom)
    level3.add_platform((650, 1080 - 70), (200, 70), platform_type="water")  # water section 2 (bottom)
    level3.add_platform((1000, 1080 - 70), (200, 70), platform_type="water")
    level3.add_platform((750, 749), (300, 30), platform_type="water")  # water section 1 (bottom)
    level3.add_platform((2750 + 750 - 300, 799), (300, 50), platform_type="water")
    level3.add_platform((2450 + 50, 575), (50, 35), platform_type="water")
    level3.add_platform((3700, 1080 - 71), (600, 35), platform_type="water")

    level3.add_platform((2750, 399), (500, 35), platform_type="water")

    level3.add_platform((3700, 399), (500, 35), platform_type="water")

    # add button/gate obstacles
    level3.add_obstacle(600, 1000, "button", fence_initial=(700, 150),  fence_final=(700, 0), fence_dimensions=(100, 300))
    level3.add_obstacle(1300, 1000, "button", fence_initial=(1150, 600),  fence_final=(1150, 450), fence_dimensions=(100, 300))
    level3.add_obstacle(950, 1000, "button", fence_initial=(1750, 150),  fence_final=(1750, 0), fence_dimensions=(100, 300))# first top gate
    level3.add_obstacle(2650, 400, "button", fence_initial=(2800 - 30, 925), fence_final=(2800 - 30, 700),
                        fence_dimensions=(70, 300*7/10))
    level3.add_obstacle((2750 + 500 + 200), 400, "button", fence_initial=(3850, 850), fence_final=(3850, 1000),
                        fence_dimensions=(100, 300))
    level3.add_obstacle(3700 + 700, 400, "button", fence_initial=(4350, 900),
                        fence_final=(4350, 750),
                        fence_dimensions=(100, 300))
        # second bottom gate

    # add demons
    level3.add_demon([1655, 300], (300, 100))
    level3.add_demon([2400, 400], (300, 100))
    level3.add_demon([2050, 500], (300, 100))
    level3.add_demon([2050, 700], (300, 100))
    level3.add_demon([3050, 400], (300, 100))

    # add tori gate obstacle
    level3.add_obstacle(4600, 350, "torigate")
    level3.add_obstacle(4750, 350, "torigate")

    # add coins
    level3.add_obstacle(3775, 370, "coin")
    level3.add_obstacle(4300, 550, "coin")
    level3.add_obstacle(4815, 850, "coin")

    momotaro = momotaro_player.Momotaro([200, 300])
    pet = pet_player.Pet([200, 900])

    return level3, momotaro, pet