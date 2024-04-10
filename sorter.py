import chess
from time import perf_counter

class Sorter():
    def __init__(self):
        self.sort_time = 0
        self.killer_moves = [None, None]
        
    def sort(self, moves: chess.LegalMoveGenerator, board: chess.Board):
        sort_start_time = perf_counter()
        smoves = sorted(moves, key = lambda move: self.move_key(move, board))
        sort_end_time = perf_counter()
        self.sort_time += sort_end_time - sort_start_time
        return smoves

    def move_key(self, move: chess.Move, board: chess.Board): 
        val = {"p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": 0}
        if self.killer_moves[0] == move:
            return 1
        if self.killer_moves[1] == move:
            return 2
        piece = board.piece_at(move.to_square)
        if  piece is not None:
            piece = piece.symbol()
            return val[piece.lower()] - val[board.piece_at(move.from_square).symbol().lower()]
        else:
            return 10
        
    def shift_killer_move(self, move: chess.Move, board: chess.Board):
        if not (board.is_capture(move) and self.killer_moves[0] == move):
            self.killer_moves[1] = self.killer_moves[0]
            self.killer_moves[0] = move

    def reset(self):
        self.sort_time = 0