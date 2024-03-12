import chess
from chessfunc import encode_board
from chess import Move
import numpy as np
import sys
from time import perf_counter

np.set_printoptions(threshold=sys.maxsize)

import chess.pgn
import numpy as np
from piece import get_piece_eval

#--------------------
# open downloaded games
#----------------------

pgn = open("master_games.pgn")
game = chess.pgn.read_game(pgn)

print(game.headers)

board = game.board()
moves = game.mainline_moves()
i = 0
for move in moves:
    if i > 6:
        break
    board.push(move)
    i+=1

print(board)

print(encode_board(board))
board.pieces()