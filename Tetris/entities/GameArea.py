import pygame

from Tetris.constants import BLOCKSIZE

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
        lines_cleared = 0
        for i in range(len(self.blocks)):
            if self.isFullRow(i):
                self.removeRow(i)
                self.moveRowsDown(i)
                lines_cleared += 1
        return lines_cleared
    
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

    def goodness(self):
        highest_column = 0
        total_holes = 0
        
        for i in range(len(self.blocks[0])):  # iterate over each column
            column_height = 0
            found_block = False  # flag to indicate if a block has been found in the current column
            hole_size = 0  # size of the current hole
            for j in range(len(self.blocks)):  # iterate over each cell in the column
                if self.blocks[j][i] is not None:
                    column_height = len(self.blocks) - j
                    found_block = True
                    if hole_size > 0:  # if a block is found and hole_size > 0, it's a hole
                        total_holes += hole_size  # add the size of the hole to total_holes
                        hole_size = 0  # reset hole_size
                elif found_block:  # if the cell is None and a block has been found above, increment hole_size
                    hole_size += 1
            highest_column = max(highest_column, column_height)
        
        return 0.5 * (len(self.blocks) - highest_column) + 0.5 * (len(self.blocks[0]) - total_holes) 
        
    def highest_column(self):
        for i in range(len(self.blocks[0])):
            for j in range(len(self.blocks)):
                if self.blocks[j][i] is not None:
                    return len(self.blocks) - j
        return 0
    
    def holes(self):
        total_holes = 0
        for i in range(len(self.blocks[0])):
            found_block = False
            hole_size = 0
            for j in range(len(self.blocks)):
                if self.blocks[j][i] is not None:
                    found_block = True
                    if hole_size > 0:
                        total_holes += hole_size
                        hole_size = 0
                elif found_block:
                    hole_size += 1
        return total_holes
    
    def bumpiness(self):
        bumpiness = 0
        for i in range(len(self.blocks[0]) - 1):
            bumpiness += abs(self.column_height(i) - self.column_height(i + 1))
        return bumpiness

    def column_height(self, column):
        for i in range(len(self.blocks)):
            if self.blocks[i][column] is not None:
                return len(self.blocks) - i
        return 0