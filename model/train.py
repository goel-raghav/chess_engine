import torch
import numpy as np
from sklearn import preprocessing
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from torch import nn
from math import inf

from small_model import NeuralNetwork

print("CUDA AVAILABLE", torch.cuda.is_available())

model = NeuralNetwork().cuda()

batch_size = 64
learning_rate = 1e-4
epochs = 200

with np.load("model/data/table_depth2.npz") as data:
    print(data["x"].shape)
    x = data['x'].reshape(-1, 1, 8, 8) 
    y = data['y'].reshape(-1, 1)

print(x.shape)
print(y.shape)


y[y == inf] = y[y != inf].max()
y[y == -inf] = y[y != -inf].min()
y = torch.sigmoid(torch.from_numpy(y) / 400)


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size= .1)






X_train = torch.tensor(X_train).to(torch.float32)
y_train = torch.tensor(y_train).to(torch.float32)
X_test = torch.tensor(X_test).to(torch.float32)
y_test = torch.tensor(y_test).to(torch.float32)

print(len(X_train))

data = TensorDataset(X_train, y_train)
dataloader = DataLoader(data, batch_size=batch_size, shuffle=True)

test_data = TensorDataset(X_test, y_test)
test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=True)

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

        if batch % 1000 == 0:
            loss, current = loss.item(), batch * batch_size + len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test_loop(dataloader, model, loss_fn):
    # Set the model to evaluation mode - important for batch normalization and dropout layers
    # Unnecessary in this situation but added for best practices
    model.eval()
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss = 0

    # Evaluating the model with torch.no_grad() ensures that no gradients are computed during test mode
    # also serves to reduce unnecessary gradient computations and memory usage for tensors with requires_grad=True
    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X.cuda())
            test_loss += loss_fn(pred, y.cuda()).item()
            
            
    test_loss /= num_batches
    print("Test_loss", test_loss)
    return test_loss

if __name__ == "__main__":
    prev_loss = []
    best = 0
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train_loop(dataloader, model, loss_fn, optimizer)
        curr = test_loop(test_dataloader, model, loss_fn)
        prev_loss.append(curr)
        torch.save(model.state_dict(), "Tdepth2_weights")

        if prev_loss[best] < curr:
             if len(prev_loss) - best - 1 >= 5:
                 break
        else:
            best = len(prev_loss) - 1
    print(prev_loss)
    print("Done!")

    