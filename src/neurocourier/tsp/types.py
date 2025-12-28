from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

Point = Tuple[float, float]
Tour = List[int]

@dataclass(frozen=True)
class Instance:
    name: str
    points: List[Point]
    seed: int
    mode: str  # uniform or clustered
    square_size: float
