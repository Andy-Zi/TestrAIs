from entities import BaseBlock

class J_Block(BaseBlock):

    color = (0, 0, 255)
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape = [
            [1, 0, 0],
            [1, 1, 1]
        ]
        self.rotation = 0