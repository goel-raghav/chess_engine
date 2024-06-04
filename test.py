from engine.engine import Engine
from model.small_model import NeuralNetwork as nn
from model.classic_eval import eval
import chess
import chess.pgn
import torch

from engine.encode import Encoder
from engine.sorter import Sorter
from engine.transposition_table import Table
from engine.search import Searcher

from math import inf

table = Table()
sorter = Sorter()
searcher = Searcher(eval, sorter, table, False)

weights = "weights/new"

engine = Engine(nn, weights, qsearch=False)

board = chess.Board("r1bqk2r/ppp1bppp/7n/2nN4/3P4/3BP3/PP3PPP/R2QK1NR w KQkq - 1 10")

print(board)
# print(engine.evaluator.evaluate(board))

score, _ = searcher.nmax(board, 2, -inf, inf)
print(_)

print(torch.sigmoid(torch.tensor(0.00328782 * score + 0.11215524)))

# random = chess.Board("r1bqk2r/ppp1bppp/7n/2PN4/8/3BP3/PP3PPP/R2QK1NR b KQkq - 0 10")

# score, _ = searcher.nmax(random, 1, -inf, inf)
# print(score, _)

# print(torch.sigmoid(torch.tensor(0.00328782 * eval(random) + 0.11215524)))

random = chess.Board("r1b1k2r/ppp1bppp/7n/2Pq4/8/3BP3/PP3PPP/R2QK1NR w KQkq - 0 11")
print(eval(random))