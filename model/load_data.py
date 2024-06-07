import torch
import numpy as np
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split


def load_data(batch_size):
    with np.load("model/data/10000.npz") as data:
        print(data["x"].shape)
        x = data['x'].reshape(-1, 1, 8, 8) 
        y = data['y'].reshape(-1, 1)
        r = data['result'].reshape(-1, 1)

    y[y >= 10_000] = y[y < 10_000].max()
    y[y <= -10_000] = y[y > -10_000].min()


    y = torch.sigmoid(0.00295567 * torch.from_numpy(y) + 0.10348419).to(torch.float32)
    y = np.hstack((y, r))
    y = torch.from_numpy(y).to(torch.float32)

    x = torch.from_numpy(x).to(torch.float32)

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size= .1)

    print(X_train.shape, y_train.shape)

    data = TensorDataset(X_train, y_train)
    dataloader = DataLoader(data, batch_size=batch_size, shuffle=True)

    test_data = TensorDataset(X_test, y_test)
    test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=True)

    return dataloader, test_dataloader

if __name__ == "__main__":
    load_data(128)