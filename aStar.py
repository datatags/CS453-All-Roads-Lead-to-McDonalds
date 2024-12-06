from WeightedGraph import *
import heapq
import math
import time

class Cell:
    def __init__(self):
        self.parent_i = None  # Parent node
        self.parent_j = None  # Parent node
        self.f = float('inf')  # Total cost of the node (g + h)
        self.g = float('inf')  # Cost from start to this node
        self.h = 0  # Heuristic cost from this node to destination

def is_destination(node, dest):
    return node == dest

# Modify this to use graph's method for neighbors and weights
def get_neighbors(graph, node):
    return graph.adj_matrix.get(node, {})

def calculate_h_value(node, dest):
    # Example heuristic: You can use any heuristic here. If you have a specific heuristic, change this.
    return abs(node - dest)  # Example for nodes that are numeric

def trace_path(came_from, dest):
    path = []
    current = dest
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path

def a_star_search(graph, start, dest):
    # Initialize the open list (priority queue) and closed list
    open_list = []
    heapq.heappush(open_list, (0, start))  # (f_score, node)
    
    # Initialize g, f scores, and the came_from dictionary
    g_scores = {start: 0}
    f_scores = {start: calculate_h_value(start, dest)}  # f = g + h
    came_from = {}

    # Main loop of A* search algorithm
    while open_list:
        _, current = heapq.heappop(open_list)

        # If we reached the destination
        if is_destination(current, dest):
            path = trace_path(came_from, dest)
            print("Path found:", path)
            return path
        
        # Explore neighbors
        for neighbor, weight in get_neighbors(graph, current).items():
            tentative_g_score = g_scores[current] + weight
            if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                came_from[neighbor] = current
                g_scores[neighbor] = tentative_g_score
                f_score = tentative_g_score + calculate_h_value(neighbor, dest)
                f_scores[neighbor] = f_score
                heapq.heappush(open_list, (f_score, neighbor))

    # If we get here, no path was found
    print("No path found")
    return None

if __name__ == "__main__":
    
    graph = WeightedGraph(0)
    graph.load_graph("rome_italy.pkl")
    start = 8430

    McDs_locations = [8389, 8390, 8391, 8392, 8393, 8394, 8395, 8396]
    for location in McDs_locations:
        start_time = time.perf_counter()
        path = a_star_search(graph, start, dest=location)  # For example, find the path to node 5
        end_time = time.perf_counter()
        McDs_time = end_time - start_time

        print("Time to find shortest path to McDonald's", location, ":", McDs_time)

