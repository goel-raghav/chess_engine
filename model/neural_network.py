from torch import nn

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(12, 256, 3, padding="same"),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.Dropout(.1),
            nn.Conv2d(256, 256, 3, padding="same"),
            nn.ReLU(),
            nn.BatchNorm2d(256),
            nn.Dropout(.1),
            nn.Conv2d(256, 64, 5),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.Flatten(),
            nn.Linear(1024, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(.3),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(.3),
            nn.Linear(64, 1),
        )

    def forward(self, x):
        logits = self.layers(x)
        return logits