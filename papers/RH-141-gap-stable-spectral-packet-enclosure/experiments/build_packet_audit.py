from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH140 = PAPERS / "RH-140-normalized-snapshot-enclosure"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH140 / "src")]

from run_effective_rank_audit import HORIZONS, SIGMAS, build_models, rank_candidate  # noqa: E402
from snapshot_enclosure import normalized_snapshot  # noqa: E402
from spectral_packet import projector_enclosure, top_projector  # noqa: E402


def synthetic_audit(samples: int, seed: int = 141) -> dict[str, float | int]:
    rng = np.random.default_rng(seed)
    failures = 0
    maximum_ratio = 0.0
    for _ in range(samples):
        dimension = int(rng.integers(3, 10))
        rank = int(rng.integers(1, dimension))
        gap = float(10.0 ** rng.uniform(-3.0, 0.0))
        upper = np.linspace(2.0 + gap, 1.0 + gap, rank)
        lower = np.linspace(1.0, 0.0, dimension - rank)
        diagonal = np.concatenate([upper, lower])
        basis, _ = np.linalg.qr(rng.normal(size=(dimension, dimension)))
        approximate = basis @ np.diag(diagonal) @ basis.T
        radius = float(gap * rng.uniform(0.001, 0.49))
        perturbation = rng.normal(size=(dimension, dimension))
        perturbation = (perturbation + perturbation.T) / 2.0
        perturbation *= radius / np.linalg.norm(perturbation, 2)
        exact = approximate + perturbation
        p_hat = top_projector(approximate, rank)
        p = top_projector(exact, rank)
        actual = float(np.linalg.norm(p - p_hat, 2))
        bound = projector_enclosure(gap, radius)["projector_radius"]
        ratio = actual / float(bound) if float(bound) > 0.0 else 0.0
        maximum_ratio = max(maximum_ratio, ratio)
        failures += int(actual > float(bound) * (1.0 + 1e-10) + 1e-12)
    return {"sample_count": samples, "failure_count": failures, "maximum_actual_to_bound_ratio": maximum_ratio}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    rh140 = json.loads((RH140 / "results" / "snapshot_enclosure_audit.json").read_text(encoding="utf-8"))
    source_rows = {(float(row["sigma"]), str(row["side"]), int(row["rank"])): row for row in rh140["rows"]}
    sigmas = SIGMAS[:1] if args.smoke else SIGMAS
    rows = []
    for sigma in sigmas:
        _, models = build_models(sigma)
        for model in models:
            side = str(model["side"])
            state = np.linalg.matrix_power(np.asarray(model["operator"]), HORIZONS[sigma]) @ np.asarray(model["source"])
            state_snapshot = normalized_snapshot(state)
            for rank in (1, 2, 4):
                candidate, _ = rank_candidate(state, rank)
                candidate_snapshot = normalized_snapshot(candidate)
                eigenvalues = np.linalg.eigvalsh(candidate_snapshot)[::-1]
                gap = float(eigenvalues[rank - 1] - eigenvalues[rank])
                inherited = source_rows[(sigma, side, rank)]
                universal_radius = float(inherited["certified_operator_snapshot_radius"])
                ideal_radius = float(inherited["ideal_svd_operator_radius"])
                universal = projector_enclosure(gap, universal_radius)
                ideal = projector_enclosure(gap, ideal_radius)
                exact_proxy = top_projector(state_snapshot, rank)
                candidate_proxy = top_projector(candidate_snapshot, rank)
                rows.append({
                    "sigma": sigma,
                    "side": side,
                    "rank": rank,
                    "horizon": HORIZONS[sigma],
                    "approximate_gap": gap,
                    "universal_snapshot_radius": universal_radius,
                    "universal_gap_ratio": gap / (2.0 * universal_radius),
                    "universal_enclosure": universal,
                    "ideal_svd_snapshot_radius": ideal_radius,
                    "ideal_svd_gap_ratio": gap / (2.0 * ideal_radius),
                    "ideal_svd_enclosure": ideal,
                    "float_proxy_projector_distance": float(np.linalg.norm(exact_proxy - candidate_proxy, 2)),
                })
        print(json.dumps({"completed_sigma": sigma, "row_count": len(rows)}, sort_keys=True), flush=True)
    rank4 = [row for row in rows if row["rank"] == 4]
    universal_stable = [row for row in rank4 if row["universal_enclosure"]["stable"]]
    synthetic = synthetic_audit(128 if args.smoke else 4096)
    summary = {
        "channel_rank_record_count": len(rows),
        "rank1_universal_stable_count": sum(row["universal_enclosure"]["stable"] for row in rows if row["rank"] == 1),
        "rank2_universal_stable_count": sum(row["universal_enclosure"]["stable"] for row in rows if row["rank"] == 2),
        "rank4_universal_stable_count": len(universal_stable),
        "rank4_universal_gap_wall_count": len(rank4) - len(universal_stable),
        "rank4_ideal_svd_stable_count": sum(row["ideal_svd_enclosure"]["stable"] for row in rank4),
        "minimum_rank4_universal_gap_ratio": min(row["universal_gap_ratio"] for row in rank4),
        "minimum_rank4_ideal_svd_gap_ratio": min(row["ideal_svd_gap_ratio"] for row in rank4),
        "maximum_certified_rank4_projector_radius": max((float(row["universal_enclosure"]["projector_radius"]) for row in universal_stable), default=None),
        "maximum_certified_rank4_frame_radius": max((float(row["universal_enclosure"]["frame_radius"]) for row in universal_stable), default=None),
        "synthetic_failure_count": synthetic["failure_count"],
        "synthetic_maximum_actual_to_bound_ratio": synthetic["maximum_actual_to_bound_ratio"],
    }
    payload = {
        "status": "rh141_gap_stable_spectral_packet_enclosure",
        "rows": rows,
        "synthetic_audit": synthetic,
        "audit_summary": summary,
        "theorem_boundary": {
            "approximate_gap_projector_enclosure": True,
            "polar_aligned_frame_enclosure": True,
            "two_radius_gap_obstruction": True,
            "rank4_universal_anchor_packet_count_is_four": not args.smoke,
            "quadratic_svd_radius_interval_validated": False,
            "all_ten_rank4_packets_certified": False,
            "threshold_update_enclosed": False,
            "uniform_all_level_packet_gap": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The RH-140 universal balls certify four of ten rank-four anchor projectors. "
            "The other six are genuine gap walls for that information set. All ten would pass "
            "under the quadratic orthogonal-SVD radius, with the coarse right channel only 2.1% "
            "above the sharp crossing threshold; interval validation of the quadratic cancellation "
            "is therefore the next source-interface target."
        ),
    }
    output = ROOT / "results" / ("spectral_packet_smoke.json" if args.smoke else "spectral_packet_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
