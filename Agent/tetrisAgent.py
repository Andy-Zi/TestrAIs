from copy import deepcopy
from Tetris.Tetris import Tetris
from Tetris.entities.Tetrimino import Tetrimino
import torch
import random
from collections import deque
import numpy as np

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
class tetrisAgent():
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = None
        self.trainer = None
    
    def get_state(self, game):
        # Game Area
        gameArea = deepcopy(game.gameArea)
        # add the active tetromino to the game area
        gameArea.addBlocks(game.active_tetromino.blocks)
        # convert the game area from blocks to a matrix of 0s and 1s
        gameAreaMatrix = []
        for row in gameArea.blocks:
            rowMatrix = []
            for block in row:
                if block == None:
                    rowMatrix.append(0)
                else:
                    rowMatrix.append(1)
            gameAreaMatrix.append(rowMatrix)
        gameAreaMatrix = np.array(gameAreaMatrix)
        gameAreaMatrix_flat = gameAreaMatrix.flatten()
        # Active Tetromino
        active_tetromino = np.array(Tetrimino(game.active_tetromino.__class__.__name__), dtype=int)
        # Next Tetromino()
        next_tetromino = np.array(Tetrimino(game.next_tetromino.__class__.__name__), dtype=int)
        # Score
        score = np.array(game.score)
        # goodness of the game area
        goodness = np.array(gameArea.goodness())

        # create the state
        return np.concatenate((gameAreaMatrix_flat, active_tetromino, next_tetromino, score, goodness))
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
    
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 4)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float).to(device)
            prediction = self.model.predict(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
    
def train(self):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = tetrisAgent()
    game = Tetris()
    while True:
        state_old = agent.get_state(game)
        
        final_move = agent.get_action(state_old)
        
        reward, done, score = game.play_step(final_move)
        
        state_new = agent.get_state(game)
        
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                # agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)

if __name__ == "__main__":
    train()