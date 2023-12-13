from entities import BaseTetromino

class ITetromino(BaseTetromino):

    color = (7, 240, 240) # Cyan color
    turningPoint = (1,2)
    
    def __init__(self, gameArea, x, y):
        super().__init__(
                shape=[
                    [1],
                    [1],
                    [1],
                    [1]
                ],
                turningPoint=self.turningPoint,
                color=self.color,
                gameArea=gameArea,
                x=x,
                y=y
            )