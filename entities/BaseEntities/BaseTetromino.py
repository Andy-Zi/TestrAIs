from entities import BaseBlock
from constants import BLOCKSIZE

class BaseTetromino:

    def __init__(self, shape, turningPoint, color, gameArea):
        self.turningPoint = turningPoint
        self.color = color
        self.gameArea = gameArea
        self.rotation = 0
        self.x = self.get_starting_position(shape)
        self.y = self.gameArea.y - len(shape) * BLOCKSIZE
        self.shape = self.shape_to_blocks(shape)
    
    def get_starting_position(self, shape):
        gameAreaWidth = self.gameArea.width // BLOCKSIZE
        tetrominoWidth = len(shape[0])
        startingPosition = (gameAreaWidth - tetrominoWidth) // 2
        startingPosition *= BLOCKSIZE
        return startingPosition + self.gameArea.x

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
        for block in self.shape:
            if block.hitGround():
                return True  
    
    def shape_to_blocks(self, shape):
        blocks = []
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] == 1:
                    turningPoint_x = (self.turningPoint[0] - j) * BLOCKSIZE
                    turningPoint_y = (self.turningPoint[1] - i) * BLOCKSIZE
                    turningPoint = (turningPoint_x, turningPoint_y)
                    # turningPoint = (self.turningPoint[0] * BLOCKSIZE, self.turningPoint[1] * BLOCKSIZE)
                    blocks.append(
                        BaseBlock(
                            x = self.x + j * BLOCKSIZE, 
                            y = self.y + i * BLOCKSIZE,
                            turningPoint = turningPoint,
                            color = self.color,
                            gameArea = self.gameArea
                            )
                        )
        return blocks

    def rotate(self):
        shift_x = []
        shift_y = []
        for block in self.shape:
            s_x, s_y = block.canRotate()
            shift_x.append(s_x)
            shift_y.append(s_y)
        # get the absolute maximum shift but keep the sign
        if max(shift_x) == 0:
            shift_x = min(shift_x)
        else:
            shift_x = max(shift_x)
        
        if max(shift_y) == 0:
            shift_y = min(shift_y)
        else:
            shift_y = max(shift_y)
            
        for block in self.shape:
            block.rotate(shift_x, shift_y)