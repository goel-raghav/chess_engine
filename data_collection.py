import numpy as np
import pickle
import chess
from math import inf

from encode import Encoder
from sorter import Sorter
from model.classic_eval import eval
from transposition_table import Table
from search import Searcher

table = Table()
sorter = Sorter()
searcher = Searcher(eval, sorter, table)

# opens filtered games
with open("games.pickle", "rb") as file:
    games = pickle.load(file)

print(len(games))
print("LOADED GAMES")

games = games[:1500]
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
            
            if board.turn == chess.BLACK:
                score, _ = searcher.nmax(board, 2, -1, -inf, inf)
                y.append(-score)
            else:
                score, _ = searcher.nmax(board, 2, 1, -inf, inf)
                y.append(score)

    if c % 1 == 0:
        print("Game number:", c, "of", len(games))

np.savez("model/data/centi_depth2_data", x=x, y=y)