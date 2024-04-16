from chess import Board
from chess.polyglot import zobrist_hash as hash


from math import inf

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

    def nmax(self, board: Board, depth, color, a, b):
        if depth == 0:
            score = self.evaluate(board)
            self.count += 1
            return score * color, []
        
        score = -inf
        best_move = []

        moves = board.legal_moves
        if moves is None:
            if board.is_checkmate():
                return 100 * color, []
            return 0, []

        moves = self.sorter.sort(moves, board)


        for move in moves:
            board.push(move)
            # key = hash(board)
            # table_score, table_depth = self.table.get(key)
            # if table_depth is not None and table_depth >= depth:
            #     e = table_score
            #     line = []
            # else:
            e, line = self.nmax(board, depth-1, -1 * color, -b, -a)
            e *= -1
            if e > score:
                score = e
                best_move = [move] + line

            board.pop()
            
            a = max(a, score)
            if a >= b:
                self.sorter.shift_killer_move(move, board)
                break
        
        # self.table.add(hash(board), score, depth)
        return score, best_move

    def iterative_deepening(self, board: Board, max_depth):
        for i in range(max_depth):
            score, best_line = self.nmax(board, i+1, 1, -inf, inf)
            print(best_line)
            self.sorter.prev_best_line = best_line
        return score, best_line
    
