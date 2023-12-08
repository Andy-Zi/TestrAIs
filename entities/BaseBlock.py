import pygame

class BaseBlock(pygame.Rect):

    borderWidth = 5
    width = 50
    height = 50
    bordercolor = (0, 0, 0)
    
    def __init__(self, x, y, color):
        super().__init__(x, y, self.width, self.height)
        self.x = x
        self.y = y
        self.color = color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.bordercolor, (self.x, self.y, self.width, self.height), self.borderWidth)
        pygame.draw.rect(screen, self.color, (self.x + self.borderWidth, self.y + self.borderWidth, self.width - self.borderWidth * 2, self.height - self.borderWidth * 2))

    def move(self, x, y):
        self.x += x
        self.y += y
    