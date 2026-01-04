class Config:
    def __init__(self):
        # --- Simulation Settings ---
        self.num_cities = 40
        self.map_size = 200
        
        # --- ACO Parameters ---
        self.alpha = 0.8        # Pheromone importance
        self.beta = 5           # Distance importance
        self.rho = 0.83         # Evaporation rate
        self.q = 165            # Deposit constant
        self.max_iterations = 30
        self.num_ants = self.num_cities
