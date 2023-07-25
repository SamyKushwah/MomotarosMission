from momotaro.game_templates import level
from momotaro.game_templates import momotaro_player, pet_player


def create_level(my_toolbox):
    # create level_1 object and load the images for tiles
    level1 = level.Level(my_toolbox, 1, 5100, 5000, background="mountains")
    level1.load_water_img()
    level1.load_stone_imgs()

    # add tutorial text
    level1.add_tutorial_text(550,500,0,900,(100,100),"Player 1: Use W, A, and D to move around and jump.", font_size=30)
    level1.add_tutorial_text(580,550,0,900,(100,100),"Player 2: Use the arrow keys to move around and jump.", font_size=30)

    level1.add_tutorial_text(1030,400,680,1200,(100,100),"Only Player 1 can collect coins.", font_size=30)

    level1.add_tutorial_text(1200,850,1100,1500,(100,100),"Stand on the button to raise the gate.", font_size=30)

    # add four walls
    level1.add_platform(position=(0, 0), dimensions=(71, 1080), facing_direction="right")  # left wall
    level1.add_platform((5100 - 70, 0), (70, 1080), facing_direction="left")  # right wall
    level1.add_platform((0, 1080 - 70), (3930, 70))  # bottom wall part 1
    level1.add_platform((0, 0), (5100, 140), facing_direction="down")  # top wall

    # fix the corners
    level1.add_platform((-10, 70), (70, 70), facing_direction=None)
    level1.add_platform((5040, 70), (70, 70), facing_direction=None)
    level1.add_platform((-10, 1080 - 70), (70, 70), facing_direction=None)
    level1.add_platform((5040, 1080 - 70), (70, 70), facing_direction=None)

    # add platforms
    level1.add_platform((400, 800), (300, 50), facing_direction="up")  # platform 1 for coin 1
    level1.add_platform((900, 690), (300, 50), facing_direction="up")  # platform 2 for coin 1
    level1.add_obstacle(1080, 600, "coin")  # coin 1

    # gate leading to after the first coin
    level1.add_obstacle(1265, 1000, 'button', fence_initial=(1458, 780), fence_final=(1458, 540), fence_dimensions=(200, 500))

    # block to cover off the gate top
    level1.add_platform((1350, 130), (215, 500), facing_direction="all")

    # second gate, must use bird
    level1.add_obstacle(1945, 597, "button", fence_initial= (2067, 820), fence_final=(2067, 500), fence_dimensions=(150, 400))

    # platforms blocking off the button and gate top
    level1.add_platform((1840, 605), (150, 50))
    level1.add_platform((1990, 410), (150, 300))

    level1.add_tutorial_text(1750, 700, 1500, 2100, (100, 100), "Bird can jump multiple times.", font_size=23)
    level1.add_tutorial_text(1780, 800, 1500, 2100, (100, 100), "Use Bird to reach high platforms.", font_size=23)

    # third gate, must use dog
    level1.add_obstacle(2630, 1000, "dog_button", fence_initial=(2762, 820), fence_final=(2762, 540),
                        fence_dimensions=(150, 400), dog_y=825)

    # platforms blocking off the button and gate top
    level1.add_platform((2690, 410), (150, 300))

    level1.add_tutorial_text(2300, 650, 2200, 2800, (100, 100), "Player 2:", font_size=25)
    level1.add_tutorial_text(2350, 700, 2200, 2800, (100, 100), "Press / to swap to Dog.", font_size=25)
    level1.add_tutorial_text(2415, 750, 2200, 2800, (100, 100), "Use . as Dog to sniff for hidden buttons.", font_size=25)

    # monkey section (NOT IMPLEMENTED YET)

    # moving platform and water section
    level1.add_platform((3930, 1015), (700, 70), platform_type="water")
    level1.add_moving_platform(position=(3900, 900), dimensions=(200, 50), max_speed=3, target=(4500, 900))
    level1.add_platform((4630, 1010), (400, 70))

    level1.add_tutorial_text(4000, 700, 3700, 4600, (100,100), text="Players will die if they touch water.")
    level1.add_tutorial_text(4000, 750, 3700, 4600, (100,100), text="Avoid it using the platforms.")

    # Platforms connecting the bottom half to the upper half
    level1.add_platform((4830, 810), (200, 50))
    level1.add_moving_platform(position=(3680, 600), dimensions=(250,50), max_speed=3, target=(4530, 600))

    # Platform with the third coin gated off by the button
    level1.add_platform((4000, 400), (1030, 50))

    # Upper platform button and gate
    level1.add_obstacle(2350, 390, "button", fence_initial=(4230, 200), fence_final=(4230, -20), fence_dimensions=(100, 400))

    # add demon and second coin
    level1.add_demon([3400, 380], (500,500))
    level1.add_tutorial_text(3500, 200, 2600, 4000, (100,100), "Demons will charge after you if you get too close.", font_size=25)
    level1.add_tutorial_text(3500, 250, 2600, 4000, (100,100), "Player 1 press and hold R to charge up an attack.", font_size=25)
    level1.add_tutorial_text(3500, 300, 2600, 4000, (100,100), "The longer you hold, the stronger and longer your attack will be.", font_size=25)
    level1.add_obstacle(2500, 280, 'coin')

    # tutorial text above button to switch cameras
    level1.add_tutorial_text(2500, 200, 2400, 2900, (100,100), "Press C to swap the camera focus between players", font_size=25)

    # add third coin and oni behind the rightmost gate
    level1.add_demon([4630, 200], (450, 450))
    level1.add_obstacle(4900, 280, 'coin')

    # add end goal torigate
    level1.add_platform((1560, 400), (2200,50), facing_direction="up")
    #level1.add_obstacle(1650, 350, "torigate", gate_num=1) # end of the level marker
    #level1.add_obstacle(1800, 350, "torigate", gate_num=2)

    level1.add_obstacle(500, 950, "torigate", gate_num=1)  # end of the level marker
    level1.add_obstacle(700, 950, "torigate", gate_num=2)

    # add vase
    level1.add_spikes((500, 750), (100, 45), (400, 950))

    momotaro = momotaro_player.Momotaro([300, 300])
    pet = pet_player.Pet([200, 300])

    return level1, momotaro, pet