### THIS IMPLEMENTATION OF DIJKSTRA WAS DONE BY "GEEKSFORGEEKS" ALL CREDIT IS DUE TO THEM. LINK TO THEIR WEBSITE: https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/

import heapq

def dijkstra(adj, src):
    V = len(adj)

    # Min-heap storing {distance, vertex}
    pq = []

    # Initialize distances to infinity
    dist = [float('inf')] * V

    # Distance from source to itself is 0
    dist[src] = 0
    heapq.heappush(pq, (0, src))

    while pq:

        d, u = heapq.heappop(pq)

        # Skip outdated entries
        if d > dist[u]:
            continue

        # Traverse adjacent vertices
        for x in adj[u]:
            v = x[0]
            weight = x[1]

            # Update distance if a shorter path is found
            if dist[v] > d + weight:
                dist[v] = d + weight
                heapq.heappush(pq, (dist[v], v))

    return dist
