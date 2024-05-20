from evaluator import Evaluator
from search import Searcher
from sorter import Sorter
from transposition_table import Table
from encode import Encoder
from model.classic_eval import eval
from math import inf

from chess import Board
from chess import BLACK
import chess.polyglot

import pickle


class Engine:
    def __init__(self, model, weights, name, qsearch=True) -> None:
        self.table = Table()
        self.encoder = Encoder()
        self.sorter = Sorter()
        self.evaluator = Evaluator(model, weights, self.encoder.encode)
        self.searcher = Searcher(self.evaluator.evaluate, self.sorter, self.table, qsearch)
        self.name = name
        self.reader = chess.polyglot.open_reader("opening.bin")


    def get_line(self, board: Board, depth):
        moves = self.reader.get(board)
        
        if moves is not None:
            entry = self.reader.weighted_choice(board)
            best_line = [entry.move]
            return 0, best_line
        else:
            return self.searcher.iterative_deepening(board, 4)
    
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

    def serialize(self):
        with open(self.name+".pkl", "wb") as file:
            pickle.dump(self, file)



