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
print("FIX SEARCH THING BEFORE DOING THIS")

DATA_LENGTH = 49000
games = games[:DATA_LENGTH]
x = []
y = []
result = []
encoder = Encoder()
    
MIN_MOVES = 5
c = 0
total_time = 0

for game in games:
    game_start = perf_counter()
    c += 1
    board = game.board()
    moves = list(game.mainline_moves())
    game_length = len(moves)

    headers = game.headers

    end =  headers["Result"]
    r = 0.5
    if end == "0-1":
        r = -1
    elif end == "1-0":
        r = 1

    for i, move in enumerate(moves):
        board.push(move)
        if (i > MIN_MOVES):
            x.append(encoder.encode(board))


            
            if board.turn == chess.BLACK:
                score, _ = searcher.nmax(board, 2, -1, -inf, inf)
                y.append(-score)
            
                result.append(r)

            else:
                score, _ = searcher.nmax(board, 2, 1, -inf, inf)
                y.append(score)

                result.append(r)
    game_end = perf_counter()
    total_time += game_end - game_start

    if c % 1 == 0:
        print("Game number:", c, "of", len(games))
        average_time = total_time / c
        print("Estimated time left", (average_time * (DATA_LENGTH - c)) / 3600) 


print(result.count(1))
print(result.count(-1))
np.savez("model/data/megadepth2", x=x, y=y, result=result)