from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List, Optional

from neurocourier.tsp.tour import tour_length, nearest_neighbor_tour
from neurocourier.tsp.types import Tour


@dataclass(frozen=True)
class SAParams:
    seed: int = 0
    T0: float = 100.0
    alpha: float = 0.995
    Tmin: float = 1e-6
    iters_per_temp: int = 0          # if 0 -> 20*n
    max_seconds: Optional[float] = None


@dataclass
class SAResult:
    best_tour: Tour
    best_cost: float


def _delta_2opt(t: Tour, i: int, k: int, d: List[List[float]]) -> float:
    n = len(t)
    a, b = t[i], t[i + 1]
    c = t[k]
    dn = t[0] if k == n - 1 else t[k + 1]
    return (d[a][c] + d[b][dn]) - (d[a][b] + d[c][dn])


def simulated_annealing_tsp(dist: List[List[float]], p: SAParams) -> SAResult:
    import time
    rng = random.Random(p.seed)
    n = len(dist)

    tour = nearest_neighbor_tour(dist)
    cur = tour_length(tour, dist)
    best_tour, best = tour[:], cur

    T = p.T0
    L = p.iters_per_temp or (20 * n)
    t0 = time.time()

    while T > p.Tmin:
        if p.max_seconds and (time.time() - t0) >= p.max_seconds:
            break

        for _ in range(L):
            i, k = sorted(rng.sample(range(n), 2))
            if i == k or k == i + 1 or (i == 0 and k == n - 1):
                continue

            dE = _delta_2opt(tour, i, k, dist)
            if dE <= 0 or rng.random() < math.exp(-dE / T):
                tour[i + 1 : k + 1] = reversed(tour[i + 1 : k + 1])
                cur += dE
                if cur < best:
                    best = cur
                    best_tour = tour[:]

        T *= p.alpha

    return SAResult(best_tour=best_tour, best_cost=best)
