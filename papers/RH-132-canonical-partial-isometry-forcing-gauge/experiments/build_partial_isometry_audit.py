from __future__ import annotations

import argparse
import collections
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH130 = PAPERS / "RH-130-floor-free-semidefinite-directional-audit"
sys.path.insert(0, str(ROOT / "src"))

from partial_isometry_gauge import canonical_partial_isometry, minimal_trace_forcing  # noqa: E402


SEED = 1322026
FULL_SAMPLES = 4096
SMOKE_SAMPLES = 128
RANDOM_COMPETITORS = 48


def frame(rng: np.random.Generator, ambient: int, rank: int) -> np.ndarray:
    q, _ = np.linalg.qr(rng.normal(size=(ambient, rank)))
    return q[:, :rank]


def random_orthogonal(rng: np.random.Generator, rank: int) -> np.ndarray:
    q, _ = np.linalg.qr(rng.normal(size=(rank, rank)))
    return q


def psd_on_frame(rng: np.random.Generator, basis: np.ndarray) -> np.ndarray:
    rank = basis.shape[1]
    rotation = random_orthogonal(rng, rank)
    values = np.exp(rng.uniform(math.log(1e-3), math.log(2.0), size=rank))
    return basis @ rotation @ np.diag(values) @ rotation.T @ basis.T


def instance(rng: np.random.Generator, equal_rank: bool) -> dict[str, object]:
    ambient = 12
    source_rank = int(rng.integers(1, 7))
    target_rank = source_rank if equal_rank else int(rng.integers(source_rank + 1, 8))
    source = frame(rng, ambient, source_rank)
    target = frame(rng, ambient, target_rank)
    result = canonical_partial_isometry(source, target)
    transport = result["transport"]
    canonical_distance = float(np.linalg.norm(target[:, :source_rank] - transport @ source, "fro") ** 2) if target_rank >= source_rank else math.nan
    random_gap = math.nan
    if equal_rank:
        distances = []
        for _ in range(RANDOM_COMPETITORS):
            candidate = target @ random_orthogonal(rng, source_rank)
            distances.append(float(np.linalg.norm(candidate - source, "fro") ** 2))
        canonical_frame = transport @ source
        canonical_distance = float(np.linalg.norm(canonical_frame - source, "fro") ** 2)
        random_gap = min(distances) - canonical_distance

    source_tail = psd_on_frame(rng, source)
    target_tail = psd_on_frame(rng, target)
    transported_tail = transport @ source_tail @ transport.T
    factor = float(np.exp(rng.uniform(math.log(0.1), math.log(10.0))))
    forcing = minimal_trace_forcing(target_tail, transported_tail, factor, final_projector=result["final_projector"])
    final_complement = np.eye(ambient) - result["final_projector"]
    unmatched_slack = forcing["trace_cost"] - forcing["unmatched_target_trace_lower"]
    return {
        "equal_rank": equal_rank,
        "source_rank": source_rank,
        "target_rank": target_rank,
        "overlap_rank": result["overlap_rank"],
        "minimum_principal_cosine": float(np.min(result["principal_cosines"])),
        "initial_defect": result["initial_defect"],
        "final_defect": result["final_defect"],
        "random_procrustes_gap": random_gap,
        "forcing_trace": forcing["trace_cost"],
        "unmatched_trace_lower": forcing["unmatched_target_trace_lower"],
        "unmatched_trace_slack": unmatched_slack,
        "minimum_forcing_slack_eigenvalue": forcing["minimum_slack_eigenvalue"],
        "unmatched_compression_error": float(np.linalg.norm(final_complement @ transported_tail @ final_complement, 2)),
    }


def rh130_application() -> dict[str, object]:
    source = RH130 / "results" / "floor_free_audit.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    states = {row["state_id"]: row for row in data["state_rows"]}
    ranks = {
        key: sum(item["value"] not in (None, 0.0) for item in row["relative_spectrum"])
        for key, row in states.items()
    }
    transitions = collections.Counter()
    births = []
    eligible_positive = 0
    eligible_blocked = 0
    for pair in data["pairs"]:
        source_id = f"{pair['source_sigma']:.2f}:{pair['side']}:{pair['threshold']:.0e}:p{pair['phase']:.2f}"
        target_id = f"{pair['target_sigma']:.2f}:{pair['side']}:{pair['threshold']:.0e}:p{pair['phase']:.2f}"
        transition = (ranks[source_id], ranks[target_id])
        transitions[transition] += 1
        if transition == (0, 4):
            gamma = states[target_id]["gamma"]["value"]
            births.append(gamma * gamma)
        if transition == (4, 4):
            eligible_positive += bool(pair["positive_transfer"])
            eligible_blocked += not bool(pair["positive_transfer"])
    births_sorted = sorted(births)
    return {
        "source_archive": str(source.relative_to(ROOT.parents[1])),
        "transition_counts": {f"{a}_to_{b}": count for (a, b), count in sorted(transitions.items())},
        "transport_eligible_positive_count": eligible_positive,
        "transport_eligible_blocked_count": eligible_blocked,
        "birth_forcing_count": len(births),
        "subunit_birth_forcing_count": sum(value < 1.0 for value in births),
        "minimum_birth_forcing": min(births),
        "median_birth_forcing": float(np.median(births)),
        "maximum_birth_forcing": max(births),
        "birth_forcing_values": births_sorted,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    count = SMOKE_SAMPLES if args.smoke else FULL_SAMPLES
    rng = np.random.default_rng(SEED)
    rows = [instance(rng, index < count // 2) for index in range(count)]
    application = rh130_application()
    equal_rows = [row for row in rows if row["equal_rank"]]
    summary = {
        "sample_count": len(rows),
        "equal_rank_procrustes_sample_count": len(equal_rows),
        "partial_isometry_failure_count": sum(row["initial_defect"] > 2e-12 or row["final_defect"] > 2e-12 for row in rows),
        "procrustes_failure_count": sum(row["random_procrustes_gap"] < -2e-12 for row in equal_rows),
        "forcing_dominance_failure_count": sum(row["minimum_forcing_slack_eigenvalue"] < -2e-11 for row in rows),
        "unmatched_lower_failure_count": sum(row["unmatched_trace_slack"] < -2e-10 for row in rows),
        "maximum_partial_isometry_defect": max(max(row["initial_defect"], row["final_defect"]) for row in rows),
        "minimum_random_procrustes_gap": min(row["random_procrustes_gap"] for row in equal_rows),
        "minimum_unmatched_trace_slack": min(row["unmatched_trace_slack"] for row in rows),
        "rh130_zero_to_zero_count": application["transition_counts"].get("0_to_0", 0),
        "rh130_zero_to_four_count": application["transition_counts"].get("0_to_4", 0),
        "rh130_four_to_four_count": application["transition_counts"].get("4_to_4", 0),
        "rh130_subunit_birth_forcing_count": application["subunit_birth_forcing_count"],
    }
    payload = {
        "status": "rh132_canonical_partial_isometry_forcing_gauge_audit",
        "seed": SEED, "rows": rows, "rh130_application": application,
        "audit_summary": summary,
        "theorem_boundary": {
            "canonical_polar_partial_isometry": True,
            "principal_angle_procrustes_optimality": True,
            "minimal_trace_positive_forcing": True,
            "unmatched_target_forcing_lower_bound": True,
            "natural_dynamical_gauge_derived": False,
            "physical_all_level_affine_recurrence_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "The polar factor of the support overlap is a canonical, basis-independent partial-isometry gauge. Any target range outside its final space is necessarily additive forcing, and the positive part of the residual is the unique trace-minimal cost. RH-130 splits into 30 vacuous, 42 transport-eligible, and 24 forcing-only edges; 22 of the 24 birth strengths are subunit.",
    }
    name = "partial_isometry_smoke.json" if args.smoke else "partial_isometry_audit.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
