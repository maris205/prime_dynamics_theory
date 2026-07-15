"""Componentwise refinement of the two finest outward-rounded scales."""

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
    ComponentwiseStoredFactorGraph,
    certify_budget,
)


DEFAULT_SIGMAS = (2.0e-4, 1.0e-4)


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


def normwise_nodes() -> dict[tuple[float, int], dict[str, str]]:
    return {
        (float(row["sigma"]), int(float(row["node"]))): row
        for row in read_csv(RESULTS / "outward_contour_nodes.csv")
    }


def audit_scale(
    sigma: float,
    setting: dict[str, int],
    normwise: dict[tuple[float, int], dict[str, str]],
):
    print(
        f"componentwise refinement sigma={sigma:g}, n={setting['dimension']}",
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
    graph = ComponentwiseStoredFactorGraph(
        data["matrix"],
        data["spectrum"]["right_modes"],
        data["spectrum"]["left_modes"],
        data["spectrum"]["peripheral_values"],
        data["pair"].synthesis,
        data["pair"].analysis,
    )
    blocks = graph.build_blocks()
    theta, points = rh26.contour_points(float(sigma))
    rows: list[dict[str, object]] = []
    phases: list[float] = []
    for node_number, (angle, zeta) in enumerate(zip(theta, points)):
        begun = time.time()
        base_evaluation = model.evaluate(zeta, depth=base_depth)
        base_solution = fom_external_solution(model, zeta, depth=base_depth)
        deep_solution = fom_external_solution(model, zeta, depth=maximum_depth)
        dual_solution = fom_external_solution(
            dual_model, np.conj(zeta), depth=maximum_depth
        )
        node = graph.node(
            blocks,
            zeta,
            base_evaluation.feshbach,
            base_solution,
            deep_solution,
            dual_solution,
        )
        primal = node.primal_residual.as_frobenius_ball()
        dual = node.dual_residual.as_frobenius_ball()
        correction = node.total_computed_correction.as_frobenius_ball()
        certificate = certify_budget(
            base_evaluation.feshbach, correction, primal, dual
        )
        prior = normwise[(float(sigma), node_number)]
        normwise_eta = float(prior["correction_rouche_ratio_upper"])
        normwise_budget = float(prior["resolvent_budget_lower"])
        corrected = base_evaluation.feshbach + correction.center
        sign, _ = np.linalg.slogdet(corrected)
        phase = float(np.angle(sign))
        phases.append(phase)
        rows.append(
            {
                "sigma": sigma,
                "node": node_number,
                "theta": angle,
                "z_real": zeta.real,
                "z_imag": zeta.imag,
                "base_depth": base_depth,
                "primal_depth": maximum_depth,
                "dual_depth": maximum_depth,
                "primal_residual_radius_frobenius": node.primal_residual.radius_frobenius_upper,
                "primal_residual_norm_upper": primal.norm_upper,
                "dual_residual_radius_frobenius": node.dual_residual.radius_frobenius_upper,
                "dual_residual_norm_upper": dual.norm_upper,
                "base_consistency_radius_frobenius": node.base_consistency.radius_frobenius_upper,
                "base_consistency_norm_upper": node.base_consistency.norm_upper,
                "total_correction_radius_frobenius": node.total_computed_correction.radius_frobenius_upper,
                "total_correction_norm_upper": correction.norm_upper,
                "correction_rouche_ratio_upper": certificate.correction_ratio_upper,
                "weighted_dual_residual_norm_upper": certificate.weighted_dual_residual_norm_upper,
                "remainder_coefficient_upper": certificate.remainder_coefficient_upper,
                "resolvent_budget_lower": certificate.resolvent_budget_lower,
                "normwise_correction_rouche_ratio_upper": normwise_eta,
                "normwise_resolvent_budget_lower": normwise_budget,
                "eta_tightening_factor": normwise_eta
                / certificate.correction_ratio_upper,
                "budget_gain_over_normwise": (
                    certificate.resolvent_budget_lower / normwise_budget
                    if normwise_budget > 0.0
                    else float("inf")
                ),
                "corrected_feshbach_smallest_singular": float(
                    np.linalg.svd(corrected, compute_uv=False)[-1]
                ),
                "corrected_determinant_phase": phase,
                "node_seconds": time.time() - begun,
            }
        )
        if node_number % 4 == 0:
            print(
                f"  node {node_number}/32: "
                f"eta+={certificate.correction_ratio_upper:.3e}, "
                f"M->={certificate.resolvent_budget_lower:.3e}",
                flush=True,
            )

    winding_float, winding_integer, phase_increment = determinant_winding(
        np.asarray(phases)
    )
    summary = {
        "sigma": sigma,
        "folded_dimension": int(setting["dimension"]),
        "packet_rank": model.packet_rank,
        "base_depth": base_depth,
        "primal_depth": maximum_depth,
        "dual_depth": maximum_depth,
        "contour_nodes": len(rows),
        "componentwise_center_winding_float": winding_float,
        "componentwise_center_winding_integer": winding_integer,
        "componentwise_center_maximum_phase_increment": phase_increment,
        "maximum_componentwise_correction_rouche_ratio_upper": max(
            float(row["correction_rouche_ratio_upper"]) for row in rows
        ),
        "minimum_componentwise_resolvent_budget_lower": min(
            float(row["resolvent_budget_lower"]) for row in rows
        ),
        "maximum_normwise_correction_rouche_ratio_upper": max(
            float(row["normwise_correction_rouche_ratio_upper"])
            for row in rows
        ),
        "minimum_normwise_resolvent_budget_lower": min(
            float(row["normwise_resolvent_budget_lower"]) for row in rows
        ),
        "minimum_eta_tightening_factor": min(
            float(row["eta_tightening_factor"]) for row in rows
        ),
        "maximum_eta_tightening_factor": max(
            float(row["eta_tightening_factor"]) for row in rows
        ),
        "minimum_positive_budget_gain_over_normwise": min(
            float(row["budget_gain_over_normwise"])
            for row in rows
            if np.isfinite(float(row["budget_gain_over_normwise"]))
        ),
        "maximum_primal_residual_norm_upper": max(
            float(row["primal_residual_norm_upper"]) for row in rows
        ),
        "maximum_dual_residual_norm_upper": max(
            float(row["dual_residual_norm_upper"]) for row in rows
        ),
        "maximum_base_consistency_norm_upper": max(
            float(row["base_consistency_norm_upper"]) for row in rows
        ),
        "minimum_corrected_feshbach_singular": min(
            float(row["corrected_feshbach_smallest_singular"])
            for row in rows
        ),
        "primal_arnoldi_seconds": float(data["build_seconds"]),
        "dual_arnoldi_seconds": dual_seconds,
    }
    del data, environment, model, dual_model, graph, blocks
    rh24.release_memory()
    return summary, rows


def plot_refinement(rows: list[dict[str, str]]) -> None:
    available = sorted({float(row["sigma"]) for row in rows}, reverse=True)
    fig, axes = plt.subplots(2, len(available), figsize=(6.0 * len(available), 7.2))
    if len(available) == 1:
        axes = np.asarray(axes)[:, None]
    for column, sigma in enumerate(available):
        selected = sorted(
            [row for row in rows if float(row["sigma"]) == sigma],
            key=lambda row: int(float(row["node"])),
        )
        theta = np.asarray([float(row["theta"]) for row in selected])
        norm_eta = np.asarray(
            [float(row["normwise_correction_rouche_ratio_upper"]) for row in selected]
        )
        component_eta = np.asarray(
            [float(row["correction_rouche_ratio_upper"]) for row in selected]
        )
        norm_budget = np.asarray(
            [float(row["normwise_resolvent_budget_lower"]) for row in selected]
        )
        component_budget = np.asarray(
            [float(row["resolvent_budget_lower"]) for row in selected]
        )
        axes[0, column].semilogy(theta, norm_eta, "o:", label="normwise")
        axes[0, column].semilogy(theta, component_eta, "s-", label="componentwise")
        axes[0, column].axhline(1.0, color="0.4", lw=0.8)
        axes[0, column].set(
            title=rf"$\sigma={sigma:.0e}$",
            ylabel=r"outward correction ratio $\eta_+$",
        )
        axes[1, column].semilogy(
            theta, np.where(norm_budget > 0.0, norm_budget, np.nan), "o:"
        )
        axes[1, column].semilogy(theta, component_budget, "s-")
        axes[1, column].set(ylabel=r"conditional budget $M_*$")
        for row in range(2):
            axes[row, column].set_xlabel(r"contour angle $\theta$")
            axes[row, column].grid(alpha=0.2, which="both")
    axes[0, 0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "componentwise_refinement.pdf")
    fig.savefig(FIGURES / "componentwise_refinement.png", dpi=220)
    plt.close(fig)


def hybrid_summary(
    componentwise: list[dict[str, str]],
) -> list[dict[str, object]]:
    """Select the successful normwise/componentwise layer at each scale."""

    refined = {float(row["sigma"]): row for row in componentwise}
    rows: list[dict[str, object]] = []
    for ordinary in read_csv(RESULTS / "outward_scale_summary.csv"):
        sigma = float(ordinary["sigma"])
        if sigma in refined:
            selected = refined[sigma]
            method = "componentwise"
            eta = float(
                selected["maximum_componentwise_correction_rouche_ratio_upper"]
            )
            budget = float(
                selected["minimum_componentwise_resolvent_budget_lower"]
            )
            winding = int(
                float(selected["componentwise_center_winding_integer"])
            )
            phase_increment = float(
                selected["componentwise_center_maximum_phase_increment"]
            )
        else:
            method = "normwise"
            eta = float(ordinary["maximum_correction_rouche_ratio_upper"])
            budget = float(ordinary["minimum_resolvent_budget_lower"])
            winding = int(float(ordinary["enclosed_center_winding_integer"]))
            phase_increment = float(
                ordinary["enclosed_center_maximum_phase_increment"]
            )
        rows.append(
            {
                "sigma": sigma,
                "folded_dimension": int(float(ordinary["folded_dimension"])),
                "packet_rank": int(float(ordinary["packet_rank"])),
                "selected_enclosure": method,
                "maximum_correction_rouche_ratio_upper": eta,
                "minimum_resolvent_budget_lower": budget,
                "center_winding_integer": winding,
                "center_maximum_phase_increment": phase_increment,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigmas", nargs="*", type=float, default=list(DEFAULT_SIGMAS))
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--reuse", action="store_true")
    arguments = parser.parse_args()
    if not arguments.reuse:
        settings = rh24.physical_settings()
        normwise = normwise_nodes()
        summaries: list[dict[str, object]] = []
        nodes: list[dict[str, object]] = []
        if arguments.resume and (RESULTS / "componentwise_scale_summary.csv").exists():
            summaries = list(read_csv(RESULTS / "componentwise_scale_summary.csv"))
            nodes = list(read_csv(RESULTS / "componentwise_contour_nodes.csv"))
        completed = {float(row["sigma"]) for row in summaries}
        order = {float(value): index for index, value in enumerate(DEFAULT_SIGMAS)}
        for sigma in arguments.sigmas:
            value = float(sigma)
            if value in completed:
                print(f"reuse completed sigma={value:g}", flush=True)
                continue
            summary, scale_nodes = audit_scale(
                value, settings[value], normwise
            )
            summaries.append(summary)
            nodes.extend(scale_nodes)
            completed.add(value)
            summaries.sort(key=lambda row: order.get(float(row["sigma"]), 99))
            nodes.sort(
                key=lambda row: (
                    order.get(float(row["sigma"]), 99),
                    int(float(row["node"])),
                )
            )
            write_csv(RESULTS / "componentwise_scale_summary.csv", summaries)
            write_csv(RESULTS / "componentwise_contour_nodes.csv", nodes)
    summaries = read_csv(RESULTS / "componentwise_scale_summary.csv")
    nodes = read_csv(RESULTS / "componentwise_contour_nodes.csv")
    plot_refinement(nodes)
    hybrid = hybrid_summary(summaries)
    write_csv(RESULTS / "hybrid_scale_summary.csv", hybrid)
    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "sigmas": [float(row["sigma"]) for row in summaries],
        "all_componentwise_center_windings": [
            int(float(row["componentwise_center_winding_integer"]))
            for row in summaries
        ],
        "maximum_componentwise_correction_rouche_ratio_upper": max(
            float(row["maximum_componentwise_correction_rouche_ratio_upper"])
            for row in summaries
        ),
        "minimum_componentwise_resolvent_budget_lower": min(
            float(row["minimum_componentwise_resolvent_budget_lower"])
            for row in summaries
        ),
        "hybrid_maximum_correction_rouche_ratio_upper": max(
            float(row["maximum_correction_rouche_ratio_upper"])
            for row in hybrid
        ),
        "hybrid_minimum_resolvent_budget_lower": min(
            float(row["minimum_resolvent_budget_lower"]) for row in hybrid
        ),
        "hybrid_all_center_windings": [
            int(row["center_winding_integer"]) for row in hybrid
        ],
        "source_hashes": {
            "refinement.py": source_hash(Path(__file__)),
            "componentwise.py": source_hash(
                ROOT / "src" / "outward_residuals" / "componentwise.py"
            ),
            "componentwise_graph.py": source_hash(
                ROOT / "src" / "outward_residuals" / "componentwise_graph.py"
            ),
        },
        "input_hashes": {
            "outward_contour_nodes.csv": source_hash(
                RESULTS / "outward_contour_nodes.csv"
            ),
            "outward_scale_summary.csv": source_hash(
                RESULTS / "outward_scale_summary.csv"
            ),
            "rh26_primal_dual_contour_nodes.csv": source_hash(
                RH26 / "results" / "primal_dual_contour_nodes.csv"
            ),
        },
    }
    with (RESULTS / "componentwise_metadata.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated componentwise outward refinement", flush=True)


if __name__ == "__main__":
    main()
