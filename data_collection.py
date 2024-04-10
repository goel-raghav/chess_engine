import chess.pgn
import numpy as np
from piece import get_piece_eval
from piece import get_move_amount
from piece import get_king_saftey

# TODO remoeve redunant data points

whiteCount=0
blackCount=0
#--------------------
# open downloaded games
#----------------------

pgn = open("data/master_games.pgn")
games = []

#--------------------------
# read and put into an array
#--------------------------
i= 0
while i < 100_000:
    current = chess.pgn.read_game(pgn)
    i+= 1
    if current is not None:
        headers = current.headers
        result = headers["Termination"]
        whiteElo = int(headers["WhiteElo"])
        blackElo = int(headers["BlackElo"]) # TODO make it so `games` is saved to a new file, so I don't have to repeat this code
        if result == "Normal":
            games.append(current)
    else:
        break

print("loaded games")
# =============================================================================
# turn games into nn stuff
# =============================================================================

# input and output for neural network
x = []
y=[]
# function to turn fen string into usuable nueral network stuff
from encode import encode
from encode import transform_fen
# function to convert get x and y
def get_data(board, i, game_length, moves):
    global blackCount
    global whiteCount

    x = encode(board).reshape(1, 8, 8)
    
    y = get_piece_eval(board)  + get_king_saftey(board) + get_move_amount(board)

    return x, y
    
# min moves before becoming data
MIN_MOVES = 2
c = 0
for game in games:
    c += 1
    board = game.board()
    moves = list(game.mainline_moves())
    game_length = len(moves)
    for i, move in enumerate(moves):
        board.push(move)
        if (i > MIN_MOVES):
            cur_x, cur_y = get_data(board, i, game_length, moves)

           

            x.append(cur_x)
            y.append(cur_y)

    if c % 1000 == 0:
        print(c)

print(whiteCount)
print(blackCount) 
# =============================================================================
# nueral network
# =============================================================================
np.savez("test_data", x=x, y=y)