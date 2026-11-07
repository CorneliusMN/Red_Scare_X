import sys


class Graph:
    def __init__(self, n, m, r, s, t, names, red, adj, directed):
        self.n = n
        self.m = m
        self.r = r
        self.s = s # int id of start vertex
        self.t = t # int id of end vertex
        self.names = names # id -> name
        self.red = red # list[bool], indexed by id
        self.adj = adj # id -> list of out-neighbours
        self.directed = directed


def read_graph(lines):
    """Parse a graph from an iterable of lines (a file object or sys.stdin)."""
    it = iter(lines)

    def next_line():
        for line in it:
            line = line.strip()
            if line:
                return line
        raise ValueError("unexpected end of input")

    n, m, r = map(int, next_line().split())
    s_name, t_name = next_line().split()

    names, red, index = [], [], {}
    for i in range(n):
        parts = next_line().split()
        name = parts[0]
        index[name] = i
        names.append(name)
        red.append(len(parts) > 1 and parts[1] == "*")

    adj = [[] for _ in range(n)]
    directed = None
    for _ in range(m):
        u, op, v = next_line().split()
        if op not in ("--", "->"):
            raise ValueError("bad edge operator: " + op)
        arc = op == "->"
        if directed is None:
            directed = arc
        elif directed != arc:
            raise ValueError("mixed directed and undirected edges")
        adj[index[u]].append(index[v])
        if not arc:
            adj[index[v]].append(index[u])

    if sum(red) != r:
        raise ValueError("header says r=%d but %d vertices are red" % (r, sum(red)))
    return Graph(n, m, r, index[s_name], index[t_name], names, red, adj, bool(directed))


def load(path):
    with open(path) as f:
        return read_graph(f)


if __name__ == "__main__":
    g = load(sys.argv[1]) if len(sys.argv) > 1 else read_graph(sys.stdin)
    print("n=%d m=%d r=%d s=%s t=%s %s" % (
        g.n, g.m, g.r, g.names[g.s], g.names[g.t],
        "directed" if g.directed else "undirected"))