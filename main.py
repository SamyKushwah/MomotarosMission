import pygame

# Accompanying script imports
import mainmenu


def main():
    pygame.init()

    # Do we want the screen to be adjustable?
    # Do we want to enforce a minimum screen resolution? (to prevent our graphics from dying if the window is scaled too small)
    # What resolution do we want?

    # Screen constants - can also be made into an object with the following attributes
    min_width = 1024
    min_height = 768
    screen_flags = None
    screen = pygame.display.set_mode((min_width, min_height), screen_flags)

    # To ask: is it ok to have the screen as a global variable or how can we make the screen object passable into the
    # other scripts that we will use? Will we need to pass the screen object into every class constructor
    # (OOP approach) or into every function call (functional approach)?



if __name__ == "__main__":
    main()