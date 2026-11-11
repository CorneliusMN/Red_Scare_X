import sys
import glob
import os

from graph import load
from dijkstra import dijkstra


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


if __name__ == "__main__":
    if len(sys.argv) > 1: # one file: python3 few.py data/G-ex.txt
        print(few(load(sys.argv[1])))
    else: # no file: run all instances
        for path in sorted(glob.glob("../data/*.txt")):
            name = os.path.basename(path)[:-4]
            print(name, few(load(path)))