"""Generate exact Schur diagnostics and figures for RH-22."""

from __future__ import annotations

import argparse
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
RH21 = PAPERS / "RH-21-peripheral-biorthogonal-branch-collapse"
sys.path.insert(0, str(ROOT / "src"))

from dark_schur import audit_matrix, bright_dark_transform  # noqa: E402


PERIPHERAL_LABELS = (
    "raw_euclidean",
    "raw_biorthogonal",
    "bulk_euclidean",
    "bulk_biorthogonal",
)
RESOLUTION_SIGMAS = (1.0e-3, 1.0e-4)
RESOLUTION_DENSITIES = (10.24, 15.36, 20.48)
WINDOW_MULTIPLE = 6.0


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


def real(value: complex) -> float:
    return float(np.real(value))


def imag(value: complex) -> float:
    return float(np.imag(value))


def sign(value: complex, tolerance: float = 1.0e-14) -> int:
    if abs(imag(value)) > tolerance:
        return 0
    if real(value) > tolerance:
        return 1
    if real(value) < -tolerance:
        return -1
    return 0


def audit_fields(matrix: np.ndarray, target: float, period: int) -> dict[str, object]:
    audit = audit_matrix(matrix, target)
    required = audit.required_shift
    ratio = audit.signed_coupling_ratio
    direct_radius = abs(audit.direct_bright) ** (1.0 / (2 * period))
    root_radius = abs(audit.bright_root) ** (1.0 / (2 * period))
    physical_radius = abs(target) ** (1.0 / (2 * period))
    companion = audit.direct_bright + audit.dark_pole - audit.target
    companion_radius = abs(companion) ** (1.0 / (2 * period))
    shift_fraction = (
        np.nan
        if required == 0
        else real(audit.bright_root_shift / required)
    )
    determinant_identity_error = abs(
        audit.determinant_residual
        - (audit.target - audit.dark_pole) * audit.schur_residual
    )
    coverage_identity_error = abs(
        abs(audit.self_energy_at_target) / abs(required) - abs(ratio)
    )
    return {
        "target_return": real(audit.target),
        "direct_bright": real(audit.direct_bright),
        "bright_to_dark": real(audit.bright_to_dark),
        "dark_to_bright": real(audit.dark_to_bright),
        "dark_pole": real(audit.dark_pole),
        "observed_product": real(audit.observed_product),
        "required_product": real(audit.required_product),
        "observed_product_sign": sign(audit.observed_product),
        "required_product_sign": sign(audit.required_product),
        "sign_compatible": int(sign(audit.observed_product) == sign(audit.required_product)),
        "signed_coupling_ratio": real(ratio),
        "absolute_coupling_coverage": abs(ratio),
        "self_energy_at_target": real(audit.self_energy_at_target),
        "required_shift": real(audit.required_shift),
        "schur_residual": real(audit.schur_residual),
        "determinant_residual": real(audit.determinant_residual),
        "bright_root_real": real(audit.bright_root),
        "bright_root_imag": imag(audit.bright_root),
        "bright_root_shift": real(audit.bright_root_shift),
        "bright_root_shift_fraction_of_required": shift_fraction,
        "small_coupling_parameter": audit.small_coupling_parameter,
        "small_coupling_root_bound": audit.small_coupling_bound,
        "small_coupling_bound_fraction_of_required": audit.small_coupling_bound / abs(required),
        "target_dark_pole_distance": audit.target_pole_distance,
        "target_dark_pole_distance_over_target": audit.target_pole_distance_ratio,
        "companion_root_at_required_product": real(companion),
        "target_is_leading_at_required_product": int(abs(audit.target) >= abs(companion)),
        "required_product_leading_one_step_radius": max(physical_radius, companion_radius),
        "direct_bright_one_step_radius": direct_radius,
        "schur_root_one_step_radius": root_radius,
        "physical_one_step_radius": physical_radius,
        "schur_root_radius_error": root_radius - physical_radius,
        "determinant_identity_error": determinant_identity_error,
        "coverage_identity_error": coverage_identity_error,
    }


def seven_scale_audit() -> list[dict[str, object]]:
    source = read_csv(RH20 / "results" / "two_branch_matrix_audit.csv")
    rows: list[dict[str, object]] = []
    for item in source:
        period = int(item["component_period"])
        radius = float(item["archived_bulk_radius"])
        target = radius ** (2 * period)
        matrix = np.asarray(
            (
                (float(item["bright_dark_00"]), float(item["bright_dark_01"])),
                (float(item["bright_dark_10"]), float(item["bright_dark_11"])),
            )
        )
        row: dict[str, object] = {
            "sigma": float(item["sigma"]),
            "folded_dimension": int(item["folded_dimension"]),
            "component_period": period,
            "archived_bulk_radius": radius,
        }
        row.update(audit_fields(matrix, target, period))
        rows.append(row)
    write_csv(RESULTS / "seven_scale_schur_audit.csv", rows)
    return rows


def peripheral_audit() -> list[dict[str, object]]:
    source = read_csv(RH21 / "results" / "biorthogonal_cycle_matrices.csv")
    rows: list[dict[str, object]] = []
    for item in source:
        period = int(item["component_period"])
        radius = float(item["archived_bulk_radius"])
        target = radius ** (2 * period)
        for label in PERIPHERAL_LABELS:
            branch_matrix = np.asarray(
                (
                    (
                        float(item[f"{label}_matrix_00"]),
                        float(item[f"{label}_matrix_01"]),
                    ),
                    (
                        float(item[f"{label}_matrix_10"]),
                        float(item[f"{label}_matrix_11"]),
                    ),
                )
            )
            matrix = bright_dark_transform(branch_matrix)
            row: dict[str, object] = {
                "sigma": float(item["sigma"]),
                "folded_dimension": int(item["folded_dimension"]),
                "component_period": period,
                "archived_bulk_radius": radius,
                "compression": label,
            }
            row.update(audit_fields(matrix, target, period))
            rows.append(row)
    write_csv(RESULTS / "peripheral_schur_audit.csv", rows)
    return rows


def roots_from_product(a: float, d: float, product: float) -> tuple[complex, complex]:
    discriminant = complex((a - d) ** 2 + 4.0 * product)
    square_root = np.sqrt(discriminant)
    roots = ((a + d + square_root) / 2.0, (a + d - square_root) / 2.0)
    ordered = sorted(roots, key=lambda value: abs(value - a))
    return complex(ordered[0]), complex(ordered[1])


def coupling_homotopy(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    selected = {1.0e-3, 1.0e-4}
    output: list[dict[str, object]] = []
    for row in rows:
        sigma = float(row["sigma"])
        if sigma not in selected:
            continue
        a = float(row["direct_bright"])
        d = float(row["dark_pole"])
        observed = float(row["observed_product"])
        required = float(row["required_product"])
        target = float(row["target_return"])
        period = int(row["component_period"])
        previous: complex | None = None
        for fraction in np.linspace(0.0, 1.0, 101):
            product = (1.0 - fraction) * observed + fraction * required
            candidates = roots_from_product(a, d, product)
            if previous is None:
                root = candidates[0]
            else:
                root = min(candidates, key=lambda value: abs(value - previous))
            previous = root
            output.append(
                {
                    "sigma": sigma,
                    "component_period": period,
                    "interpolation_fraction": fraction,
                    "coupling_product": product,
                    "bright_root_real": root.real,
                    "bright_root_imag": root.imag,
                    "bright_root_one_step_radius": abs(root) ** (1.0 / (2 * period)),
                    "target_return": target,
                    "target_one_step_radius": target ** (1.0 / (2 * period)),
                }
            )
    write_csv(RESULTS / "target_coupling_homotopy.csv", output)
    return output


def release_memory() -> None:
    gc.collect()
    try:
        ctypes.CDLL(None).malloc_trim(0)
    except (AttributeError, OSError):
        pass


def resolution_audit() -> list[dict[str, object]]:
    """Rebuild selected branch matrices at three points per Gaussian width."""

    sys.path[:0] = [
        str(RH16 / "src"),
        str(RH17 / "src"),
        str(RH18 / "src"),
        str(RH19 / "src"),
        str(RH20 / "src"),
    ]
    from complement_excursions import critical_branch_masks
    from gaussian_return import (
        effective_noise_scales,
        packet_masks,
        periodic_packet_tube,
        positive_midpoints,
        sparse_folded_gaussian_matrix,
    )
    from sector_branches import branch_profile_basis, compressed_branch_cycle
    from time_ordered_monodromy import boundary_cycle, critical_constants

    source = {
        float(row["sigma"]): row
        for row in read_csv(RH20 / "results" / "two_branch_matrix_audit.csv")
    }
    constants = critical_constants(130)
    rows: list[dict[str, object]] = []
    for sigma in RESOLUTION_SIGMAS:
        archived = source[sigma]
        period = int(archived["component_period"])
        radius = float(archived["archived_bulk_radius"])
        target = radius ** (2 * period)
        cycle = boundary_cycle(period, 130)
        points = np.asarray([float(value) for value in cycle.orbit])
        multipliers = np.abs(
            np.asarray([float(value) for value in cycle.two_step_derivatives])
        )
        tube = periodic_packet_tube(
            multipliers, effective_noise_scales(points, float(constants.u))
        )
        for density in RESOLUTION_DENSITIES:
            dimension = int(round(density / sigma))
            print(
                f"resolution sigma={sigma:g}, n={dimension}, n*sigma={density:g}",
                flush=True,
            )
            started = time.time()
            grid = positive_midpoints(dimension)
            transition = sparse_folded_gaussian_matrix(
                dimension, sigma, u=float(constants.u)
            )
            base = packet_masks(
                grid,
                points,
                sigma * tube.widths,
                window_multiple=WINDOW_MULTIPLE,
                critical_partition=float(constants.first_interior_point),
            )
            left, right, _ = critical_branch_masks(
                grid,
                base,
                points[-1],
                sigma * tube.widths[-1],
                window_multiple=WINDOW_MULTIPLE,
                partition=float(constants.first_interior_point),
            )

            def two_step(values: np.ndarray) -> np.ndarray:
                return transition @ (transition @ values)

            endpoint = np.exp(
                -0.5 * ((grid - points[0]) / (sigma * tube.widths[0])) ** 2
            )
            endpoint[~left[0]] = 0.0
            critical = two_step(endpoint)
            basis = branch_profile_basis(critical, left[-1], right[-1])
            branch = compressed_branch_cycle(two_step, left[:-1], basis)
            matrix = bright_dark_transform(branch)
            row: dict[str, object] = {
                "sigma": sigma,
                "folded_dimension": dimension,
                "dimension_times_sigma": density,
                "component_period": period,
                "archived_bulk_radius": radius,
                "elapsed_seconds": time.time() - started,
            }
            row.update(audit_fields(matrix, target, period))
            rows.append(row)
            del transition, grid, base, left, right, endpoint, critical, basis, branch
            release_memory()
    write_csv(RESULTS / "resolution_schur_audit.csv", rows)
    return rows


def plot_seven_scale(rows: list[dict[str, object]]) -> None:
    sigma = np.asarray([float(row["sigma"]) for row in rows])
    order = np.argsort(sigma)[::-1]
    signed = np.asarray([float(row["signed_coupling_ratio"]) for row in rows])
    coverage = np.asarray([float(row["absolute_coupling_coverage"]) for row in rows])
    signs = np.asarray([int(row["sign_compatible"]) for row in rows], dtype=bool)
    direct = np.asarray([float(row["direct_bright_one_step_radius"]) for row in rows])
    root = np.asarray([float(row["schur_root_one_step_radius"]) for row in rows])
    physical = np.asarray([float(row["physical_one_step_radius"]) for row in rows])
    shift_fraction = np.abs(
        np.asarray([float(row["bright_root_shift_fraction_of_required"]) for row in rows])
    )
    pole_ratio = np.asarray(
        [float(row["target_dark_pole_distance_over_target"]) for row in rows]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axes[0, 0].semilogx(sigma[order], signed[order], "o-", color="#2b5c9a")
    axes[0, 0].axhline(0.0, color="0.5", lw=0.8)
    axes[0, 0].axhline(1.0, color="#a0263f", ls=":", label="required value")
    axes[0, 0].set_yscale("symlog", linthresh=1.0e-4, linscale=0.8)
    axes[0, 0].invert_xaxis()
    axes[0, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel=r"signed coupling ratio $bc/p_{\rm req}$",
        title="Six of seven local couplings have the wrong sign",
    )
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.2)

    colors = np.where(signs, "#27824b", "#a0263f")
    axes[0, 1].scatter(sigma, coverage, c=colors, s=42, zorder=3)
    axes[0, 1].plot(sigma[order], coverage[order], color="0.55", lw=0.8)
    axes[0, 1].axhline(1.0, color="black", ls=":", label="target closure")
    axes[0, 1].set_xscale("log")
    axes[0, 1].set_yscale("log")
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel=r"$|bc|/|p_{\rm req}|$",
        title="Magnitude coverage stays below 14%",
    )
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.2, which="both")

    axes[1, 0].semilogx(sigma[order], direct[order], "o--", label="direct bright entry")
    axes[1, 0].semilogx(sigma[order], root[order], "s-", label="exact 2x2 Schur root")
    axes[1, 0].semilogx(sigma[order], physical[order], "k.-", label="physical bulk edge")
    axes[1, 0].invert_xaxis()
    axes[1, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel="one-step radius",
        title="The local dark channel does not close the radius gap",
    )
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.2)

    axes[1, 1].loglog(sigma[order], shift_fraction[order], "o-", label="actual root shift / required shift")
    axes[1, 1].loglog(sigma[order], pole_ratio[order], "s--", label=r"$|\tau-d|/|\tau|$")
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="dimensionless ratio",
        title="Small root motion and no dark-pole resonance",
    )
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(alpha=0.2, which="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "local_dark_schur_no_go.pdf")
    fig.savefig(FIGURES / "local_dark_schur_no_go.png", dpi=220)
    plt.close(fig)


def plot_peripheral(rows: list[dict[str, object]]) -> None:
    display = {
        "raw_euclidean": "raw Euclidean",
        "raw_biorthogonal": "raw biorthogonal",
        "bulk_euclidean": "bulk Euclidean",
        "bulk_biorthogonal": "bulk biorthogonal",
    }
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    for column, sigma in enumerate(RESOLUTION_SIGMAS):
        selected = [row for row in rows if float(row["sigma"]) == sigma]
        selected.sort(key=lambda row: PERIPHERAL_LABELS.index(str(row["compression"])))
        labels = [display[str(row["compression"])] for row in selected]
        positions = np.arange(len(selected))
        ratios = np.asarray([float(row["signed_coupling_ratio"]) for row in selected])
        axes[0, column].bar(positions, ratios, color=["#27824b" if value > 0 else "#a0263f" for value in ratios])
        axes[0, column].axhline(0.0, color="0.45", lw=0.8)
        axes[0, column].axhline(1.0, color="black", ls=":")
        axes[0, column].set_yscale("symlog", linthresh=1.0e-5)
        axes[0, column].set_xticks(positions, labels, rotation=20, ha="right", fontsize=8)
        axes[0, column].set(
            ylabel=r"$bc/p_{\rm req}$",
            title=rf"Compression robustness, $\sigma={sigma:.0e}$",
        )
        axes[0, column].grid(axis="y", alpha=0.2)

        direct = np.asarray([float(row["direct_bright_one_step_radius"]) for row in selected])
        root = np.asarray([float(row["schur_root_one_step_radius"]) for row in selected])
        physical = float(selected[0]["physical_one_step_radius"])
        width = 0.36
        axes[1, column].bar(positions - width / 2, direct, width, label="direct bright")
        axes[1, column].bar(positions + width / 2, root, width, label="Schur root")
        axes[1, column].axhline(physical, color="black", ls=":", label="physical edge")
        axes[1, column].set_xticks(positions, labels, rotation=20, ha="right", fontsize=8)
        axes[1, column].set(
            ylabel="one-step radius",
            title="Peripheral extraction narrows but does not close the gap",
        )
        axes[1, column].grid(axis="y", alpha=0.2)
        if column == 0:
            axes[1, column].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "peripheral_schur_robustness.pdf")
    fig.savefig(FIGURES / "peripheral_schur_robustness.png", dpi=220)
    plt.close(fig)


def plot_homotopy(rows: list[dict[str, object]]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.1))
    for axis, sigma in zip(axes, RESOLUTION_SIGMAS):
        selected = [row for row in rows if float(row["sigma"]) == sigma]
        fraction = np.asarray([float(row["interpolation_fraction"]) for row in selected])
        radius = np.asarray([float(row["bright_root_one_step_radius"]) for row in selected])
        target = float(selected[0]["target_one_step_radius"])
        axis.plot(fraction, radius, color="#2b5c9a", lw=2.0)
        axis.axhline(target, color="black", ls=":", label="physical target")
        axis.scatter((0.0, 1.0), (radius[0], radius[-1]), color=("#a0263f", "#27824b"), zorder=3)
        axis.set(
            xlabel=r"coupling interpolation $(1-s)bc+s p_{\rm req}$",
            ylabel="one-step bright-root radius",
            title=rf"Required self-energy at $\sigma={sigma:.0e}$",
        )
        if abs(radius[-1] - target) > 1.0e-5:
            axis.annotate(
                "bright branch ends at companion root",
                xy=(1.0, radius[-1]),
                xytext=(0.53, 0.90),
                textcoords="axes fraction",
                arrowprops={"arrowstyle": "->", "color": "0.35"},
                fontsize=8,
                ha="center",
            )
        axis.grid(alpha=0.2)
        axis.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "required_coupling_homotopy.pdf")
    fig.savefig(FIGURES / "required_coupling_homotopy.png", dpi=220)
    plt.close(fig)


def plot_resolution(rows: list[dict[str, object]]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.1))
    for axis, sigma in zip(axes, RESOLUTION_SIGMAS):
        selected = [row for row in rows if float(row["sigma"]) == sigma]
        density = np.asarray([float(row["dimension_times_sigma"]) for row in selected])
        product = np.asarray([float(row["observed_product"]) for row in selected])
        required = np.asarray([float(row["required_product"]) for row in selected])
        axis.plot(density, product, "o-", label="observed $bc$")
        axis.plot(density, required, "s--", label=r"required $p_{\rm req}$")
        axis.axhline(0.0, color="0.5", lw=0.8)
        axis.set_yscale("symlog", linthresh=1.0e-9, linscale=0.8)
        axis.set(
            xlabel=r"grid density $n\sigma$",
            ylabel="return-scale coupling product",
            title=rf"Resolution sign audit, $\sigma={sigma:.0e}$",
        )
        axis.grid(alpha=0.2)
        axis.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "resolution_sign_audit.pdf")
    fig.savefig(FIGURES / "resolution_sign_audit.png", dpi=220)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rebuild-resolution",
        action="store_true",
        help="recompute six sparse Gaussian branch matrices",
    )
    arguments = parser.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    seven = seven_scale_audit()
    peripheral = peripheral_audit()
    homotopy = coupling_homotopy(seven)
    if arguments.rebuild_resolution:
        resolution = resolution_audit()
    else:
        resolution_path = RESULTS / "resolution_schur_audit.csv"
        resolution = read_csv(resolution_path) if resolution_path.exists() else []

    plot_seven_scale(seven)
    plot_peripheral(peripheral)
    plot_homotopy(homotopy)
    if resolution:
        plot_resolution(resolution)

    compatible = [row for row in seven if int(row["sign_compatible"]) == 1]
    smallest = min(seven, key=lambda row: float(row["sigma"]))
    maximum_identity_error = max(
        max(float(row["determinant_identity_error"]), float(row["coverage_identity_error"]))
        for row in seven + peripheral
    )
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "seven_scale_sign_compatible_count": len(compatible),
        "maximum_absolute_coupling_coverage": max(
            float(row["absolute_coupling_coverage"]) for row in seven
        ),
        "smallest_noise_signed_coupling_ratio": float(
            smallest["signed_coupling_ratio"]
        ),
        "smallest_noise_target_pole_distance_ratio": float(
            smallest["target_dark_pole_distance_over_target"]
        ),
        "smallest_noise_small_coupling_parameter": float(
            smallest["small_coupling_parameter"]
        ),
        "maximum_algebraic_identity_error": maximum_identity_error,
        "resolution_rows": len(resolution),
        "source_hashes": {
            "audit.py": source_hash(Path(__file__)),
            "algebra.py": source_hash(ROOT / "src" / "dark_schur" / "algebra.py"),
            "rh20_two_branch_matrix_audit.csv": source_hash(
                RH20 / "results" / "two_branch_matrix_audit.csv"
            ),
            "rh21_biorthogonal_cycle_matrices.csv": source_hash(
                RH21 / "results" / "biorthogonal_cycle_matrices.csv"
            ),
        },
    }
    with (RESULTS / "dark_schur_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated RH-22 dark-channel Schur audits", flush=True)


if __name__ == "__main__":
    main()
