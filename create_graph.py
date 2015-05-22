#!/usr/bin/env python

import networkx as nx
import vkapi as vk
from progressbar import ProgressBar

# data initialization
PROGRESS = True
USERS_FILE = "data/users.txt"
GRAPH_FILE = "data/graph.gpickle"

users = set(int(l.strip()) for l in open(USERS_FILE, 'r')) # users from group

def group_neighbors(uid):
    friends, followers = set(vk.get_friends(uid)), set(vk.get_followers(uid))
    return {u for u in users if u in friends or u in followers} # fast intersection

# generate edges
pbar = ProgressBar()
items = pbar(users) if PROGRESS else users
edges = ((u, v) for u in items for v in group_neighbors(u))

# create graph
print("Create graph...")
G = nx.Graph()
print("Add nodes...")
G.add_nodes_from(users)
print("Adding edges...")
G.add_edges_from(edges)
print("Converting to undirected...")
G.to_undirected()
print("Done...")

# save graph for further analysis
print("Saving graph...")
nx.write_gpickle(G, GRAPH_FILE)
print("Done")


