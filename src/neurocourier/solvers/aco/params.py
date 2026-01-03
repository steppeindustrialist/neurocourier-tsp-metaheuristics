from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ACOParams:
    """Parameters for Ant Colony Optimization (ACO) for metric TSP."""

    # Influence of pheromone vs heuristic (1/distance)
    alpha: float = 1.0
    beta: float = 5.0

    # Evaporation rate in (0, 1)
    rho: float = 0.5

    # Pheromone deposit scaling constant
    q: float = 100.0

    # Iterations and colony size
    iterations: int = 50
    ants: int = 0  # if 0, use n

    # Numerics
    epsilon: float = 1e-10

    # Reproducibility
    seed: int = 0
