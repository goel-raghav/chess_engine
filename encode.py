import numpy as np
from chess import Board
from chess import Move
from chess import BLACK, WHITE
from sklearn import preprocessing


piece_val = {"P": 11, "B": 31, "N": 32, "R": 54, "Q": 95,"K": 100,
                "p": -11, "b": -31, "n": -32, "r": -54, "q": -95, "k": -100}


def transform_fen(fen):
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

def encode(board: Board):
    matrix = np.zeros((1, 8, 8), dtype=np.float16)

    piece_val = {"P": 11, "B": 31, "N": 32, "R": 54, "Q": 95,"K": 100,
                "p": -11, "b": -31, "n": -32, "r": -54, "q": -95, "k": -100}

    pieces = board.piece_map()

    for piece in pieces:
        matrix[0][-(piece // 8) + 7][piece % 8] = piece_val[pieces[piece].symbol()] * .01
    
    if board.turn == BLACK:
        matrix *= -1

    return matrix

def encode_moves(board: Board, matrix):
    piece_index = {"P": 0, "B": 1, "N": 2, "R": 3, "Q": 4, "K": 5,
                "p": 6, "b": 7, "n": 8, "r": 9, "q": 10, "k": 11}
    
    moves = board.legal_moves
    for move in moves:
        start = move.from_square
        end = move.to_square

        piece = board.piece_at(start).symbol()
        matrix[int(end)] |= 2**piece_index[piece]

def encode_matrix(board: Board):
    piece_val = {"P": 12, "B": 13, "N": 14, "R": 15, "Q": 16, "K": 17,
                "p": 18, "b": 19, "n": 20, "r": 21, "q": 22, "k": 23}
    
    matrix = np.zeros((64)).astype(int)

    encode_moves(board, matrix)
    board.push(Move.null())
    encode_moves(board, matrix)
    board.pop()
    
    

    for i in range(64):
        piece = board.piece_at(i)
        if piece is not None:
            piece = piece.symbol()
            matrix[i] |= 2**piece_val[piece]
    matrix = matrix.reshape((1,8,8))
    matrix = np.flip(matrix, 0)
    matrix = preprocessing.normalize(matrix) 
    return matrix

def encode_board(board: Board):
    matrix = np.zeros((12, 64), dtype=np.float16)

    piece_index = {"P": 0, "B": 1, "N": 2, "R": 3, "Q": 4, "K": 5,
                "p": 6, "b": 7, "n": 8, "r": 9, "q": 10, "k": 11}
    
    piece_val = {"P": 11, "B": 31, "N": 32, "R": 54, "Q": 95,"K": 100,
                "p": -11, "b": -31, "n": -32, "r": -54, "q": -95, "k": -100}
    
    moves = board.legal_moves

    for move in moves:
        start = move.from_square
        end = move.to_square

        piece = board.piece_at(start).symbol()
        index = piece_index[piece]
    
        matrix[index][int(end)] = piece_val[piece]

    board.push(Move.null())

    for move in moves:
        start = move.from_square
        end = move.to_square

        piece = board.piece_at(start).symbol()
        index = piece_index[piece]
    
        matrix[index][int(end)] = piece_val[piece]

    board.pop()

    if board.turn == WHITE:
        for i in range(len(matrix)):
            matrix[i] = np.flip(matrix[i], axis=0)


    matrix = matrix.reshape((12, 8, 8))

    return matrix * .1