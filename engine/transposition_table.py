from time import perf_counter
from math import inf
from chess.polyglot import zobrist_hash as hash


class Table():
   def __init__(self):
      self.index = {}
      self.score = []
      self.depth = []
      self.count = []

      self.hits = 1
      self.time = 0
      self.MAX_SIZE = 1000
      self.current_index = 0

   def add(self, key, score, depth):
      start_time = perf_counter()

      if len(self.score) < self.MAX_SIZE:
         self.index[key] = self.current_index
         self.score.append(score)
         self.depth.append(depth)
         self.count.append(0)
         self.current_index += 1
      else:
         min_count_game = min(self.index, key=lambda i: self.count[self.index[i]])
         min_index = self.index[min_count_game]
         del self.index[min_count_game]
         self.index[key] = min_index
         self.score[min_index] = score
         self.depth[min_index] = depth
         self.count[min_index] = 0


      end_time = perf_counter()

      self.time += end_time - start_time

   def get(self, key):
      start_time = perf_counter()

      index = self.index.get(key)
      score, depth = None, None
      if index is not None:
         self.hits += 1
         score = self.score[index]
         depth = self.depth[index]
         self.count[index] += 1

         

      end_time = perf_counter()
      self.time += end_time - start_time
      return score, depth
   
   def reset(self):
      self.hits = 1
      self.time = 0
   
   def profile(self):
      print("Table Count:", self.hits)
      print("Table Time:", self.time)
      if len(self.count) > 0:
         print("Max hit:", max(self.count))
         print("Min hit:", min(self.count))
         print("Len table:", len(self.count))
         print(" ")

   def clear(self):
      self.index = {}
      self.score = []
      self.depth = []
      self.count = []

      