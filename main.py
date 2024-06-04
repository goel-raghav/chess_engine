from chess import Board
import chess.polyglot
from time import perf_counter
from engine.engine import Engine
from model.small_model import NeuralNetwork
from model.classic_eval import eval
import torch

weights = "weights/new"


test = Board("r1bqk1nr/pppnbppp/8/3p2B1/3P4/2NBP3/PP3PPP/R2QK1NR w KQkq - 2 8")
# "Q7/8/8/2p1k3/2P5/1P1P4/5PR1/2K5 w - - 1 51" good mate in 3 checker


in_opening = True

engine = Engine(NeuralNetwork, weights)


while True:
    best_line = []
    score = 0
    t2 = 0
    t1 = 0

    t1 = perf_counter()
    score, best_line = engine.get_line(test, 4)
    t2 = perf_counter()

    for move in best_line:
        print(move)
        test.push(move)
        print(test.fen())

    print(torch.sigmoid(torch.tensor(0.00328782 * eval(test) + 0.11215524)))

    for i in range(len(best_line)):
        test.pop()


    engine.profile()
    print("Time: ", t2 - t1)
    print("Score:", float(score))
    print("Depth:", len(best_line))
    print("Best Move: ", best_line[0])

    test.push(best_line[0])
    print(test)

    if test.is_checkmate():
        print("BOT WINS HAHAHAHAHAHAHAHAHAHAHA")
        exit()

    flag = True
    next_move = input("next move: ")
    while flag:
        try:
            test.push_san(next_move)
            flag = False
        except:
            next_move = input("next move: ")

    with open("saved.txt", "w") as file:
        file.write(test.fen())
 
    
    print(test)
