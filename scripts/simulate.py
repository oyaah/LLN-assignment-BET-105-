"""Simulate sampling from Uniform[1, n] and record sample means."""
import sys
import numpy as np

def run_simulation(n, k, repeats, outpath):
    rng = np.random.default_rng(seed=k * 31 + repeats)
    with open(outpath, "w") as f:
        f.write("k\ttrial\tsample_mean\n")
        for trial in range(1, repeats + 1):
            samples = rng.integers(1, n + 1, size=k)
            mean_val = np.mean(samples)
            f.write(f"{k}\t{trial}\t{mean_val:.4f}\n")

if __name__ == "__main__":
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    repeats = int(sys.argv[3])
    outpath = sys.argv[4]
    run_simulation(n, k, repeats, outpath)
