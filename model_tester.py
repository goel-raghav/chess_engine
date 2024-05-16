from evaluator import Evaluator
from model.small_model import NeuralNetwork
from encode import Encoder
from chess import Board
from model.classic_eval import eval
from search import Searcher
from transposition_table import Table
from sorter import Sorter
from torch import sigmoid, tensor
from math import inf

table = Table()
sorter = Sorter()

encoder = Encoder()

evaluator = Evaluator(NeuralNetwork, "megadepth2_weights", encoder.encode)

board = Board("rn3rk1/pppqppbp/6p1/7n/2BPP1b1/2N1BN2/PP3PPP/2RQK2R w K - 3 10")
classic_searcher = Searcher(eval, sorter, table)
nn_searcher = Searcher(evaluator.evaluate, sorter, table)

print(board)
board.push_uci("f3e5")


score, best_line = classic_searcher.nmax(board, 1, 1, -inf, inf)
nn_score, nn_best_line = nn_searcher.nmax(board, 1, 1, -inf, inf)

print("classic", best_line[0])
print(score)
print()
print("nn", nn_best_line)
print(nn_score)

board.push(nn_best_line[0])
print(board)