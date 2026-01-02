# graph_tools.py
import math
import random
import heapq

def generate_cities(num_cities, map_size):
    """Generates a list of [id, x, y] for cities."""
    cities = []
    for i in range(num_cities):
        cities.append([i, random.randint(0, map_size), random.randint(0, map_size)])
    return cities

def calculate_matrices(cities):
    """
    Calculates distance and visibility matrices.
    PREVENTS DIVISION BY ZERO by adding a small epsilon.
    """
    n = len(cities)
    distances = [[0 for _ in range(n)] for _ in range(n)]
    visibilities = [[0 for _ in range(n)] for _ in range(n)]
    
    epsilon = 1e-10  # Safety buffer

    for i in range(n):
        distances[i][i] = 0
        visibilities[i][i] = 0
        for j in range(i + 1, n):
            x1, y1 = cities[i][1], cities[i][2]
            x2, y2 = cities[j][1], cities[j][2]
            
            euclidean = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            
            distances[i][j] = euclidean
            distances[j][i] = euclidean
            
            # --- SAFETY CHECK: Prevent Division by Zero ---
            # If distance is near 0 (duplicate cities), we use epsilon
            safe_dist = euclidean if euclidean > epsilon else epsilon
            
            visibilities[i][j] = 1.0 / safe_dist
            visibilities[j][i] = 1.0 / safe_dist
            
    return distances, visibilities

def get_mst_lower_bound(num_cities, dist_matrix):
    """Calculates MST using Prim's Algorithm for lower bound comparison."""
    start_node = 0
    visited = set([start_node])
    edges = []
    
    # Init edges
    for to_city in range(num_cities):
        if to_city != start_node:
            heapq.heappush(edges, (dist_matrix[start_node][to_city], to_city))
    
    mst_cost = 0.0
    while len(visited) < num_cities:
        if not edges: break 
        
        cost, u = heapq.heappop(edges)
        
        if u in visited:
            continue
            
        visited.add(u)
        mst_cost += cost
        
        for v in range(num_cities):
            if v not in visited:
                heapq.heappush(edges, (dist_matrix[u][v], v))
                
    return mst_cost
