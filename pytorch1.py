import torch
import numpy as np
from sklearn import preprocessing
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from torch import nn

print("CUDA AVAILABLE", torch.cuda.is_available())

with np.load("data_elo_transform_board.npz") as data:
    x = data['x'].reshape(-1, 1, 8, 8)
    y = data['y'].reshape(-1, 1)

y = preprocessing.normalize(y)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size= .1)


X_train = torch.tensor(X_train).to(torch.float32)
y_train = torch.tensor(y_train).to(torch.float32)
X_test = torch.tensor(X_test).to(torch.float32)
y_test = torch.tensor(y_test).to(torch.float32)

print(X_train.dtype)
print(y_train.dtype)

data = TensorDataset(X_train, y_train)
dataloader = DataLoader(data, batch_size=256)

test_data = TensorDataset(X_test, y_test)
test_dataloader = DataLoader(test_data, batch_size=256)

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
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


model = NeuralNetwork().cuda()

learning_rate = 1e-3
batch_size = 256
epochs = 30

loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    # Set the model to training mode - important for batch normalization and dropout layers
    # Unnecessary in this situation but added for best practices
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        # Compute prediction and loss
        pred = model(X.cuda())
        loss = loss_fn(pred, y.cuda())

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * batch_size + len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test_loop(dataloader, model, loss_fn):
    # Set the model to evaluation mode - important for batch normalization and dropout layers
    # Unnecessary in this situation but added for best practices
    model.eval()
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    # Evaluating the model with torch.no_grad() ensures that no gradients are computed during test mode
    # also serves to reduce unnecessary gradient computations and memory usage for tensors with requires_grad=True
    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X.cuda())
            test_loss += loss_fn(pred, y.cuda()).item()
            
            
    test_loss /= num_batches
    print("Test_loss", test_loss)

if __name__ == "__main__":
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train_loop(dataloader, model, loss_fn, optimizer)
        test_loop(test_dataloader, model, loss_fn)
    print("Done!")

    torch.save(model, "model.pth")
    torch.save(model.state_dict(), "model_weights")