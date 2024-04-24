class Table():
   def __init__(self):
      self.positions = {}
      self.depth = {}
      self.count = 1

   def add(self, key, val, depth):
      self.positions[key] = val
      self.depth[key] = depth

   def get(self, key):
      score = self.positions.get(key)
      if score is not None:
         self.count += 1
      return score, self.depth.get(key)
   
   def reset(self):
      self.count = 1
   
   def profile(self):
      print("Table Count:", self.count)

   def clear(self):
      self.positions = {}
      self.depth = {}

      