from entities import BaseBlock
from constants import BLOCKSIZE

class BaseTetromino:

    def __init__(self, shape, turningPoint, color, gameArea):
        self.turningPoint = turningPoint
        self.color = color
        self.gameArea = gameArea
        self.rotation = 0
        self.x = (self.gameArea.width - len(shape[0]) * BLOCKSIZE) // 2 + self.gameArea.x
        self.y = self.gameArea.y - len(shape) * BLOCKSIZE
        self.shape = self.shape_to_blocks(shape)

    # def rotate(self):
        # self.rotation = (self.rotation + 1) % len(self.shape)

    def rotate_back(self):
        self.rotation = (self.rotation - 1) % len(self.shape)

    def draw(self, surface):
        for block in self.shape:
            block.draw(surface)
    
    def move_left(self):
        for block in self.shape:
            if not block.canMoveLeft():
                return
        for block in self.shape:
            block.moveLeft()
        
    def move_right(self):
        for block in self.shape:
            if not block.canMoveRight():
                return
        for block in self.shape:
            block.moveRight()
        
    def move_down(self):
        for block in self.shape:
            if not block.canMoveDown():
                return
        for block in self.shape:
            block.moveDown()
    
    def shape_to_blocks(self, shape):
        blocks = []
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] == 1:
                    turningPoint = (self.turningPoint[0] * BLOCKSIZE, self.turningPoint[1] * BLOCKSIZE)
                    blocks.append(BaseBlock(self.x + j * BLOCKSIZE, self.y + i * BLOCKSIZE, turningPoint, self.color, self.gameArea))
        return blocks

    def rotate(self):
        for block in self.shape:
            block.rotate()