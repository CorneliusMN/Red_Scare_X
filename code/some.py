import sys
from collections import deque
from graph import load
import glob
import os


# BFS to find if there is a path from s (source) to t (target)
def bfs(g, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in g.adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited


# Topological ordering of the graph G to know which order to process in and whether G is a DAG or not.
def topo_order(g):
    indeg = [0] * g.n
    for u in range(g.n):
        for v in g.adj[u]:
            indeg[v] += 1
    queue = deque(v for v in range(g.n) if indeg[v] == 0)
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in g.adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)            

    return order if len(order) == g.n else None


# Dynamic programming to find maximum number of red nodes in any path from s to t using longest-path approach assigning weight 1 to red and 0 to black
def many_dag(g, order):
    NEG = float("-inf")
    dp = [NEG] * g.n # list with one entry per node in G initialized with negative infinity
    dp[g.s] = int(g.red[g.s]) # check if node s is red (assign True, 1) or black (assign False, 0)
    for u in order: # go through every node in G using topological order
        if dp[u] == NEG: # if u can't be reached from s, skip it
            continue
        for v in g.adj[u]: # look at the neighbors of u (those having an edge coming from u) 
            dp[v] = max(dp[v], dp[u] + g.red[v]) # you compare the best score found from reaching v to the score of v reached through u. Pick the best one
    return dp[g.t] # return maximum number of red nodes from s to t


# Max flow
def path_through(g, w):
    n = g.n # number of nodes
    # Instead of limiting edges, we do so with nodes. Each node is split into two to turn it into an edge, so node v is split into in(v) and out(v)
    T = 2 * n 
    N = 2 * n + 1  

    to = [] # where edge e points
    cap = [] # how much capacity edge e has (left)
    out_edges = [[] for _ in range(N)] # list of edge numbers leave node x

    def add_edge(a, b, c): # every time you call this function you add and edge from a to b with capacity c (forward edge) and edge b to a with capacity 0 (backward edge)
        out_edges[a].append(len(to))
        to.append(b)
        cap.append(c)  
        out_edges[b].append(len(to))
        to.append(a)
        cap.append(0) 

    for v in range(g.n): # build edges from every node v in G that is not the node w
        if v != w:
            add_edge(2 * v, 2 * v + 1, 1)   

    for u in range(g.n): # build edges from every node v in G which is neighbor of u
        for v in g.adj[u]:
            add_edge(2 * u + 1, 2 * v, 1)   

    add_edge(2 * g.s + 1, T, 1) # build edges touching s
    add_edge(2 * g.t + 1, T, 1) # build edges touching t

    source = 2 * w + 1 # where the flow starts (form w)
    flow = 0 # flow counts how many units have reached T (the sink)

    while flow < 2: # the s,t path through w has two halves: one from w to s and one form w to t. Each half is one path leaving from w and each unit of flow is also one path leaving from w. Therefore, you need two flows, one from w to s and one from w to t.
        # A list with one entry per flow node, all starting at -1 (“no edge yet”). During the BFS, parent_edge[y] is filled in with the edge number we used to arrive at node y. After the BFS finishes, we follow these entries backwards from T to rebuild the exact path that was found, so we know which capacities to update. -1 is just a placeholder because real edge numbers start at 0.
        parent_edge = [-1] * N 
        seen = [False] * N
        seen[source] = True
        queue = deque([source])

        # standard BFS. It only follows an edge if its capacity is > 0 and it stops as soon as T (sink) is reached
        while queue and not seen[T]:
            x = queue.popleft()
            for e in out_edges[x]:
                y = to[e]
                if cap[e] > 0 and not seen[y]:
                    seen[y] = True
                    parent_edge[y] = e
                    queue.append(y)

        # if T is never reached, you leave the loop with whichever flow we have
        if not seen[T]:
            break  

        # backwards path from T (sink) to the source
        y = T
        while y != source:
            e = parent_edge[y]
            cap[e] -= 1     
            cap[e ^ 1] += 1    
            y = to[e ^ 1] 
        flow += 1

    return flow == 2 # flow of 2 means that one unit reached s and one reached t with no shared vertex, which means that there is a path form s,t through w (the red vertex)
    

def some(g):
    if g.s == g.t: # s and t are the same
        return g.red[g.s] # bool instead of int of many
    if g.t not in bfs(g, g.s): # no path from s to t
        return False # False instead of -1 of many
    if g.r == 0: # no red nodes
        return False # False instead of 0 of many
    if g.directed: # Case with DAG
        order = topo_order(g)
        if order is not None:
            return many_dag(g, order) >= 1 # added >= 1 to return a boolean answer
        return "?" # case with a cycle
    for w in range(g.n): # try every red node, not only when r == 1
        if g.red[w]:
            if w == g.s or w == g.t: # red node is s or t
                return True # True instead of 1 of many
            if path_through(g, w):
                return True
    return False # False instead of ? of many


if __name__ == "__main__":
    if len(sys.argv) > 1: # one file: python3 some.py data/G-ex.txt
        print(some(load(sys.argv[1])))
    else: # no file: run all instances
        for path in sorted(glob.glob("data/*.txt")):
            name = os.path.basename(path)[:-4]
            print(name, some(load(path)))