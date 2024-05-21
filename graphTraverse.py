import networkx as nx
import time as t
import random


def waypointPicker(G, points=2, isolates=False):
    
    # TODO: find only the nodes with 1 connection (i.e. dead ends) -- is this useful/desired?

    #TODO : let A go to destination C through waypoint B
    nodes = random.sample(list(G.nodes()), points)

    start = nodes[0]
    end = nodes[-1]
    #waypoints = [start, end]

    return nodes

def astar(G, start, end):
    try:
        path = nx.astar_path(G, start, end)
    except (nx.exception.NetworkXNoPath):
        print ("Could not reach the endpoint")
    return path

# TODO
# from any point, allow jumping at a high cost and compare to non-jump version
def hybridDijkstra(G, start, end):
    try:
        path = nx.dijkstra_path(G, start, end)
    except (nx.exception.NetworkXNoPath):
        print ("Could not reach the endpoint")
    return path