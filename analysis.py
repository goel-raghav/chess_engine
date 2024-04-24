import matplotlib.pyplot as plt
import numpy as np
from torch import sigmoid, from_numpy
import pickle

# with np.load("model/data/table_depth2.npz") as data:
#     x = data['x'].reshape(-1, 1, 8, 8) 
#     y = data['y'].reshape(-1, 1)

# with open("games.pickle", "rb") as file:
#     games = pickle.load(file)

# black_elo = []
# white_elo = []
# for i in range(1500):
#     game = games[i]
#     headers = game.headers

#     white_elo.append(int(headers["WhiteElo"]))
#     black_elo.append(int(headers["BlackElo"]))

# index = range(1500)

fig, ax = plt.subplots()
# ax.set_facecolor("black")
# ax.scatter(index, white_elo, color="white", label="White Elo", marker="x")
# ax.scatter(index, black_elo, color="darkgoldenrod", label="Black Elo", marker="x")
# ax.set_xlabel("Game Number")
# ax.set_ylabel("Elo")
# ax.set_title("Elo of Dataset")
# ax.legend()

loss = [0.029805292703316246, 0.01535958595390261, 0.013557804741857337, 0.013705773744732141, 0.012775192434020656, 0.012772257331575096, 0.012367449989411193, 0.012760208814706601, 0.012133675502796828, 0.011908680276000793, 0.012222058916936668, 0.011883309989852804, 0.01124087101648706, 0.011203279777784163, 0.011009168463536131, 0.011191091172292198, 0.010842864306538667, 0.01123932186468229, 0.010807021658762659, 0.011041701264666314, 0.01061110184724692, 0.01059331812954862, 0.010755450782877669, 0.010316831538532401, 0.010788032762102887, 0.01030533811287351, 0.010542399302439791, 0.010502938605831857, 0.010496104680473956, 0.010320932676517208, 0.010321213417804577]
ax.plot(range(1, len(loss)+1), loss)
ax.set_title("Test Loss over Time")
ax.set_xlabel("Epoch")
ax.set_ylabel("MSE Loss")
plt.show()