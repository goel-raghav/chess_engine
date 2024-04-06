from chess import Board
from chess import Move

def get_piece_eval(board: Board):
    piece_val = {"P": 1, "B": 3, "N": 3, "R": 5, "Q": 9, "K": 0,
                "p": -1, "b": -3, "n": -3, "r": -5, "q": -9, "k": 0}
    
    s = 0
    for i in range(64):
        p = board.piece_at(i)
        if p is not None:
            p = p.symbol()
            s += piece_val[p]

    return s * .1

def get_move_amount(board: Board):
    current = len(board.legal_moves)

    board.push()