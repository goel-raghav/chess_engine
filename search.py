from chess import Board
from chess import Move

from time import perf_counter
from math import inf

import numpy as np

import torch

from encode import transform_fen
from encode import encode

from model.neural_network import NeuralNetwork

from evaluator import Evaluator

# TODO break down into more functions 

evaluator = Evaluator(NeuralNetwork, "test_model_weights1", encode)

print('Ready')

total_sort_time = 0
test_time = 0

killer_moves = [None, None]
prev_move = None
table = {}
    
def capture_search(board: Board, color):
        score = -inf
        best_move = []
        for move in board.legal_moves:
            if board.is_capture(move) and board.peek().to_square == move.to_square:
                
                board.push(move)
                e, line = evaluate([board], color*-1)
                e *= color
                board.pop()

                if e > score:
                    score = e
                    best_move = [move] + line

        if score == -inf:
            score, best_move = evaluate([board], color)
            score *= color
        return score, best_move

def nmax(board: Board, depth, color, a, b):
    global total_sort_time
    global test_time
    if depth == 0:
        score, _ = evaluator.evaluate(board)
        return score * color, []
    
    score = -inf
    best_move = []

    moves = board.legal_moves

    sort_t1 = perf_counter()
    moves = sorted(moves, key=lambda move: move_key(move, board))
    sort_t2 = perf_counter()
    total_sort_time += sort_t2 - sort_t1

    

    # still in testing
    # if depth == 1:

    #     boards = []
    #     for move in moves:
    #         if board.is_capture(move):
    #             board.push(move)
    #             e, line = capture_search(board, color * -1)
    #             e *= -1
    #             if e > score:
    #                 score = e
    #                 best_move = [move] + line
    #             board.pop()

    #             a = max(a, score)
    #             if a >= b:
    #                 shift_killer_move(best_move[0], board)
    #                 break
               
    #         board.push(move)
    #         boards.append(board.copy())
    #         board.pop()
            
    #     for i in range(0, len(boards), 2):
    #         current = boards[i: i+2]
    #         scores, _ = evaluate(current, color * -1)
    #         scores *= color
            
            
    #         bi = torch.argmax(scores)
    #         if scores[bi] > score:
    #             score = scores[bi]
    #             best_move = [boards[i + bi].peek()]
            

    #         a = max(a, score)
    #         if a >= b:
    #             shift_killer_move(best_move[0], board)
    #             break
            
    #     return score, best_move
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
    global total_sort_time
    global table_time
    global test_time

    print("Amount of evaluations: ", evaluator.eval_count)
    print("Total time by network predictions: ", evaluator.pred_time)
    print("Average predict time: ", evaluator.pred_time / evaluator.eval_count)
    print("Total eval time:", evaluator.eval_time)
    print("Total sort time: ", total_sort_time)
    print("Test time:", test_time)

    total_sort_time = 0
    table_time = 0
    test_time = 0

def shift_killer_move(move: Move, board: Board):
    global killer_moves

    piece = board.piece_at(move.to_square)
    if piece is None and not killer_moves[0] == move:
        killer_moves[1] = killer_moves[0]
        killer_moves[0] = move

