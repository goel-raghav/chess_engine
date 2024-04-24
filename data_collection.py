import numpy as np
import pickle
import chess
from math import inf
from time import perf_counter

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

print("FIX CHECKMATES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

DATA_LENGTH = 1500
games = games[:DATA_LENGTH]
x = []
y = []
encoder = Encoder()
    
MIN_MOVES = 2
c = 0
total_time = 0

for game in games:
    game_start = perf_counter()
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
    game_end = perf_counter()
    total_time += game_end - game_start

    if c % 1 == 0:
        print("Game number:", c, "of", len(games))
        average_time = total_time / c
        print("Estimated time left", average_time * (DATA_LENGTH - c))

np.savez("model/data/table_depth2", x=x, y=y)