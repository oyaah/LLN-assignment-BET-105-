"""Generate LLN convergence plot from simulation results."""
import sys
import os
import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def load_results(results_dir):
    data = {}
    for fpath in sorted(glob.glob(os.path.join(results_dir, "k_*.tsv"))):
        with open(fpath) as f:
            header = f.readline()
            for line in f:
                parts = line.strip().split("\t")
                k = int(parts[0])
                mean_val = float(parts[2])
                data.setdefault(k, []).append(mean_val)
    return data

def make_plot(data, n, outpath):
    expected = (n + 1) / 2.0
    ks = sorted(data.keys())
    means = [data[k] for k in ks]

    fig, ax = plt.subplots(figsize=(10, 6))

    positions = range(1, len(ks) + 1)
    vp = ax.violinplot(means, positions=positions, showmeans=True,
                       showmedians=False, showextrema=False)

    for body in vp["bodies"]:
        body.set_facecolor("#7fb3d8")
        body.set_edgecolor("#1a5276")
        body.set_alpha(0.7)
    vp["cmeans"].set_color("#c0392b")
    vp["cmeans"].set_linewidth(2)

    for i, (pos, vals) in enumerate(zip(positions, means)):
        jitter = np.random.default_rng(42 + i).uniform(-0.12, 0.12, len(vals))
        ax.scatter(pos + jitter, vals, color="#2c3e50", s=18, alpha=0.6, zorder=3)

    ax.axhline(y=expected, color="#27ae60", linestyle="--", linewidth=2,
               label=f"E[X] = {expected:.1f}")

    ax.set_xticks(list(positions))
    ax.set_xticklabels([str(k) for k in ks], fontsize=10)
    ax.set_xlabel("Number of draws (k)", fontsize=12)
    ax.set_ylabel("Sample mean", fontsize=12)
    ax.set_title(f"Law of Large Numbers: Convergence for Uniform[1, {n}]",
                 fontsize=14, fontweight="bold")
    ax.legend(fontsize=11, loc="upper right")
    ax.grid(axis="y", alpha=0.3)

    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.tight_layout()
    plt.savefig(outpath, dpi=200, bbox_inches="tight")
    print(f"Plot saved to {outpath}")

if __name__ == "__main__":
    results_dir = sys.argv[1]
    n = int(sys.argv[2])
    outpath = sys.argv[3]
    data = load_results(results_dir)
    make_plot(data, n, outpath)
