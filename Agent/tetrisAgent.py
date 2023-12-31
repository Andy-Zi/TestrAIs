from copy import deepcopy
from Agent.helper import plot
from Model.Model import Model, QTrainer
from Tetris.Tetris import Tetris
from Tetris.entities.Tetrimino import Tetrominos
import torch
import random
from collections import deque
import numpy as np

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
class tetrisAgent():
    def __init__(self, game) -> None:
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Model().to(device)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
    def get_state(self, game):
        # Game Area
        gameArea = deepcopy(game.gameArea)
        # add the active tetromino to the game area
        if game.active_tetromino != None:
            gameArea.addBlocks(game.active_tetromino.shape)
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
        # gameAreaMatrix_flat = gameAreaMatrix.flatten()
        # gameAreaMatrix_flat = gameAreaMatrix_flat.reshape(1, -1)
        # Active Tetromino
        if game.active_tetromino != None:
            active_tetromino = np.array(Tetrominos[game.active_tetromino.__class__.__name__].value, dtype=int)
        else:
            active_tetromino = np.array(0)
        active_tetromino = active_tetromino.reshape(1, -1)
        # Next Tetromino()
        if game.next_tetromino != None:
            next_tetromino = np.array(Tetrominos[game.next_tetromino.__class__.__name__].value, dtype=int)
        else:
            next_tetromino = np.array(0)
        next_tetromino = next_tetromino.reshape(1, -1)
        # Score
        score = np.array(game.score)
        score = score.reshape(1, -1)
        # goodness of the game area
        goodness = np.array(gameArea.goodness())
        goodness = goodness.reshape(1, -1)

        features = np.concatenate((active_tetromino, next_tetromino, score, goodness), axis=1)[0]
        return gameAreaMatrix, features
    
    def remember(self, state_area, state_features, action, reward, next_state_area, next_state_features, done):
        self.memory.append((state_area, state_features, action, reward, next_state_area, next_state_features, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        state_area, state_features, action, reward, next_state_area, next_state_features, done = zip(*mini_sample)
        self.trainer.train_step(state_area, state_features, action, reward, next_state_area, next_state_features, done)
        
    
    def train_short_memory(self, state_area, state_features, action, reward, next_state_area, next_state_features, done):
        self.trainer.train_step(state_area, state_features, action, reward, next_state_area, next_state_features, done)
    
    def get_action(self, area, features):
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 4)
            final_move[move] = 1
        else:
            area0 = torch.tensor(area, dtype=torch.float).to(device).unsqueeze(0)
            features0 = torch.tensor(features, dtype=torch.float).to(device).unsqueeze(0)
            prediction = self.model(area0, features0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return np.array(final_move)
    
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    game = Tetris()
    game.start_ai()
    agent = tetrisAgent(game)
    while True:
        state_old_area, state_old_features = agent.get_state(game)
        
        final_move = agent.get_action(state_old_area, state_old_features)
        
        reward, done, score = game.play_ai(final_move)
        
        state_new_area, state_new_features = agent.get_state(game)
        
        agent.train_short_memory(state_old_area, state_old_features, final_move, reward, state_new_area, state_new_features, done)

        agent.remember(state_old_area, state_old_features, final_move, reward, state_new_area, state_new_features, done)

        if done:
            game.restart()
            game.start()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == "__main__":
    train()