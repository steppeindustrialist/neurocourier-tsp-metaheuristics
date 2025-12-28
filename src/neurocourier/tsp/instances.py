from __future__ import annotations
import random
from typing import List, Tuple
from .types import Point

def generate_uniform_points(n: int, seed: int, square_size: float = 1000.0) -> List[Point]:
    rng = random.Random(seed)
    return [(rng.uniform(0, square_size), rng.uniform(0, square_size)) for _ in range(n)]

def generate_clustered_points(
    n: int,
    seed: int,
    square_size: float = 1000.0,
    k_clusters: int = 4,
    cluster_spread: float = 60.0,
) -> List[Point]:
    rng = random.Random(seed)
    centers = [(rng.uniform(0, square_size), rng.uniform(0, square_size)) for _ in range(k_clusters)]
    pts: List[Point] = []
    for i in range(n):
        cx, cy = centers[i % k_clusters]
        x = rng.gauss(cx, cluster_spread)
        y = rng.gauss(cy, cluster_spread)
        x = min(max(x, 0.0), square_size)
        y = min(max(y, 0.0), square_size)
        pts.append((x, y))
    rng.shuffle(pts)
    return pts
