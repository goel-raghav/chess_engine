from chess import Board
from math import inf
from time import perf_counter
from search import profile
from search import nmax
from search import predict
from encode import transform_fen


# TODO create a command prompt for easier testing

test = Board() 

while True:
    t1 = perf_counter()
    # score, best_line, best_depth = iterative_deepening(test, 5)
    score, best_line = nmax(test, 4, 1, -inf, inf)
    t2 = perf_counter()

    print("Time: ", t2 - t1)
    profile()

    print("Score:", float(score))

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
