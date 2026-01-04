# neurocourier-tsp-metaheuristics
Metaheuristics (Simulated Annealing &amp; Ant Colony) for Metric TSP – CMP3005 Term Project

This repository contains an academic term project on solving a metric Traveling Salesperson Problem (TSP) using metaheuristic algorithms, focusing on Simulated Annealing (SA) and Ant Colony Optimization (ACO) implemented in Python.
The project is framed around a fictional logistics company (NeuroCourier) that must plan efficient daily delivery routes under time constraints, where exact algorithms do not scale.

## The Problem:
  Given a complete graph with distances satisfying the triangle inequality
  Find a minimum-length tour that:
   visits each city exactly once
   returns to the starting city
## Complexity:
  The decision version of TSP is NP-complete
  The optimization version is NP-hard
  Exact solvers do not scale beyond small instances
Therefore, we focus on approximation via metaheuristics.

# Installation:
```
git clone https://github.com/steppeindustrialist/neurocourier-tsp-metaheuristics
cd neurocourier-tsp-metaheuristics

python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```
# Usage Example
```
from neurocourier.tsp.instances import generate_uniform_points
from neurocourier.tsp.distance import euclidean_distance_matrix
from neurocourier.solvers import (
    SAParams,
    simulated_annealing_tsp,
    ACOParams,
    ant_colony_optimize,
)
```
### Generate synthetic instance
```
pts = generate_uniform_points(50, seed=1)
dist = euclidean_distance_matrix(pts)
```
### Run Simulated Annealing
```
sa_res = simulated_annealing_tsp(
    dist,
    SAParams(seed=1, max_seconds=0.3)
)
```
 ### Run Ant Colony Optimization
 ```
aco_res = ant_colony_optimize(
    dist,
    ACOParams(seed=1, iterations=50)
)

print("SA cost:", sa_res.best_cost)
print("ACO cost:", aco_res.best_cost)
```
### One-Block Simple Demo
```
git clone https://github.com/steppeindustrialist/neurocourier-tsp-metaheuristics && \
cd neurocourier-tsp-metaheuristics && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -e . && \
python - <<'PY'
from neurocourier.tsp.instances import generate_uniform_points
from neurocourier.tsp.distance import euclidean_distance_matrix
from neurocourier.solvers import SAParams, simulated_annealing_tsp, ACOParams, ant_colony_optimize

pts = generate_uniform_points(50, seed=1)
dist = euclidean_distance_matrix(pts)

sa = simulated_annealing_tsp(dist, SAParams(max_seconds=0.3))
aco = ant_colony_optimize(dist, ACOParams(iterations=50))

print("Simulated Annealing cost:", sa.best_cost)
print("Ant Colony Optimization cost:", aco.best_cost)
PY
```
### One-Block Benchmark
```
git clone git@github.com:steppeindustrialist/neurocourier-tsp-metaheuristics.git && \
cd neurocourier-tsp-metaheuristics && \
python3 -m venv .venv && \
source .venv/bin/activate && \
pip install -e . && \
mkdir -p results && \
python experiments/benchmark.py --sizes 20,50,100 --runs 5 --sa_seconds 0.3 --aco_iters 60

```