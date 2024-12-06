#modified by Dietrich Zacher for WSU-TC Fall 2024 CPT_S 453 Graph Theory
#based on code provided by Dr. Sihui Li
import pickle

class WeightedGraph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.adj_matrix = {}

    def load_graph(self, filename):
        # Load a graph from a file
        with open(filename, "rb") as f:
            self.adj_matrix = pickle.load(f)
            self.num_nodes = len(self.adj_matrix)

    def save_graph(self, filename):
        # Save the graph to a file
        with open(filename, "wb") as f:
            pickle.dump(self.adj_matrix, f)

    def add_edge(self, node1, node2, w):
        # Add an undirected edge from node1 to node2
        if node1 not in self.adj_matrix:
            self.adj_matrix[node1] = {}
        if node2 not in self.adj_matrix:
            self.adj_matrix[node2] = {}
        self.adj_matrix[node1][node2] = w
        self.adj_matrix[node2][node1] = w

    def remove_edge(self, node1, node2):
        # Remove the edge between node1 and node2
        if node1 in self.adj_matrix:
            self.adj_matrix[node1][node2] = 0
        if node2 in self.adj_matrix:
            self.adj_matrix[node2][node1] = 0
    
    def get_edge_weight(self, node1, node2):
        # Return the weight of the edge from node1 to node2
        if node1 not in self.adj_matrix or node2 not in self.adj_matrix[node1]:
            return 0
        return self.adj_matrix[node1][node2]

    def num_edges(self):
        return 0
        # num_edges = 0
        # for i in range(self.num_nodes):
        #     for j in range(i+1, self.num_nodes):
        #         if self.adj_matrix[i][j] != 0:
        #             num_edges += 1
        # return num_edges

    def print_graph(self):
        # Print the adjacency matrix
        pass

if __name__ == "__main__":
    # use case
    test_graph = WeightedGraph(3)
    test_graph.add_edge(1, 0, 2)
    test_graph.add_edge(1, 2, 3)
    test_graph.print_graph()
    print(test_graph.num_edges())