from entities import BaseTetromino

class LTetromino(BaseTetromino):

    color = (240, 159, 3)  # Orange color
    turningPoint = (1.5, 1.5)
    
    def __init__(self, gameArea, x ,y):
        super().__init__(
                shape=[
                    [0, 0, 1],
                    [1, 1, 1],
                ],
                turningPoint=self.turningPoint,
                color=self.color,
                gameArea=gameArea,
                x=x,
                y=y
            )