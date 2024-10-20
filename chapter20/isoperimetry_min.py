import math
from re import sub

vertices = list(range(10))
edges = [
        (0, 6),
        (0, 7), 
        (1, 9),
        (1, 8), 
        (1, 4), 
        (1, 5), 
        (2, 3), 
        (2, 5), 
        (2, 9), 
        (4, 7), 
        (4, 8), 
        (4,9), 
        (5,9), 
        (7,9), 
        (8,9)
    ]


def calc_iso(vertices, edges):
    return len(edges) / len(vertices)


def calc_min_isoperimetry(vertices, edges):
    n = len(vertices)
    m = len(edges)
    min_isoperimetry = math.inf

    min_subset = []

    for i in range(1 << n):

        subset_vertices = [j for j in range(n) if i & (1 << j)]

        if len(subset_vertices) == 0 or len(subset_vertices) > n // 2:
            continue

        boundary_edges = [edge for edge in edges if (edge[0] in subset_vertices and edge[1] not in subset_vertices) or (edge[1] in subset_vertices and edge[0] not in subset_vertices)]

        if len(boundary_edges) / len(subset_vertices) < min_isoperimetry:
            min_subset = subset_vertices
            min_isoperimetry = len(boundary_edges) / len(subset_vertices)

    return min_subset, min_isoperimetry

print(calc_min_isoperimetry(vertices, edges))




def calc_vol(vertex_set, all_vertices, adj):
    res = 0
    for v in vertex_set:
        for v2 in all_vertices:
            res += adj[v][v2]

    return res

def calc_min_conductance(vertices, edges, edge_weights, adj):
    n = len(vertices)
    m = len(edges)
    min_conductance = math.inf

    new_edge_weights = {}
    new_vertices = list(range(n))
    new_edges = []

    for v1, v2 in edges:
        new_edges.append((v1-1, v2-1))

    for v1, v2 in edge_weights:
        new_edge_weights[(v1-1, v2-1)] = edge_weights[(v1, v2)]

    min_subset = []

    print(edge_weights)
    d_V = sum(edge_weights.values())

    for i in range(1 << n):
        subset_vertices = [j for j in range(n) if i & (1 << j)]

        if len(subset_vertices) == 0 or len(subset_vertices) > n // 2:
            continue

        subset_edges = [(v1, v2) for v1, v2 in new_edges if (v1 in subset_vertices and v2 not in subset_vertices) or (v2 in subset_vertices and v1 not in subset_vertices)]

        w_S = sum(new_edge_weights[e] for e in subset_edges)
        d_S = calc_vol(subset_vertices, new_vertices, adj)
        d_V_S = calc_vol([v for v in new_vertices if v not in subset_vertices], new_vertices, adj)

        if d_S == 0 or d_V_S == 0:
            continue
        
        conductance = (d_V * w_S) / (d_S * d_V_S)
    
        if conductance < min_conductance:
            min_subset = subset_vertices
            min_conductance = conductance

    return min_subset, min_conductance
