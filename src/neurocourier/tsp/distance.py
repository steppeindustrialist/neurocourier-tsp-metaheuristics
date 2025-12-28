from __future__ import annotations
import math
from typing import List
from .types import Point

def euclidean_distance_matrix(points: List[Point]) -> List[List[float]]:
    n = len(points)
    d = [[0.0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            dist = math.hypot(xi - xj, yi - yj)
            d[i][j] = dist
            d[j][i] = dist
    return d
