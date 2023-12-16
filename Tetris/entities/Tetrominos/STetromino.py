from Tetris.entities import BaseTetromino

class STetromino(BaseTetromino):

    color = (7, 240, 1)  # Green color
    turningPoint = (1.5, 1.5)
    
    def __init__(self, gameArea, x, y):
        super().__init__(
                shape=[
                    [0, 1, 1],
                    [1, 1, 0],
                ],
                turningPoint=self.turningPoint,
                color=self.color,
                gameArea=gameArea,
                x=x,
                y=y
            )