from engine.engine import Engine
from model.small_model import NeuralNetwork as nn
import chess
import chess.pgn

new_weights = "weights/new"
old_weights = "15000depth2_weights"

new_engine = Engine(nn, new_weights, qsearch=False)
old_engine = Engine(nn, new_weights, qsearch=False, classic=True)


def play_games():
    
    board = chess.Board("rnbq1rk1/pp1nbppp/4p3/2ppP1B1/3P3P/2NB4/PPP2PP1/R2QK1NR w KQ c6 0 8")

    while True:

        score, line = new_engine.get_line(board, 4)
        board.push(line[0])

        print(board)
        
        score, line = old_engine.get_line(board, 4)
        print(score)
        board.push(line[0])

        print(board)

        game = chess.pgn.Game.from_board(board)
        print(game, file=open("test.pgn", "w"), end="\n\n")

test = chess.Board("rn1qkbnr/ppp1pppp/8/3p4/4P1b1/P1N5/1PPP1PPP/R1BQKBNR b KQkq - 0 1")
print(old_engine.get_line(test, 1))

