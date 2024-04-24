from chess import Board
from math import inf
from time import perf_counter


from search import Searcher
from model.small_model import NeuralNetwork
from transposition_table import Table
from encode import Encoder
from evaluator import Evaluator
from sorter import Sorter
from model.classic_eval import eval



weights = "Tdepth2_weights"

encoder = Encoder()
evaluator = Evaluator(NeuralNetwork, weights, encoder.encode)
table = Table()
sorter = Sorter()
searcher = Searcher(evaluator.evaluate, sorter, table)

test = Board("Q7/8/8/2p1k3/2P5/1P1P4/5PR1/2K5 w - - 1 51")


while True:
    t1 = perf_counter()
    # score, best_line = searcher.iterative_deepening(test, 7)
    score, best_line = searcher.nmax(test, 5, 1, -inf, inf)
    t2 = perf_counter()

    table.clear()

    for move in best_line:
        print(move)
        test.push(move)
        print(test)

    print(eval(test))

    for i in range(len(best_line)):
        test.pop()

    evaluator.profile()
    evaluator.reset()
    sorter.profile()
    sorter.reset()
    table.profile()
    table.reset()

    print("Time: ", t2 - t1)
    print("Score:", float(score))
    print("Depth:", len(best_line))

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
