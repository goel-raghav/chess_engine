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
from piece import get_king_saftey
from piece import get_move_amount

np.set_printoptions(threshold=sys.maxsize)

network = NeuralNetwork()
network.load_state_dict(torch.load("test_model_weights1"))
network.eval()

sample_input = torch.rand(1, 1, 8, 8)
torch.jit.enable_onednn_fusion(True)
traced_model = torch.jit.trace(network, sample_input)
traced_model = torch.jit.freeze(traced_model)
traced_model(sample_input)
traced_model(sample_input)

import chess.pgn
import numpy as np

board = Board()
board.push(Move.from_uci("e2e3"))
board.push(Move.from_uci("c7c6"))
board.push(Move.from_uci("d1h5"))
# board.push(Move.from_uci("d7d6"))
# board.push(Move.from_uci("d2d3"))
board.push(Move.from_uci("d8a5"))
board.push(Move.from_uci("h5a5"))



print(board)

t = perf_counter()
x = board.knights
t2 = perf_counter()
