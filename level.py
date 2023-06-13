class Level:
    def __init__(self, lvl_num, lvl_width, lvl_height):
        self.__width = lvl_width
        self.__height = lvl_height
        self.__lvl_num = lvl_num
        self.__screen = pygame.display.set_mode((lvl_width, lvl_height))
        #self.__momotaro = Momotaro()
        #self.__animals = Animals()
        self.__platform_list = []
        self.__obstacle_list = []
        self.__coin_list = []
        self.__demon_list = []
        self.__coins_collected = 0
        self.__lvl_complete = False

    #def run(self):
        # run event handling for the level until lvl_complete == True
        """while not self.__lvl_complete:
            
            #event handling
            
            #draw to screen
            self.draw(self)
            pygame.display.update()"""
        
    def draw(self):
        self.__screen.fill((0, 0, 0))
        for rectangle in self.__platform_list:
            #placeholder color
            pygame.draw.rect(self.__screen, (0,200,0), rectangle.get_rect())
        #draw rest of characters and objects

    def get_screen(self):
        return self.__screen

    def get_lvl_num(self):
        return self.__lvl_num

    def add_platform(self,x,y,height,width):
        temp_platform = Platform(x,y,height,width)
        self.__platform_list.append(temp_platform)

    #def add_demon(self,x,y)
    #def add_obstacle(self,x,y)
    #def add_coin(self,x,y)

class Platform:
    def __init__(self, x, y, width, height):
        self.__height = height
        self.__width = width
        self.__x = x
        self.__y = y
        self.__rect = pygame.Rect(x,y,width,height)
    def get_rect(self):
        return self.__rect
