import pygame
import sys

from Game import Game

tetris = Game()

clock = pygame.time.Clock()

tetris.start()
# Game loop
while True:
    # calculate the frame rate
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    tetris.handle_keypressed()
    tetris.updateScreen()
