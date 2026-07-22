"""Create RH-67 covariance-envelope tradeoff figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "covariance_envelope_pilot.json"
PDF = ROOT / "figures" / "physical_covariance_block_envelopes.pdf"
PNG = ROOT / "figures" / "physical_covariance_block_envelopes.png"


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    cancellation, chain, phase = payload["models"]
    figure, axes = plt.subplots(1, 2, figsize=(10.6, 4.2))

    rows = cancellation["rows"]
    epsilons = [row["epsilon"] for row in rows]
    axes[0].loglog(
        epsilons,
        [row["physical_gain"] for row in rows],
        marker="o",
        linewidth=1.9,
        color="#2f7d5b",
        label="physical-ray gain",
    )
    axes[0].loglog(
        epsilons,
        [row["global_spectral_gain"] for row in rows],
        marker="s",
        linewidth=1.9,
        color="#9c2f2f",
        label="global spectral gain",
    )
    axes[0].set_title("Exact cancellation tradeoff")
    axes[0].set_xlabel(r"covariance floor $\varepsilon$")
    axes[0].set_ylabel("envelope / exact")
    axes[0].invert_xaxis()
    axes[0].grid(True, which="both", alpha=0.24)
    axes[0].legend(frameon=False, fontsize=9)

    for model, color, marker, label in (
        (chain, "#9c2f2f", "o", "nonnormal chain"),
        (phase, "#4f7cac", "s", "complex phase"),
    ):
        rows = model["rows"]
        excess = [
            max(
                1.0e-16,
                row["physical_gain"] / row["directional_optimal_gain"]
                - 1.0,
            )
            for row in rows
        ]
        axes[1].loglog(
            [row["epsilon"] for row in rows],
            excess,
            marker=marker,
            linewidth=1.9,
            color=color,
            label=label,
        )
    axes[1].set_title("Convergence to directional optimum")
    axes[1].set_xlabel(r"covariance floor $\varepsilon$")
    axes[1].set_ylabel("physical gain / optimum $-1$")
    axes[1].invert_xaxis()
    axes[1].grid(True, which="both", alpha=0.24)
    axes[1].legend(frameon=False, fontsize=9)
    figure.tight_layout()
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)
    print(PDF.relative_to(ROOT))
    print(PNG.relative_to(ROOT))


if __name__ == "__main__":
    main()
