"""Seven-scale outward-rounded stored-matrix primal-dual audit."""

from __future__ import annotations

import argparse
import csv
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
RH23 = PAPERS / "RH-23-physical-packet-complement-feshbach"
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH26 = PAPERS / "RH-26-primal-dual-directional-certificate"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH26 / "src"),
    str(RH26 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_directional_closure_audit as rh25  # noqa: E402
import run_primal_dual_audit as rh26  # noqa: E402
from directional_rouche import determinant_winding, fom_external_solution  # noqa: E402
from outward_residuals import (  # noqa: E402
    LongDoubleFactorGraph,
    StoredFactorGraph,
    ball_utilization,
    certify_budget,
    frobenius_upper_array,
    longdouble_frobenius,
)


DEFAULT_SIGMAS = rh24.DEFAULT_SIGMAS
CONTOUR_NODES = rh26.CONTOUR_NODES


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rh26_deep_nodes() -> dict[tuple[float, int], dict[str, str]]:
    summaries = {
        float(row["sigma"]): int(float(row["dual_maximum_depth"]))
        for row in read_csv(RH26 / "results" / "primal_dual_scale_summary.csv")
    }
    return {
        (float(row["sigma"]), int(float(row["node"]))): row
        for row in read_csv(RH26 / "results" / "primal_dual_contour_nodes.csv")
        if int(float(row["dual_depth"])) == summaries[float(row["sigma"])]
    }


def rh23_resolvent_lower_bounds() -> dict[float, float]:
    return {
        float(row["sigma"]): float(row["external_resolvent_lower_bound"])
        for row in read_csv(RH23 / "results" / "physical_eigenmode_closure.csv")
    }


def relative_frobenius_center(values: np.ndarray, denominator: float) -> float:
    return float(np.linalg.norm(np.asarray(values), ord="fro") / denominator)


def crosscheck_row(
    sigma: float,
    node_number: int,
    graph: StoredFactorGraph,
    blocks,
    node,
    spectral_parameter: complex,
    base_feshbach: np.ndarray,
    base_solution: np.ndarray,
    deep_solution: np.ndarray,
    dual_solution: np.ndarray,
) -> dict[str, object]:
    """Reevaluate one physical node with explicit 80-bit CSR reductions."""

    begun = time.time()
    reference_graph = LongDoubleFactorGraph(
        graph.matrix,
        graph.right,
        graph.left,
        graph.values,
        graph.synthesis,
        graph.analysis,
    )
    reference_blocks = reference_graph.build_blocks()
    reference_node = reference_graph.node(
        reference_blocks,
        spectral_parameter,
        base_feshbach,
        base_solution,
        deep_solution,
        dual_solution,
    )
    return {
        "sigma": sigma,
        "node": node_number,
        "longdouble_mantissa_bits": int(np.finfo(np.longdouble).nmant),
        "direct_ball_utilization": ball_utilization(
            reference_blocks.direct, blocks.direct
        ),
        "forcing_ball_utilization": ball_utilization(
            reference_blocks.forcing, blocks.forcing
        ),
        "observation_adjoint_ball_utilization": ball_utilization(
            reference_blocks.observation_adjoint,
            blocks.observation_adjoint,
        ),
        "primal_residual_ball_utilization": ball_utilization(
            reference_node.primal_residual, node.primal_residual
        ),
        "dual_residual_ball_utilization": ball_utilization(
            reference_node.dual_residual, node.dual_residual
        ),
        "base_consistency_ball_utilization": ball_utilization(
            reference_node.base_consistency, node.base_consistency
        ),
        "total_correction_ball_utilization": ball_utilization(
            reference_node.total_computed_correction,
            node.total_computed_correction,
        ),
        "longdouble_primal_residual_frobenius": float(
            longdouble_frobenius(reference_node.primal_residual)
        ),
        "longdouble_dual_residual_frobenius": float(
            longdouble_frobenius(reference_node.dual_residual)
        ),
        "elapsed_seconds": time.time() - begun,
    }


def audit_scale(
    sigma: float,
    setting: dict[str, int],
    previous_nodes: dict[tuple[float, int], dict[str, str]],
    rh23_lower_bound: float,
    *,
    perform_crosscheck: bool,
):
    print(
        f"outward audit sigma={sigma:g}, n={setting['dimension']}",
        flush=True,
    )
    data = rh25.build_physical_extended_model(float(sigma), setting)
    environment = rh26.attach_adjoint_environment(data)
    model = data["model"]
    base_depth = int(data["base_depth"])
    maximum_depth = int(data["maximum_depth"])
    dual_model, _, dual_seconds = rh26.build_dual_arnoldi(
        environment, maximum_depth
    )
    graph = StoredFactorGraph(
        data["matrix"],
        data["spectrum"]["right_modes"],
        data["spectrum"]["left_modes"],
        data["spectrum"]["peripheral_values"],
        data["pair"].synthesis,
        data["pair"].analysis,
    )
    statistics = graph.statistics()
    blocks = graph.build_blocks()
    forcing_scale = max(
        frobenius_upper_array(blocks.forcing.center), np.finfo(float).tiny
    )
    dual_scale = max(
        frobenius_upper_array(blocks.observation_adjoint.center),
        np.finfo(float).tiny,
    )
    direct_center_defect = float(
        np.linalg.norm(blocks.direct.center - np.asarray(data["reduced"]), ord="fro")
    )
    forcing_center_defect = float(
        np.linalg.norm(blocks.forcing.center - np.asarray(data["forcing"]), ord="fro")
    )
    observation_center_defect = float(
        np.linalg.norm(
            blocks.observation_adjoint.center
            - np.asarray(environment["observation_matrix"]).conj().T,
            ord="fro",
        )
    )

    theta, points = rh26.contour_points(float(sigma))
    phases: list[float] = []
    node_rows: list[dict[str, object]] = []
    crosschecks: list[dict[str, object]] = []
    for node_number, (angle, zeta) in enumerate(zip(theta, points)):
        begun = time.time()
        base_evaluation = model.evaluate(zeta, depth=base_depth)
        base_solution = fom_external_solution(model, zeta, depth=base_depth)
        deep_solution = fom_external_solution(model, zeta, depth=maximum_depth)
        dual_solution = fom_external_solution(
            dual_model, np.conj(zeta), depth=maximum_depth
        )
        node = graph.node_enclosures(
            blocks,
            zeta,
            base_evaluation.feshbach,
            base_solution,
            deep_solution,
            dual_solution,
        )
        certificate = certify_budget(
            base_evaluation.feshbach,
            node.total_computed_correction,
            node.primal_residual,
            node.dual_residual,
        )
        prior = previous_nodes[(float(sigma), node_number)]
        ordinary_budget = float(prior["primal_dual_resolvent_budget"])
        primal_center_norm = float(
            np.linalg.norm(node.primal_residual.center, ord="fro")
        )
        dual_center_norm = float(
            np.linalg.norm(node.dual_residual.center, ord="fro")
        )
        correction_center_ratio = float(
            np.linalg.norm(
                np.linalg.solve(
                    base_evaluation.feshbach,
                    node.total_computed_correction.center,
                ),
                ord=2,
            )
        )
        corrected = (
            base_evaluation.feshbach
            + node.total_computed_correction.center
        )
        sign, _ = np.linalg.slogdet(corrected)
        phase = float(np.angle(sign))
        phases.append(phase)
        row: dict[str, object] = {
            "sigma": sigma,
            "node": node_number,
            "theta": angle,
            "z_real": zeta.real,
            "z_imag": zeta.imag,
            "base_depth": base_depth,
            "primal_depth": maximum_depth,
            "dual_depth": maximum_depth,
            "primal_residual_center_frobenius": primal_center_norm,
            "primal_residual_radius": node.primal_residual.radius,
            "primal_residual_norm_upper": certificate.primal_residual_norm_upper,
            "primal_residual_center_relative_to_forcing": primal_center_norm
            / forcing_scale,
            "primal_residual_upper_relative_to_forcing_center": certificate.primal_residual_norm_upper
            / forcing_scale,
            "primal_residual_inflation": certificate.primal_residual_norm_upper
            / max(primal_center_norm, np.finfo(float).tiny),
            "dual_residual_center_frobenius": dual_center_norm,
            "dual_residual_radius": node.dual_residual.radius,
            "dual_residual_norm_upper": node.dual_residual.norm_upper,
            "dual_residual_center_relative_to_rhs": dual_center_norm / dual_scale,
            "dual_residual_upper_relative_to_rhs_center": node.dual_residual.norm_upper
            / dual_scale,
            "dual_residual_inflation": node.dual_residual.norm_upper
            / max(dual_center_norm, np.finfo(float).tiny),
            "base_consistency_center_frobenius": float(
                np.linalg.norm(node.base_consistency.center, ord="fro")
            ),
            "base_consistency_radius": node.base_consistency.radius,
            "base_consistency_norm_upper": node.base_consistency.norm_upper,
            "total_correction_center_frobenius": float(
                np.linalg.norm(node.total_computed_correction.center, ord="fro")
            ),
            "total_correction_radius": node.total_computed_correction.radius,
            "total_correction_norm_upper": node.total_computed_correction.norm_upper,
            "correction_center_rouche_ratio": correction_center_ratio,
            "correction_rouche_ratio_upper": certificate.correction_ratio_upper,
            "weighted_dual_residual_norm_upper": certificate.weighted_dual_residual_norm_upper,
            "remainder_coefficient_upper": certificate.remainder_coefficient_upper,
            "resolvent_budget_lower": certificate.resolvent_budget_lower,
            "rh26_unrounded_resolvent_budget": ordinary_budget,
            "budget_retention_fraction": certificate.resolvent_budget_lower
            / ordinary_budget,
            "budget_to_rh23_lower_bound": certificate.resolvent_budget_lower
            / rh23_lower_bound,
            "base_inverse_norm_upper": certificate.inverse_certificate.inverse_norm_upper,
            "base_inverse_neumann_defect_upper": certificate.inverse_certificate.defect_norm_upper,
            "corrected_feshbach_smallest_singular": float(
                np.linalg.svd(corrected, compute_uv=False)[-1]
            ),
            "corrected_determinant_phase": phase,
            "node_seconds": time.time() - begun,
        }
        node_rows.append(row)
        if perform_crosscheck and node_number == 0:
            print("  explicit 80-bit graph cross-check", flush=True)
            crosschecks.append(
                crosscheck_row(
                    sigma,
                    node_number,
                    graph,
                    blocks,
                    node,
                    zeta,
                    base_evaluation.feshbach,
                    base_solution,
                    deep_solution,
                    dual_solution,
                )
            )
        if node_number % 8 == 0:
            print(
                f"  node {node_number}/{CONTOUR_NODES}: "
                f"eta+={certificate.correction_ratio_upper:.3e}, "
                f"M->={certificate.resolvent_budget_lower:.3e}",
                flush=True,
            )

    winding_float, winding_integer, phase_increment = determinant_winding(
        np.asarray(phases)
    )
    summary: dict[str, object] = {
        "sigma": sigma,
        "folded_dimension": int(setting["dimension"]),
        "packet_rank": model.packet_rank,
        "base_depth": base_depth,
        "primal_depth": maximum_depth,
        "dual_depth": maximum_depth,
        "contour_nodes": CONTOUR_NODES,
        "enclosed_center_winding_float": winding_float,
        "enclosed_center_winding_integer": winding_integer,
        "enclosed_center_maximum_phase_increment": phase_increment,
        "maximum_primal_residual_center_relative": max(
            float(row["primal_residual_center_relative_to_forcing"])
            for row in node_rows
        ),
        "maximum_primal_residual_upper_relative": max(
            float(row["primal_residual_upper_relative_to_forcing_center"])
            for row in node_rows
        ),
        "maximum_dual_residual_center_relative": max(
            float(row["dual_residual_center_relative_to_rhs"])
            for row in node_rows
        ),
        "maximum_dual_residual_upper_relative": max(
            float(row["dual_residual_upper_relative_to_rhs_center"])
            for row in node_rows
        ),
        "maximum_primal_residual_inflation": max(
            float(row["primal_residual_inflation"]) for row in node_rows
        ),
        "maximum_dual_residual_inflation": max(
            float(row["dual_residual_inflation"]) for row in node_rows
        ),
        "maximum_base_consistency_norm_upper": max(
            float(row["base_consistency_norm_upper"]) for row in node_rows
        ),
        "maximum_correction_center_rouche_ratio": max(
            float(row["correction_center_rouche_ratio"]) for row in node_rows
        ),
        "maximum_correction_rouche_ratio_upper": max(
            float(row["correction_rouche_ratio_upper"]) for row in node_rows
        ),
        "minimum_resolvent_budget_lower": min(
            float(row["resolvent_budget_lower"]) for row in node_rows
        ),
        "minimum_rh26_unrounded_resolvent_budget": min(
            float(row["rh26_unrounded_resolvent_budget"]) for row in node_rows
        ),
        "minimum_budget_retention_fraction": min(
            float(row["budget_retention_fraction"]) for row in node_rows
        ),
        "minimum_budget_to_rh23_lower_bound": min(
            float(row["budget_to_rh23_lower_bound"]) for row in node_rows
        ),
        "maximum_base_inverse_neumann_defect_upper": max(
            float(row["base_inverse_neumann_defect_upper"]) for row in node_rows
        ),
        "maximum_base_inverse_norm_upper": max(
            float(row["base_inverse_norm_upper"]) for row in node_rows
        ),
        "minimum_corrected_feshbach_singular": min(
            float(row["corrected_feshbach_smallest_singular"])
            for row in node_rows
        ),
        "rh23_eigenmode_resolvent_lower_bound": rh23_lower_bound,
        "direct_block_radius": blocks.direct.radius,
        "forcing_block_radius": blocks.forcing.radius,
        "observation_adjoint_block_radius": blocks.observation_adjoint.radius,
        "direct_center_reproduction_defect": direct_center_defect,
        "forcing_center_reproduction_defect": forcing_center_defect,
        "observation_center_reproduction_defect": observation_center_defect,
        "primal_arnoldi_seconds": float(data["build_seconds"]),
        "dual_arnoldi_seconds": dual_seconds,
    }
    summary.update(statistics)
    del data, environment, model, dual_model, graph, blocks
    gc.collect()
    rh24.release_memory()
    return summary, node_rows, crosschecks


def plot_summary(rows: list[dict[str, str]]) -> None:
    ordered = sorted(rows, key=lambda row: float(row["sigma"]), reverse=True)
    sigma = np.asarray([float(row["sigma"]) for row in ordered])
    primal_center = np.asarray(
        [float(row["maximum_primal_residual_center_relative"]) for row in ordered]
    )
    primal_upper = np.asarray(
        [float(row["maximum_primal_residual_upper_relative"]) for row in ordered]
    )
    dual_center = np.asarray(
        [float(row["maximum_dual_residual_center_relative"]) for row in ordered]
    )
    dual_upper = np.asarray(
        [float(row["maximum_dual_residual_upper_relative"]) for row in ordered]
    )
    enclosed_budget = np.asarray(
        [float(row["minimum_resolvent_budget_lower"]) for row in ordered]
    )
    ordinary_budget = np.asarray(
        [float(row["minimum_rh26_unrounded_resolvent_budget"]) for row in ordered]
    )
    comparison = np.asarray(
        [float(row["rh23_eigenmode_resolvent_lower_bound"]) for row in ordered]
    )
    eta = np.asarray(
        [float(row["maximum_correction_rouche_ratio_upper"]) for row in ordered]
    )
    eta_center = np.asarray(
        [float(row["maximum_correction_center_rouche_ratio"]) for row in ordered]
    )
    primal_inflation = np.asarray(
        [float(row["maximum_primal_residual_inflation"]) for row in ordered]
    )
    dual_inflation = np.asarray(
        [float(row["maximum_dual_residual_inflation"]) for row in ordered]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axes[0, 0].loglog(sigma, primal_center, "o:", label="primal centre")
    axes[0, 0].loglog(sigma, primal_upper, "o-", label="primal upper")
    axes[0, 0].loglog(sigma, dual_center, "s:", label="dual centre")
    axes[0, 0].loglog(sigma, dual_upper, "s--", label="dual upper")
    axes[0, 0].set(ylabel="relative Frobenius residual", title="Outward residual envelopes")
    axes[0, 0].legend(frameon=False, fontsize=8)

    axes[0, 1].loglog(sigma, ordinary_budget, "o:", label="RH-26 floating")
    axes[0, 1].loglog(sigma, enclosed_budget, "s-", label="outward lower")
    axes[0, 1].loglog(sigma, comparison, "^--", label="RH-23 lower bound")
    axes[0, 1].set(ylabel=r"conditional inverse budget $M_*$", title="Budget after enclosure")
    axes[0, 1].legend(frameon=False, fontsize=8)

    axes[1, 0].loglog(sigma, eta_center, "o:", label="centre")
    axes[1, 0].loglog(sigma, eta, "s-", label="outward upper")
    axes[1, 0].axhline(1.0, color="0.4", lw=0.8)
    axes[1, 0].set(ylabel=r"maximum $\eta$", title="Computed perturbation margin")
    axes[1, 0].legend(frameon=False, fontsize=8)

    axes[1, 1].loglog(sigma, primal_inflation, "o-", label="primal")
    axes[1, 1].loglog(sigma, dual_inflation, "s--", label="dual")
    axes[1, 1].set(ylabel="upper / floating-centre norm", title="Residual inflation")
    axes[1, 1].legend(frameon=False, fontsize=8)
    for axis in axes.flat:
        axis.set_xlabel(r"noise $\sigma$")
        axis.invert_xaxis()
        axis.grid(alpha=0.2, which="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "outward_residual_summary.pdf")
    fig.savefig(FIGURES / "outward_residual_summary.png", dpi=220)
    plt.close(fig)


def plot_contours(rows: list[dict[str, str]]) -> None:
    selected_sigmas = (1.0e-3, 2.0e-4, 1.0e-4)
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.8))
    for axis, sigma in zip(axes, selected_sigmas):
        selected = sorted(
            [row for row in rows if float(row["sigma"]) == sigma],
            key=lambda row: int(float(row["node"])),
        )
        if not selected:
            continue
        theta = np.asarray([float(row["theta"]) for row in selected])
        enclosed = np.asarray(
            [float(row["resolvent_budget_lower"]) for row in selected]
        )
        ordinary = np.asarray(
            [float(row["rh26_unrounded_resolvent_budget"]) for row in selected]
        )
        axis.semilogy(theta, ordinary, "o:", ms=3, label="RH-26 floating")
        axis.semilogy(theta, enclosed, "s-", ms=3, label="outward lower")
        axis.set(
            xlabel=r"contour angle $\theta$",
            ylabel=r"conditional budget $M_*$",
            title=rf"$\sigma={sigma:.0e}$",
        )
        axis.grid(alpha=0.2, which="both")
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "outward_contour_budgets.pdf")
    fig.savefig(FIGURES / "outward_contour_budgets.png", dpi=220)
    plt.close(fig)


def regenerate() -> None:
    summaries = read_csv(RESULTS / "outward_scale_summary.csv")
    nodes = read_csv(RESULTS / "outward_contour_nodes.csv")
    plot_summary(summaries)
    if {1.0e-3, 2.0e-4, 1.0e-4}.issubset(
        {float(row["sigma"]) for row in nodes}
    ):
        plot_contours(nodes)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigmas", nargs="*", type=float, default=list(DEFAULT_SIGMAS))
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--reuse", action="store_true")
    parser.add_argument("--skip-crosscheck", action="store_true")
    arguments = parser.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    if not arguments.reuse:
        settings = rh24.physical_settings()
        previous_nodes = rh26_deep_nodes()
        lower_bounds = rh23_resolvent_lower_bounds()
        summaries: list[dict[str, object]] = []
        nodes: list[dict[str, object]] = []
        crosschecks: list[dict[str, object]] = []
        if arguments.resume and (RESULTS / "outward_scale_summary.csv").exists():
            summaries = list(read_csv(RESULTS / "outward_scale_summary.csv"))
            nodes = list(read_csv(RESULTS / "outward_contour_nodes.csv"))
            if (RESULTS / "longdouble_crosscheck.csv").exists():
                crosschecks = list(read_csv(RESULTS / "longdouble_crosscheck.csv"))
        completed = {float(row["sigma"]) for row in summaries}
        order = {float(value): index for index, value in enumerate(DEFAULT_SIGMAS)}
        for sigma in arguments.sigmas:
            value = float(sigma)
            if value in completed:
                print(f"reuse completed sigma={value:g}", flush=True)
                continue
            summary, scale_nodes, scale_crosschecks = audit_scale(
                value,
                settings[value],
                previous_nodes,
                lower_bounds[value],
                perform_crosscheck=(
                    value == float(DEFAULT_SIGMAS[0])
                    and not arguments.skip_crosscheck
                ),
            )
            summaries.append(summary)
            nodes.extend(scale_nodes)
            crosschecks.extend(scale_crosschecks)
            completed.add(value)
            summaries.sort(key=lambda row: order[float(row["sigma"])])
            nodes.sort(
                key=lambda row: (
                    order[float(row["sigma"])],
                    int(float(row["node"])),
                )
            )
            write_csv(RESULTS / "outward_scale_summary.csv", summaries)
            write_csv(RESULTS / "outward_contour_nodes.csv", nodes)
            if crosschecks:
                write_csv(RESULTS / "longdouble_crosscheck.csv", crosschecks)
    regenerate()
    summaries = read_csv(RESULTS / "outward_scale_summary.csv")
    crosschecks = (
        read_csv(RESULTS / "longdouble_crosscheck.csv")
        if (RESULTS / "longdouble_crosscheck.csv").exists()
        else []
    )
    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "unit_roundoff": 2.0 ** -53,
        "sigmas": [float(row["sigma"]) for row in summaries],
        "contour_nodes": CONTOUR_NODES,
        "all_enclosed_center_windings": [
            int(float(row["enclosed_center_winding_integer"]))
            for row in summaries
        ],
        "maximum_correction_rouche_ratio_upper": max(
            float(row["maximum_correction_rouche_ratio_upper"])
            for row in summaries
        ),
        "minimum_resolvent_budget_lower": min(
            float(row["minimum_resolvent_budget_lower"]) for row in summaries
        ),
        "minimum_budget_retention_fraction": min(
            float(row["minimum_budget_retention_fraction"])
            for row in summaries
        ),
        "minimum_budget_to_rh23_lower_bound": min(
            float(row["minimum_budget_to_rh23_lower_bound"])
            for row in summaries
        ),
        "maximum_residual_inflation": max(
            max(
                float(row["maximum_primal_residual_inflation"]),
                float(row["maximum_dual_residual_inflation"]),
            )
            for row in summaries
        ),
        "maximum_longdouble_ball_utilization": max(
            (
                max(
                    float(value)
                    for key, value in row.items()
                    if key.endswith("_ball_utilization")
                )
                for row in crosschecks
            ),
            default=float("nan"),
        ),
        "source_hashes": {
            "audit.py": source_hash(Path(__file__)),
            "enclosures.py": source_hash(
                ROOT / "src" / "outward_residuals" / "enclosures.py"
            ),
            "factor_graph.py": source_hash(
                ROOT / "src" / "outward_residuals" / "factor_graph.py"
            ),
            "crosscheck.py": source_hash(
                ROOT / "src" / "outward_residuals" / "crosscheck.py"
            ),
        },
        "input_hashes": {
            "rh23_physical_eigenmode_closure.csv": source_hash(
                RH23 / "results" / "physical_eigenmode_closure.csv"
            ),
            "rh26_primal_dual_scale_summary.csv": source_hash(
                RH26 / "results" / "primal_dual_scale_summary.csv"
            ),
            "rh26_primal_dual_contour_nodes.csv": source_hash(
                RH26 / "results" / "primal_dual_contour_nodes.csv"
            ),
        },
    }
    with (RESULTS / "outward_metadata.json").open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated outward-rounded residual audit", flush=True)


if __name__ == "__main__":
    main()
