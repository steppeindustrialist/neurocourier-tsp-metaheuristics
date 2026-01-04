from __future__ import annotations

import argparse
import csv
import statistics as stats
import time

from neurocourier.tsp.instances import generate_uniform_points
from neurocourier.tsp.distance import euclidean_distance_matrix
from neurocourier.solvers import (
    SAParams,
    simulated_annealing_tsp,
    ACOParams,
    ant_colony_optimize,
)


def summarize(values):
    return {
        "best": min(values),
        "mean": stats.mean(values),
        "stdev": stats.pstdev(values) if len(values) > 1 else 0.0,
    }


def main():
    ap = argparse.ArgumentParser(description="Benchmark SA vs ACO on synthetic metric TSP instances.")
    ap.add_argument("--sizes", default="20,50,100", help="Comma-separated sizes, e.g. 20,50,100,200")
    ap.add_argument("--runs", type=int, default=5, help="Runs per size (different seeds)")

    ap.add_argument("--sa_seconds", type=float, default=0.3, help="SA time budget per run (seconds)")
    ap.add_argument("--aco_iters", type=int, default=60, help="ACO iterations per run")
    ap.add_argument("--out", default="results/benchmark.csv", help="CSV output path")
    args = ap.parse_args()

    sizes = [int(x.strip()) for x in args.sizes.split(",") if x.strip()]

    rows = []
    print("\nBenchmark: SA vs ACO")
    print(f"  sizes={sizes} runs={args.runs} sa_seconds={args.sa_seconds} aco_iters={args.aco_iters}\n")

    for n in sizes:
        sa_costs, sa_times = [], []
        aco_costs, aco_times = [], []

        for r in range(args.runs):
            seed = 1000 + r
            pts = generate_uniform_points(n, seed=seed)
            dist = euclidean_distance_matrix(pts)

            t0 = time.perf_counter()
            sa = simulated_annealing_tsp(dist, SAParams(seed=seed, max_seconds=args.sa_seconds))
            sa_times.append(time.perf_counter() - t0)
            sa_costs.append(sa.best_cost)

            t0 = time.perf_counter()
            aco = ant_colony_optimize(dist, ACOParams(seed=seed, iterations=args.aco_iters))
            aco_times.append(time.perf_counter() - t0)
            aco_costs.append(aco.best_cost)

        sa_s = summarize(sa_costs)
        aco_s = summarize(aco_costs)

        row = {
            "n": n,
            "runs": args.runs,
            "sa_seconds": args.sa_seconds,
            "aco_iters": args.aco_iters,
            "sa_best": sa_s["best"],
            "sa_mean": sa_s["mean"],
            "sa_stdev": sa_s["stdev"],
            "sa_time_mean_s": stats.mean(sa_times),
            "aco_best": aco_s["best"],
            "aco_mean": aco_s["mean"],
            "aco_stdev": aco_s["stdev"],
            "aco_time_mean_s": stats.mean(aco_times),
        }
        rows.append(row)

        print(
            f"n={n:>3} | "
            f"SA mean={row['sa_mean']:.2f} (best={row['sa_best']:.2f}) time={row['sa_time_mean_s']:.3f}s | "
            f"ACO mean={row['aco_mean']:.2f} (best={row['aco_best']:.2f}) time={row['aco_time_mean_s']:.3f}s"
        )

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"\nSaved: {args.out}\n")


if __name__ == "__main__":
    main()

