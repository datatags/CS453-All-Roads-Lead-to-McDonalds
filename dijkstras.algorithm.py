from WeightedGraph import *
import heapq
import math
import time

def build_tree(T, r):
    """Builds a dictionary representing the tree from the list of parents."""
    n = len(T)
    tree = {i: [] for i in range(n)}  # Create an empty list for each node
    root = r

    # Construct the tree
    for child, parent in enumerate(T):
        if parent != -1:
            tree[parent].append(child)

    return tree, root

def print_tree(T, d, r):
    tree, root = build_tree(T, r)
    def print_tree(node, level=0):
        indent = "  " * level
        print(f"{indent}- Node {node} (distance: {d[node]})")
        for child in tree[node]:
            print_tree(child, level + 1)

    if root is not None:
        print("root is not None")
        print_tree(root)
    else:
        print("No root found")

def Dijkstras(g, r, dest=None):
    """
    Dijkstra's algorithm to find the shortest path from source node `r` to destination node `dest`.
    - g: The weighted graph
    - r: The root/source node
    - dest: The destination node (optional)
    
    Returns:
    - T: Parent node list (for path reconstruction)
    - d: Distance list (shortest distance from source to each node)
    - path: The list of nodes representing the shortest path from source to destination (if dest is provided)
    - total_distance: The total distance from source to destination (if dest is provided)
    """
    root = r
    Visited = [False] * g.num_nodes
    T = [-1] * g.num_nodes  # Parent list
    pq = []  # Priority queue
    d = [math.inf] * g.num_nodes  # Distance list
    d[root] = 0
    heapq.heappush(pq, (0, root))  # Insert the root node into the priority queue

    while pq:
        # Pop the node with the smallest distance
        weight, node = heapq.heappop(pq)

        if Visited[node]:
            continue

        Visited[node] = True

        for i in range(g.num_nodes):
            if not Visited[i] and g.get_edge_weight(node, i) != 0:  # There's an edge between node and i
                new_weight = d[node] + g.get_edge_weight(node, i)
                if new_weight < d[i]:
                    d[i] = new_weight
                    T[i] = node
                    heapq.heappush(pq, (d[i], i))

    # If a destination node is specified, reconstruct the path and return total distance
    path = []
    total_distance = None
    if dest is not None:
        # Backtrack from the destination node to the root using the parent list (T)
        current = dest
        while current != -1:
            path.append(current)
            current = T[current]
        path.reverse()  # Reverse to get the path from root to destination
        total_distance = d[dest]  # The total distance to the destination

    return T, d, path, total_distance

#Rome Italy
g = WeightedGraph(0)
g.load_graph("rome_italy.pkl")
r = 8430
#McD's at 8389, 8390, 8391, 8392, 8393, 8394, 8395, 8396

McDs_locations = [8389, 8390, 8391, 8392, 8393, 8394, 8395, 8396]
for location in McDs_locations:
    average_time = 0
    for i in range(10):
        start_time = time.perf_counter()
        T, d, path, total_distance = Dijkstras(g, r, dest=location)  # For example, find the path to node 5
        end_time = time.perf_counter()
        McDs_time = end_time - start_time
        average_time += McDs_time
    print(f"Time to find shortest path to McDonald's", location, ":", average_time/10)

    #print("Time to find shortest path to McDonald's", location, ":", McDs_time)
    #print_tree(T, d, r)
    print("Shortest Path from root to destination:", path)
    print(f"Total Distance from root to destination:", total_distance)
    print(f"Number of elements in the path: {len(path)}")
