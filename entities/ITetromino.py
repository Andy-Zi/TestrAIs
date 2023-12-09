from entities import BaseTetromino

class ITetromino(BaseTetromino):

    color = (0, 255, 255)  # Cyan color
    turningPoint = (2,1)
    
    def __init__(self, gameArea):
        super().__init__(
                [
                    [1, 1, 1, 1]
                ],
                self.turningPoint,
                self.color,
                gameArea
            )