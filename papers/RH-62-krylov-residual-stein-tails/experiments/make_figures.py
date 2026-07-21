"""Render the RH-62 Krylov residual figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "krylov_tail_pilot.json"
PDF = ROOT / "figures" / "krylov_residual_tail.pdf"
PNG = ROOT / "figures" / "krylov_residual_tail.png"


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    models = payload["models"]
    figure, axes = plt.subplots(1, 2, figsize=(10.0, 4.2))
    colors = ("#1f77b4", "#d62728", "#2ca02c")

    axis = axes[0]
    for index, model in enumerate(models):
        dimensions = sorted(
            int(value) for value in model["horizons"]["32"].keys()
        )
        ratios = [
            model["horizons"]["32"][str(dimension)]["krylov_over_exact"]
            for dimension in dimensions
        ]
        geometric = model["endpoint_geometric_gain"]
        axis.semilogy(
            dimensions,
            ratios,
            "o-",
            color=colors[index],
            label=model["name"].replace("_", " "),
        )
        axis.axhline(
            geometric,
            color=colors[index],
            linestyle="--",
            alpha=0.45,
        )
    axis.set_xlabel("Krylov dimension")
    axis.set_ylabel("upper / exact power norm at $L=32$")
    axis.set_title("Residual certificate versus ordinary norm")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(frameon=False, fontsize=7)

    endpoint = models[0]
    axis = axes[1]
    horizons = sorted(int(value) for value in endpoint["horizons"])
    for dimension, marker, color in ((1, "o", "#1f77b4"), (2, "s", "#d62728")):
        ratios = [
            endpoint["horizons"][str(horizon)][str(dimension)][
                "krylov_over_exact"
            ]
            for horizon in horizons
        ]
        geometric = [
            endpoint["horizons"][str(horizon)][str(dimension)][
                "geometric_over_exact"
            ]
            for horizon in horizons
        ]
        axis.semilogy(
            horizons,
            ratios,
            marker=marker,
            color=color,
            label=f"Krylov k={dimension}",
        )
        if dimension == 1:
            axis.semilogy(
                horizons,
                geometric,
                "--",
                color="#555555",
                label="ordinary norm envelope",
            )
    axis.set_xlabel("horizon $L$")
    axis.set_ylabel("upper / exact power norm")
    axis.set_title("RH-61-calibrated slow/fast surrogate")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(frameon=False, fontsize=8)

    figure.tight_layout(pad=1.0)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=180, bbox_inches="tight")
    print(
        json.dumps(
            {"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT))},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
