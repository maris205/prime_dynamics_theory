from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "dyadic_gauge_audit.json").read_text(encoding="utf-8"))
    rows = data["rows"]
    eligible = [row for row in rows if row["natural_tail_factor"]["value"] not in (None, 0.0)]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))

    colors = ["tab:red" if row["optimal_positive_transfer"] and not row["natural_positive_transfer"] else "tab:blue" for row in eligible]
    axes[0].scatter(
        [row["minimum_principal_cosine"] for row in eligible],
        [row["natural_to_optimal_factor"]["log10"] for row in eligible],
        c=colors, s=35, alpha=0.72,
    )
    axes[0].set_xlabel("minimum principal cosine")
    axes[0].set_ylabel("log10 natural / optimal tail factor")
    axes[0].set_title("Packet angle does not control tail alignment")
    axes[0].grid(True, alpha=0.22)

    axes[1].scatter(
        [row["optimal_tail_factor"]["log10"] for row in eligible],
        [row["natural_tail_factor"]["log10"] for row in eligible],
        c=colors, s=35, alpha=0.72,
    )
    low = min(row["optimal_tail_factor"]["log10"] for row in eligible)
    high = max(row["natural_tail_factor"]["log10"] for row in eligible)
    axes[1].plot([low, high], [low, high], "k--", linewidth=1)
    axes[1].set_xlabel("optimal tail factor log10")
    axes[1].set_ylabel("natural tail factor log10")
    axes[1].set_title("Exact-Gram lift is feasible but nonoptimal")
    axes[1].grid(True, alpha=0.22)

    labels = ["vacuous", "birth/infinite", "eligible positive", "eligible blocked"]
    values = [30, 24, data["audit_summary"]["natural_positive_transport_eligible_count"], 42 - data["audit_summary"]["natural_positive_transport_eligible_count"]]
    axes[2].bar(labels, values, color=["tab:gray", "tab:red", "tab:green", "tab:purple"])
    axes[2].tick_params(axis="x", rotation=25)
    axes[2].set_ylabel("adjacent-scale pairs")
    axes[2].set_title("Natural dyadic-gauge outcome")
    axes[2].text(2, values[2] + 1.0, "35/42", ha="center", fontsize=9)
    axes[2].grid(True, axis="y", alpha=0.22)

    fig.tight_layout()
    output = ROOT / "figures" / "dyadic_packet_transport_gauge"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
