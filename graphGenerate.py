import string
import random
import sys
import datetime
import math
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import csv

def tags_generator(n, tagLength):
	# Generate some number of dummy tags
	tagsDict = {}
	for i in range(n):
		id = id_generator(tagLength)
		while (id in tagsDict.values()):
			id = id_generator(tagLength)
		tagsDict[i] = id
	return tagsDict

def name_generator(n, source):
	with open(source, "r", newline='') as f:
		csv_reader = csv.reader(f)
		names = list(csv_reader)
	tagsDict = {}
	for i in range(n):
		id = random.choice(names[0])
		while (id in tagsDict.values() and (len(names[0]) >= n)):
			id = random.choice(names[0])
		tagsDict[i] = id
	return tagsDict

# only uppercase hex	
def id_generator(size=24, chars=(string.hexdigits.replace("abcdef",""))):
    # return random hex string 24 chars long
    return ''.join(random.choice(chars) for _ in range(size))

def node_generator(numNodes=5,numConnections=6, strictNoClusters=True):
	if numNodes > numConnections + 1:
		print ("Valid number of connections not specified; setting to ",(numNodes-1))
		numConnections = numNodes - 1
		exclusters = set()


	if ((not strictNoClusters) or (numNodes > 60)):
		G = nx.gnm_random_graph(numNodes, numConnections, directed=False)

	else:
		while 1:
			# uses Erdos-Renyi randomization model
			G = nx.gnm_random_graph(numNodes, numConnections, directed=False)
			components = list(nx.connected_components(G)) # list because it returns a generator
			
			# get largest group -- sort by size of cluster and get first element		
			components.sort(key=len, reverse=True)
			largest = components.pop(0)
			
			# keep generating until there are no multiple isolate clusters
			exclusters = set( g for cc in components for g in cc )
			if len(exclusters) == 0: 
				break

		

	G.remove_nodes_from(list(nx.isolates(G))) # get rid of lone nodes that make no sense in terms of navigation
	G = nx.convert_node_labels_to_integers(G)
	# for each node, assign a tag, label, weight
	# not using C struct-style because it gets nasty in python (array of
	# dictionaries)
	labels={}
	weights={}
	print("node\tdegree\tclustering\tweight\ttag\n")
	tags = name_generator(G.number_of_nodes(), 'planetNames_40k.csv')
	metadata = {}
	for v in G.nodes():
		labels[v]=v
		# weighted NODES, not connections -- may be desired at some point
		weights[v]=round(random.uniform(0,1),2)
		# TODO: further processing of weights?
		print('%s\t%d\t%f\t%s\t%s' % (v, nx.degree(G, v), nx.clustering(G,v),weights[v],tags[v]))

	for (u,v,w) in G.edges(data=True):
		w['weight'] = round(random.uniform(0.1,1),2)

	return [G, tags]

def displayGraph(G, tags, nodePos={}, history=[], NODISPLAY=False):
	numNodes = G.number_of_nodes()
	weights = [G[u][v]['weight'] for u,v in G.edges()]

	fontsize = 2 + (((100-numNodes)/100) * 8)
	fontsize = min(12,fontsize)
	nodesize = 10 + (((100-numNodes)/100) * 200)

	if (nodePos == {}):
		pos = nx.spring_layout(G,k=4/math.sqrt(numNodes))
	else:
		pos = nodePos

	if (history == []):
		nodeColors = [float(x[1]) for x in nx.degree(G)]
		nodeColors = [ x / max(nodeColors) for x in nodeColors]
		#edgeStyle = 'solid'
		edgeStyle = '--'
		nx.draw_networkx_nodes(G,pos,node_size=nodesize,node_color=nodeColors)

		nx.draw_networkx_labels(G, pos, labels=tags,font_size=fontsize)

		nx.draw_networkx_edges(G, pos, style=edgeStyle, alpha=weights)
		edge_labels = nx.get_edge_attributes(G, "weight")
		nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size = fontsize*0.6 )

		filename = "baseGraph.png"

	else:

		# draw nodes taken
		nodeColor = 'red'
		edgeStyle = 'solid'
		targetNodes = history
		
		nx.draw_networkx_nodes(G,pos,nodelist=targetNodes,node_size=nodesize,node_color=nodeColor)
		nx.draw_networkx_labels(G, pos, labels={n:f"{tags[n]}\n{n}" for n in G if n in targetNodes}, font_size=fontsize)

		edge_labels = nx.get_edge_attributes(G, "weight")
		targetEdges = [[u,v] for [u,v] in G.edges if ((u in targetNodes) and (v in targetNodes))]
		targetLabels = {(u,v):edge_labels[u,v] for (u,v) in edge_labels.keys() if ((u in targetNodes) and (v in targetNodes))}
		print ("Total weight traversed:", sum(targetLabels.values()))
		nx.draw_networkx_edges(G, pos, edgelist=targetEdges, style=edgeStyle, alpha=1.0)
		nx.draw_networkx_edge_labels(G, pos, targetLabels, font_size = fontsize*0.6,)

		# draw nodes not taken
		nodeColor = 'grey'
		edgeStyle = '--'
		targetNodes = list(set(G.nodes() - set(history)))
		nx.draw_networkx_nodes(G,pos,nodelist=targetNodes,node_size=nodesize,node_color=nodeColor)
		#nx.draw_networkx_labels(G, pos, labels=tags,font_size=fontsize)
		targetEdges = [[u,v] for [u,v] in G.edges if ((u in targetNodes) or (v in targetNodes))]
		nx.draw_networkx_edges(G, pos, edgelist=targetEdges, style=edgeStyle, alpha=0.1)

		#nx.draw_networkx_labels(G, pos, labels=tags,font_size=fontsize)
		targetLabels = {(u,v):edge_labels[u,v] for (u,v) in edge_labels.keys() if ((u in targetNodes) or (v in targetNodes))}
		nx.draw_networkx_edge_labels(G, pos, targetLabels, font_size = fontsize*0.6, alpha=0.1)

		filename = "pathTaken.png"

	plt.savefig(filename,dpi=200)

	if not NODISPLAY:
		plt.show()

	return pos
