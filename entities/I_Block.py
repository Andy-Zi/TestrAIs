from entities import BaseBlock

class I_Block(BaseBlock):

    color = (0, 255, 255)
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape = [
            [1, 1, 1, 1]
        ]
        self.rotation = 0