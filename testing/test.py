import chess
# from encode import transform_fen
# from encode import encode
from chess import Move
from chess import Board
import numpy as np
import sys
from time import perf_counter

np.set_printoptions(threshold=sys.maxsize)

import chess.pgn
import numpy as np

def encode(board: Board):
    matrix = np.zeros((1, 8, 8), dtype=np.float16)

    piece_val = {"P": 11, "B": 31, "N": 32, "R": 54, "Q": 95,"K": 100,
                "p": -11, "b": -31, "n": -32, "r": -54, "q": -95, "k": -100}

    pieces = board.piece_map()

    for piece in pieces:
        matrix[0][-(piece // 8) + 7][piece % 8] = piece_val[pieces[piece].symbol()] * .01
    
    if board.turn == chess.BLACK:
        matrix *= -1

    return matrix

def transform_fen(fen):
    piece_val = {"P": 11, "B": 31, "N": 32, "R": 54, "Q": 95,"K": 100,
                "p": -11, "b": -31, "n": -32, "r": -54, "q": -95, "k": -100}
    matrix = []
    pos, col_to_move = fen.split(" ")[:2]
    for char in pos:
        if char == "/":
            continue
        elif char.isnumeric():
            matrix += [0] * int(char)
        else:
            matrix.append(piece_val[char] * .01)
    
    matrix = np.array(matrix, dtype=np.float16).reshape(1, 8, 8)
    if col_to_move == "b":
        matrix *= -1
    
    return matrix

#--------------------
# open downloaded games
#----------------------
pgn = open("data/master_games.pgn")
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

t1 = perf_counter()
x = transform_fen(board.fen())
t2 = perf_counter()
print(t2 - t1)

print(x)

t1 = perf_counter()
y = encode(board)
t2 = perf_counter()
print(t2 - t1)

print(y)

print(board)
# print(transform_fen(board.fen()))

t1 = perf_counter()
y = board.piece_map()
t2 = perf_counter()
print(t2 - t1)