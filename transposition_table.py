class Table():
    def __init__(self):
      self.positions = {}

    def add(self, key, val):
       self.positions[key] = val

    def get(self, key):
       return self.positions.get(key)