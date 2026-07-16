"""Full-contour arcwise enclosure of the stored rational Arnoldi models."""

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
from fractions import Fraction
from multiprocessing import get_context
from pathlib import Path

import numpy as np
import scipy
import flint
import threadpoolctl
from threadpoolctl import threadpool_limits


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH26 = PAPERS / "RH-26-primal-dual-directional-certificate"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH26 / "src"),
    str(RH26 / "experiments"),
    str(RH27 / "src"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_directional_closure_audit as rh25  # noqa: E402
import run_primal_dual_audit as rh26  # noqa: E402
from arcwise_feshbach import (  # noqa: E402
    bisect_circular_arc_disc,
    build_static_arc_certificate,
    circular_arc_discs,
    evaluate_arc_budget,
)
from outward_residuals import ComponentwiseStoredFactorGraph  # noqa: E402


DEFAULT_SIGMAS = rh24.DEFAULT_SIGMAS
DEFAULT_ARCS = 64
DEFAULT_MAXIMUM_REFINEMENT = 14
DEFAULT_WORKERS = 16

_ARC_EVALUATION_CONTEXT = None


def _evaluate_arc_candidate(arc):
    """Process-pool entry point using fork-shared read-only model data."""

    if _ARC_EVALUATION_CONTEXT is None:
        raise RuntimeError("arc evaluation context is not initialized")
    primal_model, dual_model, static, base_depth, maximum_depth = (
        _ARC_EVALUATION_CONTEXT
    )
    begun = time.time()
    try:
        budget = evaluate_arc_budget(
            arc,
            primal_model,
            dual_model,
            static,
            base_depth=base_depth,
            maximum_depth=maximum_depth,
        )
        admissible = budget.correction_ratio_upper < 1.0
        failure = "correction ratio did not close"
    except RuntimeError as error:
        budget = None
        admissible = False
        failure = str(error)
    return arc, budget, admissible, failure, time.time() - begun


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def contour_parameters(sigma: float) -> tuple[complex, float]:
    row = rh25.baseline_rows()[float(sigma)]
    center = complex(
        float(row["direct_center_real"]),
        float(row["direct_center_imag"]),
    )
    return center, float(row["selected_contour_radius"])


def audit_scale(
    sigma: float,
    setting: dict[str, int],
    *,
    arc_count: int,
    maximum_refinement: int,
    workers: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    print(
        f"arcwise audit sigma={sigma:g}, n={setting['dimension']}, "
        f"arcs={arc_count}",
        flush=True,
    )
    scale_started = time.time()
    data = rh25.build_physical_extended_model(float(sigma), setting)
    environment = rh26.attach_adjoint_environment(data)
    primal_model = data["model"]
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
    static = build_static_arc_certificate(
        graph,
        blocks,
        primal_model,
        dual_model,
        base_depth=base_depth,
        maximum_depth=maximum_depth,
    )
    print(
        "  static defects: "
        f"direct={static.direct_defect_norm_upper:.3e}, "
        f"primal relation={max(row.relation_norm_upper for row in static.primal):.3e}, "
        f"dual relation={max(row.relation_norm_upper for row in static.dual):.3e}",
        flush=True,
    )
    contour_center, contour_radius = contour_parameters(float(sigma))
    initial_arcs = circular_arc_discs(
        contour_center, contour_radius, int(arc_count)
    )
    pending = list(reversed(initial_arcs))
    accepted: list[tuple[object, object, float]] = []
    attempted = 0
    subdivisions = 0
    next_index = int(arc_count)
    next_progress = 100

    worker_count = max(1, int(workers))
    global _ARC_EVALUATION_CONTEXT
    _ARC_EVALUATION_CONTEXT = (
        primal_model,
        dual_model,
        static,
        base_depth,
        maximum_depth,
    )
    fork_context = get_context("fork")
    with threadpool_limits(limits=1, user_api="blas"):
        with fork_context.Pool(processes=worker_count) as pool:
            while pending:
                batch = [
                    pending.pop()
                    for _ in range(
                        min(max(1, 4 * worker_count), len(pending))
                    )
                ]
                outcomes = pool.map(
                    _evaluate_arc_candidate, batch, chunksize=1
                )
                attempted += len(outcomes)
                for arc, budget, admissible, failure, elapsed in outcomes:
                    if admissible:
                        accepted.append((arc, budget, elapsed))
                        continue
                    if int(arc.refinement_level) >= int(maximum_refinement):
                        raise RuntimeError(
                            f"arc at theta={arc.angle:.9f} reached refinement "
                            f"level {maximum_refinement}: {failure}"
                        )
                    left, right = bisect_circular_arc_disc(
                        arc,
                        contour_center,
                        contour_radius,
                        first_index=next_index,
                    )
                    next_index += 2
                    subdivisions += 1
                    pending.append(right)
                    pending.append(left)
                while attempted >= next_progress:
                    print(
                        f"  attempted {attempted}: accepted={len(accepted)}, "
                        f"pending={len(pending)}, splits={subdivisions}",
                        flush=True,
                    )
                    next_progress += 100
    _ARC_EVALUATION_CONTEXT = None

    accepted.sort(
        key=lambda item: Fraction(
            item[0].start_numerator, item[0].turn_denominator
        )
    )
    cursor = Fraction(0, 1)
    for arc, _, _ in accepted:
        start = Fraction(arc.start_numerator, arc.turn_denominator)
        end = Fraction(arc.end_numerator, arc.turn_denominator)
        if start != cursor:
            raise RuntimeError("adaptive arc leaves do not form a partition")
        cursor = end
    if cursor != Fraction(1, 1):
        raise RuntimeError("adaptive arc cover does not reach one full turn")
    rows: list[dict[str, object]] = []
    for leaf_index, (arc, budget, arc_seconds) in enumerate(accepted):
        rows.append(
            {
                "sigma": sigma,
                "arc": leaf_index,
                "construction_index": arc.index,
                "start_numerator": arc.start_numerator,
                "end_numerator": arc.end_numerator,
                "turn_denominator": arc.turn_denominator,
                "refinement_level": arc.refinement_level,
                "theta_start": 2.0
                * np.pi
                * arc.start_numerator
                / arc.turn_denominator,
                "theta_end": 2.0
                * np.pi
                * arc.end_numerator
                / arc.turn_denominator,
                "theta_midpoint": budget.angle,
                "center_real": budget.center.real,
                "center_imag": budget.center.imag,
                "disc_radius": budget.radius,
                "base_depth": base_depth,
                "primal_depth": maximum_depth,
                "dual_depth": maximum_depth,
                "correction_ratio_upper": budget.correction_ratio_upper,
                "remainder_coefficient_upper": budget.remainder_coefficient_upper,
                "resolvent_budget_lower": budget.resolvent_budget_lower,
                "primal_residual_norm_upper": budget.primal_residual_norm_upper,
                "dual_residual_norm_upper": budget.dual_residual_norm_upper,
                "base_consistency_norm_upper": budget.base_consistency_norm_upper,
                "primal_increment_norm_upper": budget.primal_increment_norm_upper,
                "dual_solution_norm_upper": budget.dual_solution_norm_upper,
                "computed_correction_norm_upper": budget.computed_correction_norm_upper,
                "projected_inverse_norm_upper": budget.projected_inverse_norm_upper,
                "projected_family_neumann_product": budget.projected_family_neumann_product,
                "projected_center_inverse_defect": budget.projected_center_inverse_defect,
                "maximum_coordinate_contraction": budget.maximum_coordinate_contraction,
                "maximum_coordinate_iterations": budget.maximum_coordinate_iterations,
                "arc_seconds": arc_seconds,
            }
        )

    print(
        f"  accepted cover: leaves={len(rows)}, splits={subdivisions}, "
        f"max level={max(int(row['refinement_level']) for row in rows)}",
        flush=True,
    )

    summary = {
        "sigma": sigma,
        "folded_dimension": int(setting["dimension"]),
        "packet_rank": int(primal_model.packet_rank),
        "base_depth": base_depth,
        "primal_depth": maximum_depth,
        "dual_depth": maximum_depth,
        "initial_arc_count": int(arc_count),
        "arc_workers": worker_count,
        "accepted_arc_count": len(rows),
        "attempted_arc_count": attempted,
        "subdivision_count": subdivisions,
        "maximum_refinement_level": max(
            int(row["refinement_level"]) for row in rows
        ),
        "exact_dyadic_partition_verified": 1,
        "contour_center_real": contour_center.real,
        "contour_center_imag": contour_center.imag,
        "contour_radius": contour_radius,
        "maximum_arc_disc_radius": max(float(row["disc_radius"]) for row in rows),
        "maximum_correction_ratio_upper": max(
            float(row["correction_ratio_upper"]) for row in rows
        ),
        "minimum_resolvent_budget_lower": min(
            float(row["resolvent_budget_lower"]) for row in rows
        ),
        "maximum_projected_inverse_norm_upper": max(
            float(row["projected_inverse_norm_upper"]) for row in rows
        ),
        "maximum_projected_family_neumann_product": max(
            float(row["projected_family_neumann_product"]) for row in rows
        ),
        "maximum_coordinate_contraction": max(
            float(row["maximum_coordinate_contraction"]) for row in rows
        ),
        "maximum_coordinate_iterations": max(
            int(row["maximum_coordinate_iterations"]) for row in rows
        ),
        "direct_defect_norm_upper": static.direct_defect_norm_upper,
        "observation_norm_upper": static.observation_norm_upper,
        "maximum_primal_relation_norm_upper": max(
            row.relation_norm_upper for row in static.primal
        ),
        "maximum_dual_relation_norm_upper": max(
            row.relation_norm_upper for row in static.dual
        ),
        "maximum_primal_source_defect_norm_upper": max(
            row.source_defect_norm_upper for row in static.primal
        ),
        "maximum_dual_source_defect_norm_upper": max(
            row.source_defect_norm_upper for row in static.dual
        ),
        "static_certificate_seconds": static.elapsed_seconds,
        "primal_arnoldi_seconds": float(data["build_seconds"]),
        "dual_arnoldi_seconds": dual_seconds,
        "scale_seconds": time.time() - scale_started,
    }
    del data, environment, primal_model, dual_model, graph, blocks, static
    gc.collect()
    rh24.release_memory()
    return summary, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sigmas", nargs="*", type=float, default=list(DEFAULT_SIGMAS)
    )
    parser.add_argument("--arcs", type=int, default=DEFAULT_ARCS)
    parser.add_argument(
        "--maximum-refinement",
        type=int,
        default=DEFAULT_MAXIMUM_REFINEMENT,
    )
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="recompute requested scales even if resume data already exist",
    )
    arguments = parser.parse_args()
    settings = rh24.physical_settings()
    summaries: list[dict[str, object]] = []
    all_rows: list[dict[str, object]] = []
    summary_path = RESULTS / "arcwise_scale_summary.csv"
    arc_path = RESULTS / "arcwise_contour_arcs.csv"
    if (
        arguments.resume
        and not arguments.no_write
        and summary_path.exists()
        and arc_path.exists()
    ):
        summaries = list(read_csv(summary_path))
        all_rows = list(read_csv(arc_path))
        for row in summaries:
            row.setdefault("arc_workers", "1")
    if arguments.replace:
        selected = {float(value) for value in arguments.sigmas}
        summaries = [
            row for row in summaries if float(row["sigma"]) not in selected
        ]
        all_rows = [
            row for row in all_rows if float(row["sigma"]) not in selected
        ]
    completed = {float(row["sigma"]) for row in summaries}
    order = {
        float(value): index for index, value in enumerate(DEFAULT_SIGMAS)
    }
    for sigma in arguments.sigmas:
        value = float(sigma)
        if value in completed:
            print(f"reuse completed sigma={value:g}", flush=True)
            continue
        summary, rows = audit_scale(
            value,
            settings[value],
            arc_count=int(arguments.arcs),
            maximum_refinement=int(arguments.maximum_refinement),
            workers=int(arguments.workers),
        )
        summaries.append(summary)
        all_rows.extend(rows)
        completed.add(value)
        summaries.sort(key=lambda row: order.get(float(row["sigma"]), 99))
        all_rows.sort(
            key=lambda row: (
                order.get(float(row["sigma"]), 99),
                int(float(row["arc"])),
            )
        )
        if not arguments.no_write:
            write_csv(summary_path, summaries)
            write_csv(arc_path, all_rows)
        print(
            f"completed sigma={value:g}: "
            f"max eta+={summary['maximum_correction_ratio_upper']:.6e}, "
            f"min M-={summary['minimum_resolvent_budget_lower']:.6e}",
            flush=True,
        )
    if not arguments.no_write:
        metadata = {
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "python_flint": flint.__version__,
            "threadpoolctl": threadpoolctl.__version__,
            "sigmas": [float(row["sigma"]) for row in summaries],
            "initial_arc_count": int(arguments.arcs),
            "maximum_correction_ratio_upper": max(
                float(row["maximum_correction_ratio_upper"])
                for row in summaries
            ),
            "minimum_resolvent_budget_lower": min(
                float(row["minimum_resolvent_budget_lower"])
                for row in summaries
            ),
            "source_hashes": {
                "run_arcwise_enclosure.py": source_hash(Path(__file__)),
                "coordinates.py": source_hash(
                    ROOT / "src" / "arcwise_feshbach" / "coordinates.py"
                ),
                "geometry.py": source_hash(
                    ROOT / "src" / "arcwise_feshbach" / "geometry.py"
                ),
                "relations.py": source_hash(
                    ROOT / "src" / "arcwise_feshbach" / "relations.py"
                ),
                "evaluator.py": source_hash(
                    ROOT / "src" / "arcwise_feshbach" / "evaluator.py"
                ),
            },
            "input_hashes": {
                "rh24_scale_summary.csv": source_hash(
                    RH24 / "results" / "scale_summary.csv"
                ),
                "rh27_hybrid_scale_summary.csv": source_hash(
                    RH27 / "results" / "hybrid_scale_summary.csv"
                ),
            },
            "result_hashes": {
                "arcwise_scale_summary.csv": source_hash(summary_path),
                "arcwise_contour_arcs.csv": source_hash(arc_path),
            },
        }
        RESULTS.mkdir(parents=True, exist_ok=True)
        with (RESULTS / "arcwise_metadata.json").open(
            "w", encoding="utf-8"
        ) as handle:
            json.dump(metadata, handle, indent=2, sort_keys=True)
            handle.write("\n")


if __name__ == "__main__":
    main()
