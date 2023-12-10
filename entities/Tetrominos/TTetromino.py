from entities import BaseTetromino

class TTetromino(BaseTetromino):

    color = (160, 0, 240) # Purple color
    turningPoint = (2,1)
    
    def __init__(self, gameArea):
        super().__init__(
                shape=[
                    [0, 1, 0],
                    [1, 1, 1],
                ],
                turningPoint=self.turningPoint,
                color=self.color,
                gameArea=gameArea
            )