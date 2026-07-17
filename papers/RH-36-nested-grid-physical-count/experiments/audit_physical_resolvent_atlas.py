"""Build an exact rational contour partition from physical center bounds."""

from __future__ import annotations

import argparse
import csv
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
sys.path[:0] = [str(RH27 / "src"), str(RH28 / "src"), str(RH33 / "src")]

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
    parser.add_argument(
        "--block-certificate",
        type=Path,
        default=Path("results/nested_block_certificate_sigma_1e-02.json"),
    )
    parser.add_argument("--base-arcs", type=int, default=64)
    parser.add_argument("--max-extra-refinement", type=int, default=12)
    parser.add_argument("--product-limit", type=float, default=1.0)
    arguments = parser.parse_args()

    block_path = arguments.block_certificate
    if not block_path.is_absolute():
        block_path = ROOT / block_path
    block = json.loads(block_path.read_text(encoding="utf-8"))
    center = complex(
        float(block["contour_center_real"]),
        float(block["contour_center_imag"]),
    )
    radius = float(block["contour_radius"])
    epsilon = float(
        block["continuation_gate"]["effective_perturbation_upper"]
    )
    theorem_budget = float(
        block["continuation_gate"]["admissible_coarse_resolvent_upper"]
    )
    product_limit = float(arguments.product_limit)
    if not 0.0 < product_limit <= 1.0:
        raise ValueError("product limit must lie in (0,1]")
    safety_budget = float(np.nextafter(product_limit / epsilon, -np.inf))
    budget = min(theorem_budget, safety_budget)
    center_dir = ROOT / "results" / "physical_centers_sigma_1e-02"
    centers = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(center_dir.glob("*.json"))
    ]
    centers = [
        row for row in centers if row["status"] == "rigorous_physical_resolvent_center"
    ]
    if not centers:
        raise RuntimeError("no rigorous physical centers are archived")

    closed_leaves = []
    unresolved_leaves = []
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
                "resolvent_budget_lower": repr(budget),
            }
            winner = None
            winner_bound = None
            winner_result = None
            for source in centers:
                point = complex(
                    float(source["spectral_parameter_real"]),
                    float(source["spectral_parameter_imag"]),
                )
                result = certify_arc_coverage(
                    point,
                    float(source["center_inverse_two_norm_upper"]),
                    target,
                )
                if result.closed and (
                    winner_bound is None
                    or result.transported_inverse_upper < winner_bound
                ):
                    winner = source
                    winner_bound = float(result.transported_inverse_upper)
                    winner_result = result
            record = {
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
                product = float(
                    np.nextafter(winner_bound * epsilon, np.inf)
                )
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
                        "transported_inverse_upper": winner_bound,
                        "continuation_product_upper": product,
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
                "source_kind": "adaptive_unresolved_midpoint",
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
    ledger_path = ROOT / "results" / "physical_resolvent_atlas_leaves.csv"
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
        "transported_inverse_upper",
        "continuation_product_upper",
    ]
    with ledger_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(all_leaves)

    maximum_inverse = max(
        (float(row["transported_inverse_upper"]) for row in closed_leaves),
        default=None,
    )
    maximum_product = max(
        (float(row["continuation_product_upper"]) for row in closed_leaves),
        default=None,
    )
    payload = {
        "status": (
            "full_physical_resolvent_continuation_atlas"
            if not unresolved_leaves
            else "partial_physical_resolvent_continuation_atlas"
        ),
        "sigma": float(block["sigma"]),
        "coarse_dimension": int(block["coarse_dimension"]),
        "fine_dimension": int(block["fine_dimension"]),
        "center_count": len(centers),
        "base_arc_count": base_count,
        "closed_leaf_count": len(closed_leaves),
        "unresolved_leaf_count": len(unresolved_leaves),
        "unresolved_component_count": len(components),
        "exact_rational_partition_verified": exact_partition_verified(all_leaves),
        "maximum_refinement_level": max(
            (int(row["refinement_level"]) for row in all_leaves), default=0
        ),
        "effective_perturbation_upper": epsilon,
        "theorem_admissible_coarse_resolvent_upper": theorem_budget,
        "atlas_resolvent_budget_lower": budget,
        "requested_continuation_product_limit": product_limit,
        "maximum_transported_inverse_upper": maximum_inverse,
        "maximum_continuation_product_upper": maximum_product,
        "all_continuation_products_below_one": bool(
            maximum_product is not None and maximum_product < 1.0
        ),
        "leaf_ledger": str(ledger_path.relative_to(ROOT)),
        "leaf_ledger_sha256": sha256_file(ledger_path),
        "unresolved_components": component_payloads,
        "suggested_centers": suggested,
    }
    output = ROOT / "results" / "physical_resolvent_atlas.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
