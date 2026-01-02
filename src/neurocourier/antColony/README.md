# Ant Colony Optimization (ACO) for TSP

This project implements the **Ant Colony Optimization** algorithm to solve the **Traveling Salesperson Problem (TSP)**. It is written in Python and modularized for clarity, maintainability, and safety (prevents division-by-zero errors).

## 📂 Project Structure

The project is split into 5 distinct modules:

| File | Description |
| :--- | :--- |
| **`main.py`** | **Entry point.** Orchestrates the setup, runs the optimizer, and compares results against the MST lower bound. |
| **`config.py`** | Contains all configuration parameters (Ants, Iterations, Alpha, Beta, etc.) to easily tweak the simulation. |
| **`optimizer.py`** | Contains the `AntColonyOptimizer` class which manages the colony, pheromone updates, and the main loop. |
| **`ant.py`** | Defines the `Ant` class, responsible for traversing the graph and selecting the next city based on probabilities. |
| **`graph_tools.py`** | Helper functions for generating cities, calculating matrices safely, and computing the MST (Minimum Spanning Tree). |

## 🚀 How to Run

1.  Ensure you have Python installed (3.6+ recommended).
2.  Place all 5 files in the same directory.
3.  Run the main script:

```bash
python main.py
