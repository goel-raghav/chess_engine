import chess.polyglot
import chess

board = chess.Board()

with chess.polyglot.open_reader("baron30.bin") as reader:
    for i in range(20):
        move = reader.get(board).move
        print(move)
        board.push(move)



