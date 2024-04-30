import chess.polyglot
import chess

board = chess.Board()

with chess.polyglot.open_reader("baron30.bin") as reader:
    for i in range(20):
        x = reader.find_all(board)
        size = sum([1 for e in x])
        print(size)
        for entry in reader.find_all(board):
            print(entry.move, entry.weight, entry.learn)
            board.push(entry.move)



