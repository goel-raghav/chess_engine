from chess import Board
import chess.polyglot
from math import inf
from time import perf_counter


from search import Searcher
from model.small_model import NeuralNetwork
from transposition_table import Table
from encode import Encoder
from evaluator import Evaluator
from sorter import Sorter
from model.classic_eval import eval



weights = "T15000depth2_weights"

encoder = Encoder()
evaluator = Evaluator(NeuralNetwork, weights, encoder.encode)
table = Table()
sorter = Sorter()
searcher = Searcher(evaluator.evaluate, sorter, table)

test = Board("rnbqr1k1/pp3pbp/3p1np1/2p5/2PNP3/2N1B3/PPQ1BPPP/R3K2R w KQ c6 0 10")
# "Q7/8/8/2p1k3/2P5/1P1P4/5PR1/2K5 w - - 1 51" good mate in 3 checker

reader = chess.polyglot.open_reader("opening.bin")
in_opening = True


while True:
    best_line = []
    score = 0
    t2 = 0
    t1 = 0

    if in_opening:
        entry = reader.get(test)
        if entry is not None:
            best_line = [entry.move]
        else:
            in_opening = False
    if not in_opening:
        t1 = perf_counter()
        score, best_line = searcher.iterative_deepening(test, 4)
        # score, best_line = searcher.nmax(test, 5, 1, -inf, inf)
        t2 = perf_counter()
        

    # table.clear()

    for move in best_line:
        print(move)
        test.push(move)
        print(test)

    print(evaluator.evaluate(test))

    for i in range(len(best_line)):
        test.pop()

    evaluator.profile()
    evaluator.reset()
    sorter.profile()
    sorter.reset()
    table.profile()
    table.reset()
    print("CUTS:", searcher.cut)
    print("TEST TIME", searcher.test_time)
    searcher.cut = 0

    print("Time: ", t2 - t1)
    print("Score:", float(score))
    print("Depth:", len(best_line))
    print("Best Move: ", best_line[0])

    test.push(best_line[0])
    print(test)

    if test.is_checkmate():
        print("BOT WINS HAHAHAHAHAHAHAHAHAHAHA")
        exit()

    flag = True
    next_move = input("next move: ")
    while flag:
        try:
            test.push_san(next_move)
            flag = False
        except:
            next_move = input("next move: ")

    with open("saved.txt", "w") as file:
        file.write(test.fen())
 
    
    print(test)
