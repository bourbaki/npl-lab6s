import networkx as nx
from statistics import mean

def have_common_item(it1, it2):
    """return True if iterators have common element"""
    intersection = set(it1) & set(it2)
    return len(intersection) != 0
    
def have_common_neighbor(G, node1, node2):
    """docstring for is_in_triangle"""
    return len(list(nx.common_neighbors(G, node1, node2))) != 0

def cumulative_degree(G, nbunch):
    """return sum of node degrees in nbunch"""
    return sum(G.degree(nbunch).values())

def community_modularity(G, s):
    """generate function for modularity summand"""
    m = G.number_of_edges()
    return s.number_of_edges() / m  - (cumulative_degree(G, s) / 2 / m) ** 2

def modularity(G, sbunch):
    """compute modularity for the partition inside graph"""
    return sum(community_modularity(G, s) for s in sbunch)
    
def triangle_nodes(G, node, nodeset=None):
    """return triangle nodes iterator"""
    if nodeset:
        nbrs = (nb for nb in G.neighbors_iter(node) if nb in nodeset)
    else:
        nbrs = G.neighbors_iter(node)
    return (nb for nb in nbrs if have_common_neighbor(G, node, nb))
    
def number_of_triangle_nodes(G, node, nodeset=None):
    """docstring for number_of_triangle_nodes"""
    return len(list(triangle_nodes(G, node, nodeset=nodeset)))
    
def node_wcc(x, S, V):
    tS, tV = nx.triangles(S, x), nx.triangles(V, x)
    vtS, vtV = number_of_triangle_nodes(S, x), number_of_triangle_nodes(V, x)
    vtV_S = vtV - vtS
    result = 0.0 if tV == 0 else tS / tV * vtV / (S.number_of_nodes() - 1 + vtV_S)
    print("node: {}, tS: {}, tV: {}, vtS: {}, vtV: {}, vtV_S: {} wcc: {}".format(x, tS, tV, vtS, vtV, vtV_S, result))
    return result
    
def wcc(S, V):
    return mean(node_wcc(node, S, V) for node in S) 