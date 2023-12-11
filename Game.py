import pygame
import random

from entities import GameArea
from entities import ITetromino, ZTetromino, OTetromino, STetromino, JTetromino, LTetromino, TTetromino

class Game:

    rotationNotPressed = True

    def __init__(
        self,
        screen_width: int = 600,
        screen_height: int = 1200,
        ) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Tetris')
        self.gameArea = GameArea(10, 20, self.screen)
        self.next_tetromino = self.get_random_tetromino()
        self.active_tetromino = None
    
    def handle_keypressed(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP] and self.rotationNotPressed:
            self.active_tetromino.rotate()
            self.rotationNotPressed = False
        if not pressed_keys[pygame.K_UP]:
            self.rotationNotPressed = True
        if pressed_keys[pygame.K_LEFT]:
            self.active_tetromino.move_left()
        if pressed_keys[pygame.K_RIGHT]:
            self.active_tetromino.move_right()
        if pressed_keys[pygame.K_DOWN]:
            if self.active_tetromino.move_down():
                self.gameArea.addBlocks(self.active_tetromino.shape)
                self.spawnTetromino()
    
    def updateScreen(self):
        self.screen.fill((128, 128, 128))
        self.gameArea.draw(self.screen)
        self.active_tetromino.draw(self.screen)
        pygame.display.flip()
    
    def spawnTetromino(self):
        self.active_tetromino = self.next_tetromino
        self.next_tetromino = self.get_random_tetromino()
    
    def get_random_tetromino(self):
        tetrominos = [ITetromino, ZTetromino, OTetromino, STetromino, JTetromino, LTetromino, TTetromino]
        return random.choice(tetrominos)(self.gameArea)
    
    def start(self):
        self.spawnTetromino()