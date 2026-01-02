import random
import math
import heapq

def get_mst_lower_bound(num_cities, dist_matrix):
    
    # Prim's Algorithm
    start_node = 0
    visited = set([start_node])
    edges = []
    
    # Add initial edges from start_node to priority queue
    for to_city in range(num_cities):
        if to_city != start_node:
            # Heap stores: (cost, to_city)
            heapq.heappush(edges, (dist_matrix[start_node][to_city], to_city))
    
    mst_cost = 0.0
    
    # We need to connect all N cities
    while len(visited) < num_cities:
        # Get cheapest edge from the queue
        cost, u = heapq.heappop(edges)
        
        if u in visited:
            continue
            
        # Add edge to tree
        visited.add(u)
        mst_cost += cost
        
        # Add new connections from the newly visited city
        for v in range(num_cities):
            if v not in visited:
                heapq.heappush(edges, (dist_matrix[u][v], v))
                
    return mst_cost

NumberOfVertecies = 40
vertecies = []
for i in range(NumberOfVertecies):
    # Random x,y coordinates between 0 and 200
    vertecies.append([i, random.randint(0, 200), random.randint(0, 200)])

# ==========================================
# PART 2: THE ANT CLASS
# ==========================================
class Ant:
    def __init__(self, num_cities):
        self.num_cities = num_cities
        self.tour = []
        self.visited = set()
        self.total_distance = 0.0
        
    def select_next_city(self, pheromone_matrix, visibility_matrix, alpha, beta):
        # Negative index gets the last item of list 
        current = self.tour[-1]
        
        # 1. Identify valid moves
        unvisited_cities = []
        for city in range(self.num_cities):
            if city not in self.visited:
                unvisited_cities.append(city)

        # 2. Calculate scores for Roulette Wheel
        scores = []
        for city in unvisited_cities:
            tau = pheromone_matrix[current][city]
            eta = visibility_matrix[current][city]
            
            # Avoid division by zero or math errors if tau is 0 (though unlikely here)
            score = (tau ** alpha) * (eta ** beta)
            scores.append(score)
        
        # 3. Pick one based on probability
        # random.choices handles the "score / total_score" logic internally
        if not scores: # Safety check
            return unvisited_cities[0]
            
        selected_city = random.choices(unvisited_cities, weights=scores, k=1)[0]
        return selected_city
    
    def visit_city(self, city_id, distance_to_add):
        self.tour.append(city_id)
        self.visited.add(city_id)
        self.total_distance += distance_to_add

    def reset(self):
        self.tour = []
        self.total_distance = 0.0
        self.visited = set()

    def current_city(self):
        return self.tour[-1]

# ==========================================
# PART 3: THE MAIN CONTROLLER
# ==========================================

# --- PARAMETERS ---
ALPHA = 0.8        # Pheromone importance 1
BETA = 5         # Distance importance 1.5 , 2.5 , 4.5++ is good
RHO = 0.83         # Evaporation rate
Q = 165          # Deposit constant
MAX_ITERATIONS = 30
NUM_ANTS = NumberOfVertecies 

# --- SETUP MATRICES ---
n = NumberOfVertecies
distances = [[0 for _ in range(n)] for _ in range(n)]
visibilities = [[0 for _ in range(n)] for _ in range(n)]
pheromones = [[1.0 for _ in range(n)] for _ in range(n)] # Init with 1.0

# Calculate Distance & Visibility
for i in range(n):
    distances[i][i] = 0
    visibilities[i][i] = 0
    for j in range(i+1, n):
        x1, y1 = vertecies[i][1], vertecies[i][2]
        x2, y2 = vertecies[j][1], vertecies[j][2]
        
        euclidian = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        
        distances[i][j] = euclidian
        visibilities[i][j] = 1.0 / euclidian
        
        distances[j][i] = euclidian
        visibilities[j][i] = 1.0 / euclidian

# Create Colony
colony = [Ant(n) for _ in range(NUM_ANTS)]
best_global_tour = []
best_global_distance = float('inf')

print(f"Starting Simulation with {n} cities...")

# --- MAIN LOOP ---
for iteration in range(MAX_ITERATIONS):
    
    # A. Reset & Scatter
    for ant in colony:
        ant.reset()
        start_city = random.randint(0, n - 1)
        ant.visit_city(start_city, 0)

    # B. Move Ants (Step-by-Step)
    for step in range(n - 1):
        for ant in colony:
            next_city = ant.select_next_city(pheromones, visibilities, ALPHA, BETA)
            dist = distances[ant.current_city()][next_city]
            ant.visit_city(next_city, dist)

    # C. Return to Start
    for ant in colony:
        start_node = ant.tour[0]
        current = ant.current_city()
        return_dist = distances[current][start_node]
        ant.visit_city(start_node, return_dist)

    # D. Update Pheromones
    # 1. Evaporation
    for i in range(n):
        for j in range(n):
            pheromones[i][j] *= (1.0 - RHO)

    # 2. Deposit
    for ant in colony:
        # Check for new record
        if ant.total_distance < best_global_distance:
            best_global_distance = ant.total_distance
            best_global_tour = list(ant.tour)
            
        deposit = Q / ant.total_distance
        
        # Add to path (including return trip)
        for i in range(n):
            u = ant.tour[i]
            v = ant.tour[(i + 1) % n] # Wraps around to 0 at the end
            
            pheromones[u][v] += deposit
            pheromones[v][u] += deposit

    print(f"Iteration {iteration + 1}: Best Distance = {best_global_distance:.2f}")

# --- FINAL OUTPUT ---
mst_bound = get_mst_lower_bound(n, distances)

print(f"Algorithm Result: {best_global_distance:.2f}")
print(f"MST Lower Bound:  {mst_bound:.2f}")

# The TSP will always be larger than the MST.
# A typical "Good" TSP solution is usually roughly 1.1x to 1.2x the MST weight.
ratio = best_global_distance / mst_bound
print(f"Ratio (TSP / MST): {ratio:.2f}")
