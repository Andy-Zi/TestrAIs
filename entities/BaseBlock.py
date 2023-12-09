import pygame
from constants import BLOCKSIZE

class BaseBlock:
    def __init__(self, x, y, color, turningPoint, gameArea):
        self.x = x
        self.y = y
        self.color = color
        self.size = BLOCKSIZE 
        self.gameArea = gameArea
        self.turningPoint = turningPoint

    def draw(self, surface):
        if self.inGameArea():
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
    
    def inGameArea(self):
        return self.x >= self.gameArea.x and self.x < self.gameArea.x + self.gameArea.width and self.y >= self.gameArea.y and self.y < self.gameArea.y + self.gameArea.height
    
    def canMoveDown(self):
        return self.y + self.size < self.gameArea.y + self.gameArea.height
    
    def canMoveLeft(self):
        return self.x > self.gameArea.x
    
    def canMoveRight(self):
        return self.x + self.size < self.gameArea.x + self.gameArea.width
    
    def moveLeft(self):
        self.x -= self.size
        
    def moveRight(self):
        self.x += self.size
    
    def moveDown(self):
        self.y += self.size
    
    def rotate(self):
        # rotate the blocks around the turning point
        x = self.x - self.turningPoint[0] * BLOCKSIZE
        y = self.y - self.turningPoint[1] * BLOCKSIZE
        x, y = y, -x
        x += self.turningPoint[0] * BLOCKSIZE
        self.x = x
        self.y = y
