from chess import Board
from chess.polyglot import zobrist_hash as hash


from math import inf

from time import perf_counter

from encode import Encoder
from model.small_model import NeuralNetwork
from evaluator import Evaluator
from sorter import Sorter
from transposition_table import Table
from typing import Callable

class Searcher():
    def __init__(self, evaluate: Callable, sorter: Sorter, table: Table):
        self.evaluate = evaluate
        self.sorter = sorter
        self.table = table
        self.count = 1
        self.cut = 0
        self.test_time = 0

    def nmax(self, board: Board, depth, color, a, b):

        score = -inf
        best_move = []
        moves = board.legal_moves
        if not any(board.generate_legal_moves()):
            if board.is_check():
                return 10000 * -1 * (depth+1), []
            else:
                return 0, []
    

        
        if depth == 0:
            score = self.evaluate(board)
            self.count += 1
            return score, []
        
        
        moves = self.sorter.sort(moves, board)


        for move in moves:

            board.push(move)
            key = hash(board)

            used_table = False
            # table_score, table_depth = self.table.get(key)
            # if table_depth is not None and table_depth >= depth:
            #     used_table = True
            #     e = table_score
            #     line = []
            
            if not used_table:
                e, line = self.nmax(board, depth-1, -1 * color, -b, -a)
                e = e * -1
            if e > score:
                score = e
                best_move = [move] + line

            board.pop()
            
            a = max(a, score)
            if a >= b:
                self.sorter.shift_killer_move(move, board)
                self.cut += 1 * depth
                break
        
        if not used_table:
            self.table.add(hash(board), score, depth)
        return score, best_move

    def iterative_deepening(self, board: Board, max_depth):
        self.sorter.prev_best_line = []
        for i in range(max_depth):
            score, best_line = self.nmax(board, i+1, 1, -inf, inf)
            print(best_line)

            if abs(score) >= 10000:
                break

            self.sorter.prev_best_line = best_line + self.sorter.prev_best_line
        return score, best_line
    
