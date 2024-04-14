import pickle
import chess.pgn
import sys


sys.setrecursionlimit(10000)

pgn = open("data_generation/master_games.pgn")
games = []


i = 0
while i < 50_000:
    current = chess.pgn.read_game(pgn)
    
    if current is not None:
        headers = current.headers
        result = headers["Termination"]
        whiteElo = int(headers["WhiteElo"])
        blackElo = int(headers["BlackElo"])

        if result == "Normal":
            games.append(current)
            i += 1
    else:
        break

with open("games.pickle", "wb") as file:
    pickle.dump(games, file)