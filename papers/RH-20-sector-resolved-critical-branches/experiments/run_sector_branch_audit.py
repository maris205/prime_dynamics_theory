"""Generate two-branch, phase-family, and bright/dark audits for RH-20."""

from __future__ import annotations

import csv
import ctypes
import gc
import hashlib
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH16 = PAPERS / "RH-16-endpoint-gaussian-resolution-rank"
RH17 = PAPERS / "RH-17-time-ordered-boundary-monodromy"
RH18 = PAPERS / "RH-18-branch-isolated-gaussian-return"
RH19 = PAPERS / "RH-19-complement-excursion-self-energy"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH16 / "src"),
    str(RH17 / "src"),
    str(RH18 / "src"),
    str(RH19 / "src"),
]

from complement_excursions import (  # noqa: E402
    apply_deflated,
    apply_restricted_return,
    critical_branch_masks,
    resolve_peripheral_projectors,
)
from endpoint_rank import (  # noqa: E402
    HALF_ENERGY_THRESHOLD,
    boundary_clearances,
    threshold_rank,
)
from gaussian_return import (  # noqa: E402
    effective_noise_scales,
    packet_masks,
    periodic_packet_tube,
    positive_midpoints,
    sparse_folded_gaussian_matrix,
)
from sector_branches import (  # noqa: E402
    branch_profile_basis,
    bright_dark_transform,
    compressed_branch_cycle,
    dense_matrix,
    forced_relative_phase,
    phase_weighted_return,
)
from time_ordered_monodromy import boundary_cycle, critical_constants  # noqa: E402


WINDOW_MULTIPLE = 6.0
DENSE_SIGMA = 1.0e-3
PHASE_POINTS = 181


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release_memory() -> None:
    gc.collect()
    try:
        ctypes.CDLL(None).malloc_trim(0)
    except (AttributeError, OSError):
        pass


def cycle_context(period: int):
    constants = critical_constants(130)
    cycle = boundary_cycle(int(period), 130)
    points = np.asarray([float(value) for value in cycle.orbit])
    multipliers = np.abs(
        np.asarray([float(value) for value in cycle.two_step_derivatives])
    )
    tube = periodic_packet_tube(
        multipliers, effective_noise_scales(points, float(constants.u))
    )
    return constants, cycle, points, tube


def context_at_noise(sigma: float, dimension: int, period: int):
    constants, cycle, points, tube = cycle_context(period)
    grid = positive_midpoints(dimension)
    matrix = sparse_folded_gaussian_matrix(
        dimension, sigma, u=float(constants.u)
    )
    base = packet_masks(
        grid,
        points,
        sigma * tube.widths,
        window_multiple=WINDOW_MULTIPLE,
        critical_partition=float(constants.first_interior_point),
    )
    left, right, both = critical_branch_masks(
        grid,
        base,
        points[-1],
        sigma * tube.widths[-1],
        window_multiple=WINDOW_MULTIPLE,
        partition=float(constants.first_interior_point),
    )
    endpoint = np.exp(
        -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
    )
    endpoint[~left[0]] = 0.0

    def two_step(vector):
        return matrix @ (matrix @ vector)

    critical = two_step(endpoint)
    basis = branch_profile_basis(critical, left[-1], right[-1])
    return {
        "sigma": sigma,
        "dimension": dimension,
        "period": period,
        "matrix": matrix,
        "grid": grid,
        "points": points,
        "tube": tube,
        "left": left,
        "right": right,
        "both": both,
        "endpoint": endpoint,
        "basis": basis,
        "two_step": two_step,
    }


def seven_noise_branch_matrices():
    archived = read_csv(RH15 / "results" / "cloud_summary.csv")
    return_rows = {
        float(row["sigma"]): row
        for row in read_csv(RH19 / "results" / "branch_return_decomposition.csv")
    }
    clearances = boundary_clearances(70, decimal_digits=110)
    rows: list[dict[str, object]] = []
    dense_context = None

    for archived_row in archived:
        sigma = float(archived_row["sigma"])
        dimension = int(float(archived_row["folded_dimension"]))
        degree = threshold_rank(
            clearances,
            sigma,
            threshold=HALF_ENERGY_THRESHOLD,
            power=0.5,
        )
        period = degree + 1
        print(
            f"branch matrix sigma={sigma:g}, n={dimension}, k={period}",
            flush=True,
        )
        started = time.time()
        context = context_at_noise(sigma, dimension, period)
        branch_matrix = compressed_branch_cycle(
            context["two_step"], context["left"][:-1], context["basis"]
        )
        values = np.linalg.eigvals(branch_matrix)
        order = np.argsort(-np.abs(values))
        bright = values[order[0]]
        dark = values[order[1]]
        transformed = bright_dark_transform(branch_matrix)

        source = return_rows[sigma]
        left_eta = float(source["left_return_eigenvalue"])
        right_eta = float(source["right_return_eigenvalue"])
        bulk_radius = float(archived_row["bulk_radius"])
        bulk_return_modulus = bulk_radius ** (2 * period)
        preserve_phase = forced_relative_phase(left_eta, right_eta, left_eta)
        try:
            bulk_phase = forced_relative_phase(
                left_eta, right_eta, bulk_return_modulus
            )
        except ValueError:
            bulk_phase = np.nan
        cubic_return = abs(
            left_eta + np.exp(2j * np.pi / 3.0) * right_eta
        )
        rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "component_period": period,
                "matrix_00": branch_matrix[0, 0].real,
                "matrix_01": branch_matrix[0, 1].real,
                "matrix_10": branch_matrix[1, 0].real,
                "matrix_11": branch_matrix[1, 1].real,
                "bright_eigenvalue_real": bright.real,
                "bright_eigenvalue_imag": bright.imag,
                "dark_eigenvalue_real": dark.real,
                "dark_eigenvalue_imag": dark.imag,
                "dark_to_bright_modulus_ratio": abs(dark) / abs(bright),
                "compressed_bright_one_step_radius": abs(bright)
                ** (1.0 / (2 * period)),
                "branch_complete_one_step_radius": float(
                    source["both_one_step_radius"]
                ),
                "bright_dark_00": transformed[0, 0].real,
                "bright_dark_01": transformed[0, 1].real,
                "bright_dark_10": transformed[1, 0].real,
                "bright_dark_11": transformed[1, 1].real,
                "left_return_eigenvalue": left_eta,
                "right_return_eigenvalue": right_eta,
                "right_to_left_return_ratio": right_eta / left_eta,
                "preserve_left_phase_over_pi": preserve_phase / np.pi,
                "match_bulk_phase_over_pi": bulk_phase / np.pi,
                "cubic_phase_one_step_radius": cubic_return
                ** (1.0 / (2 * period)),
                "left_one_step_radius": float(source["left_one_step_radius"]),
                "archived_bulk_radius": bulk_radius,
                "elapsed_seconds": time.time() - started,
            }
        )
        if abs(sigma - DENSE_SIGMA) < 1.0e-15:
            dense_context = context
        else:
            del context
            release_memory()

    write_csv(RESULTS / "two_branch_matrix_audit.csv", rows)
    if dense_context is None:
        raise RuntimeError("dense audit context was not retained")
    return rows, dense_context


def dense_phase_audit(context):
    matrix = context["matrix"]
    left = context["left"]
    right = context["right"]
    period = int(context["period"])
    dimension = int(context["dimension"])
    endpoint_indices = np.flatnonzero(left[0])

    def return_operator(masks, step):
        return lambda vector: apply_restricted_return(
            step,
            masks,
            endpoint_indices,
            vector,
            dimension=dimension,
        )

    print(f"materializing {endpoint_indices.size}x{endpoint_indices.size} raw returns", flush=True)
    raw_left = dense_matrix(
        return_operator(left, context["two_step"]), endpoint_indices.size
    )
    raw_right = dense_matrix(
        return_operator(right, context["two_step"]), endpoint_indices.size
    )
    projectors = resolve_peripheral_projectors(matrix)

    def bulk_step(vector):
        return apply_deflated(matrix, projectors, vector)

    def bulk_two_step(vector):
        return bulk_step(bulk_step(vector))

    print("materializing bulk-deflated returns", flush=True)
    bulk_left = dense_matrix(
        return_operator(left, bulk_two_step), endpoint_indices.size
    )
    bulk_right = dense_matrix(
        return_operator(right, bulk_two_step), endpoint_indices.size
    )
    bulk_branch = compressed_branch_cycle(
        bulk_two_step, left[:-1], context["basis"]
    )

    archived = {
        float(row["sigma"]): row
        for row in read_csv(RH15 / "results" / "cloud_summary.csv")
    }
    bulk_edge = float(archived[DENSE_SIGMA]["bulk_radius"])
    phase_rows: list[dict[str, object]] = []
    phases = np.linspace(0.0, np.pi, PHASE_POINTS)
    families = {
        "raw": (raw_left, raw_right),
        "bulk_deflated": (bulk_left, bulk_right),
    }
    for phase in phases:
        row: dict[str, object] = {
            "sigma": DENSE_SIGMA,
            "component_period": period,
            "phase": phase,
            "phase_over_pi": phase / np.pi,
        }
        for label, (first, second) in families.items():
            values = np.linalg.eigvals(phase_weighted_return(first, second, phase))
            leading = values[np.argmax(np.abs(values))]
            row[f"{label}_leading_real"] = leading.real
            row[f"{label}_leading_imag"] = leading.imag
            row[f"{label}_leading_modulus"] = abs(leading)
            row[f"{label}_one_step_radius"] = abs(leading) ** (
                1.0 / (2 * period)
            )
        phase_rows.append(row)

    def radius_at(phase, first, second):
        values = np.linalg.eigvals(phase_weighted_return(first, second, phase))
        return max(abs(values)) ** (1.0 / (2 * period))

    raw_matching_phase = brentq(
        lambda phase: radius_at(phase, raw_left, raw_right) - bulk_edge,
        0.0,
        np.pi,
    )
    deflated_matching_phase = brentq(
        lambda phase: radius_at(phase, bulk_left, bulk_right) - bulk_edge,
        0.0,
        np.pi,
    )
    rows = []
    for label, first, second in (
        ("raw", raw_left, raw_right),
        ("bulk_deflated", bulk_left, bulk_right),
    ):
        singular = np.linalg.svd(first + second, compute_uv=False)
        rows.append(
            {
                "sigma": DENSE_SIGMA,
                "component_period": period,
                "operator_type": label,
                "left_right_relative_frobenius_difference": np.linalg.norm(
                    first - second
                )
                / np.linalg.norm(first),
                "both_singular_ratio_1": singular[1] / singular[0],
                "both_singular_ratio_2": singular[2] / singular[0],
                "both_singular_ratio_3": singular[3] / singular[0],
                "cubic_phase_radius": radius_at(
                    2.0 * np.pi / 3.0, first, second
                ),
                "antisymmetric_radius": radius_at(np.pi, first, second),
                "phase_matching_bulk_over_pi": (
                    raw_matching_phase
                    if label == "raw"
                    else deflated_matching_phase
                )
                / np.pi,
                "perron_eigenvalue": projectors[0].eigenvalue,
                "parity_eigenvalue": projectors[1].eigenvalue,
            }
        )
    raw_branch = compressed_branch_cycle(
        context["two_step"], left[:-1], context["basis"]
    )
    for label, branch in (("raw", raw_branch), ("bulk_deflated", bulk_branch)):
        transformed = bright_dark_transform(branch)
        for row in rows:
            if row["operator_type"] == label:
                row.update(
                    {
                        "branch_matrix_00": branch[0, 0].real,
                        "branch_matrix_01": branch[0, 1].real,
                        "branch_matrix_10": branch[1, 0].real,
                        "branch_matrix_11": branch[1, 1].real,
                        "bright_dark_00": transformed[0, 0].real,
                        "bright_dark_01": transformed[0, 1].real,
                        "bright_dark_10": transformed[1, 0].real,
                        "bright_dark_11": transformed[1, 1].real,
                    }
                )
    write_csv(RESULTS / "phase_family_sigma_1e-3.csv", phase_rows)
    write_csv(RESULTS / "dense_branch_sector_audit.csv", rows)
    del matrix
    release_memory()
    return phase_rows, rows


def plot_results(branch_rows, phase_rows, dense_rows):
    sigma = np.asarray([float(row["sigma"]) for row in branch_rows])
    order = np.argsort(sigma)[::-1]
    dark_ratio = np.asarray(
        [float(row["dark_to_bright_modulus_ratio"]) for row in branch_rows]
    )
    preserve = np.asarray(
        [float(row["preserve_left_phase_over_pi"]) for row in branch_rows]
    )
    match_bulk = np.asarray(
        [float(row["match_bulk_phase_over_pi"]) for row in branch_rows]
    )
    cubic = np.asarray(
        [float(row["cubic_phase_one_step_radius"]) for row in branch_rows]
    )
    left = np.asarray([float(row["left_one_step_radius"]) for row in branch_rows])
    bulk = np.asarray([float(row["archived_bulk_radius"]) for row in branch_rows])
    bright = np.asarray(
        [float(row["compressed_bright_one_step_radius"]) for row in branch_rows]
    )
    complete = np.asarray(
        [float(row["branch_complete_one_step_radius"]) for row in branch_rows]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axes[0, 0].loglog(sigma[order], dark_ratio[order], "o-", color="#a0263f")
    axes[0, 0].invert_xaxis()
    axes[0, 0].set(xlabel=r"noise $\sigma$", ylabel="dark / bright eigenvalue modulus", title="The antisymmetric branch channel stays dark")
    axes[0, 0].grid(alpha=0.22)

    axes[0, 1].semilogx(sigma[order], bright[order], "o-", label="compressed 2x2 bright")
    axes[0, 1].semilogx(sigma[order], complete[order], "s--", label="full branch-complete return")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(xlabel=r"noise $\sigma$", ylabel="one-step radius", title="Two-profile compression resolves the bright return")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    axes[1, 0].semilogx(sigma[order], preserve[order], "o-", label="preserve one-branch modulus")
    axes[1, 0].semilogx(sigma[order], match_bulk[order], "s--", label="match archived bulk edge")
    axes[1, 0].axhline(2.0 / 3.0, color="0.3", ls=":", label=r"$2/3$")
    axes[1, 0].invert_xaxis()
    axes[1, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel=r"conditional phase $\theta/\pi$",
        title="Unit-weight normalization: a conditional phase test",
    )
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.22)

    axes[1, 1].semilogx(sigma[order], left[order], "o-", label="left branch")
    axes[1, 1].semilogx(sigma[order], cubic[order], "^--", label=r"two branches at $\theta=2\pi/3$")
    axes[1, 1].semilogx(sigma[order], bulk[order], "k.-", label="archived bulk edge")
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(xlabel=r"noise $\sigma$", ylabel="one-step radius", title="Conditional cubic-phase radius")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.22)
    fig.tight_layout()
    fig.savefig(FIGURES / "bright_dark_cubic_phase.pdf")
    fig.savefig(FIGURES / "bright_dark_cubic_phase.png", dpi=220)
    plt.close(fig)

    raw = next(row for row in dense_rows if row["operator_type"] == "raw")
    bulk_row = next(
        row for row in dense_rows if row["operator_type"] == "bulk_deflated"
    )
    raw_matrix = np.asarray(
        ((raw["branch_matrix_00"], raw["branch_matrix_01"]),
         (raw["branch_matrix_10"], raw["branch_matrix_11"])),
        dtype=float,
    )
    raw_bd = np.asarray(
        ((raw["bright_dark_00"], raw["bright_dark_01"]),
         (raw["bright_dark_10"], raw["bright_dark_11"])),
        dtype=float,
    )
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    for axis, matrix, title in (
        (axes[0, 0], raw_matrix, "Raw left/right branch matrix"),
        (axes[0, 1], raw_bd, "Raw bright/dark representation"),
    ):
        image = axis.imshow(matrix, cmap="coolwarm")
        for (row, column), value in np.ndenumerate(matrix):
            axis.text(column, row, f"{value:.3e}", ha="center", va="center", fontsize=9)
        axis.set_xticks((0, 1))
        axis.set_yticks((0, 1))
        axis.set_title(title)
        fig.colorbar(image, ax=axis, fraction=0.046)

    phase = np.asarray([float(row["phase_over_pi"]) for row in phase_rows])
    raw_radius = np.asarray([float(row["raw_one_step_radius"]) for row in phase_rows])
    deflated_radius = np.asarray(
        [float(row["bulk_deflated_one_step_radius"]) for row in phase_rows]
    )
    target = float(
        next(
            row["archived_bulk_radius"]
            for row in branch_rows
            if abs(float(row["sigma"]) - DENSE_SIGMA) < 1.0e-15
        )
    )
    axes[1, 0].plot(phase, raw_radius, label="raw phase family")
    axes[1, 0].plot(phase, deflated_radius, "--", label="bulk-deflated phase family")
    axes[1, 0].axhline(target, color="black", ls=":", label="archived bulk edge")
    axes[1, 0].axvline(2.0 / 3.0, color="0.4", ls="-.", label=r"$2\pi/3$")
    axes[1, 0].set(xlabel=r"relative branch phase $\theta/\pi$", ylabel="one-step radius", title=r"Sector phase family at $\sigma=10^{-3}$")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.22)

    raw_values = np.asarray(
        [complex(float(row["raw_leading_real"]), float(row["raw_leading_imag"])) for row in phase_rows]
    )
    axes[1, 1].plot(raw_values.real, raw_values.imag, color="#2455a4")
    axes[1, 1].scatter(raw_values[::20].real, raw_values[::20].imag, s=20, color="#a0263f")
    axes[1, 1].axhline(0.0, color="0.8", lw=0.7)
    axes[1, 1].axvline(0.0, color="0.8", lw=0.7)
    axes[1, 1].set_aspect("equal")
    axes[1, 1].set(xlabel="real return eigenvalue", ylabel="imaginary return eigenvalue", title="The bright eigenvalue follows a near-circle arc")
    axes[1, 1].grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(FIGURES / "sector_phase_family.pdf")
    fig.savefig(FIGURES / "sector_phase_family.png", dpi=220)
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    branch_rows, context = seven_noise_branch_matrices()
    phase_rows, dense_rows = dense_phase_audit(context)
    plot_results(branch_rows, phase_rows, dense_rows)
    smallest = branch_rows[-1]
    raw_dense = next(row for row in dense_rows if row["operator_type"] == "raw")
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "window_multiple": WINDOW_MULTIPLE,
        "smallest_noise_dark_to_bright_ratio": float(
            smallest["dark_to_bright_modulus_ratio"]
        ),
        "smallest_noise_preserve_left_phase_over_pi": float(
            smallest["preserve_left_phase_over_pi"]
        ),
        "smallest_noise_match_bulk_phase_over_pi": float(
            smallest["match_bulk_phase_over_pi"]
        ),
        "smallest_noise_cubic_phase_edge_error": float(
            smallest["cubic_phase_one_step_radius"]
        )
        - float(smallest["archived_bulk_radius"]),
        "dense_raw_second_singular_ratio": float(
            raw_dense["both_singular_ratio_1"]
        ),
        "source_hashes": {
            "audit.py": source_hash(Path(__file__)),
            "algebra.py": source_hash(ROOT / "src" / "sector_branches" / "algebra.py"),
            "operators.py": source_hash(ROOT / "src" / "sector_branches" / "operators.py"),
            "rh19_branch_returns.csv": source_hash(RH19 / "results" / "branch_return_decomposition.csv"),
        },
    }
    with (RESULTS / "sector_branch_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated RH-20 sector-branch audits", flush=True)


if __name__ == "__main__":
    main()
