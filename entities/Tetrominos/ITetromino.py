from entities import BaseTetromino

class ITetromino(BaseTetromino):

    color = (7, 240, 240) # Cyan color
    turningPoint = (2,1)
    
    def __init__(self, gameArea):
        super().__init__(
                shape=[
                    [1],
                    [1],
                    [1],
                    [1]
                ],
                turningPoint=self.turningPoint,
                color=self.color,
                gameArea=gameArea
            )