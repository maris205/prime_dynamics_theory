"""Reproduce the deterministic audits, small-noise tables, and all figures."""

from __future__ import annotations

import csv
import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy

from small_noise_cycles import (
    cycle_orbits,
    directed_curvature_extrapolation,
    directed_orbit_trace,
    estimate_boundary_minima,
    folded_gaussian_matrix,
    periodic_orbit_trace,
    trace_three,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
U_CRITICAL = 1.543689012692
SEPARATION = 0.12
PARAMETERS = (U_CRITICAL - SEPARATION, U_CRITICAL, U_CRITICAL + SEPARATION)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def word_cases() -> dict[str, tuple[float, ...]]:
    a, b, c = PARAMETERS
    return {
        "autonomous_three": (b,) * 3,
        "autonomous_six": (b,) * 6,
        "directed_three_forward": (a, b, c),
        "directed_three_reverse": (a, c, b),
        "directed_six_forward": (a, a, b, b, c, c),
        "directed_six_reverse": (a, a, c, c, b, b),
    }


def deterministic_audit() -> tuple[list[dict[str, object]], dict[str, float]]:
    rows: list[dict[str, object]] = []
    totals: dict[str, float] = {}
    for case, parameters in word_cases().items():
        records = cycle_orbits(parameters, grid_size=120_001)
        totals[case] = float(sum(record.weight for record in records))
        for index, record in enumerate(records, start=1):
            rows.append(
                {
                    "case": case,
                    "orbit_index": index,
                    "length": len(parameters),
                    "root": record.root,
                    "multiplier": record.multiplier,
                    "weight": record.weight,
                    "boundary_clearance": record.boundary_clearance,
                    "closure_error": record.closure_error,
                }
            )
    write_csv(RESULTS / "deterministic_orbits.csv", rows)
    return rows, totals


def boundary_action_audit() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for offset, (case, parameters) in enumerate(word_cases().items()):
        minima = estimate_boundary_minima(parameters, starts=800, seed=1729 + offset)
        for rank, record in enumerate(minima[:8], start=1):
            rows.append(
                {
                    "case": case,
                    "rank": rank,
                    "action": record.action,
                    "active_coordinates": record.active_coordinates,
                    "points": " ".join(f"{value:.12g}" for value in record.points),
                }
            )
    write_csv(RESULTS / "boundary_action_minima.csv", rows)
    return rows


def deterministic_curvatures() -> tuple[list[dict[str, object]], dict[str, float]]:
    separations = np.array((0.0030, 0.0020, 0.0015, 0.0010, 0.0007))
    rows: list[dict[str, object]] = []
    limits: dict[str, float] = {}
    for block_length, label in ((1, "three_step"), (2, "six_step")):
        audit = directed_curvature_extrapolation(
            U_CRITICAL,
            separations,
            block_length=block_length,
            grid_size=120_001,
        )
        limits[label] = float(audit["limit"])
        for epsilon, quotient in zip(audit["separations"], audit["quotients"]):
            rows.append(
                {
                    "case": label,
                    "separation": float(epsilon),
                    "separation_squared": float(epsilon * epsilon),
                    "vandermonde_quotient": float(quotient),
                    "extrapolated_limit": float(audit["limit"]),
                }
            )
    write_csv(RESULTS / "deterministic_curvature.csv", rows)
    return rows, limits


def finite_noise_audit(targets: dict[str, float]) -> list[dict[str, object]]:
    settings = (
        (0.080, 384),
        (0.060, 512),
        (0.050, 640),
        (0.040, 768),
        (0.030, 1024),
        (0.025, 1280),
        (0.020, 1536),
        (0.015, 2048),
        (0.012, 2560),
        (0.010, 3072),
        (0.008, 3840),
        (0.006, 5120),
        (0.005, 6144),
        (0.004, 7680),
    )
    a, b, c = PARAMETERS
    rows: list[dict[str, object]] = []
    target_three = targets["autonomous_three"]
    target_six = targets["autonomous_six"]
    target_directed_three = targets["directed_three_forward"] - targets["directed_three_reverse"]
    target_directed_six = targets["directed_six_forward"] - targets["directed_six_reverse"]

    for index, (sigma, dimension) in enumerate(settings, start=1):
        print(f"small-noise matrix {index}/{len(settings)}: sigma={sigma}, n={dimension}", flush=True)
        first = folded_gaussian_matrix(dimension, a, sigma)
        second = folded_gaussian_matrix(dimension, b, sigma)
        third = folded_gaussian_matrix(dimension, c, sigma)

        second_square = second @ second
        second_cube = second_square @ second
        trace_three_autonomous = float(np.trace(second_cube))
        trace_six_autonomous = float(np.trace(second_cube @ second_cube))

        directed_three = trace_three(first, second, third) - trace_three(first, third, second)
        first_square = first @ first
        third_square = third @ third
        directed_six = trace_three(first_square, second_square, third_square) - trace_three(
            first_square, third_square, second_square
        )

        rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "full_dimension": 2 * dimension,
                "dimension_times_sigma": dimension * sigma,
                "trace_three": trace_three_autonomous,
                "trace_three_target": target_three,
                "trace_three_error": abs(trace_three_autonomous - target_three),
                "trace_six": trace_six_autonomous,
                "trace_six_target": target_six,
                "trace_six_error": abs(trace_six_autonomous - target_six),
                "directed_three": directed_three,
                "directed_three_target": target_directed_three,
                "directed_three_error": abs(directed_three - target_directed_three),
                "directed_six": directed_six,
                "directed_six_target": target_directed_six,
                "directed_six_error": abs(directed_six - target_directed_six),
            }
        )
    write_csv(RESULTS / "small_noise_traces.csv", rows)
    return rows


def lowest_noise_resolution_audit(smallest_noise_row: dict[str, object]) -> list[dict[str, object]]:
    """Hold ``sigma=0.004`` fixed and verify that the orbit approach is resolved."""

    sigma = float(smallest_noise_row["sigma"])
    a, b, c = PARAMETERS
    rows: list[dict[str, object]] = []
    for dimension in (3072, 4096, 5120, 6144):
        print(f"resolution audit: sigma={sigma}, n={dimension}", flush=True)
        first = folded_gaussian_matrix(dimension, a, sigma)
        second = folded_gaussian_matrix(dimension, b, sigma)
        third = folded_gaussian_matrix(dimension, c, sigma)
        second_square = second @ second
        second_cube = second_square @ second
        first_square = first @ first
        third_square = third @ third
        rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "full_dimension": 2 * dimension,
                "dimension_times_sigma": dimension * sigma,
                "trace_three": float(np.trace(second_cube)),
                "trace_six": float(np.trace(second_cube @ second_cube)),
                "directed_three": trace_three(first, second, third) - trace_three(first, third, second),
                "directed_six": trace_three(first_square, second_square, third_square)
                - trace_three(first_square, third_square, second_square),
            }
        )
    rows.append(
        {
            key: smallest_noise_row[key]
            for key in (
                "sigma",
                "folded_dimension",
                "full_dimension",
                "dimension_times_sigma",
                "trace_three",
                "trace_six",
                "directed_three",
                "directed_six",
            )
        }
    )
    write_csv(RESULTS / "lowest_noise_resolution.csv", rows)
    return rows


def fit_power(rows: list[dict[str, object]], field: str, tail: int = 5) -> float:
    sigma = np.asarray([float(row["sigma"]) for row in rows[-tail:]])
    error = np.asarray([float(row[field]) for row in rows[-tail:]])
    return float(np.polyfit(np.log(sigma), np.log(error), 1)[0])


def plot_orbit_geometry(
    orbit_rows: list[dict[str, object]],
    action_rows: list[dict[str, object]],
) -> None:
    grid = np.linspace(-1.0, 1.0, 4001)

    def composed(points: np.ndarray, length: int) -> np.ndarray:
        values = points.copy()
        for _ in range(length):
            values = 1.0 - U_CRITICAL * values * values
        return values

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.45))
    for length, color in ((3, "#2455a4"), (6, "#a0273f")):
        residual = composed(grid, length) - grid
        axes[0].plot(grid, residual, color=color, lw=1.2, label=fr"$f^{{{length}}}(x)-x$")
    axes[0].axhline(0.0, color="0.25", lw=0.8)
    axes[0].set(xlabel=r"$x$", ylabel="fixed-point residual", title="Deterministic closure")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(alpha=0.22)

    six = [row for row in orbit_rows if row["case"] == "autonomous_six"]
    scatter = axes[1].scatter(
        [float(row["root"]) for row in six],
        [float(row["weight"]) for row in six],
        c=[float(row["boundary_clearance"]) for row in six],
        cmap="viridis",
        s=35,
        edgecolor="black",
        linewidth=0.3,
    )
    colorbar = fig.colorbar(scatter, ax=axes[1], fraction=0.046, pad=0.04)
    colorbar.set_label("boundary clearance", fontsize=8)
    colorbar.ax.tick_params(labelsize=7)
    axes[1].set(
        xlabel="six-step fixed point",
        ylabel=r"$|1-(f^6)'|^{-1}$",
        title="Fifteen six-step weights",
    )
    axes[1].grid(alpha=0.22)

    cases = [
        "autonomous_three",
        "autonomous_six",
        "directed_three_forward",
        "directed_three_reverse",
        "directed_six_forward",
        "directed_six_reverse",
    ]
    labels = ["3", "6", "3F", "3R", "6F", "6R"]
    minima = []
    for case in cases:
        values = [float(row["action"]) for row in action_rows if row["case"] == case]
        minima.append(min(values) if values else np.nan)
    axes[2].bar(labels, minima, color=["#2455a4", "#a0273f", "#3a8f6b", "#78b79c", "#cf7b28", "#e4aa67"])
    axes[2].set_yscale("log")
    axes[2].set(xlabel="parameter word", ylabel="least audited positive action", title="Boundary-action onset")
    axes[2].grid(axis="y", alpha=0.22)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"orbit_action_geometry.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_small_noise(rows: list[dict[str, object]]) -> None:
    sigma = np.asarray([float(row["sigma"]) for row in rows])
    order = np.argsort(sigma)
    sigma = sigma[order]

    def values(field: str) -> np.ndarray:
        return np.asarray([float(row[field]) for row in rows])[order]

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.0))
    panels = (
        ("trace_three", "trace_three_target", r"$\operatorname{tr}K_\sigma^3$", "Three-step localization", False),
        ("trace_six", "trace_six_target", r"$\operatorname{tr}K_\sigma^6$", "Six-step localization", False),
        ("directed_three", "directed_three_target", r"$\Omega_{3,\sigma}/\Omega_{3,0}$", "Directed three-step trace", True),
        ("directed_six", "directed_six_target", r"$\Omega_{6,\sigma}/\Omega_{6,0}$", "Directed six-step trace", True),
    )
    for axis, (field, target_field, ylabel, title, normalize) in zip(axes.flat, panels):
        data = values(field)
        target = values(target_field)[0]
        if normalize:
            data = data / target
            target = 1.0
        axis.plot(sigma, data, "o-", color="#2455a4", lw=1.4, ms=4, label="finite noise")
        axis.axhline(target, color="#b52a3a", ls="--", lw=1.2, label="orbit target")
        axis.set(xscale="log", xlabel=r"noise width $\sigma$", ylabel=ylabel, title=title)
        axis.invert_xaxis()
        axis.grid(alpha=0.25)
        axis.legend(frameon=False, fontsize=8)
        if field == "directed_three":
            axis.set_yscale("log")
        if field == "directed_six":
            axis.set_yscale("symlog", linthresh=0.25)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"small_noise_localization.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def plot_curvature(rows: list[dict[str, object]]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9.9, 3.65))
    for axis, case, color, title in (
        (axes[0], "three_step", "#2455a4", "Three-step deterministic curvature"),
        (axes[1], "six_step", "#a0273f", "Parity-compatible six-step curvature"),
    ):
        selected = [row for row in rows if row["case"] == case]
        x = np.asarray([float(row["separation_squared"]) for row in selected])
        quotient = np.asarray([float(row["vandermonde_quotient"]) for row in selected])
        target = float(selected[0]["extrapolated_limit"])
        y = quotient - target
        coefficients = np.polyfit(x, y, 2)
        xx = np.linspace(0.0, 1.05 * np.max(x), 200)
        axis.plot(xx, np.polyval(coefficients, xx), color=color, lw=1.4, label="quadratic fit")
        axis.scatter(x, y, color=color, edgecolor="black", linewidth=0.3, zorder=3, label="orbit quotient")
        axis.scatter([0.0], [0.0], marker="*", s=85, color="#e39b20", edgecolor="black", linewidth=0.4, zorder=4, label="diagonal limit")
        axis.set(xlabel=r"squared separation $\varepsilon^2$", ylabel="quotient minus diagonal limit", title=title)
        axis.ticklabel_format(axis="y", style="sci", scilimits=(0, 0), useOffset=False)
        axis.grid(alpha=0.24)
        axis.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    for suffix in ("pdf", "png"):
        fig.savefig(FIGURES / f"deterministic_curvature.{suffix}", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    FIGURES.mkdir(exist_ok=True)
    orbit_rows, totals = deterministic_audit()
    action_rows = boundary_action_audit()
    curvature_rows, curvature_limits = deterministic_curvatures()
    noise_rows = finite_noise_audit(totals)
    resolution_rows = lowest_noise_resolution_audit(noise_rows[-1])

    directed_three_target = totals["directed_three_forward"] - totals["directed_three_reverse"]
    directed_six_target = totals["directed_six_forward"] - totals["directed_six_reverse"]
    summary = {
        "parameters": {
            "u_critical": U_CRITICAL,
            "directed_triple": PARAMETERS,
            "folded_dimension_convention": "full dimension is twice the recorded dimension",
        },
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "deterministic_targets": {
            "trace_three": totals["autonomous_three"],
            "trace_six": totals["autonomous_six"],
            "directed_three": directed_three_target,
            "directed_six": directed_six_target,
            "curvature_three": curvature_limits["three_step"],
            "curvature_six": curvature_limits["six_step"],
        },
        "fixed_point_audit": {
            case: {
                "count": sum(row["case"] == case for row in orbit_rows),
                "minimum_boundary_clearance": min(
                    float(row["boundary_clearance"]) for row in orbit_rows if row["case"] == case
                ),
                "minimum_determinant": min(
                    abs(1.0 - float(row["multiplier"])) for row in orbit_rows if row["case"] == case
                ),
            }
            for case in word_cases()
        },
        "least_positive_boundary_actions": {
            case: min(float(row["action"]) for row in action_rows if row["case"] == case)
            for case in word_cases()
        },
        "small_noise_fits": {
            "trace_three_error_power": fit_power(noise_rows, "trace_three_error", tail=5),
            "directed_three_error_power": fit_power(noise_rows, "directed_three_error", tail=4),
        },
        "smallest_noise": noise_rows[-1],
        "lowest_noise_resolution_spread": {
            field: max(float(row[field]) for row in resolution_rows)
            - min(float(row[field]) for row in resolution_rows)
            for field in ("trace_three", "trace_six", "directed_three", "directed_six")
        },
    }
    (RESULTS / "small_noise_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    plot_orbit_geometry(orbit_rows, action_rows)
    plot_small_noise(noise_rows)
    plot_curvature(curvature_rows)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
