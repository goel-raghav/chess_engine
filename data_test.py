import numpy as np
import pickle
import chess
from math import inf
from time import perf_counter
from chess import WHITE, BLACK

from encode import Encoder
from sorter import Sorter
from model.classic_eval import eval
from transposition_table import Table
from search import Searcher

table = Table()
sorter = Sorter()
searcher = Searcher(eval, sorter, table)


board = chess.Board('r1bqkbnr/1pp2ppp/p1n5/4p3/3pP2P/P2P1PP1/1PP5/RNBQKBNR b KQkq - 0 6')

time = 0
iterations = 1000

print(bin(board.occupied_co[WHITE]))
print(board.piece_map())


start = perf_counter()
for i in range(iterations):
    t2 = perf_counter()
    # x = searcher.nmax(board, 2, -1, -inf, inf)
    x = eval(board)
    t1 = perf_counter()

    time += t1 - t2
end = perf_counter()

print(board)
print(x)

print(end - start)
print(time / iterations)