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
    level3.add_platform((0, 1000), (300, 85), facing_direction="up", corners=True)
    level3.add_platform((500, 1000), (150, 85), facing_direction="up", corners=True)                                            # bottom wall section 1
    level3.add_platform((850, 1000), (150, 85), facing_direction="up", corners=True)
    level3.add_platform((1200, 1080 - 80), (2500, 85), facing_direction="up", corners=True)                                           # bottom wall section 3
    level3.add_platform((4300, 1080 - 80), (750, 85), facing_direction="up", corners=True)                                           # bottom wall section 4

    # fix the corners
    level3.add_platform((-10, 85), (70, 70), facing_direction=None)
    level3.add_platform((5040, 85), (70, 70), facing_direction=None)
    level3.add_platform((-10, 1000), (70, 70), facing_direction=None)
    level3.add_platform((5040, 1080 - 70), (70, 70), facing_direction=None)

    # add moving platforms throughout
    level3.add_moving_platform((350, 525), (100, 50), 2, (350, 700), facing_direction="up")    # first water section
    level3.add_moving_platform((500, 300), (100, 50), 2, (500, 525), facing_direction="up")
    level3.add_moving_platform((850, 300), (100, 50), 2, (850, 775), facing_direction="up")

    level3.add_moving_platform((-2000, 0), (2000, 800), 0.75, (0, 0), facing_direction="up")
    #over water at top for momotaro
    #level3.add_moving_platform((2750, 350), (100, 35), 2, (3150, 350), facing_direction="up")
    #level3.add_moving_platform((3700, 350), (100, 35), 2, (4100, 350), facing_direction="up")

    # add regular platforms
    level3.add_platform((50, 750), (600, 50), facing_direction="up")
    level3.add_platform((1050, 750), (650, 50), facing_direction="up")

    level3.add_platform((650, 300), (100, 500), facing_direction="up")
    level3.add_platform((1100, 140), (100, 515), facing_direction="down")
    level3.add_platform((1200, 600), (150, 50), facing_direction="up")
    level3.add_platform((1550, 450), (150, 50), facing_direction="up")
    level3.add_platform((1200, 300), (150, 50), facing_direction="up")
    level3.add_platform((1700, 300), (100, 450 + 50), facing_direction="up")

    level3.add_platform((2000, 70), (50, 450 + 50 + 330), facing_direction=None)
    level3.add_platform((2450, 400), (50, 450 + 50), facing_direction=None)
    level3.add_platform((2050, 800), (150, 50), facing_direction="up")
    level3.add_platform((2450 - 150, 575), (150, 50), facing_direction="up")
    level3.add_platform((2050, 400), (150, 50), facing_direction="up")
    level3.add_platform((2450, 400), (2400, 70), facing_direction="up")
    #level3.add_platform((3250, 400), (450, 70), facing_direction="up")
    #level3.add_platform((4200, 400), (600, 70), facing_direction="up")
    #level3.add_platform((2450, 400), (2450, 70), facing_direction="up")


    level3.add_platform((2750, 800), (475, 70), facing_direction="up")
    level3.add_platform((2750 + 750 - 200, 675), (200, 35), facing_direction="up")
    level3.add_platform((3500, 400), (70, 450 + 20), facing_direction="up")

    #level3.add_platform((3850, 850), (300, 50), facing_direction="up")
    level3.add_platform((4300, 450), (100, 375), facing_direction=None)

    level3.add_platform((4700, 400), (100, 500), facing_direction="up")


    # add water sections
    level3.add_platform((300, 1080 - 70), (200, 70), platform_type="water")  # water section 1 (bottom)
    level3.add_platform((650, 1080 - 70), (200, 70), platform_type="water")  # water section 2 (bottom)
    level3.add_platform((1000, 1080 - 70), (200, 70), platform_type="water")
    level3.add_platform((750, 769), (300, 25), platform_type="water")  # water section 1 (bottom)
    level3.add_platform((750, 794), (300, 5), facing_direction=None)  # water section 1 (bottom)

    level3.add_platform((2750 + 770 - 300, 815), (300, 25), platform_type="water")
    level3.add_platform((2750 + 770 - 300, 840), (300, 30), facing_direction=None)
    level3.add_platform((2425 + 70, 575), (200, 25), platform_type="water")
    level3.add_platform((2425 + 70, 600), (200, 25), facing_direction=None)
    level3.add_platform((3700, 1100 - 71), (600, 25), platform_type="water")
    level3.add_platform((3700, 1125 - 71), (600, 25), facing_direction=None)
    #level3.add_platform((2750, 419), (500, 25), platform_type="water")
    #level3.add_platform((2750, 444), (500, 25), facing_direction=None)
    #level3.add_platform((3700, 419), (500, 25), platform_type="water")
    level3.add_platform((3700, 444), (500, 25), facing_direction=None)

    # add button/gate obstacles
    level3.add_obstacle(570, 992, "button", fence_initial=(700, 150),  fence_final=(700, 0), fence_dimensions=(100, 300))
    level3.add_obstacle(1270, 992, "button", fence_initial=(1150, 600),  fence_final=(1150, 450), fence_dimensions=(100, 300))
    level3.add_obstacle(920, 992, "dog_button", fence_initial=(1750, 150),  fence_final=(1750, 0), fence_dimensions=(100, 300), dog_y=900)# first top gate
    level3.add_obstacle(3600, 395, "button", fence_initial=(2800 , 925), fence_final=(2800 , 700),
                        fence_dimensions=(70, 300*7/10))
    level3.add_obstacle(4050, 395, "button", fence_initial=(3950, 750), fence_final=(3950, 600),
                        fence_dimensions=(100, 300))
    # add surrounding platforms for walls
    level3.add_platform(position=(3900, 470), dimensions=(110, 300), facing_direction="down")
    level3.add_platform(position=(3900,900), dimensions=(110, 200), facing_direction="up")


    level3.add_obstacle(4350, 395, "button", fence_initial=(4350, 900),
                        fence_final=(4350, 600),
                        fence_dimensions=(100, 300))
    level3.add_obstacle(3400, 670, "button", fence_initial=(3500, 250),
                        fence_final=(3500, -50),
                        fence_dimensions=(100, 300))
        # second bottom gate

    level3.add_spikes((2700, 300), (500, 100), vase_position=(2500, 515), duration=500)

    #level3.add_obstacle(3400, 670, 'dog_button', fence_initial=(3300, 290), fence_final=(3300, 590), fence_dimensions=(100, 300), dog_y=550)

    # add demons
    level3.add_demon([1610, 300], (475, 100))
    level3.add_demon([2350, 400], (475, 100))
    level3.add_demon([2050, 700], (475, 100))
    level3.add_demon([3900, 200], (475, 100))

    # add tori gate obstacle
    level3.add_obstacle(4550, 300, "torigate", gate_num=1)
    level3.add_obstacle(4700, 300, "torigate", gate_num=2)

    # add coins
    level3.add_obstacle(4200, 280, "coin")
    level3.add_obstacle(2060, 300, "coin")
    level3.add_obstacle(1550, 650, "coin")

    momotaro = momotaro_player.Momotaro([200, 300])
    # momotaro = momotaro_player.Momotaro([200, 900])
    pet = pet_player.Pet([200, 900])

    return level3, momotaro, pet