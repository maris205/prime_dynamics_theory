from __future__ import annotations

import argparse
import collections
import json
import math
from pathlib import Path
import sys

import mpmath as mp
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH58 = PAPERS / "RH-58-time-ordered-schur-cross-gramian"
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
RH108 = PAPERS / "RH-108-finite-memory-fourth-cross-support"
RH110 = PAPERS / "RH-110-finite-memory-three-mode-capacity"
RH113 = PAPERS / "RH-113-right-frame-directional-wedge"
RH130 = PAPERS / "RH-130-floor-free-semidefinite-directional-audit"
sys.path[:0] = [
    str(ROOT / "src"), str(RH58 / "experiments"), str(RH77 / "experiments"),
    str(RH82 / "src"), str(RH94 / "src"), str(RH94 / "experiments"),
    str(RH96 / "src"), str(RH96 / "experiments"), str(RH108 / "src"),
    str(RH110 / "src"), str(RH113 / "src"), str(RH130 / "experiments"),
]

from dyadic_packet_gauge import dyadic_polar_alignment  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_schur_fusion_pilot import coarse_embedding  # noqa: E402
import build_floor_free_audit as floorfree  # noqa: E402


MP_DPS = 90
DEPTH = floorfree.DEPTH
PHASES = floorfree.PHASES
THRESHOLDS = floorfree.THRESHOLDS
RANK_OFFSET = floorfree.RANK_OFFSET


def mp_root_pair(matrix: mp.matrix) -> tuple[mp.matrix, mp.matrix]:
    values, vectors = mp.eigsy((matrix + matrix.T) / 2)
    root = vectors * mp.diag([mp.sqrt(values[i]) for i in range(values.rows)]) * vectors.T
    inverse = vectors * mp.diag([1 / mp.sqrt(values[i]) for i in range(values.rows)]) * vectors.T
    return root, inverse


def matrix_norm(matrix: mp.matrix) -> mp.mpf:
    values, _ = mp.eigsy((matrix.T * matrix + matrix.T * matrix) / 2)
    return mp.sqrt(max(values))


def relative_factor(source: mp.matrix, target: mp.matrix) -> mp.mpf:
    source_norm = max(abs(source[i, j]) for i in range(source.rows) for j in range(source.cols))
    target_norm = max(abs(target[i, j]) for i in range(target.rows) for j in range(target.cols))
    zero = mp.power(10, -(MP_DPS - 20))
    if source_norm <= zero:
        return mp.mpf("0") if target_norm <= zero else mp.inf
    _, inverse = mp_root_pair(source)
    relative = inverse * target * inverse
    values, _ = mp.eigsy((relative + relative.T) / 2)
    return max(mp.mpf("0"), values[-1])


def finite(value: mp.mpf) -> dict[str, object]:
    if not mp.isfinite(value):
        return {"value": None, "log10": None, "infinite": True}
    if value <= 0:
        return {"value": 0.0, "log10": None, "infinite": False}
    logarithm = mp.log10(value)
    return {
        "value": float(value) if -300 < logarithm < 300 else None,
        "log10": float(logarithm), "infinite": False,
    }


def phase_records(model: dict[str, object], sigma: float, threshold: float, rank: int) -> dict[float, dict[str, object]]:
    endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
    chosen = {phase: max(1, min(endpoint, int(round(phase * endpoint)))) for phase in PHASES}
    states = floorfree.state_history(model, endpoint)
    packet = floorfree.source_right_packet(np.asarray(states[0], dtype=float), rank)
    records: dict[float, dict[str, object]] = {}
    for time in range(1, endpoint + 1):
        recent_gram, tail_gram, full_gram = floorfree.direct_memory_parts(states, time)
        recent_cross = floorfree.projected_cross(recent_gram, packet)
        frame = floorfree.top_right_frame(np.asarray(recent_cross, dtype=float))
        action = recent_cross @ frame
        packet_frame = packet @ frame
        block = packet_frame.T @ tail_gram @ packet_frame
        block = (block + block.T) / 2.0
        past_count = max(0, time - DEPTH + 1)
        delta = mp.mpf(repr(float(floorfree.finite_tail_operator_bound(floorfree.ETA, DEPTH, past_count))))
        gram = floorfree.mp_gram(action)
        tail = delta * floorfree.mp_matrix(block)
        spectrum = floorfree.mp_relative_spectrum(gram, tail)
        gamma = mp.sqrt(max(mp.mpf("0"), spectrum[-1]))
        for phase, selected_time in chosen.items():
            if selected_time == time:
                records[phase] = {
                    "input_frame": np.asarray(packet_frame, dtype=float),
                    "gram": gram, "tail": tail, "relative_spectrum": spectrum,
                    "gamma": gamma, "time": time,
                }
        packet, _ = floorfree.one_step(np.asarray(full_gram, dtype=float), packet, threshold)
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    mp.mp.dps = MP_DPS
    sigmas = SIGMAS[:2] if args.smoke else SIGMAS
    thresholds = THRESHOLDS[:1] if args.smoke else THRESHOLDS
    sides = ("left",) if args.smoke else ("left", "right")
    states: dict[tuple[float, str, float], dict[float, dict[str, object]]] = {}
    for sigma in sigmas:
        rank = floorfree.clock_rank(sigma, offset=RANK_OFFSET)
        _, models = build_models(sigma)
        for model in models:
            if model["side"] not in sides:
                continue
            for threshold in thresholds:
                states[(sigma, str(model["side"]), threshold)] = phase_records(model, sigma, threshold, rank)
        print(json.dumps({"assembled_sigma": sigma, "state_groups": len(states)}, sort_keys=True), flush=True)

    rh130 = json.loads((RH130 / "results" / ("floor_free_smoke.json" if args.smoke else "floor_free_audit.json")).read_text(encoding="utf-8"))
    rh130_pairs = {pair["pair_id"]: pair for pair in rh130["pairs"]}
    rows = []
    for source_sigma, target_sigma in zip(sigmas, sigmas[1:]):
        for side in sides:
            for threshold in thresholds:
                for phase in PHASES:
                    source = states[(source_sigma, side, threshold)][phase]
                    target = states[(target_sigma, side, threshold)][phase]
                    embedding = coarse_embedding(target["input_frame"].shape[0])
                    alignment = dyadic_polar_alignment(source["input_frame"], target["input_frame"], embedding)
                    orthogonal = floorfree.mp_matrix(alignment["target_to_source"])
                    target_root, _ = mp_root_pair(target["gram"])
                    _, source_inverse = mp_root_pair(source["gram"])
                    gauge = source_inverse * orthogonal * target_root
                    gram_error = matrix_norm(gauge.T * source["gram"] * gauge - target["gram"])
                    transported_tail = gauge.T * source["tail"] * gauge
                    natural_factor = relative_factor(transported_tail, target["tail"])
                    optimal_factor = floorfree.ordered_semidefinite_factor(source["relative_spectrum"], target["relative_spectrum"])
                    if mp.isfinite(natural_factor) and mp.isfinite(optimal_factor) and optimal_factor > 0:
                        optimality_loss = natural_factor / optimal_factor
                    elif natural_factor == optimal_factor == 0:
                        optimality_loss = mp.mpf("1")
                    else:
                        optimality_loss = mp.inf
                    natural_gamma_upper = mp.inf if not mp.isfinite(natural_factor) else mp.sqrt(natural_factor) * source["gamma"]
                    pair_id = f"{source_sigma:.2f}-{target_sigma:.2f}:{side}:{threshold:.0e}:p{phase:.2f}"
                    reference = rh130_pairs[pair_id]
                    rows.append({
                        "pair_id": pair_id, "source_sigma": source_sigma, "target_sigma": target_sigma,
                        "side": side, "threshold": threshold, "phase": phase,
                        "minimum_principal_cosine": alignment["minimum_principal_cosine"],
                        "maximum_principal_angle": alignment["maximum_principal_angle"],
                        "aligned_frame_distance": alignment["aligned_frame_distance"],
                        "gram_alignment_error": float(gram_error),
                        "natural_tail_factor": finite(natural_factor),
                        "optimal_tail_factor": finite(optimal_factor),
                        "natural_to_optimal_factor": finite(optimality_loss),
                        "natural_gamma_upper": finite(natural_gamma_upper),
                        "natural_positive_transfer": bool(mp.isfinite(natural_gamma_upper) and natural_gamma_upper < 1),
                        "optimal_positive_transfer": bool(reference["positive_transfer"]),
                    })

    finite_eligible = [row for row in rows if not row["natural_tail_factor"]["infinite"] and row["natural_tail_factor"]["value"] not in (None, 0.0)]
    losses = [row["natural_to_optimal_factor"]["log10"] for row in rows if row["natural_to_optimal_factor"]["log10"] is not None]
    eligible_losses = [row["natural_to_optimal_factor"]["log10"] for row in finite_eligible]
    eligible_cosines = [row["minimum_principal_cosine"] for row in finite_eligible]
    summary = {
        "scale_count": len(sigmas), "pair_count": len(rows),
        "finite_nonzero_natural_pair_count": len(finite_eligible),
        "infinite_natural_factor_count": sum(row["natural_tail_factor"]["infinite"] for row in rows),
        "natural_positive_transfer_count": sum(row["natural_positive_transfer"] for row in rows),
        "optimal_positive_transfer_count": sum(row["optimal_positive_transfer"] for row in rows),
        "minimum_principal_cosine": min(row["minimum_principal_cosine"] for row in rows),
        "median_principal_cosine": float(np.median([row["minimum_principal_cosine"] for row in rows])),
        "maximum_principal_angle": max(row["maximum_principal_angle"] for row in rows),
        "maximum_gram_alignment_error": max(row["gram_alignment_error"] for row in rows),
        "minimum_natural_to_optimal_log10": min(losses, default=None),
        "median_natural_to_optimal_log10": float(np.median(losses)) if losses else None,
        "maximum_natural_to_optimal_log10": max(losses, default=None),
        "minimum_eligible_natural_to_optimal_log10": min(eligible_losses, default=None),
        "median_eligible_natural_to_optimal_log10": float(np.median(eligible_losses)) if eligible_losses else None,
        "maximum_eligible_natural_to_optimal_log10": max(eligible_losses, default=None),
        "eligible_cosine_loss_correlation": float(np.corrcoef(eligible_cosines, eligible_losses)[0, 1]) if len(eligible_losses) > 1 else None,
        "natural_positive_transport_eligible_count": sum(row["natural_positive_transfer"] for row in finite_eligible),
        "optimal_positive_transport_eligible_count": sum(row["optimal_positive_transfer"] for row in finite_eligible),
        "natural_recovers_all_optimal_positive_count": sum(row["natural_positive_transfer"] and row["optimal_positive_transfer"] for row in rows),
        "optimal_positive_lost_by_natural_count": sum((not row["natural_positive_transfer"]) and row["optimal_positive_transfer"] for row in rows),
    }
    payload = {
        "status": "rh133_dyadic_packet_transport_gauge_audit",
        "precision_decimal_digits": MP_DPS, "rows": rows, "audit_summary": summary,
        "theorem_boundary": {
            "dyadic_packet_polar_gauge_constructed": True,
            "exact_gram_metric_lift_theorem": True,
            "natural_factor_dominates_optimal_factor": True,
            "five_scale_natural_gauge_audited": not args.smoke,
            "uniform_principal_angle_law_proved": False,
            "uniform_natural_tail_factor_proved": False,
            "physical_all_level_affine_recurrence_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "The model's dyadic isometry and recursively generated packet frames determine a genuine natural cross-scale polar gauge. Its exact-Gram metric lift can be compared directly with the post-hoc minimax gauge. Principal-angle coherence alone need not imply tail coherence; the finite audit quantifies the resulting optimality loss and decides whether this natural gauge preserves the positive transfers.",
    }
    name = "dyadic_gauge_smoke.json" if args.smoke else "dyadic_gauge_audit.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
