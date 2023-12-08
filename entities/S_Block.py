from entities import BaseBlock

class S_Block(BaseBlock):
    
    color = (0, 255, 0)
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape = [
            [0, 1, 1],
            [1, 1, 0]
        ]
        self.rotation = 0