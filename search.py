from chess import Board
from chess import Move

from time import perf_counter
from math import inf

import numpy as np

import torch
from torch import nn

from encode import transform_fen
from encode import encode_board

from model.neural_network import NeuralNetwork

# TODO break down into more functions 

network = NeuralNetwork()
network.load_state_dict(torch.load("model_weights"))
network.eval()

sample_input = torch.rand(1, 1, 8, 8)
torch.jit.enable_onednn_fusion(True)
traced_model = torch.jit.trace(network, sample_input)
traced_model = torch.jit.freeze(traced_model)
traced_model(sample_input)
traced_model(sample_input)

print('Ready')

def predict(val):
    val = torch.from_numpy(val)
    val = val.float()
    with torch.no_grad():
        e = traced_model(val)
    return e

eval_count = 0
table_count = 0
total_predict_time = 0
total_eval_time = 0
total_sort_time = 0
table_time = 0
test_time = 0

killer_moves = [None, None]
prev_move = None
table = {}
    
def nmax(board: Board, depth, color, a, b):
    global total_sort_time
    global test_time
    if depth == 0:
        score, _ = evaluate([board], color)
        return score * color, []
    
    
    
    score = -inf
    best_move = []

    moves = board.legal_moves

    sort_t1 = perf_counter()
    moves = sorted(moves, key=lambda move: move_key(move, board))
    sort_t2 = perf_counter()
    total_sort_time += sort_t2 - sort_t1

    # still in testing
    if depth == 1:
        boards = []
        for move in moves:
            board.push(move)
            boards.append(board.copy())
            board.pop()
        


            
        for i in range(0, len(boards), 10):
            current = boards[i: i+10]
            scores, _ = evaluate(current, color * -1)
            scores *= color
            
            
            bi = torch.argmax(scores)
            t1 = perf_counter()
            if scores[bi] > score:
                score = scores[bi]
                best_move = [boards[i + bi].peek()]
            t2 = perf_counter()
            test_time += t2 - t1

            a = max(a, score)
            if a >= b:
                shift_killer_move(best_move[0], board)
                break
            
        return score, best_move
    # # still in testing

    for move in moves:
        board.push(move)
        e, line = nmax(board, depth-1, -1 * color, -b, -a)
        e *= -1
        if e > score:
            score = e
            best_move = [move] + line

        board.pop()
        
        a = max(a, score)
        if a >= b:
            shift_killer_move(move, board)
            break

    return score, best_move

def evaluate(boards, color):
    global eval_count
    global table_count
    global total_predict_time
    global total_eval_time
    global network
    global table_time

    eval_t1 = perf_counter()
    
    eval_count += 1

    # if board.is_checkmate():
    #     return 100 * color, []
    
    cur_x = list(map(lambda x: transform_fen(x.fen()), boards))
    cur_x = np.stack(cur_x)

    t1 = perf_counter()
    score = predict(cur_x)
    t2 = perf_counter()
    total_predict_time += t2 - t1

    eval_t2 = perf_counter()
    total_eval_time += eval_t2 - eval_t1

    return score, []

def move_key(move: Move, board: Board): 
    global killer_moves
    global prev_move

    val = {"p": -1, "n": -3, "b": -3, "r": -5, "q": -9, "k": 0}
    if prev_move == move:
        return 3
    if killer_moves[0] == move:
        return 1
    if killer_moves[1] == move:
        return 2
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
    global table_time
    global test_time

    print("Amount of evaluations: ", eval_count)
    print("Table Counts: ", table_count)
    print("Total time by network predictions: ", total_predict_time)
    print("Average predict time: ", total_predict_time / eval_count)
    print("Total eval time:", total_eval_time)
    print("Total sort time: ", total_sort_time)
    print("Total table time:", table_time)
    print("Test time:", test_time)

    total_eval_time = 0
    eval_count = 0
    table_count = 0
    total_predict_time = 0
    total_sort_time = 0
    table_time = 0
    test_time = 0

def shift_killer_move(move: Move, board: Board):
    global killer_moves

    piece = board.piece_at(move.to_square)
    if piece is None and not killer_moves[0] == move:
        killer_moves[1] = killer_moves[0]
        killer_moves[0] = move

