# optimizer.py
import random
from ant import Ant
from graph_tools import calculate_matrices

class AntColonyOptimizer:
    def __init__(self, cities, config):
        self.cities = cities
        self.cfg = config
        self.n = len(cities)
        
        # Initialize Matrices using the tools
        self.distances, self.visibilities = calculate_matrices(cities)
        self.pheromones = [[1.0 for _ in range(self.n)] for _ in range(self.n)]
        
        # Initialize Colony
        self.colony = [Ant(self.n) for _ in range(self.cfg.num_ants)]
        
        # Stats
        self.best_global_tour = []
        self.best_global_distance = float('inf')

    def _move_ants(self):
        # Initialize start positions
        for ant in self.colony:
            ant.reset()
            start_node = random.randint(0, self.n - 1)
            ant.visit_city(start_node, 0)
            
        # Step through the remaining n-1 cities
        for _ in range(self.n - 1):
            for ant in self.colony:
                next_city = ant.select_next_city(
                    self.pheromones, 
                    self.visibilities, 
                    self.cfg.alpha, 
                    self.cfg.beta
                )
                dist = self.distances[ant.current_city()][next_city]
                ant.visit_city(next_city, dist)
                
        # Return to start to close the loop
        for ant in self.colony:
            start_node = ant.tour[0]
            current = ant.current_city()
            return_dist = self.distances[current][start_node]
            ant.visit_city(start_node, return_dist)

    def _update_pheromones(self):
        # 1. Evaporation
        for i in range(self.n):
            for j in range(self.n):
                self.pheromones[i][j] *= (1.0 - self.cfg.rho)
                
        # 2. Deposit
        for ant in self.colony:
            if ant.total_distance < self.best_global_distance:
                self.best_global_distance = ant.total_distance
                self.best_global_tour = list(ant.tour)
            
            # --- SAFETY CHECK: Prevent Division by Zero ---
            if ant.total_distance > 0:
                deposit = self.cfg.q / ant.total_distance
            else:
                deposit = 0 
            
            for i in range(self.n):
                u = ant.tour[i]
                v = ant.tour[(i + 1) % self.n] 
                
                self.pheromones[u][v] += deposit
                self.pheromones[v][u] += deposit

    def run(self):
        print(f"Starting Simulation with {self.n} cities...")
        
        for iteration in range(self.cfg.max_iterations):
            self._move_ants()
            self._update_pheromones()
            print(f"Iteration {iteration + 1}: Best Distance = {self.best_global_distance:.2f}")
            
        return self.best_global_distance
