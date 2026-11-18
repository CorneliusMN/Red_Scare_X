import sys
import glob
import os

from graph import load
from dijkstra import dijkstra
import time


def few(g):
    #converting graph to weighted adjacency list
    weighted_adj = [[] for _ in range(g.n)]

    for u in range(g.n):
        for v in g.adj[u]:
            weight = 1 if g.red[v] else 0
            weighted_adj[u].append([v, weight])

    #run dijkstra
    dist = dijkstra(weighted_adj, g.s)

    #check if path, if no we do -1
    if dist[g.t] == float('inf'):
        return -1

    # else we return path, checking if s is red, since it can be
    return dist[g.t] + (1 if g.red[g.s] else 0)

def run(name, g):
    start = time.perf_counter()
    ans = few(g)                                # only the algorithm is timed
    elapsed = time.perf_counter() - start
    line = f"{name} {ans} {elapsed:.4f}s"        # name, result, time on one line
    print(line)
    return line


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))   # the code/ folder
    data_dir = os.path.join(base, "..", "data")
    out_dir = os.path.join(base, "results")

    if len(sys.argv) > 1:  # one file: python3 none.py ../data/G-ex.txt
        path = sys.argv[1]
        run(os.path.basename(path)[:-4], load(path))    # prints only
    else:                  # no file: run all instances
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "few_results.txt"), "w") as f:
            for path in sorted(glob.glob(os.path.join(data_dir, "*.txt"))):
                line = run(os.path.basename(path)[:-4], load(path))
                f.write(line + "\n")
      