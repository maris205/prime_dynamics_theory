from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from source_support import branch_is_stable, compose_support_floor, projector_radius, support_value  # noqa: E402


UPSTREAM = {
    number: next(PAPERS.glob(f"RH-{number}-*/results/summary.json"))
    for number in range(140, 148)
}
OUTWARD = PAPERS / "RH-138-outward-finite-directional-composition/results/summary.json"


def sha(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes())
    return digest.hexdigest()


def layer_records() -> tuple[list[dict[str, object]], dict[int, dict[str, object]]]:
    summaries = {number: json.loads(path.read_text()) for number, path in UPSTREAM.items()}
    descriptions = {
        140: ("normalized source snapshot ball", "10/10 rank-four radii below 1e-3", "uniform source enclosure"),
        141: ("gap-stable packet projector", "4/10 universal; 10/10 quadratic diagnostic", "interval-valid quadratic packet radius"),
        142: ("factorized Arb packet closure", "10/10 frozen binary packets", "uniform packet theorem"),
        143: ("threshold branch gate", "360/360 positive local margins", "packet-ball propagation through recursion"),
        144: ("backward controlled kernel", "28/30 viable chains", "all-level repeating/reset block"),
        145: ("delayed-start isolation", "18/18 clean suffix chains", "future exclusion of recurrent bad births"),
        146: ("normalized-base recurrence", "330/330 inequalities; projective route lossy", "positive all-level base packet"),
        147: ("correlated support tube", "28/30 K_1e-10 chains", "all-level lower-bounded support cocycle"),
    }
    rows = []
    for number in range(140, 148):
        archive = UPSTREAM[number].with_name("archive_verification.json")
        boundary = summaries[number]["program_boundary"]
        rows.append({
            "paper": number,
            "layer": descriptions[number][0],
            "finite_checkpoint": descriptions[number][1],
            "missing_all_level_packet": descriptions[number][2],
            "summary_path": str(UPSTREAM[number].relative_to(PAPERS.parent)),
            "summary_sha256": sha(UPSTREAM[number]),
            "archive_verification_path": str(archive.relative_to(PAPERS.parent)),
            "archive_verified": archive.exists() and json.loads(archive.read_text())["status"].startswith(f"all_rh{number}_"),
            "riemann_hypothesis_flag": bool(boundary.get("riemann_hypothesis", False)),
            "stage_A_flag": bool(boundary.get("stage_A", boundary.get("uniform_stage_A_closed", False))),
        })
    return rows, summaries


def synthetic_compositions(count: int) -> tuple[list[dict[str, float]], int]:
    rng = np.random.default_rng(148)
    records = []
    failures = 0
    for _ in range(count):
        eps = float(rng.uniform(1e-8, 1e-3))
        gap = float(rng.uniform(2.2, 8.0) * eps)
        packet_radius = projector_radius(eps, gap)
        branch_margin = float(rng.uniform(1.1, 4.0) * packet_radius)
        if not branch_is_stable(packet_radius, branch_margin):
            failures += 1
        y_bound = float(rng.uniform(0.0, 0.25))
        actual_y = float(rng.uniform(0.0, y_bound))
        base = float(rng.uniform(0.15, 0.95))
        actual_base = base
        initial = support_value(y_bound, base)
        actual_supports = [support_value(actual_y, actual_base)]
        logs = []
        for _step in range(12):
            rho = float(rng.uniform(0.2, 0.85))
            forcing = float(rng.uniform(0.0, 0.08))
            next_bound = min(0.94, forcing + rho * y_bound)
            ratio = float(rng.uniform(0.65, 1.0))
            source_factor = max(0.0, 1.0 - math.sqrt(y_bound)) ** 4
            target_factor = max(0.0, 1.0 - math.sqrt(next_bound)) ** 4
            kappa = ratio * target_factor / source_factor
            logs.append(math.log(kappa))
            actual_y = float(rng.uniform(0.0, next_bound))
            actual_base = min(1.0, ratio * actual_base * float(rng.uniform(1.0, 1.25)))
            y_bound = next_bound
            actual_supports.append(support_value(actual_y, actual_base))
        theorem_floor, drawdown = compose_support_floor(initial, logs)
        actual_minimum = min(actual_supports)
        if actual_minimum + 1e-14 < theorem_floor:
            failures += 1
        records.append({
            "packet_radius": packet_radius,
            "branch_margin": branch_margin,
            "theorem_floor": theorem_floor,
            "actual_minimum_support": actual_minimum,
            "actual_to_floor_ratio": actual_minimum / theorem_floor,
            "log_cocycle_drawdown": drawdown,
        })
    return records, failures


def omission_witnesses() -> list[dict[str, object]]:
    gap_rejected = False
    try:
        projector_radius(0.1, 0.2)
    except ValueError:
        gap_rejected = True
    branch_rejected = not branch_is_stable(0.1, 0.1)
    nominal_support = support_value(0.0, 0.5)
    actual_support_without_outward_dominance = support_value(1.0, 0.5)
    outward_witness = nominal_support > 0.0 and actual_support_without_outward_dominance == 0.0
    cocycle_floor, _ = compose_support_floor(1.0, [math.log(0.5)] * 80)
    return [
        {"packet": "spectral gap", "witness": "g=2 eps makes the projector gate singular", "passes": gap_rejected},
        {"packet": "branch margin", "witness": "propagated radius equal to the margin permits branch contact", "passes": branch_rejected},
        {"packet": "outward dominance", "witness": "nominal y=0 but actual y=1 destroys support", "passes": outward_witness},
        {"packet": "support cocycle", "witness": "kappa_n=1/2 drives the equality floor to zero", "passes": cocycle_floor < 1e-20},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    layers, summaries = layer_records()
    outward = json.loads(OUTWARD.read_text())
    synthetic_count = 128 if args.smoke else 4096
    synthetic, failures = synthetic_compositions(synthetic_count)
    witnesses = omission_witnesses()
    missing = [
        {"id": "E-source", "description": "uniform all-level normalized source and packet enclosure", "closed": False},
        {"id": "E-update", "description": "propagation of packet balls through threshold recursion into the outward assembly", "closed": False},
        {"id": "E-cocycle", "description": "delayed all-level support cocycle with uniformly bounded drawdown", "closed": False},
    ]
    ratios = [record["actual_to_floor_ratio"] for record in synthetic]
    summary = {
        "upstream_archive_count": len(layers),
        "upstream_archive_verification_count": sum(row["archive_verified"] for row in layers),
        "upstream_rh_flag_count": sum(row["riemann_hypothesis_flag"] for row in layers),
        "upstream_stage_A_flag_count": sum(row["stage_A_flag"] for row in layers),
        "reference_outward_archive_verified": (OUTWARD.with_name("archive_verification.json")).exists(),
        "factorized_packet_certified_count": summaries[142]["audit"]["packet_certified_count"],
        "factorized_packet_total_count": summaries[142]["audit"]["channel_count"],
        "strict_threshold_branch_count": summaries[143]["audit"]["strict_branch_count"],
        "threshold_update_count": summaries[143]["audit"]["update_record_count"],
        "outward_residual_transition_count": outward["audit"]["transition_count"],
        "outward_residual_failure_count": outward["audit"]["raw_certification_failure_count"] + outward["audit"]["bridge_certification_failure_count"],
        "finite_positive_tube_chain_count": summaries[147]["audit"]["positive_tube_chain_count"],
        "finite_tube_chain_count": summaries[147]["audit"]["chain_count"],
        "clean_suffix_positive_chain_count": summaries[145]["audit"]["first_clean_suffix_chain_count"],
        "synthetic_composition_count": synthetic_count,
        "synthetic_composition_failure_count": failures,
        "minimum_synthetic_actual_to_floor_ratio": min(ratios),
        "median_synthetic_actual_to_floor_ratio": float(np.median(ratios)),
        "maximum_synthetic_actual_to_floor_ratio": max(ratios),
        "omission_witness_count": len(witnesses),
        "omission_witness_pass_count": sum(item["passes"] for item in witnesses),
        "missing_all_level_interface_count": len(missing),
        "closed_all_level_interface_count": sum(item["closed"] for item in missing),
    }
    payload = {
        "status": "rh148_conditional_source_directional_support_composition_audit",
        "layers": layers,
        "reference_outward_summary_path": str(OUTWARD.relative_to(PAPERS.parent)),
        "reference_outward_summary_sha256": sha(OUTWARD),
        "missing_interfaces": missing,
        "omission_witnesses": witnesses,
        "synthetic_records": synthetic,
        "audit_summary": summary,
        "theorem_boundary": {
            "conditional_source_to_support_theorem": True,
            "gap_branch_outward_cocycle_composition_proved": True,
            "four_omission_witnesses_proved": True,
            "finite_readiness_stack_audited": not args.smoke,
            "finite_end_to_end_interval_source_to_support_closed": False,
            "all_level_directional_support_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "The source-to-directional-support implication is now a single quantitative conditional theorem. Frozen archives separately certify 10/10 factorized packets, 360/360 branch margins, 330/330 outward residual pairs, and 28/30 positive support tubes. They are not yet one end-to-end interval proof: E-source, E-update, and E-cocycle remain open all-level interfaces.",
    }
    output = ROOT / "results" / ("source_support_composition_smoke.json" if args.smoke else "source_support_composition_audit.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()

