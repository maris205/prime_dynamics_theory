"""Refine RH-28 leaves until the current center atlas closes each subarc."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
sys.path[:0] = [str(ROOT / "src"), str(RH28 / "src"), str(RH27 / "src")]

from arcwise_feshbach import (  # noqa: E402
    bisect_circular_arc_disc,
    fractional_circular_arc_disc,
)
from resolvent_atlas import (  # noqa: E402
    certify_arc_coverage,
    contour_point,
    merge_circular_gap_components,
    turn_center_id,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def center_identifier(record: dict[str, object]) -> str:
    if "center_id" in record:
        return str(record["center_id"])
    return f"arc_{int(record['source_arc']):05d}"


def fraction_payload(prefix: str, value: Fraction) -> dict[str, int]:
    return {
        f"{prefix}_numerator": int(value.numerator),
        f"{prefix}_denominator": int(value.denominator),
    }


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--max-extra-refinement", type=int, default=8)
    arguments = parser.parse_args()
    sigma = float(arguments.sigma)
    scale = next(
        row
        for row in read_csv(RH28 / "results" / "arcwise_scale_summary.csv")
        if float(row["sigma"]) == sigma
    )
    contour_center = complex(
        float(scale["contour_center_real"]), float(scale["contour_center_imag"])
    )
    contour_radius = float(scale["contour_radius"])
    parents = [
        row
        for row in read_csv(RH28 / "results" / "arcwise_contour_arcs.csv")
        if float(row["sigma"]) == sigma
    ]
    center_dir = ROOT / "results" / "centers" / f"sigma_{sigma:.0e}"
    centers = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(center_dir.glob("*.json"))
    ]
    centers = [
        row for row in centers if row["status"] == "rigorous_direct_center_certificate"
    ]
    if not centers:
        raise RuntimeError("no certified atlas centers are archived")

    closed_leaves = []
    unresolved_leaves = []
    maximum_level = 0
    for parent in parents:
        original_level = int(parent["refinement_level"])
        root = fractional_circular_arc_disc(
            contour_center,
            contour_radius,
            int(parent["start_numerator"]),
            int(parent["end_numerator"]),
            int(parent["turn_denominator"]),
            index=int(parent["arc"]),
            refinement_level=original_level,
        )
        pending = [root]
        while pending:
            arc = pending.pop()
            target = {
                "arc": str(parent["arc"]),
                "center_real": repr(arc.center.real),
                "center_imag": repr(arc.center.imag),
                "disc_radius": repr(arc.radius),
                "resolvent_budget_lower": parent["resolvent_budget_lower"],
            }
            winner = None
            winner_arc = None
            winner_bound = None
            winner_result = None
            for center in centers:
                source = complex(
                    float(center["spectral_parameter_real"]),
                    float(center["spectral_parameter_imag"]),
                )
                result = certify_arc_coverage(
                    source, float(center["center_inverse_two_norm_upper"]), target
                )
                if result.closed and (
                    winner_bound is None
                    or result.transported_inverse_upper < winner_bound
                ):
                    winner = center_identifier(center)
                    winner_arc = (
                        int(center["source_arc"])
                        if "source_arc" in center
                        else None
                    )
                    winner_bound = float(result.transported_inverse_upper)
                    winner_result = result
            extra = int(arc.refinement_level) - original_level
            maximum_level = max(maximum_level, int(arc.refinement_level))
            record = {
                "parent_arc": int(parent["arc"]),
                "start_numerator": int(arc.start_numerator),
                "end_numerator": int(arc.end_numerator),
                "turn_denominator": int(arc.turn_denominator),
                "refinement_level": int(arc.refinement_level),
                "extra_refinement": extra,
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
                record["center_id"] = winner
                if winner_arc is not None:
                    record["center_arc"] = winner_arc
                record["transported_inverse_upper"] = winner_bound
                record["distance_upper"] = winner_result.distance_upper
                record["neumann_product_upper"] = (
                    winner_result.neumann_product_upper
                )
                record["budget_lower"] = winner_result.budget_lower
                record["budget_ratio_upper"] = (
                    math.nextafter(
                        winner_bound / winner_result.budget_lower, math.inf
                    )
                )
                record["status"] = "closed"
                closed_leaves.append(record)
            elif extra >= int(arguments.max_extra_refinement):
                record["status"] = "unresolved"
                unresolved_leaves.append(record)
            else:
                left, right = bisect_circular_arc_disc(
                    arc,
                    contour_center,
                    contour_radius,
                    first_index=0,
                )
                pending.append(right)
                pending.append(left)

    components = merge_circular_gap_components(unresolved_leaves)
    component_payloads = []
    suggested_centers = []
    for index, component in enumerate(components):
        midpoint = component.midpoint_turn
        point = contour_point(contour_center, contour_radius, midpoint)
        identifier = turn_center_id(midpoint)
        component_payloads.append(
            {
                "component": index,
                "leaf_count": component.leaf_count,
                "parent_arcs": list(component.parent_arcs),
                **fraction_payload("start_turn", component.start_turn),
                **fraction_payload("end_turn_unwrapped", component.end_turn),
                **fraction_payload("length_turns", component.length_turns),
                **fraction_payload("midpoint_turn", midpoint),
                "angular_length": 2.0 * math.pi * float(component.length_turns),
                "center_id": identifier,
                "center_real": point.real,
                "center_imag": point.imag,
            }
        )
        suggested_centers.append(
            {
                "center_id": identifier,
                "source_kind": "adaptive_gap_midpoint",
                "component": index,
                "parent_arcs": list(component.parent_arcs),
                **fraction_payload("turn", midpoint),
                "spectral_parameter_real": point.real,
                "spectral_parameter_imag": point.imag,
            }
        )

    all_leaves = sorted(
        [*closed_leaves, *unresolved_leaves],
        key=lambda row: Fraction(
            int(row["start_numerator"]), int(row["turn_denominator"])
        ),
    )
    ledger_fields = [
        "status",
        "parent_arc",
        "start_numerator",
        "end_numerator",
        "turn_denominator",
        "refinement_level",
        "extra_refinement",
        "theta_start",
        "theta_end",
        "theta_midpoint",
        "center_real",
        "center_imag",
        "disc_radius",
        "center_id",
        "center_arc",
        "distance_upper",
        "neumann_product_upper",
        "transported_inverse_upper",
        "budget_lower",
        "budget_ratio_upper",
    ]
    ledger_path = (
        ROOT / "results" / f"refined_atlas_sigma_{sigma:.0e}_leaves.csv"
    )
    with ledger_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=ledger_fields,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in all_leaves:
            writer.writerow(row)

    exact_partition = exact_partition_verified(all_leaves)
    closed_products = [
        float(row["neumann_product_upper"]) for row in closed_leaves
    ]
    closed_ratios = [float(row["budget_ratio_upper"]) for row in closed_leaves]
    used_centers = sorted({str(row["center_id"]) for row in closed_leaves})

    payload = {
        "status": "full_refined_atlas" if not unresolved_leaves else "partial_refined_atlas",
        "sigma": sigma,
        "center_count": len(centers),
        "parent_arc_count": len(parents),
        "closed_refined_leaf_count": len(closed_leaves),
        "unresolved_refined_leaf_count": len(unresolved_leaves),
        "exact_rational_partition_verified": exact_partition,
        "maximum_refinement_level": maximum_level,
        "maximum_extra_refinement": int(arguments.max_extra_refinement),
        "maximum_extra_refinement_used": max(
            (int(row["extra_refinement"]) for row in all_leaves), default=0
        ),
        "used_center_count": len(used_centers),
        "used_center_ids": used_centers,
        "maximum_neumann_product_upper": max(closed_products, default=None),
        "maximum_budget_ratio_upper": max(closed_ratios, default=None),
        "minimum_budget_margin_factor_lower": (
            None
            if not closed_ratios
            else math.nextafter(1.0 / max(closed_ratios), -math.inf)
        ),
        "leaf_ledger": str(ledger_path.relative_to(ROOT)),
        "leaf_ledger_sha256": sha256_file(ledger_path),
        "unresolved_component_count": len(components),
        "unresolved_components": component_payloads,
        "suggested_centers": suggested_centers,
        "unresolved_examples": unresolved_leaves[:100],
    }
    output = ROOT / "results" / f"refined_atlas_sigma_{sigma:.0e}.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
