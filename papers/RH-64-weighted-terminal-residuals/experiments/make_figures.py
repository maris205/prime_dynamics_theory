"""Render the RH-64 weighted residual figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
INPUT = ROOT / "results" / "weighted_residual_pilot.json"
RH63 = PAPERS / "RH-63-nested-krylov-residual-closure" / "results" / "nested_krylov_pilot.json"
PDF = ROOT / "figures" / "weighted_terminal_residuals.pdf"
PNG = ROOT / "figures" / "weighted_terminal_residuals.png"


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    inherited = json.loads(RH63.read_text(encoding="utf-8"))
    names = [model["name"].replace("_", " ") for model in payload["models"]]
    positions = np.arange(len(names))
    euclidean = [model["euclidean_operator_norm"] for model in payload["models"]]
    weighted = [model["metric_contraction"] for model in payload["models"]]
    inherited_gain = [
        model["one_level_endpoint_gain"] for model in inherited["models"]
    ]
    weighted_gain = [
        model["one_level_endpoint_gain"] for model in payload["models"]
    ]

    figure, axes = plt.subplots(1, 2, figsize=(10.0, 4.2))
    width = 0.35
    axis = axes[0]
    axis.bar(positions - width / 2, euclidean, width, label="Euclidean norm", color="#9e9e9e")
    axis.bar(positions + width / 2, weighted, width, label="Lyapunov metric", color="#1f77b4")
    axis.axhline(1.0, color="#d62728", linestyle="--", linewidth=1.0)
    axis.set_xticks(positions, [str(index + 1) for index in positions])
    axis.set_ylabel("propagation contraction")
    axis.set_xlabel("model index")
    axis.set_title("Terminal propagation norm")
    axis.grid(True, axis="y", alpha=0.25)
    axis.legend(frameon=False, fontsize=8)

    axis = axes[1]
    axis.semilogy(
        positions,
        inherited_gain,
        "o-",
        color="#d62728",
        label="Euclidean residual",
    )
    axis.semilogy(
        positions,
        weighted_gain,
        "s-",
        color="#1f77b4",
        label="Lyapunov-weighted residual",
    )
    axis.set_xticks(positions, [str(index + 1) for index in positions])
    axis.set_ylabel("one-level upper / exact at $L=32$")
    axis.set_xlabel("model index")
    axis.set_title("Weighted one-level improvement")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(frameon=False, fontsize=8)

    figure.suptitle(
        "Models: 1 slow/fast surrogate, 2 two-block, 3 nonnormal chain",
        fontsize=10,
    )
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
