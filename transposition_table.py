from time import perf_counter


class Table():
   def __init__(self):
      self.positions = {}
      self.depth = {}
      self.count = 1
      self.time = 0

   def add(self, key, val, depth):
      start_time = perf_counter()
      self.positions[key] = val
      self.depth[key] = depth
      end_time = perf_counter()
      self.time += end_time - start_time

   def get(self, key):
      start_time = perf_counter()
      score = self.positions.get(key)
      if score is not None:
         self.count += 1
      end_time = perf_counter()
      self.time += end_time - start_time
      return score, self.depth.get(key)
   
   def reset(self):
      self.count = 1
   
   def profile(self):
      print("Table Count:", self.count)
      print("Table Time:", self.time)
      print(" ")

   def clear(self):
      self.positions = {}
      self.depth = {}

      