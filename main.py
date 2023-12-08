import pygame

from entities import BaseBlock 

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

color = (255, 255, 255)

player = BaseBlock(100, 100, color)

run = True

while run:

    screen.fill((0, 255, 0))

    player.draw(screen)

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-1, 0)
    if key[pygame.K_RIGHT]:
        player.move(1, 0)
    if key[pygame.K_UP]:
        player.move(0, -1)
    if key[pygame.K_DOWN]:
        player.move(0, 1)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()
