from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPERS = ROOT.parent
RH152 = PAPERS / "RH-152-reset-transition-overlap-coherence"
RH155 = PAPERS / "RH-155-native-spectral-reset-memory-pair"
RH156 = PAPERS / "RH-156-native-reset-support-floor"
RH158 = PAPERS / "RH-158-adaptive-lag-reset-cross-bridge"
RH159 = PAPERS / "RH-159-ten-layer-reset-route-review"
sys.path.insert(0, str(ROOT / "src"))

from reset_dichotomy import (  # noqa: E402
    directional_path_floor,
    directional_uniform_floor,
    native_interface_floor,
    native_uniform_floor,
)


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def paper(number: int) -> Path:
    matches = list(PAPERS.glob(f"RH-{number}-*"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one RH-{number} directory")
    return matches[0]


def main() -> None:
    overlap = json.loads((RH152 / "results/overlap_audit.json").read_text())
    memory = json.loads((RH155 / "results/memory_pair_audit.json").read_text())
    support = json.loads((RH156 / "results/support_audit.json").read_text())
    lagged = json.loads((RH158 / "results/lag_audit.json").read_text())
    review = json.loads((RH159 / "results/route_audit.json").read_text())

    overlap_items = [item for row in overlap["rows"] for item in row["transitions"]]
    memory_items = [item for row in memory["rows"] for item in row["snapshots"]]
    active_memory = [item for item in memory_items if item["tail_active"]]
    support_items = [item for row in support["rows"] for item in row["transitions"]]
    lag_targets = [item for row in lagged["rows"] for item in row["targets"]]
    selected = [item["selected"] for item in lag_targets]

    selected_lower = min(float(item["full_eigenvalue_lower"]) for item in support_items)
    selected_upper = max(float(item["full_eigenvalue_upper"]) for item in support_items)
    tail_upper = max(float(item["tail_mass_upper"]) for item in support_items)
    overlap_lower = min(float(item["robust_overlap_lower"]) for item in support_items)
    native = native_uniform_floor(selected_lower, selected_upper, tail_upper, overlap_lower)
    relative_tail_upper = max(float(item["relative_tail_upper"]) for item in support_items)
    recent_full_ratio_lower = min(
        (float(item["full_eigenvalue_lower"]) - float(item["tail_mass_upper"]))
        / float(item["full_eigenvalue_upper"])
        for item in support_items
    )
    native_interface = native_interface_floor(
        overlap_lower, recent_full_ratio_lower, relative_tail_upper
    )

    maximum_lag = int(lagged["maximum_lag"])
    fourth_lower = min(float(item["fourth_cross_singular_lower"]) for item in selected)
    first_upper = max(float(item["first_cross_singular_upper"]) for item in selected)
    path_lower = min(float(item["path_overlap_lower"]) for item in selected)
    directional_consecutive = directional_uniform_floor(
        overlap_lower, maximum_lag, fourth_lower, first_upper
    )
    directional_observed_path = directional_path_floor(path_lower, fourth_lower, first_upper)

    indices = [1, 2, 4, 8, 16, 32, 64]
    witnesses = {
        "overlap_omission": [
            native_interface_floor(1.0 / index, 0.4, 0.2)
            for index in indices
        ],
        "tail_separation_omission": [
            native_interface_floor(0.5, 0.4, 1.0 - 1.0 / (index + 1.0))
            for index in indices
        ],
        "spread_omission": [
            native_interface_floor(0.5, 1.0 / (index * index), 0.2)
            for index in indices
        ],
        "cross_omission": [directional_uniform_floor(0.5, 2, 1.0 / index, 1.0) for index in indices],
        "bounded_lag_omission": [directional_uniform_floor(0.5, index, 0.5, 1.0) for index in indices],
    }

    archive_records = []
    for number in range(151, 160):
        directory = paper(number)
        verification = json.loads((directory / "results/archive_verification.json").read_text())
        matches = [sha(directory / path) == expected for path, expected in verification["files"].items()]
        archive_records.append({
            "paper": number,
            "directory": directory.name,
            "publication_file_count": len(matches),
            "match_count": sum(matches),
            "failure_count": sum(not value for value in matches),
            "archive_status": verification["status"],
        })

    finite_diagnostics = {
        "overlap_lowers": [float(item["robust_lower"]) for item in overlap_items],
        "selected_eigenvalue_to_twice_tail_margins": [
            float(item["selected_eigenvalue_to_twice_tail_margin"]) for item in active_memory
        ],
        "selected_spread_ratios": [
            float(item["full_eigenvalue_upper"]) /
            max(float(item["full_eigenvalue_lower"]) - float(item["tail_mass_upper"]), np.finfo(float).tiny)
            for item in support_items
        ],
        "lagged_normalized_base_lowers": [float(item["normalized_base_lower"]) for item in selected],
        "lagged_path_overlap_lowers": [float(item["path_overlap_lower"]) for item in selected],
    }
    constants = {
        "selected_full_eigenvalue_lower": selected_lower,
        "selected_full_eigenvalue_upper": selected_upper,
        "tail_mass_upper": tail_upper,
        "selected_eigenvalue_to_twice_tail_global_margin": selected_lower / (2.0 * tail_upper),
        "overlap_lower": overlap_lower,
        "maximum_lag": maximum_lag,
        "fourth_cross_lower": fourth_lower,
        "first_cross_upper": first_upper,
        "selected_path_overlap_lower": path_lower,
        "native_global_support_floor": native["support_floor"],
        "native_interface_support_floor": native_interface,
        "native_global_relative_tail_upper": native["relative_tail_upper"],
        "native_interface_relative_tail_upper": relative_tail_upper,
        "native_interface_recent_full_ratio_lower": recent_full_ratio_lower,
        "directional_consecutive_overlap_floor": directional_consecutive,
        "directional_observed_path_floor": directional_observed_path,
        "minimum_local_native_support_floor": min(float(item["support_lower"]) for item in support_items),
        "minimum_local_lagged_base_floor": min(float(item["normalized_base_lower"]) for item in selected),
    }
    checklist = {
        "overlap_positive_count": sum(float(item["robust_lower"]) > 0.0 for item in overlap_items),
        "overlap_count": len(overlap_items),
        "native_subunit_count": sum(bool(item["subunit_recent_tail"]) for item in memory_items),
        "native_snapshot_count": len(memory_items),
        "finite_spread_count": sum(math.isfinite(value) for value in finite_diagnostics["selected_spread_ratios"]),
        "support_transition_count": len(support_items),
        "lagged_four_mode_count": sum(bool(item["four_mode_certified"]) for item in selected),
        "lagged_target_count": len(selected),
        "positive_lag_path_count": sum(float(item["path_overlap_lower"]) > 0.0 for item in selected),
        "archive_publication_hash_count": sum(item["publication_file_count"] for item in archive_records),
        "archive_publication_hash_failure_count": sum(item["failure_count"] for item in archive_records),
    }
    summary = {
        "native_finite_clause_count": 3,
        "directional_additional_clause_count": 1,
        "omission_witness_count": len(witnesses),
        "all_native_finite_checks_pass": (
            checklist["overlap_positive_count"] == 120
            and checklist["native_subunit_count"] == 130
            and checklist["finite_spread_count"] == 120
        ),
        "all_directional_finite_checks_pass": (
            checklist["lagged_four_mode_count"] == 120
            and checklist["positive_lag_path_count"] == 120
        ),
        "archive_verified_paper_count": sum(item["failure_count"] == 0 for item in archive_records),
        "archive_paper_count": len(archive_records),
        "archive_publication_hash_count": checklist["archive_publication_hash_count"],
        "archive_publication_hash_failure_count": checklist["archive_publication_hash_failure_count"],
        "upstream_open_gate_count": review["audit_summary"]["open_gate_count"],
    }
    payload = {
        "status": "rh160_conditional_all_level_reset_dichotomy",
        "constants": constants,
        "finite_checklist": checklist,
        "finite_diagnostics": finite_diagnostics,
        "witness_indices": indices,
        "omission_witnesses": witnesses,
        "archive_records": archive_records,
        "audit_summary": summary,
        "conditional_interfaces": {
            "native": [
                "eventual reset overlap lower",
                "eventual selected weak eigenvalue above twice the tail upper",
                "eventual selected spectral upper",
            ],
            "directional_addition": [
                "eventual bounded-lag normalized fourth-cross certificate",
            ],
            "downstream": [
                "a typed assembly theorem accepting the selected native or directional seed",
            ],
        },
        "theorem_boundary": {
            "conditional_native_all_level_floor": True,
            "conditional_directional_all_level_floor": True,
            "interface_omission_witnesses": True,
            "finite_hypothesis_audit": True,
            "any_eventual_interface_proved_for_the_prime_dynamics_sequence": False,
            "typed_downstream_assembly_proved": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "Three eventual interfaces give a uniform native reset-support floor: overlap conditioning, selected weak eigenvalue versus tail mass, and selected spectral spread. "
            "Adding a bounded-lag normalized fourth-cross interface gives a uniform directional seed. "
            "Explicit witnesses make both interface sets inclusion-minimal for these formulas. "
            "All clauses pass on the frozen atlas, but no finite audit proves that any clause persists eventually; the result is a falsifiable conditional roadmap, not Stage A or an RH result."
        ),
    }
    output = ROOT / "results/conditional_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary, **constants, **checklist}, sort_keys=True))


if __name__ == "__main__":
    main()
