class Level:
    def __init__(self, lvl_num, lvl_width, lvl_height):
        self.width = lvl_width
        self.height = lvl_height
        self.lvl_num = lvl_num
        self.screen = pygame.display.set_mode((lvl_width, lvl_height))
        #self.momotaro = Momotaro()
        #self.animals = Animals()
        self.platform_list = []
        self.obstacle_list = []
        self.coin_list = []
        self.demon_list = []
        self.coins_collected = 0
        self.lvl_complete = False

    def draw(self):
        self.screen.fill((0, 0, 0))
        for rectangle in self.platform_list:
            #placeholder color
            pygame.draw.rect(self.screen, (0,200,0), rectangle.get_rect())

    def get_screen(self):
        return self.screen

    def add_platform(self,x,y,height,width):
        temp_platform = Platform(x,y,height,width)
        self.platform_list.append(temp_platform)
    
    #def add_demon(self,x,y)
    #def add_obstacle(self,x,y)
    #def add_coin(self,x,y)

class Platform:
    def __init__(self, x, y, width, height):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.__rect = pygame.Rect(x,y,width,height)
    def get_rect(self):
        return self.__rect
