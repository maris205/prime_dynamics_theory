from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results/cross_audit.json").read_text())
    rows = data["rows"]
    labels = [f"{row['sigma']:g}{row['side'][0].upper()}" for row in rows]
    active = [item for row in rows for item in row["snapshots"] if item["tail_active"]]
    fig, axes = plt.subplots(2, 2, figsize=(11.3, 7.1), constrained_layout=True)

    ax = axes[0, 0]
    nominal = [item["nominal_fourth_coupling_singular"] for item in active]
    radii = [item["coupling_operator_radius"] for item in active]
    ax.loglog(nominal, radii, "o", ms=4, alpha=0.7, color="#4c72b0")
    lo = min(nominal + radii); hi = max(nominal + radii)
    ax.loglog([lo, hi], [lo, hi], "--", color="black", lw=1)
    ax.set_xlabel("nominal fourth tail-coupling singular value")
    ax.set_ylabel("outward coupling radius")
    ax.set_title("A. Twenty-six active fourth modes hit the radius wall")

    ax = axes[0, 1]
    counts = [sum(item["four_mode_coupling_certified"] for item in row["snapshots"] if item["tail_active"]) for row in rows]
    totals = [sum(item["tail_active"] for item in row["snapshots"]) for row in rows]
    x = np.arange(len(rows))
    ax.bar(x, totals, color="#d9d9d9", label="tail-active")
    ax.bar(x, counts, color="#55a868", label="four-mode certified")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylabel("snapshot count")
    ax.set_title("B. Certification disappears near fine terminals")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 0]
    bases = [item["four_mode_normalized_base_lower"] for item in active]
    ax.semilogy(np.arange(len(bases)), np.maximum(bases, 1e-8), ".", color="#8172b2")
    ax.axhline(1e-8, color="black", ls="--", lw=1)
    ax.set_xlabel("tail-active snapshot index")
    ax.set_ylabel("four-mode cross-base lower (zeros clipped)")
    ax.set_title("C. Only 54 of 80 active bases are positive")

    ax = axes[1, 1]
    categories = ["inactive\nexact zero", "active\ncertified", "active\nwall"]
    values = [
        data["audit_summary"]["tail_inactive_exact_zero_count"],
        data["audit_summary"]["active_four_mode_coupling_certificate_count"],
        data["audit_summary"]["active_four_mode_coupling_failure_count"],
    ]
    ax.bar(categories, values, color=["#c44e52", "#55a868", "#8172b2"])
    for index, value in enumerate(values):
        ax.text(index, value + 1.5, str(value), ha="center", fontweight="bold")
    ax.set_ylim(0, 60)
    ax.set_ylabel("snapshot count")
    ax.set_title("D. Contemporaneous reset cannot close the bridge")

    for axis in axes.flat:
        axis.spines[["top", "right"]].set_visible(False)
        axis.grid(axis="y", alpha=0.18)
    output = ROOT / "figures/spectral_reset_cross_action_cancellation"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
