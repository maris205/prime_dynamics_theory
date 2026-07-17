"""Audit a tightened A2048 atlas and propagate it to the A4096 resolvent."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH33 = PAPERS / "RH-33-certified-complement-resolvent-atlas"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH27 / "src"),
    str(RH28 / "src"),
    str(RH33 / "src"),
]

from arcwise_feshbach import (  # noqa: E402
    bisect_circular_arc_disc,
    fractional_circular_arc_disc,
)
from iterated_grid import propagate_resolvent_bound  # noqa: E402
from resolvent_atlas import (  # noqa: E402
    certify_arc_coverage,
    contour_point,
    merge_circular_gap_components,
    turn_center_id,
)


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_partition_verified(records: list[dict[str, object]]) -> bool:
    intervals = sorted(
        (
            Fraction(int(row["start_numerator"]), int(row["turn_denominator"])),
            Fraction(int(row["end_numerator"]), int(row["turn_denominator"])),
        )
        for row in records
    )
    if not intervals or intervals[0][0] != 0 or intervals[-1][1] != 1:
        return False
    return all(left[1] == right[0] for left, right in zip(intervals, intervals[1:]))


def archived_centers() -> tuple[list[dict[str, object]], int, int]:
    directories = [
        ("inherited", RH36 / "results" / "physical_centers_sigma_1e-02"),
        ("additional", ROOT / "results" / "physical_centers_sigma_1e-02"),
    ]
    rows: dict[str, dict[str, object]] = {}
    origins: dict[str, str] = {}
    for origin, directory in directories:
        for path in sorted(directory.glob("*.json")):
            record = load(path)
            if record.get("status") == "rigorous_physical_resolvent_center":
                rows[str(record["center_id"])] = record
                origins[str(record["center_id"])] = origin
    inherited_count = sum(origin == "inherited" for origin in origins.values())
    additional_count = sum(origin == "additional" for origin in origins.values())
    return list(rows.values()), inherited_count, additional_count


def second_epsilon(path: Path | None) -> float | None:
    if path is None:
        return None
    record = load(path)
    return float(record["continuation_gate"]["effective_perturbation_upper"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-arcs", type=int, default=64)
    parser.add_argument("--max-extra-refinement", type=int, default=14)
    parser.add_argument("--first-product-limit", type=float, default=0.75)
    parser.add_argument("--second-product-limit", type=float, default=1.0)
    parser.add_argument("--second-block-certificate", type=Path)
    arguments = parser.parse_args()

    first_block_path = (
        RH36 / "results" / "nested_block_certificate_sigma_1e-02.json"
    )
    first_block = load(first_block_path)
    first_gate = first_block["continuation_gate"]
    center = complex(
        float(first_block["contour_center_real"]),
        float(first_block["contour_center_imag"]),
    )
    radius = float(first_block["contour_radius"])
    epsilon_one = float(first_gate["effective_perturbation_upper"])
    first_limit = float(arguments.first_product_limit)
    second_limit = float(arguments.second_product_limit)
    if not 0.0 < first_limit < 1.0:
        raise ValueError("first product limit must lie in (0,1)")
    if not 0.0 < second_limit <= 1.0:
        raise ValueError("second product limit must lie in (0,1]")
    coarse_budget = float(np.nextafter(first_limit / epsilon_one, -np.inf))
    second_path = arguments.second_block_certificate
    if second_path is not None and not second_path.is_absolute():
        second_path = ROOT / second_path
    epsilon_two = second_epsilon(second_path)
    centers, inherited_center_count, additional_center_count = archived_centers()
    if not centers:
        raise RuntimeError("no rigorous A2048 resolvent centers are available")

    closed_leaves: list[dict[str, object]] = []
    unresolved_leaves: list[dict[str, object]] = []
    base_count = int(arguments.base_arcs)
    for parent in range(base_count):
        root = fractional_circular_arc_disc(
            center,
            radius,
            parent,
            parent + 1,
            base_count,
            index=parent,
            refinement_level=0,
        )
        pending = [root]
        while pending:
            arc = pending.pop()
            target = {
                "arc": str(parent),
                "center_real": repr(arc.center.real),
                "center_imag": repr(arc.center.imag),
                "disc_radius": repr(arc.radius),
                "resolvent_budget_lower": repr(coarse_budget),
            }
            winner = None
            winner_result = None
            winner_bound = None
            winner_propagated = None
            for source in centers:
                point = complex(
                    float(source["spectral_parameter_real"]),
                    float(source["spectral_parameter_imag"]),
                )
                coverage = certify_arc_coverage(
                    point,
                    float(source["center_inverse_two_norm_upper"]),
                    target,
                )
                if not coverage.closed:
                    continue
                propagated = propagate_resolvent_bound(
                    float(coverage.transported_inverse_upper),
                    first_effective_perturbation_upper=epsilon_one,
                    first_detail_resolvent_upper=float(
                        first_gate["detail_resolvent_upper"]
                    ),
                    first_coarse_to_detail_upper=float(
                        first_gate["coarse_to_detail_upper"]
                    ),
                    first_detail_to_coarse_upper=float(
                        first_gate["detail_to_coarse_upper"]
                    ),
                    second_effective_perturbation_upper=epsilon_two,
                )
                closes_second = bool(
                    propagated.second_continuation_product_upper is None
                    or propagated.second_continuation_product_upper < second_limit
                )
                if closes_second and (
                    winner_bound is None
                    or propagated.fine_resolvent_upper < winner_bound
                ):
                    winner = source
                    winner_result = coverage
                    winner_bound = propagated.fine_resolvent_upper
                    winner_propagated = propagated

            record: dict[str, object] = {
                "parent_arc": parent,
                "start_numerator": int(arc.start_numerator),
                "end_numerator": int(arc.end_numerator),
                "turn_denominator": int(arc.turn_denominator),
                "refinement_level": int(arc.refinement_level),
                "theta_start": 2.0
                * math.pi
                * int(arc.start_numerator)
                / int(arc.turn_denominator),
                "theta_end": 2.0
                * math.pi
                * int(arc.end_numerator)
                / int(arc.turn_denominator),
                "theta_midpoint": arc.angle,
                "center_real": arc.center.real,
                "center_imag": arc.center.imag,
                "disc_radius": arc.radius,
            }
            if winner is not None:
                record.update(
                    {
                        "status": "closed",
                        "center_id": winner["center_id"],
                        "center_inverse_upper": float(
                            winner["center_inverse_two_norm_upper"]
                        ),
                        "distance_upper": winner_result.distance_upper,
                        "neumann_product_upper": (
                            winner_result.neumann_product_upper
                        ),
                        "transported_coarse_resolvent_upper": (
                            winner_result.transported_inverse_upper
                        ),
                        **asdict(winner_propagated),
                    }
                )
                closed_leaves.append(record)
            elif int(arc.refinement_level) >= int(arguments.max_extra_refinement):
                record["status"] = "unresolved"
                unresolved_leaves.append(record)
            else:
                left, right = bisect_circular_arc_disc(
                    arc, center, radius, first_index=0
                )
                pending.append(right)
                pending.append(left)

    components = merge_circular_gap_components(unresolved_leaves)
    suggested = []
    component_payloads = []
    for index, component in enumerate(components):
        turn = component.midpoint_turn
        point = contour_point(center, radius, turn)
        identifier = turn_center_id(turn)
        suggested.append(
            {
                "center_id": identifier,
                "source_kind": "iterated_atlas_unresolved_midpoint",
                "turn_numerator": int(turn.numerator),
                "turn_denominator": int(turn.denominator),
                "spectral_parameter_real": point.real,
                "spectral_parameter_imag": point.imag,
            }
        )
        component_payloads.append(
            {
                "component": index,
                "leaf_count": component.leaf_count,
                "start_numerator": int(component.start_turn.numerator),
                "start_denominator": int(component.start_turn.denominator),
                "end_numerator": int(component.end_turn.numerator),
                "end_denominator": int(component.end_turn.denominator),
                "midpoint_numerator": int(turn.numerator),
                "midpoint_denominator": int(turn.denominator),
                "angular_length": 2.0 * math.pi * float(component.length_turns),
                "center_id": identifier,
            }
        )

    all_leaves = sorted(
        [*closed_leaves, *unresolved_leaves],
        key=lambda row: Fraction(
            int(row["start_numerator"]), int(row["turn_denominator"])
        ),
    )
    results = ROOT / "results"
    results.mkdir(parents=True, exist_ok=True)
    ledger_path = results / "propagated_resolvent_atlas_leaves.csv"
    fields = [
        "status",
        "parent_arc",
        "start_numerator",
        "end_numerator",
        "turn_denominator",
        "refinement_level",
        "theta_start",
        "theta_end",
        "theta_midpoint",
        "center_real",
        "center_imag",
        "disc_radius",
        "center_id",
        "center_inverse_upper",
        "distance_upper",
        "neumann_product_upper",
        "transported_coarse_resolvent_upper",
        "first_effective_product_upper",
        "first_effective_resolvent_upper",
        "column_factor_upper",
        "row_factor_upper",
        "fine_resolvent_upper",
        "second_effective_perturbation_upper",
        "second_continuation_product_upper",
    ]
    with ledger_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(all_leaves)

    maximum_coarse = max(
        (
            float(row["transported_coarse_resolvent_upper"])
            for row in closed_leaves
        ),
        default=None,
    )
    maximum_first = max(
        (float(row["first_effective_product_upper"]) for row in closed_leaves),
        default=None,
    )
    maximum_fine = max(
        (float(row["fine_resolvent_upper"]) for row in closed_leaves),
        default=None,
    )
    second_values = [
        float(row["second_continuation_product_upper"])
        for row in closed_leaves
        if row.get("second_continuation_product_upper") is not None
    ]
    maximum_second = max(second_values, default=None)
    payload = {
        "status": (
            "full_iterated_propagated_resolvent_atlas"
            if not unresolved_leaves
            else "partial_iterated_propagated_resolvent_atlas"
        ),
        "evidence_level": "rigorous_inherited_centers_and_outward_propagation",
        "sigma": float(first_block["sigma"]),
        "base_dimension": int(first_block["coarse_dimension"]),
        "propagated_dimension": int(first_block["fine_dimension"]),
        "target_dimension": 2 * int(first_block["fine_dimension"]),
        "inherited_first_block_certificate": str(first_block_path),
        "inherited_first_block_certificate_sha256": sha256_file(first_block_path),
        "second_block_certificate": (
            str(second_path.relative_to(ROOT)) if second_path is not None else None
        ),
        "second_block_certificate_sha256": (
            sha256_file(second_path) if second_path is not None else None
        ),
        "center_count": len(centers),
        "inherited_center_count": inherited_center_count,
        "additional_center_count": additional_center_count,
        "base_arc_count": base_count,
        "closed_leaf_count": len(closed_leaves),
        "unresolved_leaf_count": len(unresolved_leaves),
        "unresolved_component_count": len(components),
        "exact_rational_partition_verified": exact_partition_verified(all_leaves),
        "maximum_refinement_level": max(
            (int(row["refinement_level"]) for row in all_leaves), default=0
        ),
        "first_effective_perturbation_upper": epsilon_one,
        "first_product_limit": first_limit,
        "coarse_resolvent_budget_lower": coarse_budget,
        "second_effective_perturbation_upper": epsilon_two,
        "second_product_limit": second_limit,
        "maximum_transported_coarse_resolvent_upper": maximum_coarse,
        "maximum_first_effective_product_upper": maximum_first,
        "maximum_propagated_fine_resolvent_upper": maximum_fine,
        "maximum_second_continuation_product_upper": maximum_second,
        "all_first_gates_closed": bool(
            maximum_first is not None and maximum_first < 1.0
        ),
        "all_second_gates_closed": (
            None
            if epsilon_two is None
            else bool(maximum_second is not None and maximum_second < second_limit)
        ),
        "leaf_ledger": str(ledger_path.relative_to(ROOT)),
        "leaf_ledger_sha256": sha256_file(ledger_path),
        "unresolved_components": component_payloads,
        "suggested_centers": suggested,
    }
    output = results / "propagated_resolvent_atlas.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
