from entities import BaseBlock

class T_Block(BaseBlock):
    
    color = (255, 0, 255)
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape = [
            [1, 1, 1],
            [0, 1, 0]
        ]
        self.rotation = 0