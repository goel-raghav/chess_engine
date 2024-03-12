from chessfunc import transform_fen
from chessfunc import encode_board
from chess import Board
from chess import Move
from keras import saving
from time import perf_counter as t
import math
import keras.backend as K

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


import tensorflow as tf
import numpy as np
import random

# predict = lambda x: tf.function(network(x))

network = saving.load_model("test_model2.keras")

@tf.function(jit_compile=True)
def predict(val):
    print("TRACING")
    return network(val)

eval_count = 0
table_count = 0
total_predict_time = 0
total_eval_time = 0
total_sort_time = 0


killer_moves = [None, None]
prev_move = None
table = {}

def iterative_deepening(board, time):

    max_depth = 100 # temp since depth won't actually reach 100
    best_depth = 0
    start_time = t()
    
    score = 0
    move = None
    prev_score = 0
    global prev_move
    for depth in range(max_depth):
        if t() - start_time < time:
            best_depth = depth
            prev_score = score
            prev_move = move
            score, move, completed = nmax(board, depth, True, -math.inf, math.inf, start_time, time)

    if not completed:
        return prev_score, prev_move, best_depth - 1, completed
    return score, move, best_depth, completed

    
def nmax(board: Board, depth, color, a, b, start_time, time):
    global total_sort_time
    if depth == 0:
        score, _ = evaluate(board, color)
        return score * color, None, True
    
    score = -math.inf
    best_move = None

    moves = board.legal_moves

    sort_t1 = t()
    moves = sorted(moves, key=lambda move: move_key(move, board))
    sort_t2 = t()
    total_sort_time += sort_t2 - sort_t1

    for move in moves:
        if t() - start_time > time:
            return score, best_move, False

        board.push(move)
        
        e, _, _ = nmax(board, depth-1, -1 * color, -b, -a, start_time, time)
        e *= -1
        if e > score:
            score = e
            best_move = move

        board.pop()
        
        a = max(a, score)
        if a >= b:
            shift_killer_move(move, board)
            break

    return score, best_move, True

def evaluate(board: Board, color):
    global eval_count
    global table_count
    global total_predict_time
    global total_eval_time
    global network

  

    eval_t1 = t()
    eval_count += 1

    table_score = table.get(str(board))
    if table_score is not None:
        table_count += 1
        eval_t2 = t()
        total_eval_time += eval_t2 - eval_t1
        return table_score, None
    
    if board.is_checkmate():
        return 100 * color, None
    
    cur_x = transform_fen(board.fen()).reshape(1, 8, 8)

    t1 = t()
    score = float(predict(cur_x))
    t2 = t()
    total_predict_time += t2 - t1

    table[str(board)] = score
    eval_t2 = t()
    total_eval_time += eval_t2 - eval_t1

    return score, None

def move_key(move: Move, board: Board): 
    global killer_moves
    global prev_move

    val = {"p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": -50}
    if prev_move == move:
        return -50
    if killer_moves[0] == move:
        return 0
    if killer_moves[1] == move:
        return 1
    piece = board.piece_at(move.to_square)
    if  piece is not None:
        piece = piece.symbol()
        return val[piece.lower()]
    else:
        return 10
    
def profile():
    global eval_count
    global table_count
    global total_predict_time
    global total_eval_time
    global total_sort_time

    print("Amount of evaluations: ", eval_count)
    print("Table Counts: ", table_count)
    print("Total time by network predictions: ", total_predict_time)
    print("Average predict time: ", total_predict_time / eval_count)
    print("Total eval time:", total_eval_time)
    print("Total sort time: ", total_sort_time)

    total_eval_time = 0
    eval_count = 0
    table_count = 0
    total_predict_time = 0
    total_sort_time = 0

def shift_killer_move(move: Move, board: Board):
    global killer_moves

    piece = board.piece_at(move.to_square)
    if piece is None and not killer_moves[0] == move:
        killer_moves[1] = killer_moves[0]
        killer_moves[0] = move

