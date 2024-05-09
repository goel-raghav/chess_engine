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

evaluator = Evaluator(NeuralNetwork, "T15000depth2_weights", encoder.encode)

board = Board("rnbk1b1r/pp1pp1pp/5n2/2p2p2/3P4/8/PPP1PPPP/RN1QKBNR w KQ - 0 5")
searcher = Searcher(eval, sorter, table)

board.push_uci("a5d8")
print(board)

print(evaluator.evaluate(board))

score, best_line = searcher.nmax(board, 2, 1, -inf, inf)
print(sigmoid(tensor(score) / 600))
