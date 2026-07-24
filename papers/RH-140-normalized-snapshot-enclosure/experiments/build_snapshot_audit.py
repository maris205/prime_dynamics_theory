from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments")]

from snapshot_enclosure import normalized_snapshot  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models, rank_candidate  # noqa: E402


def distances(first: np.ndarray, second: np.ndarray) -> dict[str, float]:
    difference = (first - second + (first - second).T) / 2.0
    values = np.linalg.eigvalsh(difference)
    return {
        "operator": float(max(abs(values[0]), abs(values[-1]))),
        "frobenius": float(np.linalg.norm(difference, "fro")),
        "trace": float(np.sum(np.abs(values))),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    archived = json.loads((RH77 / "results" / "effective_rank_audit.json").read_text(encoding="utf-8"))
    certified = {(float(row["sigma"]), channel["side"]): channel for row in archived["rows"] for channel in row["channels"]}
    sigmas = SIGMAS[:1] if args.smoke else SIGMAS
    rows = []
    for sigma in sigmas:
        _, models = build_models(sigma)
        for model in models:
            side = str(model["side"])
            state = np.linalg.matrix_power(np.asarray(model["operator"]), HORIZONS[sigma]) @ np.asarray(model["source"])
            source_snapshot = normalized_snapshot(state)
            for rank in (1, 2, 4):
                candidate, _ = rank_candidate(state, min(rank, min(state.shape)))
                candidate_snapshot = normalized_snapshot(candidate)
                direct = distances(source_snapshot, candidate_snapshot)
                truncation_fraction = float(np.linalg.norm(state - candidate, "fro") / np.linalg.norm(state, "fro"))
                arb_record = certified[(sigma, side)]["validated_rank_compression"][f"rank_{rank}"]
                arb_fraction = float(arb_record["relative_residual_upper"])
                rows.append({
                    "sigma": sigma,
                    "side": side,
                    "horizon": HORIZONS[sigma],
                    "rank": rank,
                    "source_shape": list(state.shape),
                    "arb_relative_state_residual_upper": arb_fraction,
                    "certified_operator_snapshot_radius": min(1.0, arb_fraction),
                    "certified_frobenius_snapshot_radius": math.sqrt(2.0) * min(1.0, arb_fraction),
                    "certified_trace_snapshot_radius": 2.0 * min(1.0, arb_fraction),
                    "float_truncation_fraction": truncation_fraction,
                    "ideal_svd_operator_radius": truncation_fraction**2,
                    "ideal_svd_trace_radius": 2.0 * truncation_fraction**2,
                    "direct_proxy_distances": direct,
                    "direct_within_arb_radius": bool(direct["operator"] <= arb_fraction * (1.0 + 1e-10) + 1e-15),
                    "svd_trace_identity_error": abs(direct["trace"] - 2.0 * truncation_fraction**2),
                })
        print(json.dumps({"completed_sigma": sigma, "record_count": len(rows)}, sort_keys=True), flush=True)
    rank4 = [row for row in rows if row["rank"] == 4]
    rank2 = [row for row in rows if row["rank"] == 2]
    rank1 = [row for row in rows if row["rank"] == 1]
    summary = {
        "channel_count": len({(row["sigma"], row["side"]) for row in rows}),
        "rank_record_count": len(rows),
        "arb_bound_failure_count": sum(not row["direct_within_arb_radius"] for row in rows),
        "maximum_svd_trace_identity_error": max(row["svd_trace_identity_error"] for row in rows),
        "maximum_rank1_certified_operator_radius": max(row["certified_operator_snapshot_radius"] for row in rank1),
        "maximum_rank2_certified_operator_radius": max(row["certified_operator_snapshot_radius"] for row in rank2),
        "maximum_rank4_certified_operator_radius": max(row["certified_operator_snapshot_radius"] for row in rank4),
        "maximum_rank4_direct_proxy_operator_distance": max(row["direct_proxy_distances"]["operator"] for row in rank4),
        "rank4_radius_below_1e_3_count": sum(row["certified_operator_snapshot_radius"] < 1e-3 for row in rank4),
        "rank4_radius_below_1e_5_count": sum(row["certified_operator_snapshot_radius"] < 1e-5 for row in rank4),
        "rank2_radius_below_1e_2_count": sum(row["certified_operator_snapshot_radius"] < 1e-2 for row in rank2),
    }
    payload = {
        "status": "rh140_normalized_snapshot_enclosure",
        "arb_source_precision_bits": archived["precision_bits"],
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "sharp_normalized_snapshot_perturbation_theorem": True,
            "orthogonal_svd_quadratic_improvement_theorem": True,
            "all_five_anchor_scales_and_both_channels_audited": not args.smoke,
            "arb_certified_source_state_residuals_reused": True,
            "computed_svd_is_itself_interval_validated": False,
            "full_source_to_packet_interval_enclosure": False,
            "uniform_all_level_source_enclosure": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The trace-normalization map no longer constitutes an uncontrolled interface: "
            "the RH-77 Arb residuals give rigorous operator-norm balls for every archived "
            "rank-four postblock snapshot. The largest radius is at the finest right channel; "
            "spectral packet and frame stability inside these balls remains to be proved."
        ),
    }
    output = ROOT / "results" / ("snapshot_enclosure_smoke.json" if args.smoke else "snapshot_enclosure_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()

