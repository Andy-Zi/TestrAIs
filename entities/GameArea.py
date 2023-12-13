import pygame

from constants import BLOCKSIZE

class GameArea:
    def __init__(self, width, height, screen):
        screen_width, screen_height = screen.get_size()
        self.x = (screen_width - width * BLOCKSIZE) / 2
        self.y = (screen_height - height * BLOCKSIZE) / 2
        self.width = width * BLOCKSIZE
        self.height = height * BLOCKSIZE
        # define self.Blocks as a matrix of the size of the game area and initialize it with None
        self.blocks = [[None for _ in range(width)] for _ in range(height)]
    
    def clear(self):
        self.blocks = [[None for _ in range(len(self.blocks[0]))] for _ in range(len(self.blocks))]
        
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height), 1)

        # add a grid
        for i in range(1, self.width // BLOCKSIZE):
            pygame.draw.line(surface, (255, 255, 255), (self.x + i * BLOCKSIZE, self.y), (self.x + i * BLOCKSIZE, self.y + self.height))
        for i in range(1, self.height // BLOCKSIZE):
            pygame.draw.line(surface, (255, 255, 255), (self.x, self.y + i * BLOCKSIZE), (self.x + self.width, self.y + i * BLOCKSIZE))
        
        # draw the blocks
        for row in self.blocks:
            for block in row:
                if block != None:
                    block.draw(surface)
    def canAddBlocks(self, blocks):
        for block in blocks:
            x = int((block.x - self.x) // BLOCKSIZE)
            y = int((block.y - self.y) // BLOCKSIZE)
            if y < 0:
                return False
            return True
        
    def addBlocks(self, blocks):
        if self.canAddBlocks(blocks):
            for block in blocks:
                x = int((block.x - self.x) // BLOCKSIZE)
                y = int((block.y - self.y) // BLOCKSIZE)
                self.blocks[y][x] = block
            return True
        return False
    
    def checkRows(self):
        for i in range(len(self.blocks)):
            if self.isFullRow(i):
                self.removeRow(i)
                self.moveRowsDown(i)
    
    def isFullRow(self, row):
        for block in self.blocks[row]:
            if block == None:
                return False
        return True
    
    def removeRow(self, row):
        for block in self.blocks[row]:
            block = None
            
    def moveRowsDown(self, row):
        for i in range(row, 0, -1):
            for j in range(len(self.blocks[i])):
                self.blocks[i][j] = self.blocks[i-1][j]
                if self.blocks[i][j] != None:
                    self.blocks[i][j].moveDown()
    
    def getPositionOnGrid(self, x, y):
        return (int((x - self.x) // BLOCKSIZE), int((y - self.y) // BLOCKSIZE))
