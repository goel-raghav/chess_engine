class Table():
    def __init__(self):
      self.positions = {}
      self.depth = {}

    def add(self, key, val, depth):
       self.positions[key] = val
       self.depth[key] = depth

    def get(self, key):
       return self.positions.get(key), self.depth.get(key)