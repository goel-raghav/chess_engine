from engine.evaluator import Evaluator
from engine.search import Searcher
from engine.sorter import Sorter
from engine.transposition_table import Table
from engine.encode import Encoder
from model.classic_eval import eval
from math import inf



from chess import Board
from chess import BLACK
import chess.polyglot

import pickle


class Engine:
    def __init__(self, model, weights, qsearch=True, classic=False) -> None:
        self.table = Table()
        self.encoder = Encoder()
        self.sorter = Sorter()
        self.evaluator = Evaluator(model, weights, self.encoder.encode)

        if not classic:
            self.searcher = Searcher(self.evaluator.evaluate, self.sorter, self.table, qsearch)
        else:
            self.searcher = Searcher(eval, self.sorter, self.table, qsearch)

        self.reader = chess.polyglot.open_reader("opening.bin")


    def get_line(self, board: Board, depth):
        moves = self.reader.get(board)
        
        if moves is not None:
            entry = self.reader.weighted_choice(board)
            best_line = [entry.move]
            return 0, best_line
        else:
            return self.searcher.iterative_deepening(board, depth)
    
    def profile(self):
        self.evaluator.profile()
        self.evaluator.reset()
        self.sorter.profile()
        self.sorter.reset()
        self.table.profile()
        self.table.reset()
        print("CUTS:", self.searcher.cut)
        print("TEST TIME", self.searcher.test_time)
        self.searcher.cut = 0



