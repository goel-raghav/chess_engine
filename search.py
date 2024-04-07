from chess import Board

from math import inf

from encode import encode

from model.neural_network import NeuralNetwork
from evaluator import Evaluator
from sorter import Sorter

evaluator = Evaluator(NeuralNetwork, "test_model_weights1", encode)
sorter = Sorter()

print('Ready')
    
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
    global test_time
    if depth == 0:
        score, _ = evaluator.evaluate(board)
        return score * color, []
    
    score = -inf
    best_move = []

    moves = board.legal_moves
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

    return score, best_move
    
def profile():
    print("Amount of evaluations: ", evaluator.eval_count)
    print("Total time by network predictions: ", evaluator.pred_time)
    print("Average predict time: ", evaluator.pred_time / evaluator.eval_count)
    print("Total eval time:", evaluator.eval_time)
    print("Total sort time: ", sorter.sort_time)

    evaluator.reset()
    sorter.reset()
