import pygame
import main_menu
def main():
    pygame.init()
    screen_width = 1024
    screen_height = 768
    screen = pygame.display.set_mode((screen_width,screen_height))
    main_menu.display_screen(screen)


if __name__ == '__main__':
    main()