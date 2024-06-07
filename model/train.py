import torch
from torch import nn
from small_model import NeuralNetwork
from load_data import load_data
from loss_fn import loss_fn
import math


model = NeuralNetwork().cuda()

batch_size = 128
learning_rate = 1e-2
epochs = 200

dataloader, test_dataloader = load_data(batch_size)
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    # Set the model to training mode - important for batch normalization and dropout layers
    # Unnecessary in this situation but added for best practices
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        # Compute prediction and loss
        pred = model(X.cuda())
        loss = loss_fn(pred, y.cuda(), .9)

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
            test_loss += loss_fn(pred, y.cuda(), .9).item()
            
            
    test_loss /= num_batches
    print("Test_loss", math.sqrt(test_loss))
    return test_loss

if __name__ == "__main__":
    prev_loss = []
    best = 0
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train_loop(dataloader, model, loss_fn, optimizer)
        curr = test_loop(test_dataloader, model, loss_fn)
        prev_loss.append(curr)
        torch.save(model.state_dict(), "weights/new")

        if prev_loss[best] < curr:
             if len(prev_loss) - best - 1 >= 7:
                 break
        else:
            best = len(prev_loss) - 1
    print(prev_loss)
    print("Done!")

    