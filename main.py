from chess import Board
from math import inf
from time import perf_counter
from search import profile
from search import nmax
from search import iterative_deepening

from model.neural_network import NeuralNetwork
from evaluator import Evaluator
from sorter import Sorter
from transposition_table import Table



# TODO create a command prompt for easier testing

test = Board() 

while True:
    t1 = perf_counter()
    score, best_line = iterative_deepening(test, 4)
    # score, best_line = nmax(test, 4, 1, -inf, inf)
    t2 = perf_counter()

    for move in best_line:
        print(move)
        test.push(move)
        print(test)

    for i in range(len(best_line)):
        test.pop()


    print("Time: ", t2 - t1)
    profile()

    print("Score:", float(score))
    print("Depth:", len(best_line))

    test.push(best_line[0])
    print(test)


    next_move = input("next move: ")

    flag = True
    while flag:
        try:
            test.push_san(next_move)
            flag = False
        except:
            next_move = input("next move: ")
 
    
    print(test)
