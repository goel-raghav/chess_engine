from engine.engine import Engine
from model.small_model import NeuralNetwork as nn
import chess
import chess.pgn

new_weights = "weights/new"
old_weights = "weights/best"

new_engine = Engine(nn, new_weights, qsearch=False)
old_engine = Engine(nn, old_weights, qsearch=False)

board = chess.Board()

while True:

    score, line = old_engine.get_line(board, 4)
    board.push(line[0])

    print(board)

    score, line = new_engine.get_line(board, 4)
    board.push(line[0])
    print(score)
    print(board)
    
    

    

    

    game = chess.pgn.Game.from_board(board)
    print(game, file=open("test.pgn", "w"), end="\n\n")


# test = chess.Board("rn3b1r/2Rq3k/7p/1p1p4/3P4/6Q1/PP1B1P1P/4R1K1 b - - 0 23")

# print(old_engine.get_line(test, 4))