from __future__ import annotations
from typing import List
from .types import Tour

def tour_length(tour: Tour, dist: List[List[float]]) -> float:
    n = len(tour)
    total = 0.0
    prev = tour[-1]
    for cur in tour:
        total += dist[prev][cur]
        prev = cur
    return total

def nearest_neighbor_tour(dist: List[List[float]], start: int = 0) -> Tour:
    n = len(dist)
    unvisited = set(range(n))
    unvisited.remove(start)
    tour: Tour = [start]
    cur = start
    while unvisited:
        nxt = min(unvisited, key=lambda j: dist[cur][j])
        unvisited.remove(nxt)
        tour.append(nxt)
        cur = nxt
    return tour
