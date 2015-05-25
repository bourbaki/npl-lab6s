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
    # tV,vtV,nbV = clique_tr(V, x)
    # tS,vtS,nbS = clique_tr(S, x)
    # vtV_S = nbV - nbS
    result = 0.0 if tV == 0 else tS / tV * vtV / (S.number_of_nodes() - 1 + vtV_S)
    print("node: {}, tS: {}, tV: {}, vtS: {}, vtV: {}, vtV_S: {} wcc: {}".format(x, tS, tV, vtS, vtV, vtV_S, result))
    return result
    
def wcc(S, V):
    return mean(node_wcc(node, S, V) for node in S)

def clique_tr(G,node):
   nb = set(nx.all_neighbors(G, node))
   tr,nodes = set(),set()
   for n in nb:
       nodes.add(n)
       for n2 in nx.all_neighbors(G, n):
           if n2 in nb:
               tr.add(tuple(sorted([n,n2])))
               nodes.add(n2)
   return (len(tr),len(nodes),len(nb))    

def old_wcc(S, V):
    nodes = nx.nodes(S)
    num_nodes_gr = len(nodes)
    wcc0 = 0.
    for node in nodes:
        tV,vtV,nbV = clique_tr(V,node)
        tS,vtS,nbS = clique_tr(S,node)
        vtV_S = nbV - nbS
        print("node: {0}, tS: {1}, tV: {2}, vtS: {3}, vtV: {4}, vtV_S: {5}".format(node, tS, tV, vtS, vtV, vtV_S))
        if tV != 0:
            wcc0 += (tS*1./tV) * (vtV/(num_nodes_gr-1+vtV_S))
    return wcc0 / num_nodes_gr

def new_clique(G, x):
    return (nx.triangles(G, x), number_of_triangle_nodes(G, x), G.degree(x))