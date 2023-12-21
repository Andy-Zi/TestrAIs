import time
import pygame

from Tetris.constants import BLOCKSIZE

from Tetris.events import *

class MovementHandler:

    def __init__(self, gameArea, active_tetromino):
        self.gameArea = gameArea
        self.staging_x = self.gameArea.x + self.gameArea.width + 80
        self.staging_y = self.gameArea.y + 50
        self.active_tetromino = active_tetromino
        self.key_last_pressed = {pygame.K_UP: 0, pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_DOWN: 0, pygame.K_SPACE: 0}
        self.key_delay = {pygame.K_UP: 0.5, pygame.K_LEFT: 0.2, pygame.K_RIGHT: 0.2, pygame.K_DOWN: 0.2, pygame.K_SPACE: 0.5}
    
    def moveDown(self, raise_event = True):
        self.active_tetromino.move_down(raise_event)
    
    def moveLeft(self):
        self.active_tetromino.move_left()
    
    def moveRight(self):
        self.active_tetromino.move_right()
    
    def rotate(self):
        self.active_tetromino.rotate()

    def hardDrop(self):
        self.active_tetromino.hardDrop()
    
    def handleMovement(self, key):
        if key in self.key_last_pressed:
            self.key_last_pressed[key] = time.time()
        match(key):
            case pygame.K_LEFT:
                self.moveLeft()
            case pygame.K_RIGHT:
                self.moveRight()
            case pygame.K_DOWN:
                pygame.time.set_timer(MOVE_DOWN_EVENT, 0)
                self.moveDown(raise_event = False)
                pygame.time.set_timer(MOVE_DOWN_EVENT, 1000)
            case pygame.K_UP:
                self.rotate()
            case pygame.K_SPACE:
                self.hardDrop()
            case _:
                pass
    
    def handle_keypressed(self):
        keys = pygame.key.get_pressed()
        for key in self.key_last_pressed:
            if keys[key] and time.time() - self.key_last_pressed.get(key, 0) > self.key_delay[key]:
                self.handleMovement(key)
                self.key_last_pressed[key] = time.time()
    
    def moveTetrimono(self, x, y):
        self.active_tetromino.move(x, y)
    
    def move_tetromino_to_starting_position(self):
        old_x = self.active_tetromino.x
        old_y = self.active_tetromino.y
        self.active_tetromino.x = self.get_x_starting_position()
        self.active_tetromino.y = self.get_y_starting_position()
        for block in self.active_tetromino.shape:
            block.x = self.active_tetromino.x + block.x - old_x
            block.y = self.active_tetromino.y + block.y - old_y
    
    def get_x_starting_position(self):
        gameAreaWidth = self.gameArea.width // BLOCKSIZE
        tetrominoWidth = len(self.active_tetromino.baseShape[0])
        startingPosition = (gameAreaWidth - tetrominoWidth) // 2
        startingPosition *= BLOCKSIZE
        return startingPosition + self.gameArea.x
    
    def get_y_starting_position(self):
        return self.gameArea.y - (BLOCKSIZE * len(self.active_tetromino.baseShape))