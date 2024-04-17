from chess import Board
from chess import Move
from chess import WHITE, BLACK


def eval(board: Board):
    m = material(board)
    curr = score(board)
    board.push(Move.null())
    opp = score(board)
    board.pop()
    
    if board.turn:
        return m + (curr - opp)
    return  (m + (curr - opp)) * -1

def score(board: Board):
    return mobility(board)

def material(board: Board):
    wp = (board.pawns & board.occupied_co[WHITE]).bit_count() * 100
    wb = (board.bishops & board.occupied_co[WHITE]).bit_count() * 330
    wn = (board.knights & board.occupied_co[WHITE]).bit_count() * 320
    wr = (board.rooks & board.occupied_co[WHITE]).bit_count() * 500
    wq = (board.queens & board.occupied_co[WHITE]).bit_count() * 900

    bp = (board.pawns & board.occupied_co[BLACK]).bit_count() * -100
    bb = (board.bishops & board.occupied_co[BLACK]).bit_count() * -330
    bn = (board.knights & board.occupied_co[BLACK]).bit_count() * -320
    br = (board.rooks & board.occupied_co[BLACK]).bit_count() * -500
    bq = (board.queens & board.occupied_co[BLACK]).bit_count() * -900

    score = wp + wb + wn + wr + wq + bp + bb + bn + br + bq
    return score

def mobility(board: Board):
    return board.legal_moves.count()
    

