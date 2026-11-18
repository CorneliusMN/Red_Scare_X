from collections import deque
from graph import load
import glob
import os
import time
import sys

def alternate(g):
    # 1 vertex
    if g.s == g.t: 
        return True

    visited = [False] * g.n  # [false,false,false...]
    visited[g.s] = True      # current vertex is true

    queue = deque()
    queue.append(g.s)  # append current vertex to queue

    # BFS from s
    while len(queue) > 0:
        u = queue.popleft()  

        for v in g.adj[u]:  # for each neighbour of u
            # skip visited
            # or if u,v are same color
            if visited[v] or g.red[u] == g.red[v]:
                continue

            # if v is the target node
            if v == g.t:
                return True

            # mark v as visited
            visited[v] = True
            queue.append(v)

    #cant reach t
    return False


def run(name, g):
    start = time.perf_counter()
    ans = alternate(g) # only the algorithm is timed
    elapsed = time.perf_counter() - start
    line = f"{name} {str(ans).lower()} {elapsed:.4f}s" # true/false
    print(line)
    return line, elapsed


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__)) # the code/ folder
    data_dir = os.path.join(base, "..", "data")
    out_dir = os.path.join(base, "results")

    if len(sys.argv) > 1: # one file: python3 alternate.py ../data/G-ex.txt
        path = sys.argv[1]
        run(os.path.basename(path)[:-4], load(path)) # prints only
    else: # no file: run all instances
        os.makedirs(out_dir, exist_ok=True)
        total = 0.0 # sum of algorithm times
        with open(os.path.join(out_dir, "alternate_results.txt"), "w") as f:
            for path in sorted(glob.glob(os.path.join(data_dir, "*.txt"))):
                g = load(path) # parsing, not timed
                line, elapsed = run(os.path.basename(path)[:-4], g)
                total += elapsed
                f.write(line + "\n")
            summary = f"TOTAL {total:.4f}s"
            print(summary)
            f.write(summary + "\n")
