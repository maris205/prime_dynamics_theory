from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "partial_isometry_audit.json").read_text(encoding="utf-8"))
    rows = data["rows"]
    app = data["rh130_application"]
    equal = [row for row in rows if row["equal_rank"]]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))

    axes[0].hist([max(row["random_procrustes_gap"], 1e-16) for row in equal], bins=38, color="tab:blue", alpha=0.8)
    axes[0].set_xscale("log")
    axes[0].set_xlabel("best sampled distance minus canonical distance")
    axes[0].set_ylabel("equal-rank instances")
    axes[0].set_title("Polar gauge wins Procrustes audit")
    axes[0].grid(True, alpha=0.2)

    unequal = [row for row in rows if not row["equal_rank"]]
    axes[1].scatter(
        [row["unmatched_trace_lower"] for row in unequal],
        [row["forcing_trace"] for row in unequal],
        s=17, alpha=0.48, color="tab:green",
    )
    limit = max(row["forcing_trace"] for row in unequal)
    axes[1].plot([0, limit], [0, limit], "k--", linewidth=1)
    axes[1].set_xlabel("unmatched target trace lower")
    axes[1].set_ylabel("minimal forcing trace")
    axes[1].set_title("Dimension mismatch has unavoidable cost")
    axes[1].grid(True, alpha=0.2)

    labels = ["0→0", "0→4", "4→4"]
    counts = [app["transition_counts"]["0_to_0"], app["transition_counts"]["0_to_4"], app["transition_counts"]["4_to_4"]]
    colors = ["tab:gray", "tab:red", "tab:blue"]
    axes[2].bar(labels, counts, color=colors)
    axes[2].set_ylabel("RH-130 adjacent pairs")
    axes[2].set_title("Vacuous / forcing-only / transport-eligible")
    axes[2].text(1, counts[1] + 1.0, "22/24 birth strengths < 1", ha="center", fontsize=9)
    axes[2].grid(True, axis="y", alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "canonical_partial_isometry_forcing_gauge"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
