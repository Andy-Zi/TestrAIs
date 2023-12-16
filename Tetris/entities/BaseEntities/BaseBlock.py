import pygame
from Tetris.constants import BLOCKSIZE

class BaseBlock:
    def __init__(self, x, y, color, turningPoint, gameArea):
        self.x = x
        self.y = y
        self.color = color
        self.size = BLOCKSIZE 
        self.gameArea = gameArea
        self.turningPoint = turningPoint

    def draw(self, surface):
        # if self.inGameArea():
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))
    
    def inGameArea(self):
        return self.x >= self.gameArea.x and self.x < self.gameArea.x + self.gameArea.width and self.y >= self.gameArea.y and self.y < self.gameArea.y + self.gameArea.height
    
    def canMoveDown(self):
        return self.y + self.size < self.gameArea.y + self.gameArea.height
    
    def canMoveLeft(self):
        if not self.x > self.gameArea.x:
            False
        for row in self.gameArea.blocks:
            for block in row:
                if block != None and block.x == self.x - self.size and block.y == self.y:
                    return False
        return True
    
    def canMoveRight(self):
        if not self.x + self.size < self.gameArea.x + self.gameArea.width:
            False
        for row in self.gameArea.blocks:
            for block in row:
                if block != None and block.x == self.x + self.size and block.y == self.y:
                    return False
        return True
    
    def moveLeft(self):
        self.x -= self.size
        
    def moveRight(self):
        self.x += self.size
    
    def moveDown(self):
        self.y += self.size
    
    def rotate(self, shift_x = 0, shift_y = 0, clockwise=True):
        rx, ry = self.turningPoint
        rx += self.x
        ry += self.y
        x, y = self.x, self.y
        y += self.size

        if clockwise:
            # For clockwise rotation
            new_x = rx + (ry - y)
            new_y = ry - (rx - x)
        else:
            # For counterclockwise rotation
            new_x = rx - (ry - y)
            new_y = ry + (rx - x)

        self.x = new_x + shift_x
        self.y = new_y + shift_y

        new_rx = rx - new_x
        new_ry = ry - new_y
        
        self.turningPoint = (new_rx, new_ry)
    
    def canRotate(self):
        rx, ry = self.turningPoint
        rx += self.x
        ry += self.y
        x, y = self.x, self.y
        y += self.size

        # For clockwise rotation
        new_x = rx + (ry - y)
        new_y = ry - (rx - x)

        shift_x = 0
        shift_y = 0
        
        if new_x < self.gameArea.x:
            shift_x = -(new_x - self.gameArea.x)
        if new_x + self.size > self.gameArea.x + self.gameArea.width:
            shift_x = -((new_x + self.size) - (self.gameArea.x + self.gameArea.width))
        if  new_y + self.size > self.gameArea.y + self.gameArea.height:
            shift_y = -30
        
        for row in self.gameArea.blocks:
            for block in row:
                if block != None and block.x == new_x + shift_x and block.y == new_y + shift_y:
                    return shift_x, shift_y, False

        return shift_x, shift_y, True

    def hitGround(self):
        # check if the block hit the ground
        if self.y + self.size >= self.gameArea.y + self.gameArea.height:
            return True
        else:
            return False
    
    def hitBlock(self, blocks):
        # check if the block hit another block
        x = int((self.x - self.gameArea.x) // BLOCKSIZE)
        y = int((self.y - self.gameArea.y) // BLOCKSIZE)
        if y + 1 < len(blocks) and blocks[y+1][x] != None and y + 1 >= 0:
            return True
        else:
            return False