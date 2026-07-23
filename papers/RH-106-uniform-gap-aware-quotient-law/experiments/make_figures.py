"""Create the RH-106 gap-aware quotient figure."""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "uniform_quotient_audit.json").read_text(encoding="utf-8"))
    thresholds = data["thresholds"]
    labels = [f"$10^{{-{int(round(-math.log10(row['threshold'])))}}}$" for row in thresholds]
    candidate = [row["candidate_count"] for row in thresholds]
    accepted = [row["accepted_count"] for row in thresholds]
    rejected = [row["rejected_count"] for row in thresholds]
    unrestricted = [row["maximum_unrestricted_endpoint_to_reference_ratio"] for row in thresholds]
    stopped = [row["maximum_stopped_endpoint_to_reference_ratio"] for row in thresholds]
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.2))
    ax = axes[0]
    x = list(range(len(labels)))
    ax.bar(x, accepted, width=0.55, label="accepted", color="tab:blue")
    ax.bar(x, rejected, width=0.55, bottom=accepted, label="rejected", color="tab:red")
    for i, total in enumerate(candidate):
        ax.text(i, total + 0.35, f"{total} candidates", ha="center", fontsize=8)
    ax.set_xticks(x, labels)
    ax.set_ylabel("quotient events")
    ax.set_title("Stopped supply remains safe")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)

    ax = axes[1]
    ax.plot(x, unrestricted, marker="s", linewidth=2.1, label="unrestricted")
    ax.plot(x, stopped, marker="o", linewidth=2.1, label="stopped")
    ax.axhline(1.01, color="tab:red", linestyle="--", linewidth=1.6, label="endpoint gate")
    ax.set_xticks(x, labels)
    ax.set_ylabel("worst endpoint/reference ratio")
    ax.set_title(r"Price is $c^2/g$, not $g$")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False)

    fig.tight_layout()
    output = ROOT / "figures" / "uniform_gap_aware_quotient"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
