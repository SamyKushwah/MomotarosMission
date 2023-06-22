from game_templates import level


def create_level(my_toolbox):
    level1 = level.Level(my_toolbox, 1, 5100, 5000)
    level1.add_platform("stone", (50, 600), (5000, 400))
    level1.add_platform("stone", (0, 100), (300, 80))
    #level1.add_platform("stone", (700, 500), (300, 30))
    #level1.add_platform("stone", (300, 300), (300, 30))
    #level1.add_platform("stone", (30, 450), (200, 30))
    #level1.add_demon(600, 501, 1000, 50)
    level1.add_demon(400, 201, 1000, 30)
    #level1.add_obstacle(500, 600, "button")
    return level1
