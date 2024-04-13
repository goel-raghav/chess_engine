from chess import Board
from chess.polyglot import zobrist_hash as hash


from math import inf

from encode import encode

from model.small_model import NeuralNetwork
from evaluator import Evaluator
from sorter import Sorter
from transposition_table import Table


evaluator = Evaluator(NeuralNetwork, "small_model_weights", encode)
sorter = Sorter()
table = Table()

print('Ready')

def qsearch(board: Board, color, a, b, depth):
    score = -inf
    best_move = []

    moves = board.legal_moves
    moves = filter(lambda move: board.is_capture(move), moves)
    moves = sorter.sort(moves, board)

    if len(moves) == 0 or depth == 0:
        # key = hash(board)
        # table_score, _ = table.get(key)
        # if table_score is not None:
        #     return table_score * color, []
        score, _ = evaluator.evaluate(board)
        # table.add(hash(board), score, 0)
        return score * color, []

    for move in moves:
        board.push(move)
        e, line = qsearch(board, -1 * color, -b, -a, depth - 1)
        e *= -1
        if e > score:
            score = e
            best_move = [move] + line
        board.pop()
        
        a = max(a, score)
        if a >= b:
            break

    

    return score, best_move

def nmax(board: Board, depth, color, a, b):
    if depth == 0:
        score, _ = evaluator.evaluate(board)
        return score * color, []
    
    score = -inf
    best_move = []

    moves = board.legal_moves
    if moves is None:
        if board.is_checkmate():
            return 100 * color
        return 0

    moves = sorter.sort(moves, board)

    


    ''' still in testing
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
    # # still in testing '''

    for move in moves:
        board.push(move)
        key = hash(board)
        table_score, table_depth = table.get(key)
        if table_depth is not None and table_depth >= depth:
            e = table_score
            line = []
        else:
            e, line = nmax(board, depth-1, -1 * color, -b, -a)
            e *= -1
        if e > score:
            score = e
            best_move = [move] + line

        board.pop()
        
        a = max(a, score)
        if a >= b:
            sorter.shift_killer_move(move, board)
            break
    
    table.add(hash(board), score, depth)
    return score, best_move

def iterative_deepening(board: Board, max_depth):
    for i in range(max_depth):
        score, best_line = nmax(board, i+1, 1, -inf, inf)
        print(best_line)
        sorter.prev_best_line = best_line
    return score, best_line
    
def profile():
    print("Amount of evaluations: ", evaluator.eval_count)
    print("Total time by network predictions: ", evaluator.pred_time)
    print("Average predict time: ", evaluator.pred_time / evaluator.eval_count)
    print("Total eval time:", evaluator.eval_time)
    print("Total sort time: ", sorter.sort_time)

    evaluator.reset()
    sorter.reset()
