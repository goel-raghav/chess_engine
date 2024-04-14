import numpy as np
from model.classic_eval import eval
import pickle
from encode import Encoder


# opens filtered games
with open("games.pickle", "rb") as file:
    games = pickle.load(file)

print("LOADED GAMES")


x = []
y = []
encoder = Encoder()
    
MIN_MOVES = 2
c = 0

for game in games:
    c += 1
    board = game.board()
    moves = list(game.mainline_moves())
    game_length = len(moves)

    for i, move in enumerate(moves):
        board.push(move)
        if (i > MIN_MOVES):
            x.append(encoder.encode(board))
            y.append(eval(board))

    if c % 1000 == 0:
        print("Game number:", c, "of", len(games))

np.savez("model/data/pickled_test_data", x=x, y=y)