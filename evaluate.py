#!/usr/bin/env python

import networkx as nx
import community_metrics as cm
from community import generate_dendogram
import sys
import json

def print_graph_stats(g):
    print(">> Nodes: {}".format(g.number_of_nodes()))
    print(">> Edges: {}".format(g.number_of_edges()))

if len(sys.argv) != 3:
    print("Error: Wrong number of arguments.")
    sys.exit(-1)

_, GRAPH_FILE, OUT_FILE = sys.argv

print("Opening {}...".format(GRAPH_FILE))
G = nx.read_gpickle(GRAPH_FILE)
print_graph_stats(G)

print("Computing k-cores...")
core_numbers = nx.core_number(G)
max_core = max(core_numbers.values())
max_core_communities = list(nx.connected_component_subgraphs(nx.k_core(G, k=max_core, core_number=core_numbers)))
print(">> max-core: {}".format(max_core))
four_cores_communities = list(nx.connected_component_subgraphs(nx.k_core(G, k=4, core_number=core_numbers)))
num_4_core = len(four_cores_communities)
print(">> num-4-cores: {}".format(num_4_core))

print("Computing modularities...")
print(">> max-core communities: {}".format(len(max_core_communities)))
modularity_max_core = cm.modularity(G, max_core_communities)
print(">> max-core modularity: {}".format(modularity_max_core))
print(">> 4-core communities: {}".format(len(four_cores_communities)))
modularity_four_core = cm.modularity(G, four_cores_communities)
print(">> 4-core modularity: {}".format(modularity_four_core))

print("Computing wcc...")
wcc_max_core = cm.wcc(max_core_communities[0], G)
print(">> max-core wcc: {}".format(wcc_max_core))
wcc_four_core = cm.wcc(four_cores_communities[0], G)
print(">> 4-core wcc: {}".format(wcc_four_core))

print("Computing louvain...")
dendo = generate_dendogram(G)
def uniq(lst):
    return len(set(lst))
louvain_steps = [uniq(prt.values()) for prt in dendo]
print(">> Louvain Steps:", louvain_steps)

print("Saving to {}".format(OUT_FILE))
RESULT = {
    "max_core": max_core,
    "num_4-cores": num_4_core,
    "modularity_max-cores": modularity_max_core,
    "modularity_4-cores": modularity_four_core,
    "wcc_max-cores": wcc_max_core,
    "wcc_4-cores": wcc_four_core,
    "louvain_steps": louvain_steps
}
with open(OUT_FILE, 'w') as out:
    out.write(json.dumps(RESULT))