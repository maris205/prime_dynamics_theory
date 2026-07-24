from __future__ import annotations

import argparse
import itertools
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
RH135 = PAPERS / "RH-135-relative-metric-affine-tail-recurrence"
sys.path[:0] = [
    str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"),
    str(RH94 / "src"), str(RH94 / "experiments"), str(RH96 / "src"),
    str(RH96 / "experiments"), str(RH108 / "src"), str(RH110 / "src"),
    str(RH113 / "src"), str(RH130 / "experiments"), str(RH134 / "src"),
    str(RH135 / "src"),
]

from memory_tail_recurrence import envelope_ratio  # noqa: E402
from metric_balanced_gauge import polar_blend  # noqa: E402
from relative_affine_tail import optimize_fixed_floor  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
import build_floor_free_audit as floorfree  # noqa: E402


ETA = floorfree.ETA
DEPTH = floorfree.DEPTH
RANK_OFFSET = floorfree.RANK_OFFSET
THRESHOLDS = floorfree.THRESHOLDS
MP_DPS = 80
BLEND_POINTS = 17


def finite(value: mp.mpf) -> dict[str, object]:
    if not mp.isfinite(value):
        return {"value": None, "log10": None, "infinite": True}
    if value <= 0:
        return {"value": 0.0, "log10": None, "infinite": False}
    logarithm = mp.log10(value)
    return {"value": float(value) if -300 < logarithm < 300 else None, "log10": float(logarithm), "infinite": False}


def mp_generalized(metric: mp.matrix, operator: mp.matrix) -> mp.mpf:
    scale = max(abs(operator[i, j]) for i in range(operator.rows) for j in range(operator.cols))
    if scale <= mp.power(10, -(MP_DPS - 15)):
        return mp.mpf("0")
    values, vectors = mp.eigsy((metric + metric.T) / 2)
    inverse = vectors * mp.diag([1 / mp.sqrt(values[i]) for i in range(values.rows)]) * vectors.T
    relative = inverse * operator * inverse
    spectrum, _ = mp.eigsy((relative + relative.T) / 2)
    return max(mp.mpf("0"), spectrum[-1])


def mp_eigenframe(matrix: mp.matrix) -> tuple[list[mp.mpf], np.ndarray]:
    values, vectors = mp.eigsy((matrix + matrix.T) / 2)
    frame = np.array([[float(vectors[i, j]) for j in range(vectors.cols)] for i in range(vectors.rows)])
    return [mp.mpf(values[i]) for i in range(values.rows)], frame


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
        past_count = max(0, time - DEPTH + 1)
        delta = floorfree.finite_tail_operator_bound(ETA, DEPTH, past_count)
        output.append({
            "time": time, "input_frame": input_frame, "gram": gram,
            "delta": delta, "tail": tail, "snapshots": snapshots,
        })
        packet, _ = floorfree.one_step(full, packet, threshold)
    return output


def endpoint_signs(source_vectors: np.ndarray, target_vectors: np.ndarray, polar: np.ndarray) -> list[np.ndarray]:
    candidates = []
    desired = np.sign(np.linalg.det(polar))
    for signs in itertools.product((-1.0, 1.0), repeat=4):
        diagonal = np.diag(signs)
        candidate = source_vectors @ diagonal @ target_vectors.T
        if np.sign(np.linalg.det(candidate)) == desired:
            candidates.append(candidate)
    return candidates


def evaluate_candidate(
    orthogonal_np: np.ndarray,
    old: dict[str, object],
    new: dict[str, object],
    ratio: float,
    boundary_compressed: np.ndarray,
    q_birth: mp.mpf,
    inverse_target_min: mp.mpf,
) -> dict[str, object]:
    orthogonal = floorfree.mp_matrix(orthogonal_np)
    metric_factor = mp_generalized(new["gram"], orthogonal.T * old["gram"] * orthogonal)
    metric_decay = mp.mpf(repr(ETA * ratio)) * metric_factor
    defect = float(np.linalg.norm(np.asarray(new["input_frame"]) - np.asarray(old["input_frame"]) @ orthogonal_np, 2))
    frame_scalar = mp.mpf(repr(float(new["delta"]) * ETA * float(old["delta"]) * defect**2))
    q_frame_base = frame_scalar * inverse_target_min
    optimization = optimize_fixed_floor(float(metric_decay), float(q_frame_base), float(q_birth))
    return {
        "orthogonal": orthogonal_np,
        "metric_factor": metric_factor,
        "metric_decay": metric_decay,
        "frame_defect": defect,
        "q_frame_base": q_frame_base,
        "optimization": optimization,
    }


def transition(old: dict[str, object], new: dict[str, object]) -> dict[str, object]:
    old_frame = np.asarray(old["input_frame"])
    new_frame = np.asarray(new["input_frame"])
    left, singular, right = np.linalg.svd(old_frame.T @ new_frame, full_matrices=False)
    polar = left @ right
    delta_old = float(old["delta"])
    delta_new = float(new["delta"])
    if delta_old <= 0.0:
        return {
            "source_time": int(old["time"]), "target_time": int(new["time"]),
            "recurrent": False, "first_birth": bool(delta_new > 0.0),
        }
    count = int(old["time"]) - DEPTH + 1
    ratio = envelope_ratio(ETA, DEPTH, count)
    boundary_index = int(new["time"]) - DEPTH
    boundary = np.asarray(old["snapshots"][boundary_index])
    boundary_compressed = new_frame.T @ boundary @ new_frame
    boundary_compressed = (boundary_compressed + boundary_compressed.T) / 2.0
    birth_matrix = mp.mpf(repr(delta_new * ETA**DEPTH)) * floorfree.mp_matrix(boundary_compressed)
    q_birth = mp_generalized(new["gram"], birth_matrix)
    target_values, target_vectors = mp_eigenframe(new["gram"])
    source_values, source_vectors = mp_eigenframe(old["gram"])
    inverse_target_min = 1 / min(target_values)
    metric_minimum = max(source_values[i] / target_values[i] for i in range(4))
    metric_decay_minimum = mp.mpf(repr(ETA * ratio)) * metric_minimum
    endpoints = endpoint_signs(source_vectors, target_vectors, polar)
    endpoints.sort(key=lambda candidate: float(np.linalg.norm(new_frame - old_frame @ candidate, 2)))
    selected_endpoints = endpoints[:2]
    candidate_matrices = [polar]
    for endpoint in selected_endpoints:
        for weight in np.linspace(0.0, 1.0, BLEND_POINTS):
            candidate_matrices.append(polar_blend(polar, endpoint, float(weight)))
    unique: list[np.ndarray] = []
    for candidate in candidate_matrices:
        if not any(np.linalg.norm(candidate - seen, "fro") < 1e-10 for seen in unique):
            unique.append(candidate)
    evaluated = [evaluate_candidate(candidate, old, new, ratio, boundary_compressed, q_birth, inverse_target_min) for candidate in unique]
    polar_result = evaluated[0]
    feasible = [item for item in evaluated if item["optimization"]["contractive_feasible"]]
    if feasible:
        best = min(feasible, key=lambda item: item["optimization"]["fixed_floor"])
    else:
        best = min(evaluated, key=lambda item: float(item["metric_decay"]))
    return {
        "source_time": int(old["time"]), "target_time": int(new["time"]),
        "recurrent": True, "first_birth": False,
        "minimum_principal_cosine": float(singular[-1]),
        "metric_minimum_factor": finite(metric_minimum),
        "metric_decay_minimum": finite(metric_decay_minimum),
        "orthogonal_contractivity_possible": bool(metric_decay_minimum < 1),
        "q_birth": finite(q_birth),
        "candidate_count": len(evaluated),
        "polar": {
            "metric_decay": finite(polar_result["metric_decay"]),
            "frame_defect": polar_result["frame_defect"],
            "q_frame_base": finite(polar_result["q_frame_base"]),
            "optimization": polar_result["optimization"],
        },
        "balanced": {
            "metric_decay": finite(best["metric_decay"]),
            "frame_defect": best["frame_defect"],
            "q_frame_base": finite(best["q_frame_base"]),
            "optimization": best["optimization"],
            "improves_polar": bool(
                best["optimization"]["contractive_feasible"]
                and (
                    not polar_result["optimization"]["contractive_feasible"]
                    or best["optimization"]["fixed_floor"] < polar_result["optimization"]["fixed_floor"]
                )
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    mp.mp.dps = MP_DPS
    sigmas = SIGMAS[:3] if args.smoke else SIGMAS
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
    recurrent = [step for row in rows for step in row["steps"] if step["recurrent"]]
    polar_feasible = [step for step in recurrent if step["polar"]["optimization"]["contractive_feasible"]]
    balanced_feasible = [step for step in recurrent if step["balanced"]["optimization"]["contractive_feasible"]]
    balanced_floors = [step["balanced"]["optimization"]["fixed_floor"] for step in balanced_feasible]
    summary = {
        "scale_count": len(sigmas), "chain_count": len(rows), "recurrent_transition_count": len(recurrent),
        "orthogonal_contractivity_possible_count": sum(step["orthogonal_contractivity_possible"] for step in recurrent),
        "orthogonal_contractivity_impossible_count": sum(not step["orthogonal_contractivity_possible"] for step in recurrent),
        "polar_contractive_feasible_count": len(polar_feasible),
        "balanced_contractive_feasible_count": len(balanced_feasible),
        "newly_recovered_contractive_count": sum(step["balanced"]["optimization"]["contractive_feasible"] and not step["polar"]["optimization"]["contractive_feasible"] for step in recurrent),
        "lost_polar_contractive_count": sum(step["polar"]["optimization"]["contractive_feasible"] and not step["balanced"]["optimization"]["contractive_feasible"] for step in recurrent),
        "balanced_subunit_fixed_floor_count": sum(step["balanced"]["optimization"]["contractive_feasible"] and step["balanced"]["optimization"]["fixed_floor"] < 1.0 for step in recurrent),
        "minimum_metric_decay_lower_bound": min(step["metric_decay_minimum"]["value"] for step in recurrent),
        "median_metric_decay_lower_bound": float(np.median([step["metric_decay_minimum"]["value"] for step in recurrent])),
        "maximum_metric_decay_lower_bound": max(step["metric_decay_minimum"]["value"] for step in recurrent),
        "minimum_balanced_fixed_floor": min(balanced_floors, default=None),
        "median_balanced_fixed_floor": float(np.median(balanced_floors)) if balanced_floors else None,
        "maximum_balanced_fixed_floor": max(balanced_floors, default=None),
        "median_polar_frame_defect": float(np.median([step["polar"]["frame_defect"] for step in recurrent])),
        "median_balanced_frame_defect": float(np.median([step["balanced"]["frame_defect"] for step in recurrent])),
    }
    payload = {
        "status": "rh136_metric_balanced_packet_gauge_audit",
        "precision_decimal_digits": MP_DPS, "blend_points": BLEND_POINTS,
        "rows": rows, "audit_summary": summary,
        "theorem_boundary": {
            "orthogonal_metric_minimax_theorem": True,
            "metric_contractivity_lower_obstruction": True,
            "deterministic_polar_metric_interpolation_audited": not args.smoke,
            "global_affine_objective_optimizer_proved": False,
            "uniform_metric_balanced_recurrence_proved": False,
            "cross_scale_relative_recurrence_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "Ordered Gram eigenframe matching gives the exact best metric factor available to any orthogonal frame gauge. This separates transitions that are universally blocked within the RH-134 orthogonal recurrence from those blocked only by the Euclidean polar choice. A deterministic interpolation audit measures how many recurrent steps can be recovered without making the optimized forcing floor superunit.",
    }
    name = "metric_balanced_smoke.json" if args.smoke else "metric_balanced_audit.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
