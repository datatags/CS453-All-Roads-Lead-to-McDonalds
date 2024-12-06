#!/usr/bin/python3
#coded by Tuff Hensen for WSU-TC Fall 2024 CPT_S 453 Graph Theory
from WeightedGraph import *
import heapq
import math
import pprint
import time

def Bellman_Ford(g, src):
    #initialize the required variables
    start = time.perf_counter()
    V = g.num_nodes #number of nodes
    min_distance = [(100000000.0, -1)] * V #the min distance array
    min_distance[src] = (0, src)

    #start the relaxation loop
    for i in range(V):
        #create an outer loop to check every vertex from 0 to V every time
        for u in range(V):
            #look at every edge connected to u
            for v, weight in g.adj_matrix[u].items():
                #if visited and min distance is lower this time, update the min distance
                if min_distance[u][0] != 100000000.0  and min_distance[u][0] + weight < min_distance[v][0]:
                    if i == V - 1: #if this is the final relaxation, there is a value-decreasing path
                        min_dist_list = list(min_distance[u])
                        min_dist_list[0] = -1
                        min_distance[u] = tuple(min_dist_list)
                    min_dist_list = list(min_distance[v])
                    min_dist_list[0] = min_distance[u][0] + weight
                    min_dist_list[1] = u
                    min_distance[v] = tuple(min_dist_list)
    end = time.perf_counter()
    print("TIME:", end-start)
    return min_distance

def findPath(bellman_ford, start, target):
    temp_result = [target]
    while target != start:
        dist, next = bellman_ford[target]
        target = next
        temp_result.append(target)
    steps = len(temp_result) - 1
    my_result = []
    while steps >= 0:
        my_result.append(temp_result[steps])
        steps = steps -1
    return my_result

def wrapper(g, start, target):
    Bellman = Bellman_Ford(g, start)
    short_path = findPath(Bellman, start, target)
    total_dist = Bellman[target][0]
    print("DISATNCE: ", total_dist, "PATH: ",short_path)
    return

g = WeightedGraph(0)
g.load_graph("rome_italy.pkl")
wrapper(g, 8430, 8389)

