from collections import deque
from graph import load
import glob
import os


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


with open("alternate_results.txt", "w") as f:
    for path in sorted(glob.glob("data/*.txt")):
        name = os.path.basename(path)[:-4]
        f.write(name + " " + str(int(alternate(load(path)))) + "\n")