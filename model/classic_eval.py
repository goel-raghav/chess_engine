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
    wp = (board.pawns & board.occupied_co[WHITE]).bit_count() * 1
    wb = (board.bishops & board.occupied_co[WHITE]).bit_count() * 3
    wn = (board.knights & board.occupied_co[WHITE]).bit_count() * 3
    wr = (board.rooks & board.occupied_co[WHITE]).bit_count() * 5
    wq = (board.queens & board.occupied_co[WHITE]).bit_count() * 9

    bp = (board.pawns & board.occupied_co[BLACK]).bit_count() * -1
    bb = (board.bishops & board.occupied_co[BLACK]).bit_count() * -3
    bn = (board.knights & board.occupied_co[BLACK]).bit_count() * -3
    br = (board.rooks & board.occupied_co[BLACK]).bit_count() * -5
    bq = (board.queens & board.occupied_co[BLACK]).bit_count() * -9

    score = wp + wb + wn + wr + wq + bp + bb + bn + br + bq
    return score

def mobility(board: Board):
    return board.legal_moves.count() * .01
    

