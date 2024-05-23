import numpy as np
from chess import Board
from chess import Move
from chess import BLACK, WHITE

class Encoder():

    def __init__(self):
      self.piece_val = {"P": 11, "B": 31, "N": 32, "R": 54, "Q": 95,"K": 100,
                "p": -11, "b": -31, "n": -32, "r": -54, "q": -95, "k": -100}


    def encode(self, board: Board):
        matrix = np.zeros((1, 8, 8), dtype=np.float16)

        pieces = board.piece_map()

        for piece in pieces:
            matrix[0][-(piece // 8) + 7][piece % 8] = self.piece_val[pieces[piece].symbol()] * .01
        
        if board.turn == BLACK:
            matrix *= -1

        return matrix
    
    def update(self, matrix, from_square, to_square, piece):
        matrix[0][-(to_square // 8) + 7][to_square % 8] = self.piece_val[piece.symbol()] * .01
        matrix[0][-(from_square // 8) + 7][from_square % 8] = 0