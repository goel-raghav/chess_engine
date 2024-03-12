import cProfile
import chess
import math
from time import perf_counter

# test = chess.Board()
# cProfile.run('nmax(test, 4, True, -math.inf, math.inf, perf_counter(), 10000)', "search_profile")


import pstats
from pstats import SortKey
with open("profile.txt", "w") as f:
    ps = pstats.Stats("search_profile", stream=f)
    ps.strip_dirs().sort_stats(SortKey.TIME).print_stats(20)