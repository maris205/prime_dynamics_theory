"""Generate sibling, finite-return, deflation, and Floquet audits for RH-19."""

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
from scipy.sparse.linalg import eigs


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH16 = PAPERS / "RH-16-endpoint-gaussian-resolution-rank"
RH17 = PAPERS / "RH-17-time-ordered-boundary-monodromy"
RH18 = PAPERS / "RH-18-branch-isolated-gaussian-return"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH16 / "src"),
    str(RH17 / "src"),
    str(RH18 / "src"),
]

from complement_excursions import (  # noqa: E402
    apply_deflated,
    apply_endpoint_return,
    apply_restricted_return,
    critical_branch_masks,
    cyclic_time_lift,
    feshbach_map,
    power_eigenpair,
    resolve_peripheral_projectors,
    time_fourier_blocks,
)
from endpoint_rank import (  # noqa: E402
    HALF_ENERGY_THRESHOLD,
    boundary_clearances,
    threshold_rank,
)
from gaussian_return import (  # noqa: E402
    conditioned_critical_profile,
    effective_noise_scales,
    packet_masks,
    periodic_packet_tube,
    positive_midpoints,
    sparse_folded_gaussian_matrix,
)
from time_ordered_monodromy import boundary_cycle, critical_constants  # noqa: E402


WINDOW_MULTIPLE = 6.0
POWER_ITERATIONS = 9
DEFLATION_SIGMA = 1.0e-3


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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
    noise = effective_noise_scales(points, float(constants.u))
    tube = periodic_packet_tube(multipliers, noise)
    return constants, cycle, points, tube


def return_operators(matrix, masks, endpoint_indices, period, dimension):
    def two_step(vector):
        return matrix @ (matrix @ vector)

    def restricted(vector):
        return apply_restricted_return(
            two_step,
            masks,
            endpoint_indices,
            vector,
            dimension=dimension,
        )

    def endpoint(vector):
        return apply_endpoint_return(
            two_step,
            masks[0],
            endpoint_indices,
            vector,
            period=period,
            dimension=dimension,
        )

    return two_step, restricted, endpoint


def branch_return_audit():
    archived = read_csv(RH15 / "results" / "cloud_summary.csv")
    rh18_rows = {
        float(row["sigma"]): row
        for row in read_csv(RH18 / "results" / "local_return_edge.csv")
    }
    clearances = boundary_clearances(70, decimal_digits=110)
    branch_rows: list[dict[str, object]] = []
    channel_rows: list[dict[str, object]] = []
    deflation_context = None
    coarse_spectrum: tuple[np.ndarray, int] | None = None

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
        constants, cycle, points, tube = cycle_context(period)
        grid = positive_midpoints(dimension)
        print(
            f"branch audit sigma={sigma:g}, n={dimension}, k={period}",
            flush=True,
        )
        started = time.time()
        matrix = sparse_folded_gaussian_matrix(
            dimension, sigma, u=float(constants.u)
        )
        base_masks = packet_masks(
            grid,
            points,
            sigma * tube.widths,
            window_multiple=WINDOW_MULTIPLE,
            critical_partition=float(constants.first_interior_point),
        )
        left_masks, right_masks, both_masks = critical_branch_masks(
            grid,
            base_masks,
            points[-1],
            sigma * tube.widths[-1],
            window_multiple=WINDOW_MULTIPLE,
            partition=float(constants.first_interior_point),
        )
        endpoint_indices = np.flatnonzero(left_masks[0])
        initial = np.exp(
            -0.5
            * (
                (grid[endpoint_indices] - points[0])
                / (sigma * tube.widths[0])
            )
            ** 2
        )
        two_step, _, endpoint_operator = return_operators(
            matrix, left_masks, endpoint_indices, period, dimension
        )

        pairs = {}
        for name, masks in (("right", right_masks), ("both", both_masks)):
            _, operator, _ = return_operators(
                matrix, masks, endpoint_indices, period, dimension
            )
            pairs[name] = power_eigenpair(
                operator, initial, iterations=POWER_ITERATIONS
            )
        pairs["full"] = power_eigenpair(
            endpoint_operator, initial, iterations=POWER_ITERATIONS
        )

        endpoint_packet = np.exp(
            -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
        )
        endpoint_packet[~left_masks[0]] = 0.0
        critical_pullback = two_step(endpoint_packet)
        left_exit = float(np.linalg.norm(critical_pullback[left_masks[-1]]))
        right_exit = float(np.linalg.norm(critical_pullback[right_masks[-1]]))
        far_exit = float(np.linalg.norm(critical_pullback[~both_masks[-1]]))

        local_eta = float(rh18_rows[sigma]["principal_return_eigenvalue"])
        local_radius = float(rh18_rows[sigma]["local_one_step_edge_radius"])
        right_eta = pairs["right"].eigenvalue
        both_eta = pairs["both"].eigenvalue
        full_eta = pairs["full"].eigenvalue
        branch_rows.append(
            {
                "sigma": sigma,
                "folded_dimension": dimension,
                "component_period": period,
                "left_return_eigenvalue": local_eta,
                "right_return_eigenvalue": right_eta,
                "both_return_eigenvalue": both_eta,
                "full_endpoint_return_eigenvalue": full_eta,
                "left_one_step_radius": local_radius,
                "right_one_step_radius": abs(right_eta) ** (1.0 / (2 * period)),
                "both_one_step_radius": abs(both_eta) ** (1.0 / (2 * period)),
                "full_endpoint_one_step_radius": abs(full_eta)
                ** (1.0 / (2 * period)),
                "archived_bulk_radius": float(archived_row["bulk_radius"]),
                "archived_cloud_mean_radius": float(
                    archived_row["cloud_radial_mean"]
                ),
                "sibling_exit_norm_ratio": right_exit / left_exit,
                "far_exit_norm_ratio": far_exit / left_exit,
                "both_additivity_defect": (both_eta - local_eta - right_eta)
                / both_eta,
                "full_vs_both_defect": (full_eta - both_eta) / full_eta,
                "right_return_residual": pairs["right"].residual,
                "both_return_residual": pairs["both"].residual,
                "full_return_residual": pairs["full"].residual,
                "elapsed_seconds": time.time() - started,
            }
        )

        if abs(sigma - DEFLATION_SIGMA) < 1.0e-15:
            for target in range(period):
                source = (target - 1) % period
                packet = np.exp(
                    -0.5
                    * (
                        (grid - points[target])
                        / (sigma * tube.widths[target])
                    )
                    ** 2
                )
                packet[~left_masks[target]] = 0.0
                pulled = two_step(packet)
                local_norm = float(np.linalg.norm(pulled[left_masks[source]]))
                complement_norm = float(
                    np.linalg.norm(pulled[~left_masks[source]])
                )
                channel_rows.append(
                    {
                        "sigma": sigma,
                        "component_period": period,
                        "target_index": target,
                        "source_index": source,
                        "local_norm": local_norm,
                        "complement_norm": complement_norm,
                        "complement_to_local_ratio": complement_norm
                        / local_norm,
                        "local_to_total_ratio": local_norm
                        / np.linalg.norm(pulled),
                    }
                )
            deflation_context = (
                matrix,
                left_masks,
                right_masks,
                both_masks,
                endpoint_indices,
                initial,
                period,
                dimension,
            )
        elif sigma == float(archived[0]["sigma"]):
            values = eigs(
                matrix,
                k=16,
                which="LM",
                tol=1.0e-10,
                maxiter=4000,
                return_eigenvectors=False,
            )
            coarse_spectrum = (values, period)

        if deflation_context is None or abs(sigma - DEFLATION_SIGMA) > 1.0e-15:
            del matrix
            release_memory()

    write_csv(RESULTS / "branch_return_decomposition.csv", branch_rows)
    write_csv(RESULTS / "channel_leakage.csv", channel_rows)
    return branch_rows, channel_rows, deflation_context, coarse_spectrum


def deflation_audit(context):
    (
        matrix,
        left_masks,
        right_masks,
        both_masks,
        endpoint_indices,
        initial,
        period,
        dimension,
    ) = context
    print("resolving peripheral projectors for deflation audit", flush=True)
    projectors = resolve_peripheral_projectors(matrix)

    def bulk_step(vector):
        return apply_deflated(matrix, projectors, vector)

    def bulk_two_step(vector):
        return bulk_step(bulk_step(vector))

    rows: list[dict[str, object]] = []
    for name, masks in (
        ("left", left_masks),
        ("right", right_masks),
        ("both", both_masks),
    ):
        operator = lambda vector, selected=masks: apply_restricted_return(
            bulk_two_step,
            selected,
            endpoint_indices,
            vector,
            dimension=dimension,
        )
        pair = power_eigenpair(operator, initial, iterations=30)
        rows.append(
            {
                "sigma": DEFLATION_SIGMA,
                "component_period": period,
                "return_type": name,
                "return_eigenvalue": pair.eigenvalue,
                "one_step_radius": abs(pair.eigenvalue) ** (1.0 / (2 * period)),
                "residual": pair.residual,
                "perron_eigenvalue": projectors[0].eigenvalue,
                "parity_eigenvalue": projectors[1].eigenvalue,
                "perron_right_residual": projectors[0].right_residual,
                "perron_left_residual": projectors[0].left_residual,
                "parity_right_residual": projectors[1].right_residual,
                "parity_left_residual": projectors[1].left_residual,
            }
        )
    full_operator = lambda vector: apply_endpoint_return(
        bulk_two_step,
        left_masks[0],
        endpoint_indices,
        vector,
        period=period,
        dimension=dimension,
    )
    pair = power_eigenpair(full_operator, initial, iterations=30)
    rows.append(
        {
            "sigma": DEFLATION_SIGMA,
            "component_period": period,
            "return_type": "full",
            "return_eigenvalue": pair.eigenvalue,
            "one_step_radius": abs(pair.eigenvalue) ** (1.0 / (2 * period)),
            "residual": pair.residual,
            "perron_eigenvalue": projectors[0].eigenvalue,
            "parity_eigenvalue": projectors[1].eigenvalue,
            "perron_right_residual": projectors[0].right_residual,
            "perron_left_residual": projectors[0].left_residual,
            "parity_right_residual": projectors[1].right_residual,
            "parity_left_residual": projectors[1].left_residual,
        }
    )
    write_csv(RESULTS / "peripheral_deflation_noncommutation.csv", rows)
    del matrix
    release_memory()
    return rows


def floquet_audit(coarse_spectrum):
    rng = np.random.default_rng(20260714)
    operator = rng.normal(size=(3, 3)) / 4.0
    period = 5
    lifted = cyclic_time_lift(operator, period)
    expected = np.concatenate(
        [np.linalg.eigvals(block) for block in time_fourier_blocks(operator, period)]
    )
    observed = np.linalg.eigvals(lifted)
    spectral_error = max(
        float(np.min(np.abs(observed - value))) for value in expected
    )
    determinant_errors = []
    for z in (0.13 + 0.07j, -0.22 + 0.11j, 0.31 - 0.09j):
        left = np.linalg.det(np.eye(lifted.shape[0]) - z * lifted)
        right = np.linalg.det(np.eye(3) - z**period * np.linalg.matrix_power(operator, period))
        determinant_errors.append(abs(left - right) / max(abs(right), 1.0))

    masks = np.zeros(lifted.shape[0], dtype=bool)
    for index in range(period):
        masks[index * 3 + index % 3] = True
    projection = np.diag(masks.astype(float))
    feshbach_errors = []
    self_energy_ratios = []
    for zeta in (0.8 + 0.2j, -0.6 + 0.35j, 0.45 - 0.55j):
        feshbach, self_energy = feshbach_map(lifted, projection, zeta)
        q_basis = np.eye(lifted.shape[0])[:, ~masks]
        cqq = q_basis.conj().T @ lifted @ q_basis
        full_det = np.linalg.det(zeta * np.eye(lifted.shape[0]) - lifted)
        factor_det = np.linalg.det(zeta * np.eye(cqq.shape[0]) - cqq) * np.linalg.det(feshbach)
        feshbach_errors.append(abs(full_det - factor_det) / max(abs(full_det), 1.0))
        local = projection @ lifted @ projection
        self_energy_ratios.append(
            np.linalg.norm(self_energy, 2)
            / max(np.linalg.norm(local, 2), np.finfo(float).eps)
        )

    values, physical_period = coarse_spectrum
    replication_rows: list[dict[str, object]] = []
    for eigen_index, value in enumerate(values):
        for phase_index in range(physical_period):
            replicated = value**2 * np.exp(2j * np.pi * phase_index / physical_period)
            replication_rows.append(
                {
                    "sigma": 1.0e-2,
                    "component_period": physical_period,
                    "physical_eigenvalue_index": eigen_index,
                    "physical_real": value.real,
                    "physical_imag": value.imag,
                    "phase_index": phase_index,
                    "lifted_real": replicated.real,
                    "lifted_imag": replicated.imag,
                    "lifted_modulus": abs(replicated),
                }
            )
    write_csv(RESULTS / "floquet_replication.csv", replication_rows)
    summary = {
        "random_operator_period": period,
        "floquet_spectral_matching_error": spectral_error,
        "floquet_determinant_max_relative_error": max(determinant_errors),
        "feshbach_factorization_max_relative_error": max(feshbach_errors),
        "random_projection_self_energy_ratio_min": min(self_energy_ratios),
        "random_projection_self_energy_ratio_max": max(self_energy_ratios),
    }
    return summary, replication_rows


def plot_results(branch_rows, channel_rows, deflation_rows, replication_rows):
    sigma = np.asarray([float(row["sigma"]) for row in branch_rows])
    order = np.argsort(sigma)[::-1]
    left = np.asarray([float(row["left_one_step_radius"]) for row in branch_rows])
    right = np.asarray([float(row["right_one_step_radius"]) for row in branch_rows])
    both = np.asarray([float(row["both_one_step_radius"]) for row in branch_rows])
    full = np.asarray([float(row["full_endpoint_one_step_radius"]) for row in branch_rows])
    bulk = np.asarray([float(row["archived_bulk_radius"]) for row in branch_rows])

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axes[0, 0].semilogx(sigma[order], left[order], "o-", label="left branch")
    axes[0, 0].semilogx(sigma[order], right[order], "s--", label="right sibling")
    axes[0, 0].semilogx(sigma[order], both[order], "^-.", label="both branches")
    axes[0, 0].semilogx(sigma[order], full[order], "d:", label="full endpoint return")
    axes[0, 0].semilogx(sigma[order], bulk[order], "k.-", label="archived bulk edge")
    axes[0, 0].invert_xaxis()
    axes[0, 0].set(xlabel=r"noise $\sigma$", ylabel="one-step radius", title="The critical sibling is not a tail")
    axes[0, 0].legend(frameon=False, fontsize=7)
    axes[0, 0].grid(alpha=0.22)

    sibling_ratio = np.asarray([float(row["sibling_exit_norm_ratio"]) for row in branch_rows])
    far_ratio = np.asarray([float(row["far_exit_norm_ratio"]) for row in branch_rows])
    axes[0, 1].semilogx(sigma[order], sibling_ratio[order], "o-", label="right / left critical mass")
    axes[0, 1].semilogx(sigma[order], far_ratio[order], "s--", label="outside two-branch tube / left")
    axes[0, 1].axhline(1.0, color="0.4", ls=":")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(xlabel=r"noise $\sigma$", ylabel="norm ratio", title="Order-one sibling leakage")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.22)

    channel_rows = sorted(channel_rows, key=lambda row: int(row["target_index"]))
    axes[1, 0].bar(
        [int(row["target_index"]) for row in channel_rows],
        [float(row["complement_to_local_ratio"]) for row in channel_rows],
        color="#315ea8",
    )
    axes[1, 0].axhline(1.0, color="0.35", ls=":")
    axes[1, 0].set(xlabel="target time index", ylabel=r"$\|QTP\|$ test ratio", title=r"Every raw channel has $O(1)$ leakage at $\sigma=10^{-3}$")
    axes[1, 0].grid(axis="y", alpha=0.22)

    types = [row["return_type"] for row in deflation_rows]
    deflated = [float(row["one_step_radius"]) for row in deflation_rows]
    raw_lookup = {
        "left": left[np.argmin(abs(sigma - DEFLATION_SIGMA))],
        "right": right[np.argmin(abs(sigma - DEFLATION_SIGMA))],
        "both": both[np.argmin(abs(sigma - DEFLATION_SIGMA))],
        "full": full[np.argmin(abs(sigma - DEFLATION_SIGMA))],
    }
    positions = np.arange(len(types))
    axes[1, 1].bar(positions - 0.18, [raw_lookup[value] for value in types], width=0.36, label="localize $K^2$")
    axes[1, 1].bar(positions + 0.18, deflated, width=0.36, label="localize bulk-deflated $K^2$")
    axes[1, 1].set_xticks(positions, types)
    axes[1, 1].set(ylabel="one-step radius", title="Spectral deflation and localization do not commute")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(axis="y", alpha=0.22)
    fig.tight_layout()
    fig.savefig(FIGURES / "critical_sibling_complement.pdf")
    fig.savefig(FIGURES / "critical_sibling_complement.png", dpi=220)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.3))
    physical = {}
    for row in replication_rows:
        physical.setdefault(
            int(row["physical_eigenvalue_index"]),
            complex(float(row["physical_real"]), float(row["physical_imag"])),
        )
    physical_values = np.asarray(list(physical.values())) ** 2
    axes[0].scatter(physical_values.real, physical_values.imag, facecolors="none", edgecolors="black", label=r"physical $K_\sigma^2$")
    lifted_values = np.asarray(
        [complex(float(row["lifted_real"]), float(row["lifted_imag"])) for row in replication_rows]
    )
    axes[1].scatter(lifted_values.real, lifted_values.imag, s=18, alpha=0.65, label=r"time lift of $K_\sigma^2$")
    for axis, title in zip(axes, ("Physical two-step spectrum", "Exact Floquet replication")):
        axis.axhline(0.0, color="0.8", lw=0.7)
        axis.axvline(0.0, color="0.8", lw=0.7)
        axis.set_aspect("equal")
        axis.set(xlabel="real part", ylabel="imaginary part", title=title)
        axis.legend(frameon=False, fontsize=8)
        axis.grid(alpha=0.15)
    fig.tight_layout()
    fig.savefig(FIGURES / "floquet_replication_no_go.pdf")
    fig.savefig(FIGURES / "floquet_replication_no_go.png", dpi=220)
    plt.close(fig)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    branch_rows, channel_rows, context, coarse_spectrum = branch_return_audit()
    if context is None or coarse_spectrum is None:
        raise RuntimeError("required audit contexts were not captured")
    deflation_rows = deflation_audit(context)
    floquet_summary, replication_rows = floquet_audit(coarse_spectrum)
    plot_results(branch_rows, channel_rows, deflation_rows, replication_rows)
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "window_multiple": WINDOW_MULTIPLE,
        "power_iterations": POWER_ITERATIONS,
        "smallest_noise_sibling_exit_ratio": float(branch_rows[-1]["sibling_exit_norm_ratio"]),
        "smallest_noise_right_to_left_return_ratio": float(branch_rows[-1]["right_return_eigenvalue"])
        / float(branch_rows[-1]["left_return_eigenvalue"]),
        "smallest_noise_full_vs_both_defect": float(branch_rows[-1]["full_vs_both_defect"]),
        "floquet": floquet_summary,
        "source_hashes": {
            "audit.py": source_hash(Path(__file__)),
            "returns.py": source_hash(ROOT / "src" / "complement_excursions" / "returns.py"),
            "floquet.py": source_hash(ROOT / "src" / "complement_excursions" / "floquet.py"),
            "deflation.py": source_hash(ROOT / "src" / "complement_excursions" / "deflation.py"),
            "rh18_local_return_edge.csv": source_hash(RH18 / "results" / "local_return_edge.csv"),
        },
    }
    with (RESULTS / "complement_audit_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated RH-19 complement and Floquet audits", flush=True)


if __name__ == "__main__":
    main()
