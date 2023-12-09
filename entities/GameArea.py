import pygame

from constants import BLOCKSIZE

class GameArea:
    def __init__(self, width, height, screen):
        screen_width, screen_height = screen.get_size()
        self.x = (screen_width - width * BLOCKSIZE) / 2
        self.y = (screen_height - height * BLOCKSIZE) / 2
        self.width = width * BLOCKSIZE
        self.height = height * BLOCKSIZE
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height), 1)