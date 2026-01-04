# main.py
from config import Config
from graph_tools import generate_cities, get_mst_lower_bound
from optimizer import AntColonyOptimizer

if __name__ == "__main__":
    # 1. Setup
    config = Config()
    cities = generate_cities(config.num_cities, config.map_size)
    
    # 2. Run ACO
    # The optimizer will internally use the safe matrix calculation
    aco = AntColonyOptimizer(cities, config)
    aco_result = aco.run()
    
    # 3. Calculate MST Lower Bound for comparison
    # We access the distance matrix generated inside the ACO instance
    mst_bound = get_mst_lower_bound(config.num_cities, aco.distances)
    
    # 4. Final Report
    print("-" * 30)
    print(f"ACO Best Result: {aco_result:.2f}")
    print(f"MST Lower Bound: {mst_bound:.2f}")
    
    if mst_bound > 0:
        ratio = aco_result / mst_bound
        print(f"Ratio (TSP / MST): {ratio:.2f}")
    else:
        print("MST is 0 (all points identical?), cannot calculate ratio.")
