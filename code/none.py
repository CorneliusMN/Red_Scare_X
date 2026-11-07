import sys
from collections import deque
from graph import load
import glob
import os


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


if __name__ == "__main__":
    if len(sys.argv) > 1: # one file: python3 many.py data/G-ex.txt
        print(none(load(sys.argv[1])))
    else: # no file: run all instances
        for path in sorted(glob.glob("data/*.txt")):
            name = os.path.basename(path)[:-4]
            print(name, none(load(path)))