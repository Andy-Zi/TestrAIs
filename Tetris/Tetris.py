import time
import pygame
import random
import sys

from Tetris.entities import GameArea, MovementHandler
from Tetris.entities import ITetromino, ZTetromino, OTetromino, STetromino, JTetromino, LTetromino, TTetromino

MOVE_DOWN_EVENT = pygame.USEREVENT + 1

class Tetris(MovementHandler):

    def __init__(self, screen_width: int = 600, screen_height: int = 1200) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        gameArea = GameArea(10, 20, self.screen)
        active_tetromino = None
        # initialize the MovementHandler
        super().__init__(gameArea, active_tetromino)

        pygame.display.set_caption('Tetris')
        self.staging_x = self.gameArea.x + self.gameArea.width + 80
        self.staging_y = self.gameArea.y + 50
        self.next_tetromino = self.get_random_tetromino()
        self.playing = True
        pygame.time.set_timer(MOVE_DOWN_EVENT, 1000)  # 1000 milliseconds = 1 second
        self.clock = pygame.time.Clock()
        self.level = 1
        self.score = 0
    
    def play(self):
        # start the game
        self.start()
        
        # game loop
        while True:
            # calculate the frame rate
            self.clock.tick(30)

            # handle events
            self.eventHandler()

            self.handle_keypressed()

            self.updateScreen()
            
            
    def eventHandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == MOVE_DOWN_EVENT:
                self.moveDown()
            if event.type == pygame.KEYDOWN:
                self.handleMovement(event.key)
    
    def quit(self):
        pygame.quit()
        sys.exit()

    def updateScreen(self):
        self.screen.fill((128, 128, 128))
        self.gameArea.draw(self.screen)
        self.active_tetromino.draw(self.screen)
        self.next_tetromino.draw(self.screen)
        # Draw the score
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(text, (20, 20))  # Adjust the position as needed

        pygame.display.flip()
    
    def spawnTetromino(self):
        self.active_tetromino = self.next_tetromino
        self.next_tetromino = self.get_random_tetromino()
        self.move_tetromino_to_starting_position()
    
    def get_random_tetromino(self):
        tetrominos = [ITetromino, ZTetromino, OTetromino, STetromino, JTetromino, LTetromino, TTetromino]
        return random.choice(tetrominos)(self.gameArea, self.staging_x, self.staging_y)
    
    def start(self):
        self.spawnTetromino()
    
    def restart(self):
        self.gameArea.clear()
        self.next_tetromino = self.get_random_tetromino()
        self.active_tetromino = None
        self.playing = True
        self.start()

    def update_score(self, lines_cleared):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800

    def gameOver(self):
        self.updateScreen()
        self.playing = False

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
    