from engine.engine import Engine
from model.small_model import NeuralNetwork as nn
import chess
import chess.pgn

new_weights = "megadepth2_weights"
old_weights = "15000depth2_weights"

new_engine = Engine(nn, new_weights, "new")
old_engine = Engine(nn, new_weights, "old", qsearch=False)

board = chess.Board()

while True:

    score, line = new_engine.get_line(board, 4)
    board.push(line[0])

    print(board)
    
    score, line = old_engine.get_line(board, 4)
    board.push(line[0])

    print(board)

    

    

    game = chess.pgn.Game.from_board(board)
    print(game, file=open("test.pgn", "w"), end="\n\n")


    