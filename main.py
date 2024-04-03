
import chess
import math

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


# import tensorflow as tf
from time import perf_counter
from search import profile
from search import nmax
from search import iterative_deepening
from search import predict
import search
from chessfunc import transform_fen



# tf.config.optimizer.set_jit(True)
# TODO create a command prompt for easier testing

test = chess.Board() 

def print_line(line, board: chess.Board):
    for move in line:
        board.push(move)
        print(board)
        print(move)
        print(" ")
    cur_x = transform_fen(board.fen()).reshape(1, 1, 8, 8)
    print(float(predict(cur_x)))

    for i in range(len(line)):
        board.pop()

while True:
    t1 = perf_counter()
    # score, best_line, best_depth = iterative_deepening(test, 5)
    score, best_line = nmax(test, 4, 1, -math.inf, math.inf)
    t2 = perf_counter()

    print(print_line(best_line, test))
    print("Time: ", t2 - t1)
    profile()

    print("Score:", float(score))
    # print("Max Depth:", best_depth)
    

    test.push(best_line[0])
    # search.table = {}
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
