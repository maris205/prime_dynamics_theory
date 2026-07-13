#!/usr/bin/env python3
"""Verify weighted slow-variation and anchored logarithmic-age coefficients."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from gaussian_response.schedules import power_weighted_schedule_means


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--horizons", nargs="+", type=int, default=[1000, 10000, 100000, 1000000, 10000000])
    parser.add_argument("--exponents", nargs="+", type=float, default=[0.0, 1.0, 3.0])
    parser.add_argument("--kappa", type=float, default=0.02)
    parser.add_argument("--p", type=float, default=2.0)
    parser.add_argument("--c", type=float, default=10.0)
    parser.add_argument("--output", type=Path, default=Path("results/schedule_scaling.csv"))
    parser.add_argument("--figure", type=Path, default=Path("figures/schedule_scaling.pdf"))
    args = parser.parse_args()

    rows: list[dict[str, float | int | str]] = []
    exponents = tuple(args.exponents)
    for T in args.horizons:
        ordinary = power_weighted_schedule_means(
            T, exponents, kappa=args.kappa, p=args.p, c=args.c, anchored=False
        )
        anchored = power_weighted_schedule_means(
            T, exponents, kappa=args.kappa, p=args.p, c=args.c, anchored=True
        )
        scale_log = np.log(T + args.c)
        for exponent in exponents:
            rows.append(
                {
                    "T": T,
                    "weight_exponent": exponent,
                    "schedule": "unanchored",
                    "scaled_coefficient": ordinary[exponent] * scale_log**args.p / args.kappa,
                    "theory": 1.0,
                }
            )
            rows.append(
                {
                    "T": T,
                    "weight_exponent": exponent,
                    "schedule": "anchored",
                    "scaled_coefficient": anchored[exponent]
                    * scale_log ** (args.p + 1.0)
                    / (args.p * args.kappa),
                    "theory": 1.0 / (exponent + 1.0),
                }
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.6), sharex=True)
    for axis, schedule, title in zip(
        axes,
        ("unanchored", "anchored"),
        ("Unanchored response", "Endpoint-anchored response"),
    ):
        for exponent in exponents:
            selected = [
                row for row in rows
                if row["schedule"] == schedule and row["weight_exponent"] == exponent
            ]
            axis.plot(
                [row["T"] for row in selected],
                [row["scaled_coefficient"] for row in selected],
                marker="o",
                label=rf"$w(x)=x^{{{exponent:g}}}$",
            )
            axis.axhline(selected[0]["theory"], color="black", linewidth=0.7, alpha=0.35)
        axis.set_xscale("log")
        axis.set_title(title)
        axis.set_xlabel(r"horizon $T$")
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("scaled weighted coefficient")
    axes[0].legend(frameon=False)
    fig.tight_layout()
    args.figure.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.figure)
    fig.savefig(args.figure.with_suffix(".png"), dpi=180)


if __name__ == "__main__":
    main()
