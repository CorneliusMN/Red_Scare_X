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


base = os.path.dirname(os.path.abspath(__file__))   # the code/ folder
data_dir = os.path.join(base, "..", "data")
out_dir = os.path.join(base, "results")
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, "alternate_results.txt"), "w") as f:
    for path in sorted(glob.glob(os.path.join(data_dir, "*.txt"))):
        name = os.path.basename(path)[:-4]
        g = load(path)                                   # parsing, not timed

        start = time.perf_counter()
        ans = alternate(g)                               # only the algorithm is timed
        elapsed = time.perf_counter() - start

        line = f"{name} {int(ans)} {elapsed:.4f}s"
        f.write(line + "\n")
        print(line)