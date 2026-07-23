"""Create the RH-108 support-certificate figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "fourth_cross_support_audit.json").read_text(encoding="utf-8"))
    thresholds = [float(value) for value in data["thresholds"]]
    colors = ["tab:blue", "tab:orange", "tab:green"]
    sigmas = [float(row["sigma"]) for row in data["rows"]]

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.35))
    ax = axes[0]
    for threshold, color in zip(thresholds, colors):
        record = data["threshold_summary"][f"{threshold:.0e}"]
        scales = record["scale_summary"]
        actual = [max(item["minimum_certified_ratio"], 1e-18) for item in scales]
        ax.semilogy(sigmas, actual, marker="o", linewidth=2.0, color=color, label=rf"certificate, $\tau={threshold:.0e}$")
        ax.axhline(threshold, color=color, linestyle="--", linewidth=1.0, alpha=0.65)
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"scale $\sigma$")
    ax.set_ylabel(r"minimum certified lower bound for $s_4/s_1$")
    ax.set_title("Five-snapshot Weyl support certificate")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    barrier = data["barrier"]["rows"]
    positive = [row for row in barrier if row["epsilon"] > 0.0]
    ax.loglog(
        [row["epsilon"] for row in positive],
        [row["ratio"] for row in positive],
        marker="o",
        linewidth=2.2,
        color="tab:red",
        label=r"exact $s_4/s_1=\varepsilon/4$",
    )
    ax.loglog(
        [row["epsilon"] for row in positive],
        [row["expected_ratio"] for row in positive],
        linestyle="--",
        color="black",
        linewidth=1.1,
        label="formula",
    )
    ax.set_xlabel(r"barrier parameter $\varepsilon$")
    ax.set_ylabel(r"$s_4/s_1$")
    ax.set_title("Normalized-memory nondegeneracy barrier")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)
    ax.text(
        0.06,
        0.08,
        "trace clock and diagonal blocks fixed\n" + r"$\varepsilon=0$ gives exact rank loss",
        transform=ax.transAxes,
        fontsize=9,
        bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
    )

    fig.tight_layout()
    output = ROOT / "figures" / "finite_memory_fourth_cross_support"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
