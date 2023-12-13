from entities import BaseTetromino

class OTetromino(BaseTetromino):

    color = (240, 240, 1)  # Yellow color
    turningPoint = (1,1)
    
    def __init__(self, gameArea,x ,y):
        super().__init__(
                shape=[
                    [1, 1],
                    [1, 1],
                ],
                turningPoint=self.turningPoint,
                color=self.color,
                gameArea=gameArea,
                x=x,
                y=y
            )