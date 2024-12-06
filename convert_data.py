#!/usr/bin/python3

#coded by Dietrich Zacher for WSU-TC Fall 2024 CPT_S 453 Graph Theory

# GitHub Copilot assisted in the trivial aspects of writing this file,
# such as generation of loops and formulas, as well as providing a bare-bones
# implementation of the class OSMHandler as a starting point.

import math
import osmium
from collections import namedtuple
from WeightedGraph import WeightedGraph

BaseNode = namedtuple("BaseNode", ["lon", "lat"])

center_x = 12.4922
center_y = 41.8907
distance =  0.02

class CustomNode:
    def __init__(self, node):
        self.id = node.id
        self.lon = node.location.lon
        self.lat = node.location.lat
        self.refs = 0

class CustomWay:
    def __init__(self, way):
        self.id = way.id
        self.speed = int(way.tags["maxspeed"])
        self.nodes = []
    
    def distance(self):
        dist = 0
        for i in range(len(self.nodes) - 1):
            node1 = self.nodes[i]
            node2 = self.nodes[i + 1]
            dist += math.sqrt((node1.lon - node2.lon)**2 + (node1.lat - node2.lat)**2)
        return dist

    def cost(self):
        return self.distance() / self.speed

class OSMHandler(osmium.SimpleHandler):
    def __init__(self, center_x, center_y, distance):
        osmium.SimpleHandler.__init__(self)
        self.center_x = center_x
        self.center_y = center_y
        self.distance = distance
        self.nodes = {}
        self.ways = []
        self.mcd = []
        self.col = []

    def node(self, n):
        if self.is_within_distance(n.location.lon, n.location.lat):
            customnode = CustomNode(n)
            self.nodes[n.id] = customnode
            if "name" in n.tags and n.tags["name"] == "McDonald's":
                self.mcd.append(customnode)

    def way(self, w):
        if w.tags.get("name", "") == "Colosseo": # Italian name for Colosseum or something?
            for n in w.nodes:
                self.col.append(self.nodes[n.ref])
            return
        if "highway" not in w.tags or "maxspeed" not in w.tags:
            return
        tag = w.tags["highway"]
        if tag not in ["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "service", "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"]:
            return
        if all(n.ref in self.nodes for n in w.nodes):
            customway = CustomWay(w)
            self.ways.append(customway)
            for n in w.nodes:
                customnode = self.nodes[n.ref]
                customway.nodes.append(customnode)
                customnode.refs += 1

    def is_within_distance(self, lon, lat):
        return (abs(lon - self.center_x) <= self.distance and
                abs(lat - self.center_y) <= self.distance)

# sqrt is relatively expensive, so we avoid it when we can
def distanceSquared(node1, node2):
    return (node1.lon - node2.lon)**2 + (node1.lat - node2.lat)**2

print("Parsing OSM file...")
handler = OSMHandler(center_x, center_y, distance)
handler.apply_file('rome_italy.osm.pbf')

print(f"Nodes: {len(handler.nodes)}")
print(f"Ways: {len(handler.ways)}")

# Count node refs
any_refs = 0
two_refs = 0
for node in handler.nodes.values():
    if node in handler.mcd or node in handler.col:
        continue
    if node.refs > 0:
        any_refs += 1
    if node.refs > 1:
        two_refs += 1

any_refs += len(handler.mcd) + len(handler.col)
two_refs += len(handler.mcd) + len(handler.col)

print(f"Nodes with any refs: {any_refs}, with more than one ref: {two_refs}, McDonald's: {len(handler.mcd)}, Colosseum: {len(handler.col)}")

import matplotlib
matplotlib.use('Agg') # Allows running without an X server, for ease of use on elec
import matplotlib.pyplot as plt
plt.figure(dpi=600) # Increase DPI so graph is less blurry, default resolution is 640x480 :(

print("Creating graph...")
node_index_mapping = {}

i = 0

for node in handler.nodes.values():
    if node.refs > 0:
        node_index_mapping[node.id] = i
        i += 1
for mcd in handler.mcd:
    node_index_mapping[mcd.id] = i
    i += 1
for col in handler.col:
    node_index_mapping[col.id] = i
    i += 1

graph = WeightedGraph(len(node_index_mapping))
for way in handler.ways:
    for i in range(len(way.nodes) - 1):
        node1 = way.nodes[i]
        node2 = way.nodes[i + 1]
        if graph.get_edge_weight(node_index_mapping[node1.id], node_index_mapping[node2.id]) != 0:
            print(f"Unexpected duplicate edge: {node1.id} <-> {node2.id}")
            continue
        distance = math.sqrt(distanceSquared(node1, node2))
        #print(f"Adding edge {node1.id} {node2.id} {distance} which is at index {node_index_mapping[node1.id]} {node_index_mapping[node2.id]}")
        graph.add_edge(node_index_mapping[node1.id], node_index_mapping[node2.id], distance / way.speed)

print("Plotting OSM data...")
# Plot nodes
for node in handler.nodes.values():
    if node.refs > 0:
        if node not in handler.mcd and node not in handler.col:
            plt.plot(node.lon, node.lat, 'bo', markersize=2)

def find_closest_node(node):
    min_dist_sqr = float('inf')
    closest_node = None
    for n_id in node_index_mapping:
        if n_id == node.id:
            continue
        n = handler.nodes[n_id]
        dist_sqr = distanceSquared(node, n)
        if dist_sqr < min_dist_sqr:
            min_dist_sqr = dist_sqr
            closest_node = n
    return closest_node, math.sqrt(min_dist_sqr)

# Plot ways
for way in handler.ways:
    lons = [node.lon for node in way.nodes]
    lats = [node.lat for node in way.nodes]
    plt.plot(lons, lats, 'r-')

# Plot McDonald's
for mcd in handler.mcd:
    plt.plot(mcd.lon, mcd.lat, 'go', markersize=5)
    print(f"McDonald's at {node_index_mapping[mcd.id]}")
    if mcd.refs < 1: # Not referenced in the filtered set of ways
        closest_node, distance = find_closest_node(mcd)
        #print(f"Closest node to McDonald's {node_index_mapping[mcd.id]} at {distance} km")
        # Average walking speed is ~5 km/h
        graph.add_edge(node_index_mapping[mcd.id], node_index_mapping[closest_node.id], distance / 5)
        plt.plot([mcd.lon, closest_node.lon], [mcd.lat, closest_node.lat], 'g-')

# Plot Colosseum
for col in handler.col:
    plt.plot(col.lon, col.lat, 'mo', markersize=2)
    #print(f"Colosseum at {node_index_mapping[col.id]}")
    if col.refs < 1: # Not referenced in the filtered set of ways
        closest_node, distance = find_closest_node(col)
        # Average walking speed is ~5 km/h
        graph.add_edge(node_index_mapping[col.id], node_index_mapping[closest_node.id], distance / 5)

graph.num_nodes += 1
col_center_index = graph.num_nodes - 1
print(f"Root node is at {col_center_index}")

# The colosseum boundary isn't defined as a complete ellipse, so we
# take the average of the extremes to get closer to the real center.
col_min_lat = min([col.lat for col in handler.col])
col_max_lat = max([col.lat for col in handler.col])
col_min_lon = min([col.lon for col in handler.col])
col_max_lon = max([col.lon for col in handler.col])
col_center_lat = (col_min_lat + col_max_lat) / 2
col_center_lon = (col_min_lon + col_max_lon) / 2
col_center = BaseNode(col_center_lat, col_center_lon)

# Assume that we start in the center of the colosseum
# and can exit via any of the points that defines the
# boundary of the colosseum by walking.
for col in handler.col:
    distance = math.sqrt(distanceSquared(col, col_center))
    graph.add_edge(col_center_index, node_index_mapping[col.id], distance / 5)
    plt.plot([col_center_lon, col.lon], [col_center_lat, col.lat], 'm-')

plt.plot(col_center_lon, col_center_lat, 'yo', markersize=2)

graph.save_graph("rome_italy.pkl")

print("Graph is ready!")

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('OSM Nodes and Ways')
print("Saving png...")
plt.savefig('osm.png')
print("Saving pdf...")
plt.savefig('osm.pdf')
