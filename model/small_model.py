from torch import nn
import torch
from torch.ao.quantization import QuantStub, DeQuantStub

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1),
            nn.ReLU(),
            nn.Dropout(.05),
            nn.Flatten(),
            nn.Linear(1024, 64),
            nn.ReLU(),
            nn.Dropout(.1),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Dropout(.1),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.layers(x)
        return x