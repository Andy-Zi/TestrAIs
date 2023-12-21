from copy import deepcopy
from Agent.helper import plot
from Model.Linear_QNet import Linear_QNet, QTrainer
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
        input_size = self.get_state(game).shape[0]
        self.model = Linear_QNet(input_size, 256, 5).to(device)
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
        gameAreaMatrix_flat = gameAreaMatrix.flatten()
        gameAreaMatrix_flat = gameAreaMatrix_flat.reshape(1, -1)
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

        # create the state
        return np.concatenate((gameAreaMatrix_flat, active_tetromino, next_tetromino, score, goodness), axis=1)[0]
    
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
            prediction = self.model(state0)
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
        state_old = agent.get_state(game)
        
        final_move = agent.get_action(state_old)
        
        reward, done, score = game.play_ai(final_move)
        
        state_new = agent.get_state(game)
        
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

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