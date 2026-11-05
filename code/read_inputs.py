# Function to read txt file containing graph properties. 
import os

def read_graph(path):
    '''
    Input: path to the txt file containing graph in a specific format.
    Input format (txt file format): 
    line1 = n m r
    line2 = s t
    line3 to line(n+2) = <vertex name> * (star only if vertex is red)
    line(n+3) to line(n+m+2) = <vertex1> -- <vertex2> (for undirected edges) || <vertex1> -> <vertex2>

    Output: n, m, r, s, t, vertices, red, edges, adj, directed.
    Output format:
    n: number of vertices - INTEGER
    m: number of edges - INTEGER
    r: number of red vertices - INTEGER
    s: source vertex - STRING
    t: target vertex - STRING
    vertices: list of vertex names - LIST OF STRINGS        ex. ['Copenhagen', 'Odense', 'Ribe']
    red: set of red vertex names - SET OF STRINGS          ex. {'Odense', 'Ribe'}
    edges: list of edges (tuples) - LIST OF TUPLES         ex. [('Copenhagen', 'Odense'), ('Odense', 'Ribe')]
    adj: adjacency list (dictionary of sets) - DICTIONARY  ex. {'Copenhagen': {'Odense'}, 'Odense': {'Copenhagen', 'Ribe'}, 'Ribe': {'Odense'}}
    directed: boolean indicating if the graph is directed or not - BOOLEAN
    '''

    with open(path) as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    # integers
    n, m, r = map(int, lines[0].split())
    # strings
    s, t = lines[1].split()

    # vertices and red vertices (first N lines)
    vertices = []
    red = set()
    for line in lines[2:2 + n]:
        parts = line.split()
        vertices.append(parts[0])
        if len(parts) > 1 and parts[1] == "*":
            red.add(parts[0])

    # The rest of the lines
    edges = []
    directed = False
    adj = {v: set() for v in vertices}
    
    for line in lines[2 + n:2 + n + m]:
        if "->" in line:
            u, v = (x.strip() for x in line.split("->"))
            directed = True
            adj[u].add(v)
        else:
            u, v = (x.strip() for x in line.split("--"))
            adj[u].add(v)
            adj[v].add(u)
        edges.append((u, v))

    return n, m, r, s, t, vertices, red, edges, adj, directed



# 1. Example of usage in this file
for file_name in sorted(os.listdir("./data")):
    path = os.path.join("./data", file_name)

    n, m, r, s, t, vertices, red, edges, adj, directed = read_graph(path)
    #print(f"File: {file_name}, n: {n}, m: {m}, r: {r}, red: {len(red)}, directed: {directed}") 
    print(f"File: {file_name:<20} n: {n:>5}, m: {m:>6}, r: {r:>4}, red: {len(red):>4}, directed: {directed}")
   


# Example of usage from different file
# from read_inputs import read_graph
# n, m, r, s, t, vertices, red, edges, adj, directed = read_graph("./data/graph1.txt")
