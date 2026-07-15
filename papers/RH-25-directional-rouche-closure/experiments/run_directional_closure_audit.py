"""Extended-Krylov and direct directional closure of the RH-24 contour."""

from __future__ import annotations

import argparse
import csv
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
from scipy.sparse.linalg import LinearOperator, gmres


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
from contour_feshbach import (  # noqa: E402
    build_batched_arnoldi_feshbach,
    determinant_newton_root,
)
from directional_rouche import (  # noqa: E402
    determinant_winding,
    fom_external_solution,
    geometric_tail_majorant,
    matrix_rouche_ratio,
)


DEFAULT_SIGMAS = rh24.DEFAULT_SIGMAS
EXTENSION = 16
HALF_EXTENSION = 8
CONTOUR_NODES = 32
CORRECTION_ATOL_FACTOR = 2.0e-14
INFORMATIVE_INCREMENT_FLOOR = 1.0e-12


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


def baseline_rows() -> dict[float, dict[str, str]]:
    return {
        float(row["sigma"]): row
        for row in read_csv(RH24 / "results" / "scale_summary.csv")
    }


def build_physical_extended_model(sigma: float, setting: dict[str, int]):
    dimension = int(setting["dimension"])
    period = int(setting["period"])
    base_depth = int(rh24.ARNOLDI_DEPTHS[sigma])
    maximum_depth = base_depth + EXTENSION
    constants = rh24.critical_constants(130)
    matrix = rh24.sparse_folded_gaussian_matrix(
        dimension,
        sigma,
        u=float(constants.u),
    )
    spectrum = rh24.resolve_peripheral_modes(matrix)
    trial = rh24.packet_trial(matrix, sigma, dimension, period)
    pair = rh24.canonical_biorthogonal_pair(
        trial,
        spectrum["right_modes"],
        spectrum["left_modes"],
    )
    synthesis = np.asarray(pair.synthesis)
    analysis = np.asarray(pair.analysis)
    _, two_step = rh24.bulk_operator(matrix, spectrum)

    def packet(values):
        array = np.asarray(values)
        return synthesis @ (analysis @ array)

    def external(values):
        array = np.asarray(values)
        return array - packet(array)

    def external_action(values):
        return external(two_step(external(values)))

    reduced = analysis @ two_step(synthesis)
    forcing = external(two_step(synthesis))
    counter = 0

    def observed_action(values):
        nonlocal counter
        counter += 1
        source = external(values)
        applied = two_step(source)
        if counter == 1 or counter % 10 == 0 or counter == maximum_depth:
            print(
                f"  extended Arnoldi {counter}/{maximum_depth}",
                flush=True,
            )
        return external(applied), analysis @ applied

    started = time.time()
    model = build_batched_arnoldi_feshbach(
        observed_action,
        forcing,
        reduced,
        steps=maximum_depth,
        reorthogonalizations=2,
        retain_bases=True,
    )
    build_seconds = time.time() - started

    def observation(values):
        return analysis @ two_step(external(values))

    return {
        "matrix": matrix,
        "spectrum": spectrum,
        "pair": pair,
        "model": model,
        "reduced": reduced,
        "forcing": forcing,
        "external_action": external_action,
        "observation": observation,
        "build_seconds": build_seconds,
        "base_depth": base_depth,
        "maximum_depth": maximum_depth,
    }


def relative_external_residual(
    action,
    forcing: np.ndarray,
    solution: np.ndarray,
    spectral_parameter: complex,
) -> tuple[np.ndarray, float]:
    residual = forcing - (
        complex(spectral_parameter) * np.asarray(solution) - action(solution)
    )
    relative = np.linalg.norm(residual) / max(
        np.linalg.norm(forcing), np.finfo(float).tiny
    )
    return residual, float(relative)


def direct_residual_correction(
    action,
    observation,
    forcing: np.ndarray,
    residual: np.ndarray,
    base_feshbach: np.ndarray,
    spectral_parameter: complex,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    dimension, rank = forcing.shape
    zeta = complex(spectral_parameter)
    operator = LinearOperator(
        (dimension, dimension),
        matvec=lambda vector: zeta * vector - action(vector),
        dtype=np.complex128,
    )
    correction = np.zeros_like(residual, dtype=np.complex128)
    rows = []
    for column in range(rank):
        source_norm = np.linalg.norm(forcing[:, column])
        initial_norm = np.linalg.norm(residual[:, column])
        history: list[float] = []
        if initial_norm <= CORRECTION_ATOL_FACTOR * source_norm:
            solution = np.zeros(dimension, dtype=np.complex128)
            info = 0
        else:
            solution, info = gmres(
                operator,
                residual[:, column],
                rtol=0.0,
                atol=CORRECTION_ATOL_FACTOR * source_norm,
                restart=100,
                maxiter=20,
                callback=lambda value: history.append(float(value)),
                callback_type="pr_norm",
            )
        correction[:, column] = solution
        final = residual[:, column] - operator @ solution
        rows.append(
            {
                "column": column,
                "gmres_info": int(info),
                "gmres_iterations": len(history),
                "initial_residual_to_forcing": initial_norm / source_norm,
                "final_residual_to_forcing": np.linalg.norm(final) / source_norm,
            }
        )
    perturbation = -observation(correction)
    remaining = residual - (zeta * correction - action(correction))
    summary = {
        "direct_correction_rouche_ratio": matrix_rouche_ratio(
            base_feshbach, perturbation
        ),
        "direct_correction_matrix_norm": float(np.linalg.norm(perturbation, 2)),
        "remaining_residual_to_forcing": float(
            np.linalg.norm(remaining) / np.linalg.norm(forcing)
        ),
        "maximum_correction_iterations": max(int(row["gmres_iterations"]) for row in rows),
        "total_correction_iterations": sum(int(row["gmres_iterations"]) for row in rows),
        "all_correction_solves_converged": int(
            all(int(row["gmres_info"]) == 0 for row in rows)
        ),
    }
    return summary, rows


def audit_scale(sigma: float, setting: dict[str, int], baseline: dict[str, str]):
    print(
        f"directional closure sigma={sigma:g}, n={setting['dimension']}",
        flush=True,
    )
    data = build_physical_extended_model(sigma, setting)
    model = data["model"]
    base_depth = int(data["base_depth"])
    middle_depth = base_depth + HALF_EXTENSION
    maximum_depth = int(data["maximum_depth"])
    center = complex(
        float(baseline["direct_center_real"]),
        float(baseline["direct_center_imag"]),
    )
    radius = float(baseline["selected_contour_radius"])
    angles = 2.0 * np.pi * np.arange(CONTOUR_NODES) / CONTOUR_NODES
    points = center + radius * np.exp(1.0j * angles)
    node_rows = []
    phases = {base_depth: [], middle_depth: [], maximum_depth: []}
    worst = None
    forcing_norm = np.linalg.norm(data["forcing"])
    for index, zeta in enumerate(points):
        evaluations = {
            depth: model.evaluate(zeta, depth=depth)
            for depth in (base_depth, middle_depth, maximum_depth)
        }
        first_delta = (
            evaluations[middle_depth].feshbach
            - evaluations[base_depth].feshbach
        )
        second_delta = (
            evaluations[maximum_depth].feshbach
            - evaluations[middle_depth].feshbach
        )
        total_delta = (
            evaluations[maximum_depth].feshbach
            - evaluations[base_depth].feshbach
        )
        first_ratio = matrix_rouche_ratio(
            evaluations[base_depth].feshbach, first_delta
        )
        second_ratio = matrix_rouche_ratio(
            evaluations[base_depth].feshbach, second_delta
        )
        total_ratio = matrix_rouche_ratio(
            evaluations[base_depth].feshbach, total_delta
        )
        tail = geometric_tail_majorant(first_ratio, second_ratio)
        increment_is_informative = first_ratio >= INFORMATIVE_INCREMENT_FLOOR
        conditional_tail_admissible = bool(
            increment_is_informative and tail.admissible
        )
        base_solution = fom_external_solution(model, zeta, depth=base_depth)
        deep_solution = fom_external_solution(model, zeta, depth=maximum_depth)
        base_residual, base_true_relative = relative_external_residual(
            data["external_action"],
            data["forcing"],
            base_solution,
            zeta,
        )
        deep_residual, deep_true_relative = relative_external_residual(
            data["external_action"],
            data["forcing"],
            deep_solution,
            zeta,
        )
        base_from_solution = (
            zeta * np.eye(model.packet_rank)
            - data["reduced"]
            - data["observation"](base_solution)
        )
        deep_from_solution = (
            zeta * np.eye(model.packet_rank)
            - data["reduced"]
            - data["observation"](deep_solution)
        )
        reconstruction_error = max(
            np.linalg.norm(
                base_from_solution - evaluations[base_depth].feshbach
            ),
            np.linalg.norm(
                deep_from_solution - evaluations[maximum_depth].feshbach
            ),
        )
        row = {
            "sigma": sigma,
            "node": index,
            "theta": angles[index],
            "z_real": zeta.real,
            "z_imag": zeta.imag,
            "base_depth": base_depth,
            "middle_depth": middle_depth,
            "maximum_depth": maximum_depth,
            "first_increment_rouche_ratio": first_ratio,
            "second_increment_rouche_ratio": second_ratio,
            "total_extended_rouche_ratio": total_ratio,
            "increment_is_informative": int(increment_is_informative),
            "observed_contraction_ratio": (
                tail.contraction_ratio if increment_is_informative else ""
            ),
            "conditional_geometric_total": (
                tail.total_from_base if conditional_tail_admissible else ""
            ),
            "conditional_tail_admissible": int(conditional_tail_admissible),
            "base_true_residual_to_forcing": base_true_relative,
            "deep_true_residual_to_forcing": deep_true_relative,
            "base_reported_residual_bound": evaluations[
                base_depth
            ].relative_frobenius_residual,
            "deep_reported_residual_bound": evaluations[
                maximum_depth
            ].relative_frobenius_residual,
            "feshbach_reconstruction_error": reconstruction_error,
            "base_smallest_feshbach_singular": evaluations[
                base_depth
            ].smallest_singular_value,
            "deep_smallest_feshbach_singular": evaluations[
                maximum_depth
            ].smallest_singular_value,
            "base_absolute_residual_norm": np.linalg.norm(base_residual),
            "deep_absolute_residual_norm": np.linalg.norm(deep_residual),
            "forcing_norm": forcing_norm,
        }
        node_rows.append(row)
        for depth in phases:
            phases[depth].append(evaluations[depth].determinant_phase)
        if worst is None or total_ratio > worst[0]:
            worst = (
                total_ratio,
                index,
                zeta,
                evaluations[base_depth].feshbach,
                base_residual,
            )
        if index % 8 == 0:
            print(
                f"  contour node {index}/{CONTOUR_NODES}, eta={total_ratio:.3e}",
                flush=True,
            )

    winding = {
        depth: determinant_winding(np.asarray(values))
        for depth, values in phases.items()
    }
    correction_started = time.time()
    correction_summary, correction_rows = direct_residual_correction(
        data["external_action"],
        data["observation"],
        data["forcing"],
        worst[4],
        worst[3],
        worst[2],
    )
    correction_seconds = time.time() - correction_started
    for row in correction_rows:
        row.update(
            {
                "sigma": sigma,
                "worst_node": worst[1],
                "z_real": worst[2].real,
                "z_imag": worst[2].imag,
            }
        )

    admissible_rows = [
        row for row in node_rows if int(row["conditional_tail_admissible"]) == 1
    ]
    informative_rows = [
        row
        for row in node_rows
        if int(row["increment_is_informative"]) == 1
    ]
    summary = {
        "sigma": sigma,
        "folded_dimension": int(setting["dimension"]),
        "packet_rank": model.packet_rank,
        "base_depth": base_depth,
        "middle_depth": middle_depth,
        "maximum_depth": maximum_depth,
        "contour_nodes": CONTOUR_NODES,
        "base_winding_float": winding[base_depth][0],
        "base_winding_integer": winding[base_depth][1],
        "middle_winding_integer": winding[middle_depth][1],
        "deep_winding_integer": winding[maximum_depth][1],
        "maximum_base_phase_increment": winding[base_depth][2],
        "maximum_deep_phase_increment": winding[maximum_depth][2],
        "maximum_first_increment_rouche_ratio": max(
            float(row["first_increment_rouche_ratio"]) for row in node_rows
        ),
        "maximum_second_increment_rouche_ratio": max(
            float(row["second_increment_rouche_ratio"]) for row in node_rows
        ),
        "maximum_total_extended_rouche_ratio": max(
            float(row["total_extended_rouche_ratio"]) for row in node_rows
        ),
        "informative_increment_node_count": len(informative_rows),
        "contracting_informative_node_count": sum(
            float(row["observed_contraction_ratio"]) < 1.0
            for row in informative_rows
        ),
        "maximum_informative_contraction_ratio": max(
            (
                float(row["observed_contraction_ratio"])
                for row in informative_rows
            ),
            default="",
        ),
        "roundoff_limited_node_count": sum(
            float(row["total_extended_rouche_ratio"])
            < INFORMATIVE_INCREMENT_FLOOR
            for row in node_rows
        ),
        "admissible_geometric_node_count": len(admissible_rows),
        "maximum_conditional_geometric_total": max(
            (
                float(row["conditional_geometric_total"])
                for row in admissible_rows
            ),
            default="",
        ),
        "maximum_base_true_residual_to_forcing": max(
            float(row["base_true_residual_to_forcing"]) for row in node_rows
        ),
        "maximum_deep_true_residual_to_forcing": max(
            float(row["deep_true_residual_to_forcing"]) for row in node_rows
        ),
        "maximum_feshbach_reconstruction_error": max(
            float(row["feshbach_reconstruction_error"]) for row in node_rows
        ),
        "minimum_base_feshbach_singular": min(
            float(row["base_smallest_feshbach_singular"]) for row in node_rows
        ),
        "minimum_deep_feshbach_singular": min(
            float(row["deep_smallest_feshbach_singular"]) for row in node_rows
        ),
        "worst_extended_node": worst[1],
        "worst_extended_z_real": worst[2].real,
        "worst_extended_z_imag": worst[2].imag,
        **correction_summary,
        "extended_arnoldi_seconds": data["build_seconds"],
        "direct_correction_seconds": correction_seconds,
    }
    del data
    rh24.release_memory()
    return summary, node_rows, correction_rows


def plot_summary(rows: list[dict[str, object]]) -> None:
    ordered = sorted(rows, key=lambda row: float(row["sigma"]), reverse=True)
    sigma = np.asarray([float(row["sigma"]) for row in ordered])
    first = np.asarray(
        [float(row["maximum_first_increment_rouche_ratio"]) for row in ordered]
    )
    second = np.asarray(
        [float(row["maximum_second_increment_rouche_ratio"]) for row in ordered]
    )
    total = np.asarray(
        [float(row["maximum_total_extended_rouche_ratio"]) for row in ordered]
    )
    direct = np.asarray(
        [float(row["direct_correction_rouche_ratio"]) for row in ordered]
    )
    base_residual = np.asarray(
        [float(row["maximum_base_true_residual_to_forcing"]) for row in ordered]
    )
    deep_residual = np.asarray(
        [float(row["maximum_deep_true_residual_to_forcing"]) for row in ordered]
    )
    remaining = np.asarray(
        [float(row["remaining_residual_to_forcing"]) for row in ordered]
    )
    correction_iterations = np.asarray(
        [int(float(row["total_correction_iterations"])) for row in ordered]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axes[0, 0].loglog(sigma, first, "o-", label=r"$J\to J+8$")
    axes[0, 0].loglog(sigma, second, "s--", label=r"$J+8\to J+16$")
    axes[0, 0].loglog(sigma, total, "^:", label=r"$J\to J+16$")
    axes[0, 0].axhline(1.0, color="0.4", lw=0.8)
    axes[0, 0].invert_xaxis()
    axes[0, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel=r"maximum $\|F_J^{-1}\Delta F\|_2$",
        title="Directional Krylov increments stay below one",
    )
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(alpha=0.2, which="both")

    axes[0, 1].loglog(
        sigma,
        np.maximum(total, 1.0e-17),
        "o-",
        label="extended directional change",
    )
    axes[0, 1].loglog(
        sigma,
        np.where(correction_iterations > 0, direct, np.nan),
        "s--",
        label="direct correction at worst node",
    )
    axes[0, 1].axhline(1.0, color="0.4", lw=0.8)
    axes[0, 1].invert_xaxis()
    axes[0, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="Rouché perturbation ratio",
        title="Direct low-rank correction confirms the extension",
    )
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(alpha=0.2, which="both")

    axes[1, 0].loglog(sigma, base_residual, "o-", label="depth J true residual")
    axes[1, 0].loglog(sigma, deep_residual, "s--", label="depth J+16 true residual")
    axes[1, 0].loglog(sigma, remaining, "^:", label="after direct correction")
    axes[1, 0].invert_xaxis()
    axes[1, 0].set(
        xlabel=r"noise $\sigma$",
        ylabel="residual / forcing",
        title="Ambient residuals, including recurrence defects",
    )
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(alpha=0.2, which="both")

    axes[1, 1].semilogx(sigma, correction_iterations, "o-", color="#6b3fa0")
    axes[1, 1].invert_xaxis()
    axes[1, 1].set(
        xlabel=r"noise $\sigma$",
        ylabel="total GMRES correction iterations",
        title="Direct directional closure becomes costlier",
    )
    axes[1, 1].grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(FIGURES / "directional_closure_summary.pdf")
    fig.savefig(FIGURES / "directional_closure_summary.png", dpi=220)
    plt.close(fig)


def plot_contour_profiles(rows: list[dict[str, object]]) -> None:
    selected_sigmas = (1.0e-2, 1.0e-3, 1.0e-4)
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.8))
    for axis, sigma in zip(axes, selected_sigmas):
        selected = sorted(
            [row for row in rows if float(row["sigma"]) == sigma],
            key=lambda row: int(float(row["node"])),
        )
        theta = np.asarray([float(row["theta"]) for row in selected])
        first = np.asarray(
            [float(row["first_increment_rouche_ratio"]) for row in selected]
        )
        second = np.asarray(
            [float(row["second_increment_rouche_ratio"]) for row in selected]
        )
        total = np.asarray(
            [float(row["total_extended_rouche_ratio"]) for row in selected]
        )
        plotting_floor = 1.0e-17
        axis.semilogy(
            theta,
            np.maximum(first, plotting_floor),
            "o-",
            ms=3,
            label=r"$J\to J+8$",
        )
        axis.semilogy(
            theta,
            np.maximum(second, plotting_floor),
            "s--",
            ms=3,
            label=r"$J+8\to J+16$",
        )
        axis.semilogy(
            theta,
            np.maximum(total, plotting_floor),
            "^:",
            ms=3,
            label="total",
        )
        axis.set(
            xlabel=r"contour angle $\theta$",
            ylabel="directional ratio",
            title=rf"$\sigma={sigma:.0e}$",
        )
        axis.grid(alpha=0.2, which="both")
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "directional_contour_profiles.pdf")
    fig.savefig(FIGURES / "directional_contour_profiles.png", dpi=220)
    plt.close(fig)


def regenerate() -> None:
    summaries = read_csv(RESULTS / "directional_scale_summary.csv")
    nodes = read_csv(RESULTS / "directional_contour_nodes.csv")
    plot_summary(summaries)
    available = {float(row["sigma"]) for row in nodes}
    if {1.0e-2, 1.0e-3, 1.0e-4}.issubset(available):
        plot_contour_profiles(nodes)


def normalize_saved_roundoff_fields() -> None:
    """Upgrade preexisting result tables without rerunning ambient operators."""

    node_path = RESULTS / "directional_contour_nodes.csv"
    summary_path = RESULTS / "directional_scale_summary.csv"
    nodes = read_csv(node_path)
    normalized_nodes = []
    for old in nodes:
        first = float(old["first_increment_rouche_ratio"])
        second = float(old["second_increment_rouche_ratio"])
        informative = first >= INFORMATIVE_INCREMENT_FLOOR
        tail = geometric_tail_majorant(first, second)
        admissible = informative and tail.admissible
        row: dict[str, object] = {}
        for key, value in old.items():
            row[key] = value
            if key == "total_extended_rouche_ratio":
                row["increment_is_informative"] = int(informative)
        row["observed_contraction_ratio"] = (
            tail.contraction_ratio if informative else ""
        )
        row["conditional_geometric_total"] = (
            tail.total_from_base if admissible else ""
        )
        row["conditional_tail_admissible"] = int(admissible)
        normalized_nodes.append(row)
    write_csv(node_path, normalized_nodes)

    grouped: dict[float, list[dict[str, object]]] = {}
    for row in normalized_nodes:
        grouped.setdefault(float(row["sigma"]), []).append(row)
    summaries = read_csv(summary_path)
    for summary in summaries:
        rows = grouped[float(summary["sigma"])]
        informative_rows = [
            row for row in rows if int(row["increment_is_informative"]) == 1
        ]
        admissible_rows = [
            row for row in rows if int(row["conditional_tail_admissible"]) == 1
        ]
        summary["informative_increment_node_count"] = len(informative_rows)
        summary["contracting_informative_node_count"] = sum(
            float(row["observed_contraction_ratio"]) < 1.0
            for row in informative_rows
        )
        summary["maximum_informative_contraction_ratio"] = max(
            (
                float(row["observed_contraction_ratio"])
                for row in informative_rows
            ),
            default="",
        )
        summary["admissible_geometric_node_count"] = len(admissible_rows)
        summary["maximum_conditional_geometric_total"] = max(
            (
                float(row["conditional_geometric_total"])
                for row in admissible_rows
            ),
            default="",
        )
    write_csv(summary_path, summaries)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigmas", nargs="*", type=float, default=list(DEFAULT_SIGMAS))
    parser.add_argument("--reuse", action="store_true")
    arguments = parser.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    if not arguments.reuse:
        settings = rh24.physical_settings()
        baselines = baseline_rows()
        outputs = []
        for sigma in arguments.sigmas:
            outputs.append(
                audit_scale(
                    float(sigma),
                    settings[float(sigma)],
                    baselines[float(sigma)],
                )
            )
            summaries = [output[0] for output in outputs]
            nodes = [row for output in outputs for row in output[1]]
            corrections = [row for output in outputs for row in output[2]]
            write_csv(RESULTS / "directional_scale_summary.csv", summaries)
            write_csv(RESULTS / "directional_contour_nodes.csv", nodes)
            write_csv(RESULTS / "direct_correction_columns.csv", corrections)
    if arguments.reuse:
        normalize_saved_roundoff_fields()
    regenerate()
    summaries = read_csv(RESULTS / "directional_scale_summary.csv")
    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "sigmas": [float(row["sigma"]) for row in summaries],
        "extension": EXTENSION,
        "half_extension": HALF_EXTENSION,
        "contour_nodes": CONTOUR_NODES,
        "correction_atol_factor": CORRECTION_ATOL_FACTOR,
        "informative_increment_floor": INFORMATIVE_INCREMENT_FLOOR,
        "all_windings": [
            int(float(row["deep_winding_integer"])) for row in summaries
        ],
        "maximum_extended_rouche_ratio": max(
            float(row["maximum_total_extended_rouche_ratio"]) for row in summaries
        ),
        "maximum_direct_correction_ratio": max(
            float(row["direct_correction_rouche_ratio"]) for row in summaries
        ),
        "source_hashes": {
            "audit.py": source_hash(Path(__file__)),
            "algebra.py": source_hash(
                ROOT / "src" / "directional_rouche" / "algebra.py"
            ),
            "rh24_audit.py": source_hash(
                RH24 / "experiments" / "run_contour_feshbach_audit.py"
            ),
            "rh24_model.py": source_hash(
                RH24 / "src" / "contour_feshbach" / "model.py"
            ),
        },
    }
    with (RESULTS / "directional_closure_summary.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated directional Rouché closure audit", flush=True)


if __name__ == "__main__":
    main()
