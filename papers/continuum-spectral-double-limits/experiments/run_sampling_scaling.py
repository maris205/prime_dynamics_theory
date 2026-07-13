#!/usr/bin/env python3
"""Measure strong-row and weak-observable multinomial sampling scales."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from continuum_limits.sampling import representative_gaussian_row, sampling_diagnostics
from continuum_limits.windows import response_windows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dimensions",
        nargs="+",
        type=int,
        default=[64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536, 2048],
    )
    parser.add_argument("--total-transitions", type=int, default=100_000_000)
    parser.add_argument("--repetitions", type=int, default=500)
    parser.add_argument("--sigma", type=float, default=0.05)
    parser.add_argument("--u", type=float, default=1.5437)
    parser.add_argument("--source", type=float, default=0.8)
    parser.add_argument("--p", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=20260713)
    parser.add_argument("--csv", type=Path, default=Path("results/sampling_scaling.csv"))
    parser.add_argument("--json", type=Path, default=Path("results/sampling_scaling.json"))
    parser.add_argument("--figure", type=Path, default=Path("figures/sampling_windows.pdf"))
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    rows: list[dict[str, float | int]] = []
    for d in args.dimensions:
        centers, probabilities = representative_gaussian_row(
            d, sigma=args.sigma, u=args.u, source=args.source
        )
        observable = np.cos(np.pi * centers) + 0.3 * np.sin(2.0 * np.pi * centers)
        source_count = max(1, args.total_transitions // d)
        diagnostics = sampling_diagnostics(
            probabilities,
            observable,
            source_count,
            args.repetitions,
            rng,
        )
        row: dict[str, float | int] = {
            "d": d,
            "total_transitions": args.total_transitions,
            "source_count": source_count,
            **diagnostics,
            "normalized_l1": diagnostics["mean_l1_error"]
            * np.sqrt(args.total_transitions)
            / d,
            "normalized_observable": diagnostics["observable_rms_error"]
            * np.sqrt(args.total_transitions / d),
        }
        rows.append(row)
        print(json.dumps(row, indent=2))

    d_values = np.array([row["d"] for row in rows], dtype=float)
    l1_values = np.array([row["mean_l1_error"] for row in rows], dtype=float)
    weak_values = np.array([row["observable_rms_error"] for row in rows], dtype=float)
    fit_mask = d_values >= 256
    l1_slope = float(np.polyfit(np.log(d_values[fit_mask]), np.log(l1_values[fit_mask]), 1)[0])
    weak_slope = float(
        np.polyfit(np.log(d_values[fit_mask]), np.log(weak_values[fit_mask]), 1)[0]
    )

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    metadata = {
        "parameters": {
            "dimensions": args.dimensions,
            "total_transitions": args.total_transitions,
            "repetitions": args.repetitions,
            "sigma": args.sigma,
            "u": args.u,
            "source": args.source,
            "p": args.p,
            "seed": args.seed,
        },
        "fitted_dimension_slopes": {
            "mean_l1_error": l1_slope,
            "observable_rms_error": weak_slope,
        },
    }
    with args.json.open("w") as handle:
        json.dump(metadata, handle, indent=2)

    fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.35))
    l1_bound = np.array([row["l1_upper_bound"] for row in rows], dtype=float)
    weak_exact = np.array([row["observable_exact_rms"] for row in rows], dtype=float)
    axes[0].loglog(d_values, l1_values, "o-", label="Monte Carlo mean")
    axes[0].loglog(d_values, l1_bound, "--", label="rigorous mean bound")
    axes[0].loglog(
        d_values,
        l1_values[0] * d_values / d_values[0],
        ":",
        label=rf"$d$ guide (fit {l1_slope:.2f})",
    )
    axes[0].set_title("Strong row error")
    axes[0].set_xlabel(r"dimension $d$")
    axes[0].set_ylabel(r"$\mathbb{E}\|\widehat p-p\|_1$")
    axes[0].legend(frameon=False, fontsize=8)

    axes[1].loglog(d_values, weak_values, "o-", label="Monte Carlo RMS")
    axes[1].loglog(d_values, weak_exact, "--", label="exact RMS")
    axes[1].loglog(
        d_values,
        weak_values[0] * np.sqrt(d_values / d_values[0]),
        ":",
        label=rf"$d^{{1/2}}$ guide (fit {weak_slope:.2f})",
    )
    axes[1].set_title("One smooth observable")
    axes[1].set_xlabel(r"dimension $d$")
    axes[1].set_ylabel("RMS error")
    axes[1].legend(frameon=False, fontsize=8)

    horizons = np.logspace(4.0, 20.0, 500)
    windows = response_windows(horizons, args.p)
    axes[2].loglog(horizons, windows["deterministic_lower"], label="discretization lower")
    axes[2].loglog(horizons, windows["strong_upper"], label="strong empirical upper")
    axes[2].loglog(horizons, windows["weak_upper"], label="weak observable upper")
    axes[2].scatter([1.0e6], [5000.0], marker="x", s=55, color="black", label="exploratory scale")
    axes[2].set_title(rf"Response windows, $p={args.p:g}$")
    axes[2].set_xlabel(r"horizon $T$")
    axes[2].set_ylabel(r"dimension scale $d(T)$")
    axes[2].legend(frameon=False, fontsize=7)

    for axis in axes:
        axis.grid(alpha=0.25, which="both")
    fig.tight_layout()
    args.figure.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.figure)
    fig.savefig(args.figure.with_suffix(".png"), dpi=180)


if __name__ == "__main__":
    main()
