import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 400
window = pygame.display.set_mode((window_width, window_height))
window2 = pygame.display.set_mode((1000,1000))
window = window2
pygame.display.set_caption("Two Player Game")

# Set up the players
player1_x = 50
player1_y = window_height // 2
player1_speed = 5

player2_x = window_width - 50
player2_y = window_height // 2
player2_speed = 0.1

player1_color = (255, 0, 0)  # Red
player2_color = (0, 0, 255)  # Blue

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1_y -= player1_speed
    if keys[pygame.K_s]:
        player1_y += player1_speed
    if keys[pygame.K_UP]:
        player2_y -= player2_speed
    if keys[pygame.K_DOWN]:
        player2_y += player2_speed

    # Check boundaries
    if player1_y < 0:
        player1_y = 0
    elif player1_y > window_height - 50:
        player1_y = window_height - 50

    if player2_y < 0:
        player2_y = 0
    elif player2_y > window_height - 50:
        player2_y = window_height - 50

    # Draw the game window
    window.fill((0, 0, 0))  # Black

    pygame.draw.rect(window, player1_color, (player1_x, player1_y, 50, 50))
    pygame.draw.rect(window, player2_color, (player2_x - 50, player2_y, 50, 50))

    pygame.display.update()

# Quit the game
pygame.quit()
sys.exit()
