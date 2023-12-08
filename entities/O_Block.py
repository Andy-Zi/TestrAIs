from entities import BaseBlock

class O_Block(BaseBlock):

    color = (255, 255, 0)
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.shape = [
            [1, 1],
            [1, 1]
        ]
        self.rotation = 0