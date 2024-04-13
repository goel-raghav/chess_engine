import chess
# from encode import transform_fen
# from encode import encode
from chess import Move
from chess import Board
import numpy as np
import sys
from time import perf_counter
from model.neural_network import NeuralNetwork
import torch
from encode import encode
from model.nn_eval import get_king_saftey
from model.nn_eval import get_move_amount
from model.nn_eval import get_piece_eval
from chess.polyglot import zobrist_hash
from evaluator import Evaluator
from encode import encode
import numba

evaluator = Evaluator(NeuralNetwork, "test_model_weights", encode)

np.set_printoptions(threshold=sys.maxsize)

network = NeuralNetwork()
network.load_state_dict(torch.load("test_model_weights1"))
network.eval()

sample_input = torch.rand(1, 1, 8, 8)
traced_model = torch.jit.trace(network, sample_input)

import chess.pgn
import numpy as np

board = Board()
board.push(Move.from_uci("e2e3"))
board.push(Move.from_uci("c7c6"))
board.push(Move.from_uci("d1h5"))
board.push(Move.from_uci("d7d6"))
board.push(Move.from_uci("d2d3"))
board.push(Move.from_uci("d8a5"))
board.push(Move.from_uci("a2a3"))
board.push(Move.from_uci("a5h5"))



print(board)

def test(b):
    l = []
    for i in range(64):
        if b >> i & 1:
            l.append(i)
    return l

s = 0
for i in range(1000):
    t = perf_counter()
    l = encode(board)    
    t2 = perf_counter()
    s += t2 - t
print(s / 1000)


# print(encode(board.piece_map(), 1))

print(get_king_saftey(board) + get_piece_eval(board) + get_move_amount(board))