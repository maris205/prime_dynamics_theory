"""Render the RH-48 quadratic-identification summary figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "results" / "dyadic_identification_pilot.json"
OUTPUT_PDF = ROOT / "figures" / "intrinsic_riesz_identification.pdf"
OUTPUT_PNG = ROOT / "figures" / "intrinsic_riesz_identification.png"


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    pilot = load(PILOT)
    rows = pilot["rows"]
    colors = plt.cm.viridis(np.linspace(0.08, 0.92, len(rows)))
    figure, axes = plt.subplots(2, 2, figsize=(11.6, 8.4))

    axis = axes[0, 0]
    for color, row in zip(colors, rows):
        adjacent = sorted(
            row["adjacent_identification_defects"],
            key=lambda item: float(item["coarse_dimension"]),
        )
        dimension = np.asarray(
            [float(item["coarse_dimension"]) for item in adjacent]
        )
        defect = np.asarray(
            [float(item["weighted_defect_frobenius"]) for item in adjacent]
        )
        axis.loglog(
            dimension,
            defect,
            marker="o",
            linewidth=1.55,
            markersize=4.2,
            color=color,
            label=rf"$\sigma={float(row['sigma']):g}$",
        )
    first = rows[2]["adjacent_identification_defects"]
    x_ref = np.asarray(
        sorted(float(item["coarse_dimension"]) for item in first)
    )
    anchor = float(first[-1]["weighted_defect_frobenius"])
    n_anchor = float(first[-1]["coarse_dimension"])
    axis.loglog(
        x_ref,
        anchor * (x_ref / n_anchor) ** -2,
        color="black",
        linestyle="--",
        linewidth=1.2,
        label=r"reference $n^{-2}$",
    )
    axis.set_xlabel("coarse dimension $n$")
    axis.set_ylabel(r"$\|\Delta_{n,\sigma}\|_{\mathfrak{S}_2}$")
    axis.set_title("(a) Exact adjacent Haar defects")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.1, ncol=2)

    axis = axes[0, 1]
    resolution_count = len(rows[0]["adjacent_identification_defects"])
    markers = ("o", "s", "^")
    for index in range(resolution_count):
        sigma = np.asarray([float(row["sigma"]) for row in rows])
        adjacent = [row["adjacent_identification_defects"][index] for row in rows]
        resolution = float(adjacent[0]["coarse_dimension_times_sigma"])
        normalized = np.asarray(
            [
                float(item["weighted_defect_frobenius"])
                * float(item["coarse_dimension_times_sigma"]) ** 2
                for item in adjacent
            ]
        )
        axis.semilogx(
            sigma,
            normalized,
            marker=markers[index],
            linewidth=1.55,
            markersize=4.2,
            label=rf"$n\sigma={resolution:g}$",
        )
    axis.invert_xaxis()
    axis.set_xlabel("noise width $\sigma$ (decreasing to the right)")
    axis.set_ylabel(r"$(n\sigma)^2\|\Delta_{n,\sigma}\|_{\mathfrak{S}_2}$")
    axis.set_title("(b) Collapse on the observed $(n\sigma)^{-2}$ clock")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=8)

    axis = axes[1, 0]
    sigma = np.asarray([float(row["sigma"]) for row in rows])
    adjacent = [row["adjacent_identification_defects"][0] for row in rows]
    for branch, label, marker in (
        ("perron", "Perron", "o"),
        ("parity", "negative parity", "s"),
        ("weighted_rank_two", "weighted rank two", "^"),
    ):
        values = np.asarray(
            [
                float(item["branches"][branch]["defect_frobenius"])
                for item in adjacent
            ]
        )
        axis.loglog(
            sigma,
            values,
            marker=marker,
            linewidth=1.55,
            markersize=4.2,
            label=label,
        )
    axis.invert_xaxis()
    axis.set_xlabel("noise width $\sigma$ (decreasing to the right)")
    axis.set_ylabel("branch defect at $n\sigma=20.48$")
    axis.set_title("(c) Branch-resolved finite-matrix audit")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=8)

    axis = axes[1, 1]
    gamma = np.linspace(0.0, 1.25, 300)
    threshold = np.maximum(2.0, 1.5 + gamma)
    axis.plot(gamma, threshold, color="#9c2f45", linewidth=2.0)
    axis.fill_between(
        gamma,
        1.9,
        threshold,
        color="#dca0a8",
        alpha=0.25,
        label="not closed by the generic bound",
    )
    axis.axvspan(
        0.0,
        0.5,
        color="#74b887",
        alpha=0.18,
        label=r"every strict $p>2$ survives",
    )
    axis.axvline(0.5, color="black", linestyle="--", linewidth=1.0)
    axis.text(0.52, 2.02, r"$\gamma=1/2$", fontsize=9, va="bottom")
    axis.set_xlim(0.0, 1.25)
    axis.set_ylim(1.9, 2.85)
    axis.set_xlabel(r"directional gain exponent $\gamma$")
    axis.set_ylabel(r"required mesh power $p>\max(2,3/2+\gamma)$")
    axis.set_title("(d) The exact remaining directional gate")
    axis.grid(True, alpha=0.22)
    axis.legend(fontsize=7.6, loc="upper left")

    figure.suptitle(
        "Quadratic Schur identification: theorem boundary and exact-Haar evidence",
        fontsize=13.2,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PDF, bbox_inches="tight")
    figure.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
