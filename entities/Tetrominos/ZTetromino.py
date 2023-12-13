from entities import BaseTetromino

class ZTetromino(BaseTetromino):

    color = (240, 0, 1)  # Red color
    turningPoint = (1.5,1.5)
    
    def __init__(self, gameArea, x, y):
        super().__init__(
                shape=[
                    [1, 1, 0],
                    [0, 1, 1],
                ],
                turningPoint=self.turningPoint,
                color=self.color,
                gameArea=gameArea,
                x=x,
                y=y
            )