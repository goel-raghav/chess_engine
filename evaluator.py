import torch
import chess
from time import perf_counter
from typing import Callable
from encode import Encoder

class Evaluator():
    def __init__(self, NeuralNetwork: torch.nn.Module, weights_path: str, encoder: Encoder):
        # set up NN
        self.network = NeuralNetwork()
        self.network.load_state_dict(torch.load(weights_path))
        self.network.eval()

        sample_input = torch.rand(1, 1, 8, 8)
        torch.jit.enable_onednn_fusion(True)
        self.network = torch.jit.trace(self.network, sample_input)
        self.network = torch.jit.freeze(self.network)
        self.network(sample_input)
        self.network(sample_input)

        # profiling
        self.eval_count = 1
        self.eval_time = 0
        self.pred_time = 0

        self.encoder = encoder
    
    def evaluate(self, board: chess.Board, root, updatable, color):
        eval_start_time = perf_counter()
        self.eval_count += 1

        pred_start_time = perf_counter()

        score = 0
        last_move = board.peek()

        

        if updatable:
            capture = self.encoder.make(root, last_move.from_square, last_move.to_square, board.piece_at(last_move.to_square), color)
            score = self.predict(root.reshape(1, 1, 8, 8))

            # if test_score != score:
            #     print("UPDATE ERROR")
            #     exit()

            self.encoder.unmake(root, last_move.from_square, last_move.to_square, board.piece_at(last_move.to_square), capture, color)
        else:
            cur_x = self.encoder.encode(board).reshape(1, 1, 8, 8)
            score = self.predict(cur_x)

        
            


        pred_end_time = perf_counter()
        self.pred_time += pred_end_time - pred_start_time

        eval_end_time = perf_counter()
        self.eval_time += eval_end_time - eval_start_time

        return score
        
        
    def predict(self, val):

        val = torch.from_numpy(val)
        val = val.float()
        with torch.no_grad():
            e = self.network(val)
        return e
    
    def reset(self):
        self.eval_count = 1
        self.eval_time = 0
        self.pred_time = 0

    def profile(self):
        print("Eval Count:", self.eval_count)
        print("Eval Time:", self.eval_time)
        print("Total Pred Time:", self.pred_time)
        print("Average Pred Time:", self.pred_time / self.eval_count)