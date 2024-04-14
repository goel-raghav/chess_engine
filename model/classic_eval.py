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

    return s

def get_move_amount(board: Board):
    default_pos = {"R": [0, 7], "N": [1, 6], "B": [2, 5], "Q": [3], "r": [56, 63], "n": [57, 62], "b": [58, 61], "q": [59]}

    current = len(list(board.legal_moves))

    

    white_default_count = 0
    black_default_count = 0
    pm = board.piece_map()
    for key in pm:
        cur = pm[key].symbol()
        if cur in ["K", "k", "P", "p"]:
            continue
        if cur.isupper() and key in default_pos[cur]:
            white_default_count += 1
        elif cur.islower() and key in default_pos[cur]:
            black_default_count += 1



    board.push(Move.null())

    opp = len(list(board.legal_moves))

    board.pop()

    color = True
    if board.turn == BLACK:
        color = False

    if color:
        score = (current - white_default_count) - (opp - black_default_count)
    else:
        score = (current - black_default_count) - (opp - white_default_count) 
        score *= -1

    

    return score * .01

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

    return score * .01

def eval(board):
    return get_piece_eval(board) + get_move_amount(board) + get_king_saftey(board)