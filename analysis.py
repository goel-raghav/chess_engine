import matplotlib.pyplot as plt
import numpy as np
from torch import sigmoid, from_numpy
import pickle

with np.load("model/data/table_depth2.npz") as data:
    x = data['x'].reshape(-1, 1, 8, 8) 
    y = data['y'].reshape(-1, 1)

print(x[y == 0][0])
# plt.scatter(y, sigmoid(from_numpy(y) / 600))
# plt.show()