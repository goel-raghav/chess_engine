
import chess
import math

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


import tensorflow as tf
from time import perf_counter
from search import profile
from search import nmax
from search import table


test = chess.Board()

while True:
    t1 = perf_counter()
    score, best_move, _ = nmax(test, 4, 1, -math.inf, math.inf, perf_counter(), 10000)
    t2 = perf_counter()

    print("Time: ", t2 - t1)
    profile()

    print("Score:", float(score))
    print(best_move)

    test.push(best_move)
    table = {}
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
