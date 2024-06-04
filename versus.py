from engine.engine import Engine
from model.small_model import NeuralNetwork as nn
import chess
import chess.pgn

def update(engine, board):
    score, line = new_engine.get_line(board, 4)
    board.push(line[0])
    
    game = chess.pgn.Game.from_board(board)
    
    print(game, file=open("test.pgn", "w"), end="\n\n")

def versus(old_engine, new_engine):

    board = chess.Board()

    while True:
        update(old_engine, board)
        update(new_engine, board)

if __name__ == "__main__":
    new_weights = "weights/new"
    old_weights = "weights/best"

    new_engine = Engine(nn, new_weights, qsearch=False)
    old_engine = Engine(nn, old_weights, qsearch=False)
    
    versus(old_engine, new_engine)