from game_templates import level
from game_templates import momotaro_player, pet_player


def create_level(my_toolbox):
    level2 = level.Level(my_toolbox, 2, 5100, 5000, background="bamboo")
    level2.load_water_img()
    level2.load_stone_imgs()

    # add four walls
    level2.add_platform(position=(0, 0), dimensions=(71, 1080), facing_direction="right")        # left wall
    level2.add_platform((5100 - 70, 0), (70, 1080), facing_direction="left")                     # right wall
    level2.add_platform((0, 0), (5100, 140), facing_direction="down")                            # top wall
    level2.add_platform((0, 1080 - 70), (300, 70))                                               # bottom wall section 1
    level2.add_platform((1000, 1080 - 70), (280, 70))                                            # bottom wall section 2
    level2.add_platform((2030, 1080 - 70), (3070, 70))                                           # bottom wall section 3
    # 2030

    # fix the corners
    level2.add_platform((-10, 70), (70, 70), facing_direction=None)
    level2.add_platform((5040, 70), (70, 70), facing_direction=None)
    level2.add_platform((-10, 1080 - 70), (70, 70), facing_direction=None)
    level2.add_platform((5040, 1080 - 70), (70, 70), facing_direction=None)

    # add water sections
    level2.add_platform((300, 1080 - 70), (700, 70), platform_type="water")    # water section 1 (bottom)
    level2.add_platform((1280, 1080 - 70), (750, 70), platform_type="water")   # water section 2 (bottom)
    level2.add_platform((4600, 1080 - 71), (430, 70), platform_type="water")   # water section 3 (bottom)
    level2.add_platform((2400, 1080 - 71), (1150, 70), platform_type="water")

    level2.add_platform((350, 340 + 20), (650, 70), platform_type="water")          # water section 1 (top)
    level2.add_platform((1280, 410 + 20), (750, 70), platform_type="water")         # water section 2 (top)

    # add moving platforms throughout
    level2.add_moving_platform((400, 940), (300, 50), 4, (600, 940), facing_direction="up")    # first water section
    level2.add_moving_platform((1330, 900), (200, 50), 5, (1430, 900), facing_direction="up")  # second water section
    level2.add_moving_platform((1680, 900), (200, 50), 5, (1780, 900), facing_direction="up")  # second water section

    level2.add_moving_platform((400, 320), (200, 50), 4, (750, 320), facing_direction="up")    # first water section (top)

    #level2.add_moving_platform((2450, 900), (200, 50), 3, (2900, 545), facing_direction="up")  # before tori gates
    #level2.add_moving_platform((2000, 900), (200, 50), 2, (2000, 545), facing_direction="up")
    level2.add_moving_platform((2400, 545), (300, 50), 2, (2400, 700), facing_direction="up")
    level2.add_moving_platform((2850, 500), (300, 50), 2, (2850, 800), facing_direction="up")
    level2.add_moving_platform((3300, 445), (300, 50), 2, (3300, 900), facing_direction="up")

    # add regular platforms
    level2.add_platform((70, 340), (280, 140), facing_direction="up")       # first section (top)
    level2.add_platform((350, 410), (370, 70),  facing_direction=None)
    level2.add_platform((720, 410), (280, 210),  facing_direction=None)
    level2.add_platform((480, 590), (240, 30), facing_direction="up")
    level2.add_platform((1000, 340), (280, 420), facing_direction="up")
    level2.add_platform((1280, 480), (750, 70), facing_direction=None)
    level2.add_platform((2030, 410), (250, 140), facing_direction="up")
    level2.add_platform((1400, 330), (510, 50), facing_direction="up")      # above second water section (top)

    #level2.add_platform((2450, 545), (200, 50), facing_direction="up")      # solo floating platform

    level2.add_platform((3700, 400), (700, 160), facing_direction="up")     # chunk with tori gates
    #level2.add_platform((4200, 600), (200, 50), facing_direction="up")      # middle with coin
    level2.add_platform((4600, 500), (430, 160), facing_direction="up")     # final chunk with fence

    level2.add_platform((4715, 900), (200, 50), facing_direction="up")      # low platform with final coin

    # add button/gate obstacles
    level2.add_obstacle(600, 580, "button", fence_initial=(1075, 140),  fence_final=(1075, -60), fence_dimensions=(150, 400))     # first top gate
    level2.add_obstacle(1200, 330, "button", fence_initial=(2105, 210), fence_final=(2105, -60), fence_dimensions=(150, 400))     # second top gate
    level2.add_obstacle(4900, 500, "button", fence_initial=(3775, 200), fence_final=(3775, -60), fence_dimensions=(150, 400))     # third top gate
    level2.add_obstacle(3950, 1000, "button", fence_initial=(4675, 300), fence_final=(4675, -60), fence_dimensions=(150, 400))    # fourth top gate
    level2.add_obstacle(1210, 1000, "button", fence_initial=(2105, 778), fence_final=(2105, 320), fence_dimensions=(150, 465))    # first bottom gate
    level2.add_obstacle(4100, 1000, "button", fence_initial=(4250, 778), fence_final=(4250, 330), fence_dimensions=(150, 465))    # second bottom gate

    # add demons
    level2.add_demon([1655, 200], (300, 100))
    level2.add_demon([2775, 1000], (700, 300))
    level2.add_demon([3900, 350], (300, 100))

    # add tori gate obstacle
    level2.add_obstacle(3950, 350, "torigate", gate_num=1)
    level2.add_obstacle(4100, 350, "torigate", gate_num=2)

    # add coins
    level2.add_obstacle(3000, 350, "coin")
    level2.add_obstacle(2550, 400, "coin")
    level2.add_obstacle(3450, 400, "coin")

    momotaro = momotaro_player.Momotaro([300, 200])
    pet = pet_player.Pet([200, 500])

    return level2, momotaro, pet