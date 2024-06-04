import matplotlib.pyplot as plt
import numpy as np
from torch import sigmoid, from_numpy
import pickle
from scipy.optimize import curve_fit

def sigmoid(x, a, b):
    return np.ravel(1 / (1 + np.exp(-(a * x + b))))

with np.load("model/data/10000.npz") as data:
    x = data['x'].reshape(-1, 1, 8, 8)[:100000]
    y = data['y'].reshape(-1, 1)[:100000]
    result = data["result"][:100000]

y[y >= 10_000] = y[y < 10_000].max()
y[y <= -10_000] = y[y > -10_000].min()

y = np.ravel(y)

# print(sigmoid(y, 10, 10))

p = curve_fit(sigmoid, y, result)
print(p)


# print(x[(y<-1000) & (result==1)][0])

plt.scatter(y, result)
plt.scatter(y, sigmoid(y, p[0][0], p[0][1]))
plt.show()