from torch import nn
import torch

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding="same"),
            nn.ReLU(),
            nn.Dropout(.1),
            nn.Flatten(),
            nn.Linear(1024, 64),
            nn.ReLU(),
            nn.Dropout(.3),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Dropout(.3),
            nn.Linear(64, 1),
        )

    def forward(self, x):
        logits = self.layers(x)
        return logits