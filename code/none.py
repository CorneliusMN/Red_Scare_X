import sys
from collections import deque
from graph import load
import glob
import os
import time


def none(g):
    dist = [-1] * g.n # at the beginning no nodes are visited
    dist[g.s] = 0 # the path containing only the source node s has a length of 0
    queue = deque([g.s]) # start BFS form s
    while queue:
        u = queue.popleft()
        if u == g.t: # we reached T
            return dist[u]
        if g.red[u] and u != g.s: # skip red nodes
            continue
        for v in g.adj[u]: # look at every neighbor of u
            if dist[v] == -1: # only visit nodes not visited before
                dist[v] = dist[u] + 1
                queue.append(v)
    return -1 # either there is no path from s to t or every s,t path passes through a red internal node

def run(name, g):
    start = time.perf_counter()
    ans = none(g)                                # only the algorithm is timed
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
        with open(os.path.join(out_dir, "none_results.txt"), "w") as f:
            for path in sorted(glob.glob(os.path.join(data_dir, "*.txt"))):
                line = run(os.path.basename(path)[:-4], load(path))
                f.write(line + "\n")
            