import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        
        # features on the game area
        self.linear1 = nn.Linear(4, 32)
        self.linear2 = nn.Linear(32, 64)

        # conv on the game area 20x10
        self.conv1 = nn.Conv2d(1, 32, (4,2))
        # what is the output of the conv1?
        # 20 - 4 + 1 = 17
        # 10 - 2 + 1 = 9
        self.pool = nn.MaxPool2d(2, 2)
        # what is the output of the pool?
        # 17 / 2 = 8
        # 9 / 2 = 4
        self.conv2 = nn.Conv2d(32, 64, (4,2))
        # what is the output of the conv2?
        # 8 - 4 + 1 = 5
        # 4 - 2 + 1 = 3
        

        # fully connected layer
        # 64 * 3 * 5 = 960
        self.fc1 = nn.Linear(192, 128)
        self.fc2 = nn.Linear(128, 5)

    
    def forward(self, area, x):
        # features on the game area
        x1 = F.relu(self.linear1(x))
        x1 = F.relu(self.linear2(x1))
        x1 = x1.reshape(-1, 64)

        # conv on the game area 10 x 20
        x2 = F.relu(self.conv1(area))
        x2 = self.pool(x2)
        x2 = F.relu(self.conv2(x2))
        x2 = self.pool(x2)
        x2 = x2.reshape(-1, 64 * 2)

        # fully connected layer
        x = torch.cat((x1, x2), dim=1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    
    def save(self, file_name='model.pth'):
        model_folder_path = './Model/models'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()
    
    def train_step(self, state_area, state_features, action, reward, next_state_area, next_state_features, done):
        state_area = torch.tensor(state_area, dtype=torch.float).to(device)
        state_features = torch.tensor(state_features, dtype=torch.float).to(device)
        next_state_area = torch.tensor(next_state_area, dtype=torch.float).to(device)
        next_state_features = torch.tensor(next_state_features, dtype=torch.float).to(device)
        action = torch.tensor(action, dtype=torch.long).to(device)
        reward = torch.tensor(reward, dtype=torch.float).to(device)
        
        if len(state_features.shape) == 1:
            # (1, x)
            state_area = torch.unsqueeze(state_area, 0).unsqueeze(0)
            state_features = torch.unsqueeze(state_features, 0)
            next_state_area = torch.unsqueeze(next_state_area, 0).unsqueeze(0)
            next_state_features = torch.unsqueeze(next_state_features, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )
        
        # 1: predicted Q values with current state
        pred = self.model(state_area, state_features)
        
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state_area[idx], next_state_features[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()