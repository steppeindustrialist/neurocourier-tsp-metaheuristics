# ant.py
import random

class Ant:
    def __init__(self, num_cities):
        self.num_cities = num_cities
        self.tour = []
        self.visited = set()
        self.total_distance = 0.0
        
    def reset(self):
        self.tour = []
        self.visited = set()
        self.total_distance = 0.0

    def visit_city(self, city_id, distance_to_add):
        self.tour.append(city_id)
        self.visited.add(city_id)
        self.total_distance += distance_to_add
        
    def current_city(self):
        return self.tour[-1]

    def select_next_city(self, pheromones, visibilities, alpha, beta):
        current = self.tour[-1]
        
        # 1. Identify valid moves
        unvisited = [c for c in range(self.num_cities) if c not in self.visited]
        
        # 2. Calculate probabilities
        scores = []
        for city in unvisited:
            tau = pheromones[current][city]
            eta = visibilities[current][city]
            # Safety: Both matrices are already safe from division by zero
            score = (tau ** alpha) * (eta ** beta)
            scores.append(score)
        
        # 3. Roulette Wheel Selection
        if not scores:
            return unvisited[0] if unvisited else None
            
        # random.choices handles normalization safely
        selected = random.choices(unvisited, weights=scores, k=1)[0]
        return selected
