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
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
RH108 = PAPERS / "RH-108-finite-memory-fourth-cross-support"
RH110 = PAPERS / "RH-110-finite-memory-three-mode-capacity"
RH113 = PAPERS / "RH-113-right-frame-directional-wedge"
RH130 = PAPERS / "RH-130-floor-free-semidefinite-directional-audit"
sys.path[:0] = [
    str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"),
    str(RH94 / "src"), str(RH94 / "experiments"), str(RH96 / "src"),
    str(RH96 / "experiments"), str(RH108 / "src"), str(RH110 / "src"),
    str(RH113 / "src"), str(RH130 / "experiments"),
]

from memory_tail_recurrence import envelope_ratio, memory_tail_update, moving_frame_tail_upper  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
import build_floor_free_audit as floorfree  # noqa: E402


ETA = floorfree.ETA
DEPTH = floorfree.DEPTH
RANK_OFFSET = floorfree.RANK_OFFSET
THRESHOLDS = floorfree.THRESHOLDS
TAU = 1.0


def temporal_records(model: dict[str, object], sigma: float, threshold: float, rank: int) -> list[dict[str, object]]:
    endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
    states = floorfree.state_history(model, endpoint)
    snapshots = [floorfree.normalized_snapshot(state) for state in states]
    packet = floorfree.source_right_packet(np.asarray(states[0], dtype=float), rank)
    records = []
    for time in range(1, endpoint + 1):
        recent, tail, full = floorfree.direct_memory_parts(states, time)
        cross = floorfree.projected_cross(recent, packet)
        frame = floorfree.top_right_frame(cross)
        input_frame = packet @ frame
        compressed_tail = input_frame.T @ tail @ input_frame
        compressed_tail = (compressed_tail + compressed_tail.T) / 2.0
        past_count = max(0, time - DEPTH + 1)
        delta = floorfree.finite_tail_operator_bound(ETA, DEPTH, past_count)
        records.append({
            "time": time, "tail": tail, "input_frame": input_frame,
            "compressed_tail": compressed_tail, "delta": delta,
            "snapshots": snapshots,
        })
        packet, _ = floorfree.one_step(full, packet, threshold)
    return records


def transition(old: dict[str, object], new: dict[str, object]) -> dict[str, object]:
    old_frame = np.asarray(old["input_frame"])
    new_frame = np.asarray(new["input_frame"])
    overlap = old_frame.T @ new_frame
    left, singular, right = np.linalg.svd(overlap, full_matrices=False)
    target_to_source = left @ right
    defect_matrix = new_frame - old_frame @ target_to_source
    defect_norm = float(np.linalg.norm(defect_matrix, 2))
    boundary_index = int(new["time"]) - DEPTH
    snapshots = old["snapshots"]
    boundary = np.zeros_like(old["tail"]) if boundary_index < 0 else np.asarray(snapshots[boundary_index])
    exact_update = memory_tail_update(np.asarray(old["tail"]), boundary, ETA, DEPTH)
    recurrence_error = float(np.linalg.norm(np.asarray(new["tail"]) - exact_update, 2))
    birth_compressed = new_frame.T @ boundary @ new_frame
    birth_compressed = (birth_compressed + birth_compressed.T) / 2.0
    bound = moving_frame_tail_upper(
        np.asarray(old["compressed_tail"]), float(old["delta"]), birth_compressed,
        target_to_source, defect_norm, ETA, DEPTH, TAU,
    )
    raw_slack = np.asarray(bound["upper"]) - np.asarray(new["compressed_tail"])
    raw_slack = (raw_slack + raw_slack.T) / 2.0
    delta_old = float(old["delta"])
    delta_new = float(new["delta"])
    if delta_old > 0.0:
        past_count = int(old["time"]) - DEPTH + 1
        ratio = envelope_ratio(ETA, DEPTH, past_count)
        rho = ETA * (1.0 + TAU) * ratio
        ratio_error = abs(ratio - delta_new / delta_old)
    else:
        ratio = None
        rho = 0.0
        ratio_error = 0.0
    weighted_forcing = delta_new * (np.asarray(bound["frame_forcing"]) + np.asarray(bound["birth_forcing"]))
    weighted_transport = delta_new * np.asarray(bound["transported"])
    weighted_target = delta_new * np.asarray(new["compressed_tail"])
    weighted_slack = weighted_transport + weighted_forcing - weighted_target
    weighted_slack = (weighted_slack + weighted_slack.T) / 2.0
    return {
        "source_time": int(old["time"]), "target_time": int(new["time"]),
        "tail_recurrence_error": recurrence_error,
        "minimum_principal_cosine": float(singular[-1]),
        "frame_defect_norm": defect_norm,
        "old_tail_envelope": delta_old, "new_tail_envelope": delta_new,
        "envelope_ratio": ratio, "envelope_ratio_error": ratio_error,
        "weighted_multiplicative_factor": rho,
        "birth_transition": bool(delta_old == 0.0 and delta_new > 0.0),
        "minimum_raw_slack": float(np.linalg.eigvalsh(raw_slack)[0]),
        "minimum_weighted_slack": float(np.linalg.eigvalsh(weighted_slack)[0]),
        "frame_forcing_norm": float(delta_new * np.linalg.norm(bound["frame_forcing"], 2)),
        "birth_forcing_norm": float(delta_new * np.linalg.norm(bound["birth_forcing"], 2)),
        "total_forcing_norm": float(np.linalg.norm(weighted_forcing, 2)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    sigmas = SIGMAS[:2] if args.smoke else SIGMAS
    thresholds = THRESHOLDS[:1] if args.smoke else THRESHOLDS
    sides = ("left",) if args.smoke else ("left", "right")
    rows = []
    for sigma in sigmas:
        rank = floorfree.clock_rank(sigma, offset=RANK_OFFSET)
        _, models = build_models(sigma)
        for model in models:
            if model["side"] not in sides:
                continue
            for threshold in thresholds:
                records = temporal_records(model, sigma, threshold, rank)
                steps = [transition(old, new) for old, new in zip(records, records[1:])]
                rows.append({
                    "sigma": sigma, "side": model["side"], "threshold": threshold,
                    "endpoint": records[-1]["time"], "steps": steps,
                })
        print(json.dumps({"completed_sigma": sigma, "chain_count": len(rows)}, sort_keys=True), flush=True)
    steps = [step for row in rows for step in row["steps"]]
    positive_forcing = [step["total_forcing_norm"] for step in steps if step["total_forcing_norm"] > 0.0]
    summary = {
        "scale_count": len(sigmas), "chain_count": len(rows), "transition_count": len(steps),
        "birth_transition_count": sum(step["birth_transition"] for step in steps),
        "tail_identity_failure_count": sum(step["tail_recurrence_error"] > 2e-13 for step in steps),
        "raw_loewner_failure_count": sum(step["minimum_raw_slack"] < -2e-13 for step in steps),
        "weighted_loewner_failure_count": sum(step["minimum_weighted_slack"] < -2e-30 for step in steps),
        "maximum_tail_recurrence_error": max(step["tail_recurrence_error"] for step in steps),
        "maximum_envelope_ratio_error": max(step["envelope_ratio_error"] for step in steps),
        "maximum_weighted_multiplicative_factor": max(step["weighted_multiplicative_factor"] for step in steps),
        "minimum_principal_cosine": min(step["minimum_principal_cosine"] for step in steps),
        "median_frame_defect_norm": float(np.median([step["frame_defect_norm"] for step in steps])),
        "maximum_frame_defect_norm": max(step["frame_defect_norm"] for step in steps),
        "minimum_positive_forcing_norm": min(positive_forcing, default=0.0),
        "median_positive_forcing_norm": float(np.median(positive_forcing)) if positive_forcing else 0.0,
        "maximum_positive_forcing_norm": max(positive_forcing, default=0.0),
        "birth_dominant_transition_count": sum(step["birth_forcing_norm"] >= step["frame_forcing_norm"] and step["total_forcing_norm"] > 0.0 for step in steps),
        "frame_dominant_transition_count": sum(step["frame_forcing_norm"] > step["birth_forcing_norm"] for step in steps),
    }
    payload = {
        "status": "rh134_moving_frame_memory_tail_recurrence_audit",
        "eta": ETA, "depth": DEPTH, "tau": TAU, "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "exact_memory_tail_birth_identity": True,
            "moving_frame_affine_loewner_recurrence": True,
            "sharp_young_frame_defect_constants": True,
            "finite_envelope_ratio_bound": True,
            "temporal_frozen_packet_audited": not args.smoke,
            "relative_gram_normalized_recurrence_proved": False,
            "cross_scale_source_recurrence_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "The finite-memory tail has an exact one-step birth law. In moving packet frames it admits a source-level affine Loewner recurrence with a strongly contractive old-tail coefficient, an explicit frame-change forcing, and the newly crossed memory slice. The remaining step is to transport the recent Gram metric simultaneously and convert these raw terms into relative coefficients rho_n and q_n.",
    }
    name = "memory_tail_smoke.json" if args.smoke else "memory_tail_audit.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
