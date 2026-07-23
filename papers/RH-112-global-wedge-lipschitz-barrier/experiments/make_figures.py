"""Create RH-112 barrier figures."""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    data = json.loads((ROOT / "results/wedge_lipschitz_audit.json").read_text(encoding="utf-8"))
    base = []
    for row in data["rows"]:
        for channel in row["channels"]:
            record = next(item for item in channel["thresholds"] if float(item["threshold"]) == 1e-8)
            base.extend((row["sigma"], step) for step in record["steps"])
    fig, axes = plt.subplots(1, 2, figsize=(10.9, 4.25))
    ax = axes[0]
    x = np.arange(len(base))
    global_values = np.array([step["global_wedge_lower"] for _, step in base])
    direct_values = np.array([step["product_weyl_lower"] for _, step in base])
    ax.semilogy(x, np.maximum(direct_values, 1e-18), label="product Weyl", lw=1.6)
    ax.semilogy(x, np.maximum(global_values, 1e-18), label="global wedge Lipschitz", lw=1.1)
    ax.set_xlabel("archived update")
    ax.set_ylabel("normalized four-volume lower bound")
    ax.set_title("Global exterior perturbation loses weak modes")
    ax.grid(True, which="both", alpha=.25); ax.legend(frameon=False)

    ax = axes[1]
    efficiencies = np.array([step["positivity_radius_efficiency"] for _, step in base])
    sigmas = np.array([sigma for sigma, _ in base])
    for sigma in sorted(set(sigmas), reverse=True):
        values = efficiencies[sigmas == sigma]
        ax.scatter(np.full(values.size, sigma), values, s=15, alpha=.75)
    ax.set_xscale("log"); ax.set_xlabel(r"scale $\sigma$")
    ax.set_ylabel("global/direct positive-radius ratio")
    ax.set_title("Sharp tolerance penalty")
    ax.grid(True, which="both", alpha=.25)
    fig.tight_layout()
    out = ROOT / "figures/global_wedge_lipschitz_barrier"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__": main()
