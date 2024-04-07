from chess import Board
from chess import Move
from chess import BLACK
from numpy import tanh

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
    current = len(list(board.legal_moves))

    board.push(Move.null())

    opp = len(list(board.legal_moves))

    board.pop()

    score = current - opp

    if board.turn == BLACK:
        score *= -1

    return score * .1

def get_king_saftey(board: Board):
    current = 0
    for move in board.legal_moves:
        if board.gives_check(move):
            current += 1

    opp = 0
    board.push(Move.null())
    for move in board.legal_moves:
        if board.gives_check(move):
            opp += 1

    board.pop()

    score = current - opp

    if board.turn == BLACK:
        score *= -1

    return score * .1
    