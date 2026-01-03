from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

from neurocourier.tsp.tour import tour_length
from neurocourier.tsp.types import Tour

from .params import ACOParams


@dataclass
class ACOResult:
    best_tour: Tour
    best_cost: float
    meta: Dict[str, float]


def ant_colony_optimize(dist: List[List[float]], p: ACOParams) -> ACOResult:
    """Ant Colony Optimization (ACO) for TSP.

    The solver takes a precomputed distance matrix (from the shared TSP core) and returns
    the best permutation tour found.
    """

    n = len(dist)
    rng = random.Random(p.seed)
    ants = p.ants or n

    # Heuristic visibility: eta = 1 / (d + eps)
    eta = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                eta[i][j] = 1.0 / (dist[i][j] + p.epsilon)

    tau = [[1.0] * n for _ in range(n)]

    best_tour: Tour = list(range(n))
    best_cost = float("inf")

    def build_tour() -> Tour:
        start = rng.randrange(n)
        tour = [start]
        unvisited = set(range(n))
        unvisited.remove(start)
        cur = start
        while unvisited:
            candidates = list(unvisited)
            weights = []
            for j in candidates:
                weights.append((tau[cur][j] ** p.alpha) * (eta[cur][j] ** p.beta))
            nxt = rng.choices(candidates, weights=weights, k=1)[0]
            tour.append(nxt)
            unvisited.remove(nxt)
            cur = nxt
        return tour

    for it in range(p.iterations):
        colony: List[Tuple[Tour, float]] = []
        for _ in range(ants):
            t = build_tour()
            c = tour_length(t, dist)
            colony.append((t, c))
            if c < best_cost:
                best_cost, best_tour = c, t

        # Evaporation
        evap = 1.0 - p.rho
        for i in range(n):
            row = tau[i]
            for j in range(n):
                row[j] *= evap

        # Deposit pheromones for each ant
        for t, c in colony:
            if c <= 0:
                continue
            deposit = p.q / c
            for i in range(n):
                u = t[i]
                v = t[(i + 1) % n]
                tau[u][v] += deposit
                tau[v][u] += deposit

    return ACOResult(best_tour=best_tour, best_cost=best_cost, meta={"iterations": float(p.iterations), "ants": float(ants)})
