import torch
import chess
from time import perf_counter
from typing import Callable

class Evaluator():
    def __init__(self, NeuralNetwork: torch.nn.Module, weights_path: str, encode: Callable):
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
        self.eval_count = 0
        self.eval_time = 0
        self.pred_time = 0

        self.encode = encode
    
    def evaluate(self, board: chess.Board):
        self.eval_count += 1
        eval_start_time = perf_counter()
        
        checkmate_score = 100
        if board.is_checkmate():
            if board.turn == chess.BLACK:
                checkmate_score *= -1

            eval_end_time = perf_counter()
            self.eval_time += eval_end_time - eval_start_time

            return checkmate_score, []
        
        cur_x = self.encode(board).reshape(1, 1, 8, 8)
        score = self.predict(cur_x)

        return score, []
        
        
    def predict(self, val):
        pred_start_time = perf_counter()
        val = torch.from_numpy(val)
        val = val.float()
        with torch.no_grad():
            e = self.network(val)
        pred_end_time = perf_counter()
        self.pred_time += pred_end_time - pred_start_time
        return e
    
    def reset(self):
        self.eval_count = 0
        self.eval_time = 0
        self.pred_time = 0