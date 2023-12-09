import pygame
import sys

from entities import GameArea, ITetromino
from constants import BLOCKSIZE

# Initialize Pygame
pygame.init()

# Set the size of the game window
screen_width = 600
screen_height = 1200
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption('Tetris')


gameArea = GameArea(10, 20, screen)
tetromino = ITetromino(gameArea)

clock = pygame.time.Clock()

# Game loop
while True:
    # calculate the frame rate
    clock.tick(60)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Fill the screen with gray
    screen.fill((128, 128, 128))

    # Draw the game area
    gameArea.draw(screen)
    
    
    # Draw the tetromino
    tetromino.draw(screen)
    
    # Handle key presses
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_UP]:
        tetromino.rotate()
    if pressed_keys[pygame.K_DOWN]:
        tetromino.move_down()
    if pressed_keys[pygame.K_LEFT]:
        tetromino.move_left()
    if pressed_keys[pygame.K_RIGHT]:
        tetromino.move_right()
    

    # Update the display
    pygame.display.flip()
