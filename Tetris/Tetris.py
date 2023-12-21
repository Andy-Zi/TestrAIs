import time
import pygame
import random
import sys

from Tetris.entities import GameArea, MovementHandler
from Tetris.entities import ITetromino, ZTetromino, OTetromino, STetromino, JTetromino, LTetromino, TTetromino

from Tetris.events import *
class Tetris(MovementHandler):

    def __init__(self, screen_width: int = 600, screen_height: int = 1200) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        gameArea = GameArea(10, 20, self.screen)
        active_tetromino = None
        # initialize the MovementHandler
        super().__init__(gameArea, active_tetromino)

        pygame.display.set_caption('Tetris')
        self.next_tetromino = self.get_random_tetromino()
        self.playing = True
        self.clock = pygame.time.Clock()
        self.level = 1
        self.score = 0
        self.lines_cleared = 0
        self.pevValues = {
            'height': 0,
            'lines': 0,
            'holes': 0,
            'bumpiness': 0,
            'fitness': 0
        }
    
    def play(self):
        while True:
            # start the game
            self.start()
            
            # game loop
            while self.playing:
                # calculate the frame rate
                self.clock.tick(30)

                self.handle_keypressed()
                # handle events
                self.eventHandler()

                self.updateScreen()
            
            self.gameOverScreen()
            
    def start_ai(self):
        self.start()

    def play_ai(self, action):
        
        self.eventHandler()
            
        up, right, down, left, space = action
        
        if up:
            self.rotate()
        if right:
            self.moveRight()
        if down:
            self.moveDown()
        if left:
            self.moveLeft()
        if space:
            self.hardDrop()

        self.eventHandler()

        reward = self.fitness_func()
    
        # update the game state
        self.updateScreen()

        # return the reward, done, score
        done = not self.playing
        score = self.score
        self.clock.tick(30)
        return reward, done, score

    def fitness_func(self):
        height = self.gameArea.highest_column()
        prev_height = self.pevValues['height']
        holes = self.gameArea.holes()
        prev_holes = self.pevValues['holes']
        bumpiness = self.gameArea.bumpiness()
        prev_bumpiness = self.pevValues['bumpiness']
        lines = self.lines_cleared
        prev_lines = self.pevValues['lines']
        
        fitness = -0.51 * (height - prev_height) + 0.76 * (lines - prev_lines) - 0.36 * (holes - prev_holes) - 0.18 * (bumpiness - prev_bumpiness)
                
        self.pevValues['height'] = height
        self.pevValues['holes'] = holes
        self.pevValues['bumpiness'] = bumpiness
        self.pevValues['lines'] = lines
        
        return fitness

    def eventHandler(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == MOVE_DOWN_EVENT:
                self.moveDown()
            if event.type == pygame.KEYDOWN:
                self.handleMovement(event.key)
            if event.type == TETROMINO_HIT_SOMETHING:
                self.tetrominoHitSomething()
    
    def tetrominoHitSomething(self):
        if not self.gameArea.addBlocks(self.active_tetromino.shape):
            self.gameOver()
            return
        lines_cleared = self.gameArea.checkRows()
        self.update_score(lines_cleared) 
        self.spawnTetromino()

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
        pygame.time.set_timer(MOVE_DOWN_EVENT, 1000)
    
    def restart(self):
        self.gameArea.clear()
        self.next_tetromino = self.get_random_tetromino()
        self.active_tetromino = None
        self.playing = True

    def update_score(self, lines_cleared):
        self.lines_cleared += lines_cleared
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
        pygame.time.set_timer(MOVE_DOWN_EVENT, 0)

    def gameOverScreen(self):
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
                        return
                    elif quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
    