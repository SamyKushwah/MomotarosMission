import pygame
from templates import button

def run_pause_screen(screen):
    # load background image and scale it to fit in the screen window
    background = pygame.image.load("../images/pause_screen/pause_screen_bkgnd.png")
    w, h = pygame.display.get_surface().get_size()
    background = pygame.transform.scale(background, (w, h))

    # load resume, restart, and home buttons - scale to background size
    resume_img =pygame.image.load("../images/pause_screen/resume_btn.png")
    resume_img = pygame.transform.scale(resume_img, (w / 3, h / 12))
    resume_btn = button.Button(resume_img)

    restart_img = pygame.image.load("../images/pause_screen/restart_btn.png")
    restart_img = pygame.transform.scale(restart_img, (w / 3, h / 12))
    restart_btn = button.Button(restart_img)

    home_img = pygame.image.load("../images/pause_screen/home_btn.png")
    home_img = pygame.transform.scale(home_img, (w / 4, h / 13))
    home_btn = button.Button(home_img)

    # driver loop setup
    running = True
    dt = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        # Check if the mouse was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check which button was clicked
                if resume_btn.is_clicked(event.pos):
                    return "resume"
                elif restart_btn.is_clicked(event.pos):
                    return "restart"
                elif home_btn.is_clicked(event.pos):
                    return "home"

            # if screen is resized rescale all buttons and images
            elif event.type == pygame.VIDEORESIZE:
                # resize screen and get new dimensions
                background = pygame.transform.scale(background, event.size)
                w, h = pygame.display.get_surface().get_size()

                # resize button images
                resume_img = pygame.transform.scale(resume_img, (w / 3, h / 12))
                resume_btn.image = resume_img
                restart_img = pygame.transform.scale(restart_img, (w / 3, h / 12))
                restart_btn.image = restart_img
                home_img = pygame.transform.scale(home_img, (w / 4, h / 13))
                home_btn.image = home_img

        # draw the background and buttons with scaled position
        screen.blit(background, (0, 0))

        resume_btn.draw(screen, (w / 2, h * (6 / 13)))
        restart_btn.draw(screen, (w / 2, h * (8 / 13)))
        home_btn.draw(screen, (w / 2, h * (10 / 13)))

        pygame.display.flip()
