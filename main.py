import graphGenerate
import graphTraverse

import networkx as nx
import numpy as np
import time

from flask import Flask

nNodes = np.random.randint(5,100)
nConnections = np.random.randint(nNodes-1, int(nNodes * 1.5))

print (f"Nodes:{nNodes}, Connections:{nConnections}")
[myGraph, tags] = graphGenerate.node_generator(nNodes,nConnections,strictNoClusters=True)
nodePositions = graphGenerate.displayGraph(myGraph, tags)

waypoints = graphTraverse.waypointPicker(myGraph)
print (f"Path: {tags[waypoints[0]]} to {tags[waypoints[-1]]}")

start = waypoints[0]
end = waypoints[-1]

t0 = time.perf_counter()
path = nx.dijkstra_path(myGraph, start, end)
t1 = time.perf_counter()
print (f"Dijkstra solved in {round((t1-t0) * 1000,4)}ms -- {path}")

graphGenerate.displayGraph(myGraph, tags, nodePositions, path, NODISPLAY=False)

t0 = time.perf_counter()
path = graphTraverse.astar(myGraph, start,end)
t1 = time.perf_counter()
print (f"A* solved in {round((t1-t0) * 1000,4)}ms -- {path}")

t0 = time.perf_counter()
path = nx.bellman_ford_path(myGraph, start,end)
t1 = time.perf_counter()
print (f"BF solved in {round((t1-t0) * 1000,4)}ms -- {path}")


