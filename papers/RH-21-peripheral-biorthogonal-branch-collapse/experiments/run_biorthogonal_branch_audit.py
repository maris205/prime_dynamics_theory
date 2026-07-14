"""Generate branch-memory and peripheral-biorthogonal audits for RH-21."""

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


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH16 = PAPERS / "RH-16-endpoint-gaussian-resolution-rank"
RH17 = PAPERS / "RH-17-time-ordered-boundary-monodromy"
RH18 = PAPERS / "RH-18-branch-isolated-gaussian-return"
RH19 = PAPERS / "RH-19-complement-excursion-self-energy"
RH20 = PAPERS / "RH-20-sector-resolved-critical-branches"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH16 / "src"),
    str(RH17 / "src"),
    str(RH18 / "src"),
    str(RH19 / "src"),
    str(RH20 / "src"),
]

from biorthogonal_branches import (  # noqa: E402
    bright_coordinate_dual,
    canonical_biorthogonal_pair,
    complement_project,
    merge_metrics,
    propagate_branch_histories,
    reduced_branch_cycle,
)
from complement_excursions import (  # noqa: E402
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
from sector_branches import branch_profile_basis  # noqa: E402
from time_ordered_monodromy import boundary_cycle, critical_constants  # noqa: E402


WINDOW_MULTIPLE = 6.0
PERIPHERAL_SIGMAS = (1.0e-3, 1.0e-4)
GAUGE = np.asarray(((1.7, 0.25), (-0.35, 0.8)), dtype=np.float64)


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
    return constants, points, tube


def build_context(sigma: float, dimension: int, period: int):
    constants, points, tube = cycle_context(period)
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

    def two_step(values):
        return matrix @ (matrix @ values)

    endpoint = np.exp(
        -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
    )
    endpoint[~left[0]] = 0.0
    endpoint /= np.linalg.norm(endpoint)
    critical = two_step(endpoint)
    basis = branch_profile_basis(critical, left[-1], right[-1])
    return {
        "sigma": sigma,
        "dimension": dimension,
        "period": period,
        "matrix": matrix,
        "grid": grid,
        "left": left,
        "right": right,
        "both": both,
        "basis": np.column_stack(basis),
        "two_step": two_step,
    }


def ordered_eigenvalues(matrix: np.ndarray) -> tuple[complex, complex]:
    values = np.linalg.eigvals(np.asarray(matrix, dtype=np.complex128))
    values = values[np.argsort(-np.abs(values))]
    return complex(values[0]), complex(values[1])


def matrix_fields(prefix: str, matrix: np.ndarray, period: int) -> dict[str, object]:
    values = np.asarray(matrix)
    bright, dark = ordered_eigenvalues(values)
    return {
        f"{prefix}_matrix_00": float(np.real(values[0, 0])),
        f"{prefix}_matrix_01": float(np.real(values[0, 1])),
        f"{prefix}_matrix_10": float(np.real(values[1, 0])),
        f"{prefix}_matrix_11": float(np.real(values[1, 1])),
        f"{prefix}_bright_real": bright.real,
        f"{prefix}_bright_imag": bright.imag,
        f"{prefix}_dark_real": dark.real,
        f"{prefix}_dark_imag": dark.imag,
        f"{prefix}_one_step_radius": abs(bright) ** (1.0 / (2 * period)),
        f"{prefix}_dark_to_bright_ratio": abs(dark) / abs(bright),
    }


def normalized_columns(values: np.ndarray) -> np.ndarray:
    source = np.asarray(values, dtype=np.float64)
    norms = np.linalg.norm(source, axis=0)
    if np.min(norms) == 0.0:
        raise RuntimeError("a branch history vanished")
    return source / norms


def seven_noise_audit():
    archived = read_csv(RH15 / "results" / "cloud_summary.csv")
    return_rows = {
        float(row["sigma"]): row
        for row in read_csv(RH19 / "results" / "branch_return_decomposition.csv")
    }
    clearances = boundary_clearances(70, decimal_digits=110)
    history_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    peripheral_rows: list[dict[str, object]] = []
    cycle_rows: list[dict[str, object]] = []

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
        started = time.time()
        print(
            f"branch memory sigma={sigma:g}, n={dimension}, k={period}",
            flush=True,
        )
        context = build_context(sigma, dimension, period)
        histories = propagate_branch_histories(
            context["two_step"], context["left"][:-1], context["basis"]
        )
        for index, history in enumerate(histories):
            metrics = merge_metrics(history[:, 0], history[:, 1])
            norms = np.linalg.norm(history, axis=0)
            history_rows.append(
                {
                    "sigma": sigma,
                    "folded_dimension": dimension,
                    "component_period": period,
                    "slice_index": index,
                    "distance_from_critical": period - 1 - index,
                    "overlap_modulus": metrics.overlap_modulus,
                    "one_minus_overlap": 1.0 - metrics.overlap_modulus,
                    "bright_singular_value": metrics.bright_singular_value,
                    "dark_singular_value": metrics.dark_singular_value,
                    "synthesis_condition": metrics.synthesis_condition,
                    "normalized_gram_condition": metrics.gram_condition,
                    "dual_norm_lower_bound": metrics.dual_norm_lower_bound,
                    "right_to_left_history_norm": norms[1] / norms[0],
                }
            )

        endpoint_metrics = merge_metrics(histories[0][:, 0], histories[0][:, 1])
        branch_matrix = reduced_branch_cycle(
            context["two_step"],
            context["left"][:-1],
            context["both"][-1],
            context["basis"],
            context["basis"].T,
        )
        branch_bright, branch_dark = ordered_eigenvalues(branch_matrix)
        returns = return_rows[sigma]
        eta_left = float(returns["left_return_eigenvalue"])
        eta_right = float(returns["right_return_eigenvalue"])
        half_radius = abs(0.5 * (eta_left + eta_right)) ** (
            1.0 / (2 * period)
        )
        cubic_radius = abs(
            eta_left + np.exp(2j * np.pi / 3.0) * eta_right
        ) ** (1.0 / (2 * period))
        summary_rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "component_period": period,
                "endpoint_overlap_modulus": endpoint_metrics.overlap_modulus,
                "endpoint_one_minus_overlap": 1.0
                - endpoint_metrics.overlap_modulus,
                "endpoint_normalized_gram_condition": endpoint_metrics.gram_condition,
                "endpoint_dual_norm_lower_bound": endpoint_metrics.dual_norm_lower_bound,
                "endpoint_right_to_left_history_norm": np.linalg.norm(
                    histories[0][:, 1]
                )
                / np.linalg.norm(histories[0][:, 0]),
                "branch_dark_to_bright_ratio": abs(branch_dark)
                / abs(branch_bright),
                "branch_bright_one_step_radius": abs(branch_bright)
                ** (1.0 / (2 * period)),
                "half_weight_one_step_radius": half_radius,
                "cubic_phase_one_step_radius": cubic_radius,
                "left_branch_one_step_radius": float(
                    returns["left_one_step_radius"]
                ),
                "archived_bulk_radius": float(archived_row["bulk_radius"]),
                "elapsed_seconds": time.time() - started,
            }
        )

        if any(abs(sigma - target) < 1.0e-15 for target in PERIPHERAL_SIGMAS):
            print(f"resolving peripheral modes at sigma={sigma:g}", flush=True)
            projectors = resolve_peripheral_projectors(context["matrix"])
            right_modes = np.column_stack([item.right for item in projectors])
            left_modes = np.column_stack([item.left for item in projectors])
            eigenvalues = np.asarray([item.eigenvalue for item in projectors])
            critical_pair = canonical_biorthogonal_pair(
                context["basis"], right_modes, left_modes
            )
            endpoint_raw = normalized_columns(histories[0])
            endpoint_q_raw = complement_project(
                endpoint_raw, right_modes, left_modes
            )
            endpoint_trial = endpoint_raw / np.linalg.norm(
                endpoint_q_raw, axis=0
            )
            endpoint_pair = canonical_biorthogonal_pair(
                endpoint_trial, right_modes, left_modes
            )
            endpoint_q_metrics = merge_metrics(
                endpoint_pair.synthesis[:, 0], endpoint_pair.synthesis[:, 1]
            )
            critical_q_metrics = merge_metrics(
                critical_pair.synthesis[:, 0], critical_pair.synthesis[:, 1]
            )
            dual_weights = bright_coordinate_dual(critical_pair.gram)
            critical_fraction = np.linalg.norm(
                critical_pair.synthesis[context["both"][-1], :]
            ) / np.linalg.norm(critical_pair.synthesis)
            endpoint_fraction = np.linalg.norm(
                endpoint_pair.synthesis[context["left"][0], :]
            ) / np.linalg.norm(endpoint_pair.synthesis)
            peripheral_rows.append(
                {
                    "sigma": sigma,
                    "folded_dimension": dimension,
                    "component_period": period,
                    "perron_eigenvalue": projectors[0].eigenvalue,
                    "parity_eigenvalue": projectors[1].eigenvalue,
                    "max_peripheral_residual": max(
                        projectors[0].right_residual,
                        projectors[0].left_residual,
                        projectors[1].right_residual,
                        projectors[1].left_residual,
                    ),
                    "critical_gram_00": float(critical_pair.gram[0, 0]),
                    "critical_gram_01": float(critical_pair.gram[0, 1]),
                    "critical_gram_10": float(critical_pair.gram[1, 0]),
                    "critical_gram_11": float(critical_pair.gram[1, 1]),
                    "critical_gram_condition": float(
                        np.linalg.cond(critical_pair.gram)
                    ),
                    "critical_q_overlap": critical_q_metrics.overlap_modulus,
                    "critical_bright_dual_left": float(dual_weights[0]),
                    "critical_bright_dual_right": float(dual_weights[1]),
                    "critical_q_local_fraction": critical_fraction,
                    "endpoint_raw_overlap": endpoint_metrics.overlap_modulus,
                    "endpoint_q_overlap": endpoint_q_metrics.overlap_modulus,
                    "endpoint_raw_gram_condition": endpoint_metrics.gram_condition,
                    "endpoint_q_gram_condition": endpoint_q_metrics.gram_condition,
                    "endpoint_raw_dual_lower_bound": endpoint_metrics.dual_norm_lower_bound,
                    "endpoint_q_dual_lower_bound": endpoint_q_metrics.dual_norm_lower_bound,
                    "endpoint_canonical_analysis_norm": float(
                        np.linalg.norm(endpoint_pair.analysis, ord=2)
                    ),
                    "endpoint_q_local_fraction": endpoint_fraction,
                    "max_pair_residual": max(
                        critical_pair.biorthogonality_residual,
                        critical_pair.right_annihilation_residual,
                        critical_pair.left_annihilation_residual,
                        endpoint_pair.biorthogonality_residual,
                        endpoint_pair.right_annihilation_residual,
                        endpoint_pair.left_annihilation_residual,
                    ),
                }
            )

            def bulk_step(values):
                source = np.asarray(values, dtype=np.float64)
                return context["matrix"] @ source - right_modes @ (
                    eigenvalues[:, None] * (left_modes.T @ source)
                    if source.ndim == 2
                    else eigenvalues * (left_modes.T @ source)
                )

            def bulk_two_step(values):
                return bulk_step(bulk_step(values))

            matrices = {
                "raw_euclidean": branch_matrix,
                "raw_biorthogonal": reduced_branch_cycle(
                    context["two_step"],
                    context["left"][:-1],
                    context["both"][-1],
                    critical_pair.synthesis,
                    critical_pair.analysis,
                ),
                "bulk_euclidean": reduced_branch_cycle(
                    bulk_two_step,
                    context["left"][:-1],
                    context["both"][-1],
                    context["basis"],
                    context["basis"].T,
                ),
                "bulk_biorthogonal": reduced_branch_cycle(
                    bulk_two_step,
                    context["left"][:-1],
                    context["both"][-1],
                    critical_pair.synthesis,
                    critical_pair.analysis,
                ),
            }
            gauge_synthesis = critical_pair.synthesis @ GAUGE
            gauge_analysis = np.linalg.solve(GAUGE, critical_pair.analysis)
            gauge_matrix = reduced_branch_cycle(
                bulk_two_step,
                context["left"][:-1],
                context["both"][-1],
                gauge_synthesis,
                gauge_analysis,
            )
            expected_gauge = np.linalg.solve(
                GAUGE, matrices["bulk_biorthogonal"] @ GAUGE
            )
            gauge_error = np.linalg.norm(gauge_matrix - expected_gauge)
            row: dict[str, object] = {
                "sigma": sigma,
                "folded_dimension": dimension,
                "component_period": period,
                "archived_bulk_radius": float(archived_row["bulk_radius"]),
                "gauge_similarity_error": gauge_error,
                "maximum_static_imaginary_entry": max(
                    float(np.max(np.abs(np.imag(value))))
                    for value in matrices.values()
                ),
            }
            for label, matrix in matrices.items():
                row.update(matrix_fields(label, matrix, period))
            cycle_rows.append(row)

        del context, histories
        release_memory()

    write_csv(RESULTS / "branch_memory_collapse.csv", history_rows)
    write_csv(RESULTS / "branch_memory_summary.csv", summary_rows)
    write_csv(RESULTS / "peripheral_biorthogonal_audit.csv", peripheral_rows)
    write_csv(RESULTS / "biorthogonal_cycle_matrices.csv", cycle_rows)
    return history_rows, summary_rows, peripheral_rows, cycle_rows


def plot_results(history_rows, summary_rows, peripheral_rows, cycle_rows):
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    for sigma in sorted({float(row["sigma"]) for row in history_rows}, reverse=True):
        selected = [row for row in history_rows if float(row["sigma"]) == sigma]
        distance = np.asarray([int(row["distance_from_critical"]) for row in selected])
        defect = np.asarray([float(row["one_minus_overlap"]) for row in selected])
        order = np.argsort(distance)
        axes[0, 0].semilogy(
            distance[order], defect[order], "o-", ms=3, label=f"{sigma:g}"
        )
    axes[0, 0].set(
        xlabel="two-step channels after critical split",
        ylabel=r"branch-memory defect $1-|\langle u_-,u_+\rangle|$",
        title="Two critical histories collapse onto one bright direction",
    )
    axes[0, 0].grid(alpha=0.2)
    axes[0, 0].legend(frameon=False, fontsize=7, ncol=2)

    sigma = np.asarray([float(row["sigma"]) for row in summary_rows])
    order = np.argsort(sigma)[::-1]
    gram = np.asarray(
        [float(row["endpoint_normalized_gram_condition"]) for row in summary_rows]
    )
    dual = np.asarray(
        [float(row["endpoint_dual_norm_lower_bound"]) for row in summary_rows]
    )
    axes[0, 1].loglog(sigma[order], gram[order], "o-", label="Gram condition")
    axes[0, 1].loglog(sigma[order], dual[order], "s--", label="dual-norm lower bound")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="endpoint conditioning",
        title="Exact two-label duals become ill-conditioned",
    )
    axes[0, 1].grid(alpha=0.2)
    axes[0, 1].legend(frameon=False, fontsize=8)

    dark_singular = np.sqrt(
        np.asarray([float(row["endpoint_one_minus_overlap"]) for row in summary_rows])
    )
    return_dark = np.asarray(
        [float(row["branch_dark_to_bright_ratio"]) for row in summary_rows]
    )
    axes[1, 0].loglog(sigma[order], dark_singular[order], "o-", label="endpoint dark singular value")
    axes[1, 0].loglog(sigma[order], return_dark[order], "s--", label="return dark/bright eigenvalue")
    axes[1, 0].invert_xaxis()
    axes[1, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel="dark-channel scale",
        title="Memory collapse accompanies a dark return channel",
    )
    axes[1, 0].grid(alpha=0.2)
    axes[1, 0].legend(frameon=False, fontsize=8)

    half = np.asarray([float(row["half_weight_one_step_radius"]) for row in summary_rows])
    cubic = np.asarray([float(row["cubic_phase_one_step_radius"]) for row in summary_rows])
    bulk = np.asarray([float(row["archived_bulk_radius"]) for row in summary_rows])
    axes[1, 1].semilogx(sigma[order], half[order], "o-", label="half-weight diagnostic")
    axes[1, 1].semilogx(sigma[order], cubic[order], "^--", label="cubic-phase diagnostic")
    axes[1, 1].semilogx(sigma[order], bulk[order], "k.-", label="archived bulk edge")
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="one-step radius",
        title="Radial agreement still cannot identify the mechanism",
    )
    axes[1, 1].grid(alpha=0.2)
    axes[1, 1].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "branch_memory_collapse.pdf")
    fig.savefig(FIGURES / "branch_memory_collapse.png", dpi=220)
    plt.close(fig)

    labels = [f"{float(row['sigma']):g}" for row in peripheral_rows]
    x = np.arange(len(labels), dtype=float)
    width = 0.34
    raw_condition = np.asarray(
        [float(row["endpoint_raw_gram_condition"]) for row in peripheral_rows]
    )
    q_condition = np.asarray(
        [float(row["endpoint_q_gram_condition"]) for row in peripheral_rows]
    )
    left_weight = np.asarray(
        [float(row["critical_bright_dual_left"]) for row in peripheral_rows]
    )
    right_weight = np.asarray(
        [float(row["critical_bright_dual_right"]) for row in peripheral_rows]
    )
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axes[0, 0].bar(x - width / 2, raw_condition, width, label="raw histories")
    axes[0, 0].bar(x + width / 2, q_condition, width, label="after Q")
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_xticks(x, labels)
    axes[0, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel="normalized Gram condition",
        title="Peripheral extraction does not restore branch memory",
    )
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(axis="y", alpha=0.2)

    axes[0, 1].bar(x - width / 2, left_weight, width, label="left coefficient")
    axes[0, 1].bar(x + width / 2, right_weight, width, label="right coefficient")
    axes[0, 1].axhline(0.5, color="black", ls=":", label="one half")
    axes[0, 1].set_xticks(x, labels)
    axes[0, 1].set_ylim(0.4998, 0.5002)
    axes[0, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="bright coordinate dual",
        title="The canonical bright coordinate uses a half-sum",
    )
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(axis="y", alpha=0.2)

    names = (
        "raw_euclidean_one_step_radius",
        "raw_biorthogonal_one_step_radius",
        "bulk_euclidean_one_step_radius",
        "bulk_biorthogonal_one_step_radius",
    )
    display = ("raw", "raw + Q pair", "bulk", "bulk + Q pair")
    markers = ("o", "s", "^", "D")
    for name, label, marker in zip(names, display, markers):
        axes[1, 0].plot(
            x,
            [float(row[name]) for row in cycle_rows],
            marker=marker,
            label=label,
        )
    axes[1, 0].plot(
        x,
        [float(row["archived_bulk_radius"]) for row in cycle_rows],
        "k.--",
        label="archived bulk edge",
    )
    axes[1, 0].set_xticks(x, labels)
    axes[1, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel="one-step radius",
        title="Biorthogonalization changes subspaces, not eigenvalue gauge",
    )
    axes[1, 0].legend(frameon=False, fontsize=7)
    axes[1, 0].grid(alpha=0.2)

    lower = np.asarray(
        [float(row["endpoint_q_dual_lower_bound"]) for row in peripheral_rows]
    )
    actual = np.asarray(
        [float(row["endpoint_canonical_analysis_norm"]) for row in peripheral_rows]
    )
    axes[1, 1].bar(x - width / 2, lower, width, label="universal lower bound")
    axes[1, 1].bar(x + width / 2, actual, width, label="canonical analysis norm")
    axes[1, 1].set_yscale("log")
    axes[1, 1].set_xticks(x, labels)
    axes[1, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="dual-map norm",
        title="The dark dual amplifies endpoint errors",
    )
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURES / "peripheral_biorthogonal_no_go.pdf")
    fig.savefig(FIGURES / "peripheral_biorthogonal_no_go.png", dpi=220)
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    history, summary, peripheral, cycles = seven_noise_audit()
    plot_results(history, summary, peripheral, cycles)
    smallest = summary[-1]
    smallest_peripheral = next(
        row for row in peripheral if abs(float(row["sigma"]) - 1.0e-4) < 1.0e-15
    )
    summary_json = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "window_multiple": WINDOW_MULTIPLE,
        "smallest_noise_endpoint_overlap": float(
            smallest["endpoint_overlap_modulus"]
        ),
        "smallest_noise_raw_gram_condition": float(
            smallest["endpoint_normalized_gram_condition"]
        ),
        "smallest_noise_q_gram_condition": float(
            smallest_peripheral["endpoint_q_gram_condition"]
        ),
        "smallest_noise_q_analysis_norm": float(
            smallest_peripheral["endpoint_canonical_analysis_norm"]
        ),
        "smallest_noise_bright_dual_left": float(
            smallest_peripheral["critical_bright_dual_left"]
        ),
        "smallest_noise_bright_dual_right": float(
            smallest_peripheral["critical_bright_dual_right"]
        ),
        "maximum_gauge_similarity_error": max(
            float(row["gauge_similarity_error"]) for row in cycles
        ),
        "maximum_pair_residual": max(
            float(row["max_pair_residual"]) for row in peripheral
        ),
        "source_hashes": {
            "audit.py": source_hash(Path(__file__)),
            "algebra.py": source_hash(
                ROOT / "src" / "biorthogonal_branches" / "algebra.py"
            ),
            "operators.py": source_hash(
                ROOT / "src" / "biorthogonal_branches" / "operators.py"
            ),
            "rh19_branch_returns.csv": source_hash(
                RH19 / "results" / "branch_return_decomposition.csv"
            ),
            "rh20_branch_matrix.csv": source_hash(
                RH20 / "results" / "two_branch_matrix_audit.csv"
            ),
        },
    }
    with (RESULTS / "biorthogonal_branch_summary.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(summary_json, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated RH-21 peripheral-biorthogonal audits", flush=True)


if __name__ == "__main__":
    main()
