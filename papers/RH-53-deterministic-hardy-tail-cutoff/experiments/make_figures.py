"""Render the RH-53 deterministic-tail and cutoff-transfer figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "results" / "deterministic_tail_pilot.json"
CERTIFICATE = ROOT / "results" / "hardy_tail_cutoff_certificate.json"
OUTPUT_PDF = ROOT / "figures" / "deterministic_hardy_tail_cutoff.pdf"
OUTPUT_PNG = ROOT / "figures" / "deterministic_hardy_tail_cutoff.png"


def main() -> None:
    pilot = json.loads(PILOT.read_text(encoding="utf-8"))
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    rows = pilot["rows"]
    dimensions = np.asarray([row["fine_dimension"] for row in rows])
    figure, axes = plt.subplots(2, 2, figsize=(11.7, 8.5))

    axis = axes[0, 0]
    for side, marker, color in (
        ("left", "o", "tab:blue"),
        ("right", "s", "tab:orange"),
    ):
        exact = np.asarray([row[side]["exact_dense_energy"] for row in rows])
        upper = np.asarray([row[side]["full_energy_upper"] for row in rows])
        axis.semilogx(
            dimensions,
            exact,
            marker + "-",
            color=color,
            label=f"{side} exact Gramian",
        )
        axis.semilogx(
            dimensions,
            upper,
            marker + "--",
            color=color,
            markerfacecolor="none",
            label=f"{side} deterministic upper",
        )
    axis.set_xlabel("fine dimension $N$")
    axis.set_ylabel("full Hardy energy")
    axis.set_title("(a) Deterministic all-column sums certify the full energy")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5)

    axis = axes[0, 1]
    for side, marker, color in (
        ("left", "o", "tab:blue"),
        ("right", "s", "tab:orange"),
    ):
        tail = np.asarray(
            [row[side]["selected_infinite_tail_upper"] for row in rows]
        )
        excess = np.asarray(
            [row[side]["relative_energy_excess"] for row in rows]
        )
        axis.loglog(
            dimensions,
            tail,
            marker + "-",
            color=color,
            label=f"{side} tail in energy squared",
        )
        axis.loglog(
            dimensions,
            excess,
            marker + ":",
            color=color,
            label=f"{side} relative energy excess",
        )
    axis.set_xlabel("fine dimension $N$")
    axis.set_ylabel("certificate remainder")
    axis.set_title("(b) One contracting block replaces fitted time-64 decay")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5)

    axis = axes[1, 0]
    for multiple, marker in ((5.0, "o"), (6.0, "s"), (8.0, "^")):
        values = [
            next(
                item["two_norm_upper"]
                for item in row["cutoff_bounds"]
                if item["declared_multiple"] == multiple
            )
            for row in rows
        ]
        axis.loglog(
            dimensions,
            values,
            marker + "-",
            label=rf"fixed $L={multiple:g}$",
        )
    adaptive = [row["adaptive_cutoff"]["two_norm_upper"] for row in rows]
    axis.loglog(dimensions, adaptive, "d--", color="black", label="adaptive $L(h)$")
    axis.set_xlabel("fine dimension $N$")
    axis.set_ylabel(r"analytic $\|P^{(L)}-P\|_2$ upper")
    axis.set_title("(c) Eight sigma is tiny on stored scales, not asymptotic")
    axis.grid(True, which="both", alpha=0.22)
    axis.legend(fontsize=7.5)

    axis = axes[1, 1]
    production = certificate["rh50_production_cutoff_ledger"]["rows"]
    production_dimension = np.asarray(
        [row["fine_dimension"] for row in production]
    )
    fixed = np.asarray(
        [row["fixed_eight_analytic_two_norm_upper"] for row in production]
    )
    adaptive_upper = np.asarray(
        [row["adaptive_analytic_two_norm_upper"] for row in production]
    )
    adaptive_multiple = np.asarray([row["adaptive_multiple"] for row in production])
    axis.loglog(
        production_dimension,
        fixed,
        "o-",
        color="tab:purple",
        label="production fixed-eight upper",
    )
    axis.loglog(
        production_dimension,
        adaptive_upper,
        "s--",
        color="tab:green",
        label="production adaptive upper",
    )
    axis.set_xlabel("RH-50 fine dimension $N$")
    axis.set_ylabel("analytic cutoff upper")
    axis.set_title("(d) Production cutoff constants through $N=40960$")
    axis.grid(True, which="both", alpha=0.22)
    twin = axis.twinx()
    twin.semilogx(
        production_dimension,
        adaptive_multiple,
        "^:",
        color="tab:red",
        label="required adaptive multiple",
    )
    twin.axhline(8.0, color="tab:red", alpha=0.35, linewidth=1.0)
    twin.set_ylabel("support multiple", color="tab:red")
    twin.tick_params(axis="y", labelcolor="tab:red")
    lines, labels = axis.get_legend_handles_labels()
    lines2, labels2 = twin.get_legend_handles_labels()
    axis.legend(lines + lines2, labels + labels2, fontsize=7.3, loc="lower left")

    figure.suptitle(
        "Deterministic Hardy tails and the honest sparse-to-full Gaussian route",
        fontsize=13.0,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(OUTPUT_PDF, bbox_inches="tight")
    figure.savefig(OUTPUT_PNG, dpi=220, bbox_inches="tight")
    plt.close(figure)


if __name__ == "__main__":
    main()
