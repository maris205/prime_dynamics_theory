"""Create the RH-98 projector propagation barrier figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "results" / "projector_propagation_audit.json"
PDF = ROOT / "figures" / "projector_lipschitz_propagation_barrier.pdf"
PNG = ROOT / "figures" / "projector_lipschitz_propagation_barrier.png"


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    keys = ["1e-08", "1e-06", "1e-04"]
    records = [record for channel in channels for key in keys for record in channel["chains"][key]["records"]]
    counter = audit["counterexample"]
    summaries = audit["audit_summary"]["threshold_summaries"]

    tail_amp = np.array([record["tail_amplification_upper"] for record in records])
    projector_amp = np.array([record["projector_secant_multiplier"] for record in records])
    local_distance = np.array([record["local_projector_distance"] for record in records])
    distance_bound = np.array([record["local_gap_distance_bound"] for record in records])
    endpoint_effect = np.array([max(record["endpoint_tail_effect_abs_upper"], 1e-30) for record in records])
    endpoint_bound = np.array([record["endpoint_tail_lipschitz_bound"] for record in records])

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9})
    figure, axes = plt.subplots(2, 2, figsize=(11.2, 7.4), constrained_layout=True)

    ax = axes[0, 0]
    ax.semilogy(np.sort(projector_amp), "o", markersize=3.8, color="#7570b3", label="projector secant")
    ax.semilogy(np.sort(tail_amp), "s", markersize=3.2, color="#1b9e77", label="tail amplification")
    ax.axhline(1.0, color="#222222", linestyle=":", label="unit level")
    ax.set_xlabel("sorted production omission")
    ax.set_ylabel("propagation multiplier")
    ax.set_title("(a) Geometry can amplify while tail energy does not")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    names = ["local loss", "endpoint effect"]
    values = [counter["local_loss_upper"], counter["endpoint_effect_abs_lower"]]
    ax.bar(names, values, color=["#66a61e", "#d95f02"])
    ax.set_yscale("log")
    ax.set_ylabel("validated tail quantity")
    ax.set_title(f"(b) Positive two-step counterexample: > {counter['certified_tail_amplification_lower']:.2f}x")
    ax.grid(alpha=0.25, axis="y", which="both")

    ax = axes[1, 0]
    ax.loglog(local_distance, distance_bound, "o", markersize=4, color="#e7298a", alpha=0.75)
    low = min(local_distance.min(), distance_bound.min())
    high = max(local_distance.max(), distance_bound.max())
    ax.plot([low, high], [low, high], color="#222222", linestyle=":", label="exact distance")
    ax.set_xlabel("local projector distance")
    ax.set_ylabel("gap-derived distance bound")
    ax.set_title("(c) Compressed gaps control every local displacement")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    ax.loglog(endpoint_effect, endpoint_bound, "o", markersize=4, color="#1f78b4", alpha=0.75)
    low = min(endpoint_effect.min(), endpoint_bound.min())
    high = max(endpoint_effect.max(), endpoint_bound.max())
    ax.plot([low, high], [low, high], color="#222222", linestyle=":", label="exact effect")
    ax.set_xlabel("validated endpoint tail effect")
    ax.set_ylabel("endpoint Gram/projector bound")
    ax.set_title("(d) Projector-Lipschitz endpoint bounds close 38/38")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    figure.suptitle("RH-98: unit tail propagation is empirical, not universal", fontsize=12)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF)
    figure.savefig(PNG, dpi=220)
    plt.close(figure)
    print(json.dumps({"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT)), "production_omissions": len(records), "counterexample_amplification": counter["certified_tail_amplification_lower"]}, sort_keys=True))


if __name__ == "__main__":
    main()
