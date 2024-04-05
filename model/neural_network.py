from torch import nn
import torch

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(1, 64, 3, padding="same"),
            nn.ReLU(),
            nn.Dropout(.1),
            nn.Conv2d(64, 64, 3, padding="same"),
            nn.ReLU(),
            nn.Dropout(.1),
            nn.Conv2d(64, 64, 5),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(1024, 256),
            nn.ReLU(),
            nn.Dropout(.3),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Dropout(.3),
            nn.Linear(256, 1),
            nn.Tanh()
        )

    def forward(self, x):
        logits = self.layers(x)
        return logits