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
from model.nn_eval import get_king_saftey
from model.nn_eval import get_move_amount
from model.nn_eval import get_piece_eval
from chess.polyglot import zobrist_hash
from evaluator import Evaluator
from encode import Encoder
import numba
import model.small_model
import os


encoder = Encoder()



import chess.pgn
import numpy as np

board = Board()
board.push(Move.from_uci("e2e3"))
x = encoder.encode(board)
print(x)
board.push(Move.from_uci("c7c6"))
encoder.update(x, board.peek().from_square, board.peek().to_square, board.piece_at(board.peek().to_square))
print(x)
board.push(Move.from_uci("d1h5"))
encoder.update(x, board.peek().from_square, board.peek().to_square, board.piece_at(board.peek().to_square))
print(x)
board.push(Move.from_uci("d7d6"))
encoder.update(x, board.peek().from_square, board.peek().to_square, board.piece_at(board.peek().to_square))
print(x)
board.push(Move.from_uci("d2d3"))
encoder.update(x, board.peek().from_square, board.peek().to_square, board.piece_at(board.peek().to_square))
print(x)
board.push(Move.from_uci("d8a5"))
encoder.update(x, board.peek().from_square, board.peek().to_square, board.piece_at(board.peek().to_square))
print(x)
board.push(Move.from_uci("a2a3"))
encoder.update(x, board.peek().from_square, board.peek().to_square, board.piece_at(board.peek().to_square))
print(x)
board.push(Move.from_uci("a5h5"))

print(board)