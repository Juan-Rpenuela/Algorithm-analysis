"""Run timing experiments comparing sorting algorithms and plot results.

Generates execution time vs input-size plots and saves to experiments/plots.
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path so sibling packages (like `algorithms`) can be
# imported when running this script directly: `python experiments/experiment.py`.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import argparse
import csv
import os
import time
import random
import statistics
from typing import Callable, Dict, List, Sequence

import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

from algorithms.sorting import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    python_sort,
)


def time_function(func: Callable[[Sequence[int]], List[int]], arr: Sequence[int]) -> float:
    start = time.perf_counter()
    func(arr)
    return time.perf_counter() - start


def run_experiments(
    sizes: List[int] = None, trials: int = 3, outdir: str = None, seed: int = 0
) -> None:
    random.seed(seed)
    algos: Dict[str, Callable[[Sequence[int]], List[int]]] = {
        "Bubble": bubble_sort,
        "Insertion": insertion_sort,
        "Merge": merge_sort,
        "Quick": quick_sort,
        "Timsort": python_sort,
    }

    if sizes is None:
        sizes = [128, 256, 512, 1024, 2048, 4096]

    results: Dict[str, List[tuple]] = {name: [] for name in algos}

    for name, func in algos.items():
        print(f"Running {name}...")
        if name in ("Bubble", "Insertion"):
            sizes_to_run = [s for s in sizes if s <= 1024]
        else:
            sizes_to_run = sizes

        for n in tqdm(sizes_to_run, desc=name):
            times = []
            for _ in range(trials):
                arr = [random.randint(0, n * 10) for _ in range(n)]
                t = time_function(func, arr)
                times.append(t)
            avg = statistics.mean(times)
            stdev = statistics.pstdev(times)
            results[name].append((n, avg, stdev))
            print(f"  size={n:5d} avg_time={avg:.6f}s stdev={stdev:.6f}s")

    # Prepare output directory
    if outdir is None:
        outdir = os.path.join(os.path.dirname(__file__), "plots")
    os.makedirs(outdir, exist_ok=True)

    # Save raw results to CSV for reproducibility
    csv_path = os.path.join(outdir, "results.csv")
    with open(csv_path, "w", newline="") as csvfile:
        w = csv.writer(csvfile)
        w.writerow(["algorithm", "n", "avg_seconds", "stdev_seconds"])
        for name, data in results.items():
            for n, avg, stdev in data:
                w.writerow([name, n, f"{avg:.8f}", f"{stdev:.8f}"])
    print(f"Results saved to {csv_path}")

    # Plotting with error bars
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    for name, data in results.items():
        if not data:
            continue
        ns = [n for n, _, _ in data]
        ts = [t for _, t, _ in data]
        errs = [e for _, _, e in data]
        plt.errorbar(ns, ts, yerr=errs, marker="o", capsize=3, label=name)

    plt.xlabel("Input size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Sorting algorithms: execution time vs input size")
    plt.xscale("log", base=2)
    plt.yscale("log")
    plt.legend()
    outpath = os.path.join(outdir, "complexity.png")
    plt.tight_layout()
    plt.savefig(outpath)
    print(f"Plot saved to {outpath}")


def main():
    parser = argparse.ArgumentParser(description="Run sorting algorithm experiments")
    parser.add_argument("--min-power", type=int, default=7, help="minimum power of two for n (default 7 -> 128)")
    parser.add_argument("--max-power", type=int, default=12, help="maximum power of two for n (default 12 -> 4096)")
    parser.add_argument("--trials", type=int, default=3, help="number of trials per size")
    parser.add_argument("--seed", type=int, default=0, help="random seed")
    parser.add_argument("--outdir", type=str, default=None, help="output directory for plots and CSV")
    args = parser.parse_args()

    sizes = [2 ** p for p in range(args.min_power, args.max_power + 1)]
    run_experiments(sizes=sizes, trials=args.trials, outdir=args.outdir, seed=args.seed)


if __name__ == "__main__":
    main()
