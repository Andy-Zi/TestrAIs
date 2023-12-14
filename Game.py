import time
import pygame
import random
import sys

from entities import GameArea
from entities import ITetromino, ZTetromino, OTetromino, STetromino, JTetromino, LTetromino, TTetromino

MOVE_DOWN_EVENT = pygame.USEREVENT + 1

class Game:

    def __init__(
        self,
        screen_width: int = 600,
        screen_height: int = 1200,
        ) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Tetris')
        self.gameArea = GameArea(10, 20, self.screen)
        self.staging_x = self.gameArea.x + self.gameArea.width + 80
        self.staging_y = self.gameArea.y + 50
        self.next_tetromino = self.get_random_tetromino()
        self.active_tetromino = None
        self.playing = True
        pygame.time.set_timer(MOVE_DOWN_EVENT, 1000)  # 1000 milliseconds = 1 second
        self.clock = pygame.time.Clock()
        self.key_last_pressed = {pygame.K_UP: 0, pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_DOWN: 0}
    
    def play(self):
        self.start()
        # Game loop
        while True:
            # calculate the frame rate
            self.clock.tick(30)

            keys = pygame.key.get_pressed()
            current_time = time.time()

            for key in [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]:
                if keys[key] and current_time - self.key_last_pressed[key] > 0.3:
                    self.handle_keypressed(key)
                    self.key_last_pressed[key] = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOVE_DOWN_EVENT:
                        if self.active_tetromino.move_down():
                            if not self.gameArea.addBlocks(self.active_tetromino.shape):
                                self.gameOver()
                            self.gameArea.checkRows()
                            self.spawnTetromino()
                        self.updateScreen()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN]:
                        self.handle_keypressed(event.key)
                        self.key_last_pressed[event.key] = current_time
                    if event.key == pygame.K_UP:
                        self.active_tetromino.rotate()
                        self.updateScreen()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                if self.active_tetromino.move_down():
                    if not self.gameArea.addBlocks(self.active_tetromino.shape):
                        self.gameOver()
                    self.gameArea.checkRows()
                    self.spawnTetromino()
                self.updateScreen()
            self.updateScreen()
        
        
    def handle_keypressed(self,key):
        if key == pygame.K_LEFT:
            self.active_tetromino.move_left()
            self.updateScreen()
        if key == pygame.K_RIGHT:
            self.active_tetromino.move_right()
            self.updateScreen()
    
    def updateScreen(self):
        self.screen.fill((128, 128, 128))
        self.gameArea.draw(self.screen)
        self.active_tetromino.draw(self.screen)
        self.next_tetromino.draw(self.screen)
        pygame.display.flip()
    
    def spawnTetromino(self):
        self.active_tetromino = self.next_tetromino
        self.next_tetromino = self.get_random_tetromino()
        self.active_tetromino.move_to_starting_position()
    
    def get_random_tetromino(self):
        tetrominos = [ITetromino, ZTetromino, OTetromino, STetromino, JTetromino, LTetromino, TTetromino]
        return random.choice(tetrominos)(self.gameArea, self.staging_x, self.staging_y)
    
    def start(self):
        self.spawnTetromino()
        self.updateScreen()
    
    def restart(self):
        self.gameArea.clear()
        self.next_tetromino = self.get_random_tetromino()
        self.active_tetromino = None
        self.playing = True
        self.start()
    
    def gameOver(self):
        self.updateScreen()
        self.playing = False
        self.score = 42069

        # Set up the font and color for text
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)  # white

        # Render the text
        game_over_text = font.render('Game Over', True, text_color)
        score_text = font.render(f'Score: {self.score}', True, text_color)
        play_again_text = font.render('Play Again', True, text_color)
        quit_text = font.render('Quit', True, text_color)

        # Position the text
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        score_rect = score_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 50))
        play_again_rect = play_again_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 100))
        quit_rect = quit_text.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 150))

        # Draw the text on the screen
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(play_again_text, play_again_rect)
        self.screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        # Wait for user input
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_again_rect.collidepoint(mouse_pos):
                        self.restart()
                    elif quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
    