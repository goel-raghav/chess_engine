from chess import Board
from chess import Move
from chess import WHITE, BLACK


def eval(board: Board):
    m = material(board)
    pos = piece_square_table(board)
    curr = score(board)
    board.push(Move.null())
    opp = score(board)
    board.pop()
    
    if board.turn:
        return m + pos + (curr - opp)
    return  (m + pos + (curr - opp)) * -1

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
    
def piece_square_table(board: Board):
    pawn = [ 0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0]

    knight = [-50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50]
    
    bishop = [-20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20]
    
    rook =  [0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            0,  0,  0,  5,  5,  0,  0,  0]
    
    queen = [-20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -5,  0,  5,  5,  5,  5,  0, -5,
            0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20]
    
    king_mid_game = [-30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -30,-40,-40,-50,-50,-40,-40,-30,
                    -20,-30,-30,-40,-40,-30,-30,-20,
                    -10,-20,-20,-20,-20,-20,-20,-10,
                    20, 20,  0,  0,  0,  0, 20, 20,
                    20, 30, 10,  0,  0, 10, 30, 20]
    
    king_end_game = [-50,-40,-30,-20,-20,-30,-40,-50,
                    -30,-20,-10,  0,  0,-10,-20,-30,
                    -30,-10, 20, 30, 30, 20,-10,-30,
                    -30,-10, 30, 40, 40, 30,-10,-30,
                    -30,-10, 30, 40, 40, 30,-10,-30,
                    -30,-10, 20, 30, 30, 20,-10,-30,
                    -30,-30,  0,  0,  0,  0,-30,-30,
                    -50,-30,-30,-30,-30,-30,-30,-50]
    
    score = 0
    piece_map = board.piece_map()

    table_map = {"p": pawn, "n": knight, "b": bishop, "r": rook, "q": queen, "k": [0]*64}

    for square in piece_map:
        piece = piece_map[square].symbol()
        table = table_map[piece.lower()]

        if piece.isupper():
            score += table[square]
        else:
            black_index = ((7 - square // 8) * 8) + (square % 8)
            score -= table[black_index]

    return square