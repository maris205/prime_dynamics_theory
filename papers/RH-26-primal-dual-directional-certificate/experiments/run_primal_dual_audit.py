"""Seven-scale primal-dual residual-squaring audit on the RH-25 contours."""

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
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_directional_closure_audit as rh25  # noqa: E402
import run_global_resolvent_probe as global_probe  # noqa: E402
from contour_feshbach import build_batched_arnoldi_feshbach  # noqa: E402
from directional_rouche import determinant_winding, fom_external_solution  # noqa: E402
from primal_dual_certificate import (  # noqa: E402
    primal_dual_correction_from_residuals,
)


DEFAULT_SIGMAS = rh24.DEFAULT_SIGMAS
CONTOUR_NODES = 32


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


def rh25_summaries() -> dict[float, dict[str, str]]:
    return {
        float(row["sigma"]): row
        for row in read_csv(RH25 / "results" / "directional_scale_summary.csv")
    }


def rh23_resolvent_lower_bounds() -> dict[float, float]:
    return {
        float(row["sigma"]): float(row["external_resolvent_lower_bound"])
        for row in read_csv(RH23 / "results" / "physical_eigenmode_closure.csv")
    }


def attach_adjoint_environment(data: dict[str, object]) -> dict[str, object]:
    return global_probe.add_adjoint_actions(
        {
            "matrix": data["matrix"],
            "spectrum": data["spectrum"],
            "synthesis": np.asarray(data["pair"].synthesis),
            "analysis": np.asarray(data["pair"].analysis),
            "forcing": data["forcing"],
            "reduced": data["reduced"],
            "external_action": data["external_action"],
            "observation": data["observation"],
        }
    )


def build_dual_arnoldi(environment: dict[str, object], steps: int):
    observation = np.asarray(environment["observation_matrix"])
    dual_rhs = observation.conj().T
    rank = observation.shape[0]
    counter = 0

    def observed_adjoint(values):
        nonlocal counter
        counter += 1
        if counter == 1 or counter % 10 == 0 or counter == int(steps):
            print(f"  dual Arnoldi {counter}/{steps}", flush=True)
        return (
            environment["external_action_adjoint"](values),
            np.zeros((rank, rank), dtype=np.complex128),
        )

    begun = time.time()
    model = build_batched_arnoldi_feshbach(
        observed_adjoint,
        dual_rhs,
        np.zeros((rank, rank), dtype=np.complex128),
        steps=int(steps),
        reorthogonalizations=2,
        retain_bases=True,
    )
    return model, dual_rhs, time.time() - begun


def contour_points(sigma: float) -> tuple[np.ndarray, np.ndarray]:
    baseline = rh25.baseline_rows()[float(sigma)]
    center = complex(
        float(baseline["direct_center_real"]),
        float(baseline["direct_center_imag"]),
    )
    radius = float(baseline["selected_contour_radius"])
    theta = 2.0 * np.pi * np.arange(CONTOUR_NODES) / CONTOUR_NODES
    return theta, center + radius * np.exp(1.0j * theta)


def true_primal_residual(data, solution: np.ndarray, zeta: complex) -> np.ndarray:
    return np.asarray(data["forcing"]) - (
        zeta * solution - data["external_action"](solution)
    )


def true_dual_residual(
    environment, dual_rhs: np.ndarray, solution: np.ndarray, zeta: complex
) -> np.ndarray:
    return dual_rhs - (
        np.conj(zeta) * solution
        - environment["external_action_adjoint"](solution)
    )


def audit_scale(
    sigma: float,
    setting: dict[str, int],
    rh25_summary: dict[str, str],
    rh23_lower_bound: float,
):
    print(
        f"primal-dual audit sigma={sigma:g}, n={setting['dimension']}",
        flush=True,
    )
    data = rh25.build_physical_extended_model(float(sigma), setting)
    environment = attach_adjoint_environment(data)
    model = data["model"]
    base_depth = int(data["base_depth"])
    middle_depth = base_depth + rh25.HALF_EXTENSION
    maximum_depth = int(data["maximum_depth"])
    dual_model, dual_rhs, dual_seconds = build_dual_arnoldi(
        environment, maximum_depth
    )
    observation = np.asarray(environment["observation_matrix"])
    forcing_norm = float(np.linalg.norm(data["forcing"]))
    dual_rhs_norm = float(np.linalg.norm(dual_rhs))
    theta, points = contour_points(float(sigma))
    dual_depths = (base_depth, middle_depth, maximum_depth)
    node_rows: list[dict[str, object]] = []
    phases = {depth: [] for depth in dual_depths}
    for node, (angle, zeta) in enumerate(zip(theta, points)):
        base_evaluation = model.evaluate(zeta, depth=base_depth)
        deep_evaluation = model.evaluate(zeta, depth=maximum_depth)
        base_solution = fom_external_solution(model, zeta, depth=base_depth)
        deep_solution = fom_external_solution(model, zeta, depth=maximum_depth)
        primal_increment = deep_solution - base_solution
        deep_residual = true_primal_residual(data, deep_solution, zeta)
        expected_primal_correction = (
            deep_evaluation.feshbach - base_evaluation.feshbach
        )
        reconstruction_defect = float(
            np.linalg.norm(
                -observation @ primal_increment - expected_primal_correction,
                2,
            )
        )
        for dual_depth in dual_depths:
            dual_solution = fom_external_solution(
                dual_model, np.conj(zeta), depth=dual_depth
            )
            dual_residual = true_dual_residual(
                environment, dual_rhs, dual_solution, zeta
            )
            result = primal_dual_correction_from_residuals(
                observation,
                base_evaluation.feshbach,
                primal_increment,
                deep_residual,
                dual_solution,
                dual_residual,
            )
            corrected = base_evaluation.feshbach + result.computed_correction
            sign, _ = np.linalg.slogdet(corrected)
            phases[dual_depth].append(float(np.angle(sign)))
            gain = (
                result.primal_dual_resolvent_budget
                / result.one_sided_resolvent_budget
                if result.one_sided_resolvent_budget > 0.0
                else 0.0
            )
            node_rows.append(
                {
                    "sigma": sigma,
                    "node": node,
                    "theta": angle,
                    "z_real": zeta.real,
                    "z_imag": zeta.imag,
                    "base_depth": base_depth,
                    "primal_depth": maximum_depth,
                    "dual_depth": dual_depth,
                    "primal_rouche_ratio": result.primal_rouche_ratio,
                    "dual_weighted_rouche_ratio": result.dual_weighted_rouche_ratio,
                    "computed_primal_dual_rouche_ratio": result.computed_rouche_ratio,
                    "deep_primal_residual_to_forcing": float(
                        np.linalg.norm(deep_residual) / forcing_norm
                    ),
                    "dual_residual_to_rhs": float(
                        np.linalg.norm(dual_residual) / dual_rhs_norm
                    ),
                    "one_sided_resolvent_coefficient": result.one_sided_resolvent_coefficient,
                    "primal_dual_resolvent_coefficient": result.primal_dual_resolvent_coefficient,
                    "one_sided_resolvent_budget": result.one_sided_resolvent_budget,
                    "primal_dual_resolvent_budget": result.primal_dual_resolvent_budget,
                    "budget_gain_factor": gain,
                    "primal_correction_reconstruction_defect": reconstruction_defect,
                    "corrected_feshbach_smallest_singular": float(
                        np.linalg.svd(corrected, compute_uv=False)[-1]
                    ),
                    "corrected_determinant_phase": phases[dual_depth][-1],
                }
            )
        if node % 8 == 0:
            selected = node_rows[-1]
            print(
                f"  node {node}/{CONTOUR_NODES}: "
                f"eta={selected['computed_primal_dual_rouche_ratio']:.3e}, "
                f"M*={selected['primal_dual_resolvent_budget']:.3e}",
                flush=True,
            )

    winding = {
        depth: determinant_winding(np.asarray(values))
        for depth, values in phases.items()
    }
    deepest = [
        row for row in node_rows if int(row["dual_depth"]) == maximum_depth
    ]
    by_depth = {
        depth: [row for row in node_rows if int(row["dual_depth"]) == depth]
        for depth in dual_depths
    }
    summary: dict[str, object] = {
        "sigma": sigma,
        "folded_dimension": int(setting["dimension"]),
        "packet_rank": model.packet_rank,
        "base_depth": base_depth,
        "primal_depth": maximum_depth,
        "dual_base_depth": base_depth,
        "dual_middle_depth": middle_depth,
        "dual_maximum_depth": maximum_depth,
        "contour_nodes": CONTOUR_NODES,
        "deep_dual_winding_float": winding[maximum_depth][0],
        "deep_dual_winding_integer": winding[maximum_depth][1],
        "deep_dual_maximum_phase_increment": winding[maximum_depth][2],
        "maximum_primal_rouche_ratio": max(
            float(row["primal_rouche_ratio"]) for row in deepest
        ),
        "maximum_dual_weighted_rouche_ratio": max(
            float(row["dual_weighted_rouche_ratio"]) for row in deepest
        ),
        "maximum_computed_primal_dual_rouche_ratio": max(
            float(row["computed_primal_dual_rouche_ratio"])
            for row in deepest
        ),
        "maximum_deep_primal_residual_to_forcing": max(
            float(row["deep_primal_residual_to_forcing"]) for row in deepest
        ),
        "maximum_deep_dual_residual_to_rhs": max(
            float(row["dual_residual_to_rhs"]) for row in deepest
        ),
        "minimum_one_sided_resolvent_budget": min(
            float(row["one_sided_resolvent_budget"]) for row in deepest
        ),
        "minimum_primal_dual_resolvent_budget": min(
            float(row["primal_dual_resolvent_budget"]) for row in deepest
        ),
        "minimum_budget_gain_factor": min(
            float(row["budget_gain_factor"]) for row in deepest
        ),
        "maximum_budget_gain_factor": max(
            float(row["budget_gain_factor"]) for row in deepest
        ),
        "rh23_eigenmode_resolvent_lower_bound": rh23_lower_bound,
        "minimum_budget_to_rh23_lower_bound": min(
            float(row["primal_dual_resolvent_budget"]) for row in deepest
        )
        / float(rh23_lower_bound),
        "maximum_primal_correction_reconstruction_defect": max(
            float(row["primal_correction_reconstruction_defect"])
            for row in deepest
        ),
        "minimum_corrected_feshbach_singular": min(
            float(row["corrected_feshbach_smallest_singular"])
            for row in deepest
        ),
        "rh25_direct_correction_rouche_ratio": float(
            rh25_summary["direct_correction_rouche_ratio"]
        ),
        "primal_arnoldi_seconds": float(data["build_seconds"]),
        "dual_arnoldi_seconds": dual_seconds,
        "external_adjoint_defect": global_probe.adjoint_defect(environment),
    }
    for label, depth in zip(("base", "middle", "maximum"), dual_depths):
        summary[f"minimum_budget_dual_{label}_depth"] = min(
            float(row["primal_dual_resolvent_budget"])
            for row in by_depth[depth]
        )
        summary[f"maximum_dual_residual_dual_{label}_depth"] = max(
            float(row["dual_residual_to_rhs"]) for row in by_depth[depth]
        )

    del data, environment, dual_model
    rh24.release_memory()
    return summary, node_rows


def plot_summary(rows: list[dict[str, str]]) -> None:
    ordered = sorted(rows, key=lambda row: float(row["sigma"]), reverse=True)
    sigma = np.asarray([float(row["sigma"]) for row in ordered])
    primal = np.asarray(
        [float(row["maximum_primal_rouche_ratio"]) for row in ordered]
    )
    primal_dual = np.asarray(
        [float(row["maximum_computed_primal_dual_rouche_ratio"]) for row in ordered]
    )
    direct = np.asarray(
        [float(row["rh25_direct_correction_rouche_ratio"]) for row in ordered]
    )
    one_budget = np.asarray(
        [float(row["minimum_one_sided_resolvent_budget"]) for row in ordered]
    )
    dual_budget = np.asarray(
        [float(row["minimum_primal_dual_resolvent_budget"]) for row in ordered]
    )
    lower = np.asarray(
        [float(row["rh23_eigenmode_resolvent_lower_bound"]) for row in ordered]
    )
    primal_residual = np.asarray(
        [float(row["maximum_deep_primal_residual_to_forcing"]) for row in ordered]
    )
    dual_residual = np.asarray(
        [float(row["maximum_deep_dual_residual_to_rhs"]) for row in ordered]
    )
    gain = np.asarray(
        [float(row["minimum_budget_gain_factor"]) for row in ordered]
    )

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    axes[0, 0].loglog(sigma, primal, "o-", label="deep primal correction")
    axes[0, 0].loglog(sigma, primal_dual, "s--", label="primal-dual correction")
    axes[0, 0].loglog(
        sigma,
        np.where(direct > 0.0, direct, np.nan),
        "^:",
        label="RH-25 direct correction",
    )
    axes[0, 0].axhline(1.0, color="0.4", lw=0.8)
    axes[0, 0].set(ylabel="maximum Rouché ratio", title="Computed correction")
    axes[0, 0].legend(frameon=False, fontsize=8)

    axes[0, 1].loglog(sigma, one_budget, "o-", label="one-sided budget")
    axes[0, 1].loglog(sigma, dual_budget, "s--", label="primal-dual budget")
    axes[0, 1].loglog(sigma, lower, "^:", label="RH-23 lower bound")
    axes[0, 1].set(
        ylabel=r"admissible resolvent scale $M_*$",
        title="Residual squaring enlarges the budget",
    )
    axes[0, 1].legend(frameon=False, fontsize=8)

    axes[1, 0].loglog(sigma, primal_residual, "o-", label="deep primal residual")
    axes[1, 0].loglog(sigma, dual_residual, "s--", label="deep dual residual")
    axes[1, 0].set(ylabel="relative true residual", title="Two residual factors")
    axes[1, 0].legend(frameon=False, fontsize=8)

    axes[1, 1].loglog(sigma, gain, "o-", color="#6b3fa0")
    axes[1, 1].set(
        ylabel="minimum budget gain factor",
        title="Gain from the adjoint residual",
    )
    for axis in axes.flat:
        axis.set_xlabel(r"noise $\sigma$")
        axis.invert_xaxis()
        axis.grid(alpha=0.2, which="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "primal_dual_summary.pdf")
    fig.savefig(FIGURES / "primal_dual_summary.png", dpi=220)
    plt.close(fig)


def plot_contours(rows: list[dict[str, str]]) -> None:
    selected_sigmas = (1.0e-3, 2.0e-4, 1.0e-4)
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.8))
    for axis, sigma in zip(axes, selected_sigmas):
        available_depths = [
            int(row["dual_depth"])
            for row in rows
            if float(row["sigma"]) == sigma
        ]
        if not available_depths:
            continue
        depth = max(available_depths)
        selected = sorted(
            [
                row
                for row in rows
                if float(row["sigma"]) == sigma
                and int(row["dual_depth"]) == depth
            ],
            key=lambda row: int(row["node"]),
        )
        theta = np.asarray([float(row["theta"]) for row in selected])
        one = np.asarray(
            [float(row["one_sided_resolvent_budget"]) for row in selected]
        )
        dual = np.asarray(
            [float(row["primal_dual_resolvent_budget"]) for row in selected]
        )
        axis.semilogy(theta, one, "o-", ms=3, label="one-sided")
        axis.semilogy(theta, dual, "s--", ms=3, label="primal-dual")
        axis.set(
            xlabel=r"contour angle $\theta$",
            ylabel=r"resolvent budget $M_*$",
            title=rf"$\sigma={sigma:.0e}$",
        )
        axis.grid(alpha=0.2, which="both")
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "primal_dual_contour_budgets.pdf")
    fig.savefig(FIGURES / "primal_dual_contour_budgets.png", dpi=220)
    plt.close(fig)


def regenerate() -> None:
    summaries = read_csv(RESULTS / "primal_dual_scale_summary.csv")
    nodes = read_csv(RESULTS / "primal_dual_contour_nodes.csv")
    plot_summary(summaries)
    available = {float(row["sigma"]) for row in nodes}
    if {1.0e-3, 2.0e-4, 1.0e-4}.issubset(available):
        plot_contours(nodes)


def normalize_legacy_depth_fields(row: dict[str, str]) -> dict[str, object]:
    """Normalize single-scale prototype rows written with depth-valued keys."""

    normalized: dict[str, object] = {
        key: value
        for key, value in row.items()
        if not key.startswith("minimum_budget_dual_depth_")
        and not key.startswith("maximum_dual_residual_dual_depth_")
    }
    depths = {
        "base": int(float(row["dual_base_depth"])),
        "middle": int(float(row["dual_middle_depth"])),
        "maximum": int(float(row["dual_maximum_depth"])),
    }
    for label, depth in depths.items():
        normalized[f"minimum_budget_dual_{label}_depth"] = row.get(
            f"minimum_budget_dual_depth_{depth}",
            row.get(f"minimum_budget_dual_{label}_depth", ""),
        )
        normalized[f"maximum_dual_residual_dual_{label}_depth"] = row.get(
            f"maximum_dual_residual_dual_depth_{depth}",
            row.get(f"maximum_dual_residual_dual_{label}_depth", ""),
        )
    return normalized


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigmas", nargs="*", type=float, default=list(DEFAULT_SIGMAS))
    parser.add_argument("--reuse", action="store_true")
    parser.add_argument("--resume", action="store_true")
    arguments = parser.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    if not arguments.reuse:
        settings = rh24.physical_settings()
        previous = rh25_summaries()
        lower_bounds = rh23_resolvent_lower_bounds()
        summaries: list[dict[str, object]] = []
        nodes: list[dict[str, object]] = []
        if arguments.resume and (RESULTS / "primal_dual_scale_summary.csv").exists():
            summaries = [
                normalize_legacy_depth_fields(row)
                for row in read_csv(RESULTS / "primal_dual_scale_summary.csv")
            ]
            nodes = list(read_csv(RESULTS / "primal_dual_contour_nodes.csv"))
        completed = {float(row["sigma"]) for row in summaries}
        order = {float(value): index for index, value in enumerate(DEFAULT_SIGMAS)}
        for sigma in arguments.sigmas:
            value = float(sigma)
            if value in completed:
                print(f"reuse completed sigma={value:g}", flush=True)
                continue
            summary, scale_nodes = audit_scale(
                value,
                settings[value],
                previous[value],
                lower_bounds[value],
            )
            summaries.append(summary)
            nodes.extend(scale_nodes)
            completed.add(value)
            summaries.sort(key=lambda row: order[float(row["sigma"])])
            nodes.sort(
                key=lambda row: (
                    order[float(row["sigma"])],
                    int(float(row["node"])),
                    int(float(row["dual_depth"])),
                )
            )
            write_csv(
                RESULTS / "primal_dual_scale_summary.csv",
                summaries,
            )
            write_csv(
                RESULTS / "primal_dual_contour_nodes.csv",
                nodes,
            )
    regenerate()
    summaries = read_csv(RESULTS / "primal_dual_scale_summary.csv")
    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "sigmas": [float(row["sigma"]) for row in summaries],
        "contour_nodes": CONTOUR_NODES,
        "all_corrected_windings": [
            int(float(row["deep_dual_winding_integer"])) for row in summaries
        ],
        "maximum_computed_primal_dual_rouche_ratio": max(
            float(row["maximum_computed_primal_dual_rouche_ratio"])
            for row in summaries
        ),
        "minimum_one_sided_resolvent_budget": min(
            float(row["minimum_one_sided_resolvent_budget"])
            for row in summaries
        ),
        "minimum_primal_dual_resolvent_budget": min(
            float(row["minimum_primal_dual_resolvent_budget"])
            for row in summaries
        ),
        "minimum_budget_gain_factor": min(
            float(row["minimum_budget_gain_factor"]) for row in summaries
        ),
        "maximum_dual_depth_budget_relative_spread": max(
            max(
                float(row["minimum_budget_dual_base_depth"]),
                float(row["minimum_budget_dual_middle_depth"]),
                float(row["minimum_budget_dual_maximum_depth"]),
            )
            / min(
                float(row["minimum_budget_dual_base_depth"]),
                float(row["minimum_budget_dual_middle_depth"]),
                float(row["minimum_budget_dual_maximum_depth"]),
            )
            - 1.0
            for row in summaries
        ),
        "source_hashes": {
            "audit.py": source_hash(Path(__file__)),
            "algebra.py": source_hash(
                ROOT / "src" / "primal_dual_certificate" / "algebra.py"
            ),
            "rh25_directional_audit.py": source_hash(
                RH25 / "experiments" / "run_directional_closure_audit.py"
            ),
            "rh25_global_probe.py": source_hash(
                RH25 / "experiments" / "run_global_resolvent_probe.py"
            ),
        },
        "input_hashes": {
            "rh23_physical_eigenmode_closure.csv": source_hash(
                RH23 / "results" / "physical_eigenmode_closure.csv"
            ),
            "rh24_scale_summary.csv": source_hash(
                RH24 / "results" / "scale_summary.csv"
            ),
            "rh25_directional_scale_summary.csv": source_hash(
                RH25 / "results" / "directional_scale_summary.csv"
            ),
        },
    }
    with (RESULTS / "primal_dual_metadata.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated primal-dual directional audit", flush=True)


if __name__ == "__main__":
    main()
