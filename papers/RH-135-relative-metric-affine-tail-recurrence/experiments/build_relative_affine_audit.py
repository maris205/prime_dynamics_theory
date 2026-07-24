from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import mpmath as mp
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
RH134 = PAPERS / "RH-134-moving-frame-memory-tail-recurrence"
sys.path[:0] = [
    str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"),
    str(RH94 / "src"), str(RH94 / "experiments"), str(RH96 / "src"),
    str(RH96 / "experiments"), str(RH108 / "src"), str(RH110 / "src"),
    str(RH113 / "src"), str(RH130 / "experiments"), str(RH134 / "src"),
]

from relative_affine_tail import optimize_fixed_floor  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from memory_tail_recurrence import envelope_ratio  # noqa: E402
import build_floor_free_audit as floorfree  # noqa: E402


ETA = floorfree.ETA
DEPTH = floorfree.DEPTH
RANK_OFFSET = floorfree.RANK_OFFSET
THRESHOLDS = floorfree.THRESHOLDS
MP_DPS = 90


def finite(value: mp.mpf) -> dict[str, object]:
    if not mp.isfinite(value):
        return {"value": None, "log10": None, "infinite": True}
    if value <= 0:
        return {"value": 0.0, "log10": None, "infinite": False}
    logarithm = mp.log10(value)
    return {"value": float(value) if -300 < logarithm < 300 else None, "log10": float(logarithm), "infinite": False}


def mp_generalized(metric: mp.matrix, operator: mp.matrix) -> mp.mpf:
    size = metric.rows
    operator_scale = max(abs(operator[i, j]) for i in range(size) for j in range(size))
    if operator_scale <= mp.power(10, -(MP_DPS - 20)):
        return mp.mpf("0")
    values, vectors = mp.eigsy((metric + metric.T) / 2)
    inverse = vectors * mp.diag([1 / mp.sqrt(values[i]) for i in range(values.rows)]) * vectors.T
    relative = inverse * operator * inverse
    spectrum, _ = mp.eigsy((relative + relative.T) / 2)
    return max(mp.mpf("0"), spectrum[-1])


def records(model: dict[str, object], sigma: float, threshold: float, rank: int) -> list[dict[str, object]]:
    endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
    states = floorfree.state_history(model, endpoint)
    snapshots = [floorfree.normalized_snapshot(state) for state in states]
    packet = floorfree.source_right_packet(states[0], rank)
    output = []
    for time in range(1, endpoint + 1):
        recent, tail, full = floorfree.direct_memory_parts(states, time)
        cross = floorfree.projected_cross(recent, packet)
        frame = floorfree.top_right_frame(cross)
        input_frame = packet @ frame
        action = cross @ frame
        gram = floorfree.mp_gram(action)
        compressed_tail = input_frame.T @ tail @ input_frame
        compressed_tail = (compressed_tail + compressed_tail.T) / 2.0
        past_count = max(0, time - DEPTH + 1)
        delta = floorfree.finite_tail_operator_bound(ETA, DEPTH, past_count)
        weighted_tail = mp.mpf(repr(delta)) * floorfree.mp_matrix(compressed_tail)
        output.append({
            "time": time, "input_frame": input_frame, "gram": gram,
            "weighted_tail": weighted_tail, "delta": delta,
            "tail": tail, "snapshots": snapshots,
        })
        packet, _ = floorfree.one_step(full, packet, threshold)
    return output


def transition(old: dict[str, object], new: dict[str, object]) -> dict[str, object]:
    old_frame = np.asarray(old["input_frame"])
    new_frame = np.asarray(new["input_frame"])
    left, singular, right = np.linalg.svd(old_frame.T @ new_frame, full_matrices=False)
    orthogonal_np = left @ right
    orthogonal = floorfree.mp_matrix(orthogonal_np)
    defect = float(np.linalg.norm(new_frame - old_frame @ orthogonal_np, 2))
    delta_old = float(old["delta"])
    delta_new = float(new["delta"])
    boundary_index = int(new["time"]) - DEPTH
    boundary = np.zeros_like(old["tail"]) if boundary_index < 0 else np.asarray(old["snapshots"][boundary_index])
    birth_compressed = new_frame.T @ boundary @ new_frame
    birth_compressed = (birth_compressed + birth_compressed.T) / 2.0
    identity = mp.eye(4)
    metric_factor = mp_generalized(new["gram"], orthogonal.T * old["gram"] * orthogonal)
    gamma_old = mp_generalized(old["gram"], old["weighted_tail"])
    gamma_new = mp_generalized(new["gram"], new["weighted_tail"])
    if delta_old > 0.0:
        count = int(old["time"]) - DEPTH + 1
        ratio = envelope_ratio(ETA, DEPTH, count)
        metric_decay = mp.mpf(repr(ETA * ratio)) * metric_factor
    else:
        ratio = None
        metric_decay = mp.mpf("0")
    frame_base_matrix = (
        mp.mpf(repr(delta_new * ETA * delta_old * defect**2)) * identity
    )
    birth_matrix = (
        mp.mpf(repr(delta_new * ETA**DEPTH)) * floorfree.mp_matrix(birth_compressed)
    )
    q_frame_base = mp_generalized(new["gram"], frame_base_matrix)
    q_birth = mp_generalized(new["gram"], birth_matrix)
    optimization = optimize_fixed_floor(float(metric_decay), float(q_frame_base), float(q_birth))
    if optimization["contractive_feasible"]:
        rho = mp.mpf(repr(optimization["rho"]))
        q = mp.mpf(repr(optimization["q"]))
        bound = rho * gamma_old + q
        recurrence_holds = gamma_new <= bound * (1 + mp.mpf("1e-12")) + mp.mpf("1e-80")
    else:
        rho = metric_decay
        q = mp.inf
        bound = mp.inf
        recurrence_holds = True
    return {
        "source_time": int(old["time"]), "target_time": int(new["time"]),
        "minimum_principal_cosine": float(singular[-1]), "frame_defect_norm": defect,
        "tail_envelope_ratio": ratio,
        "metric_factor": finite(metric_factor), "metric_decay_base": finite(metric_decay),
        "q_frame_base": finite(q_frame_base), "q_birth": finite(q_birth),
        "source_gamma_squared": finite(gamma_old), "target_gamma_squared": finite(gamma_new),
        "first_birth": bool(delta_old == 0.0 and delta_new > 0.0),
        "optimization": optimization,
        "optimized_bound": finite(bound),
        "recurrence_holds": bool(recurrence_holds),
        "optimized_subunit_rho": bool(optimization["contractive_feasible"] and optimization["rho"] < 1.0),
        "optimized_fixed_floor_subunit": bool(optimization["contractive_feasible"] and optimization["fixed_floor"] < 1.0),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    mp.mp.dps = MP_DPS
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
                temporal = records(model, sigma, threshold, rank)
                steps = [transition(old, new) for old, new in zip(temporal, temporal[1:])]
                rows.append({"sigma": sigma, "side": model["side"], "threshold": threshold, "steps": steps})
        print(json.dumps({"completed_sigma": sigma, "chain_count": len(rows)}, sort_keys=True), flush=True)
    steps = [step for row in rows for step in row["steps"]]
    nontrivial = [step for step in steps if step["target_gamma_squared"]["value"] not in (None, 0.0)]
    recurrent = [step for step in steps if step["metric_decay_base"]["value"] not in (None, 0.0)]
    zero_target = [step for step in steps if step["target_gamma_squared"]["value"] == 0.0]
    births = [step for step in steps if step["first_birth"]]
    optimized = [step for step in steps if step["optimization"]["contractive_feasible"]]
    floors = [step["optimization"]["fixed_floor"] for step in optimized if math.isfinite(step["optimization"]["fixed_floor"])]
    summary = {
        "scale_count": len(sigmas), "chain_count": len(rows), "transition_count": len(steps),
        "nontrivial_target_transition_count": len(nontrivial),
        "zero_target_transition_count": len(zero_target),
        "first_birth_count": sum(step["first_birth"] for step in steps),
        "recurrent_transition_count": len(recurrent),
        "recurrent_contractive_feasible_count": sum(step["optimization"]["contractive_feasible"] for step in recurrent),
        "recurrent_contractive_infeasible_count": sum(not step["optimization"]["contractive_feasible"] for step in recurrent),
        "birth_contractive_feasible_count": sum(step["optimization"]["contractive_feasible"] for step in births),
        "nontrivial_contractive_feasible_count": sum(step["optimization"]["contractive_feasible"] for step in nontrivial),
        "recurrence_failure_count": sum(not step["recurrence_holds"] for step in steps),
        "contractive_feasible_count": sum(step["optimization"]["contractive_feasible"] for step in steps),
        "contractive_infeasible_count": sum(not step["optimization"]["contractive_feasible"] for step in steps),
        "optimized_fixed_floor_subunit_count": sum(step["optimized_fixed_floor_subunit"] for step in steps),
        "maximum_metric_factor_log10": max(step["metric_factor"]["log10"] for step in steps if step["metric_factor"]["log10"] is not None),
        "median_metric_factor_log10": float(np.median([step["metric_factor"]["log10"] for step in steps if step["metric_factor"]["log10"] is not None])),
        "maximum_metric_decay_base": max(step["metric_decay_base"]["value"] for step in recurrent if step["metric_decay_base"]["value"] is not None),
        "minimum_recurrent_metric_decay_base": min(step["metric_decay_base"]["value"] for step in recurrent if step["metric_decay_base"]["value"] is not None),
        "median_recurrent_metric_decay_base": float(np.median([step["metric_decay_base"]["value"] for step in recurrent if step["metric_decay_base"]["value"] is not None])),
        "maximum_q_birth_log10": max(step["q_birth"]["log10"] for step in nontrivial if step["q_birth"]["log10"] is not None),
        "median_q_birth_log10": float(np.median([step["q_birth"]["log10"] for step in nontrivial if step["q_birth"]["log10"] is not None])),
        "maximum_q_frame_base_log10": max(step["q_frame_base"]["log10"] for step in recurrent if step["q_frame_base"]["log10"] is not None),
        "minimum_optimized_fixed_floor": min(floors),
        "median_optimized_fixed_floor": float(np.median(floors)),
        "maximum_optimized_fixed_floor": max(floors),
    }
    payload = {
        "status": "rh135_relative_metric_affine_tail_recurrence_audit",
        "precision_decimal_digits": MP_DPS, "eta": ETA, "depth": DEPTH,
        "rows": rows, "audit_summary": summary,
        "theorem_boundary": {
            "relative_metric_affine_recurrence_theorem": True,
            "sharp_metric_amplification_coefficients": True,
            "vanishing_absolute_forcing_obstruction": True,
            "temporal_rho_q_audited": not args.smoke,
            "uniform_subunit_rho_proved": False,
            "uniform_subunit_fixed_floor_proved": False,
            "cross_scale_relative_recurrence_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "The raw memory recurrence converts exactly into gamma_{t+1}^2 <= rho_t gamma_t^2 + q_t. Both coefficients expose target-Gram amplification. Tiny Euclidean forcing is not enough without a metric lower bound. The 90-digit temporal audit determines how often a contractive Young parameter exists and how often the optimized affine fixed floor is subunit.",
    }
    name = "relative_affine_smoke.json" if args.smoke else "relative_affine_audit.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
