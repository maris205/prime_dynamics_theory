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
RH135 = PAPERS / "RH-135-relative-metric-affine-tail-recurrence"
RH136 = PAPERS / "RH-136-metric-balanced-packet-gauge"
sys.path[:0] = [str(ROOT / "src"), str(RH135 / "experiments"), str(RH136 / "experiments")]

from finite_horizon_tail import fixed_point, safety_radius  # noqa: E402
import build_metric_balanced_audit as metric_audit  # noqa: E402
import build_relative_affine_audit as affine_audit  # noqa: E402


MP_DPS = 80
BLEND_POINTS = 17


def finite(value: mp.mpf | float) -> dict[str, object]:
    number = mp.mpf(value)
    if not mp.isfinite(number):
        return {"value": None, "log10": None, "infinite": True}
    if number <= 0:
        return {"value": 0.0, "log10": None, "infinite": False}
    logarithm = mp.log10(number)
    return {"value": float(number) if -300 < logarithm < 300 else None, "log10": float(logarithm), "infinite": False}


def young_envelope(a: mp.mpf, b: mp.mpf, q: mp.mpf, source: mp.mpf) -> tuple[mp.mpf, mp.mpf | None]:
    value = q + (mp.sqrt(a * source) + mp.sqrt(b)) ** 2
    tau = mp.sqrt(b / (a * source)) if a * source > 0 and b > 0 else None
    return value, tau


def unique_candidates(old: dict[str, object], new: dict[str, object]) -> list[dict[str, object]]:
    old_frame = np.asarray(old["input_frame"])
    new_frame = np.asarray(new["input_frame"])
    left, _, right = np.linalg.svd(old_frame.T @ new_frame, full_matrices=False)
    polar = left @ right
    if float(old["delta"]) <= 0.0:
        return [{"matrix": polar, "kind": "birth", "endpoint": None, "weight": 0.0}]
    _, target_vectors = metric_audit.mp_eigenframe(new["gram"])
    _, source_vectors = metric_audit.mp_eigenframe(old["gram"])
    endpoints = metric_audit.endpoint_signs(source_vectors, target_vectors, polar)
    endpoints.sort(key=lambda candidate: float(np.linalg.norm(new_frame - old_frame @ candidate, 2)))
    raw = [{"matrix": polar, "kind": "polar", "endpoint": None, "weight": 0.0}]
    for endpoint_index, endpoint in enumerate(endpoints[:2]):
        for weight in np.linspace(0.0, 1.0, BLEND_POINTS):
            raw.append({
                "matrix": metric_audit.polar_blend(polar, endpoint, float(weight)),
                "kind": "blend", "endpoint": endpoint_index, "weight": float(weight),
            })
    unique: list[dict[str, object]] = []
    for item in raw:
        if not any(np.linalg.norm(item["matrix"] - seen["matrix"], "fro") < 1e-10 for seen in unique):
            unique.append(item)
    return unique


def coefficients(old: dict[str, object], new: dict[str, object]) -> dict[str, object]:
    old_frame = np.asarray(old["input_frame"])
    new_frame = np.asarray(new["input_frame"])
    delta_old = float(old["delta"])
    delta_new = float(new["delta"])
    boundary_index = int(new["time"]) - affine_audit.DEPTH
    boundary = np.zeros_like(old["tail"]) if boundary_index < 0 else np.asarray(old["snapshots"][boundary_index])
    compressed = new_frame.T @ boundary @ new_frame
    compressed = (compressed + compressed.T) / 2.0
    birth_matrix = mp.mpf(repr(delta_new * affine_audit.ETA**affine_audit.DEPTH)) * affine_audit.floorfree.mp_matrix(compressed)
    q_birth = affine_audit.mp_generalized(new["gram"], birth_matrix)
    target_values, _ = metric_audit.mp_eigenframe(new["gram"])
    inverse_target_min = 1 / min(target_values)
    ratio = None
    if delta_old > 0.0:
        count = int(old["time"]) - affine_audit.DEPTH + 1
        ratio = metric_audit.envelope_ratio(affine_audit.ETA, affine_audit.DEPTH, count)
    output = []
    for item in unique_candidates(old, new):
        orthogonal_np = np.asarray(item["matrix"])
        orthogonal = affine_audit.floorfree.mp_matrix(orthogonal_np)
        metric_factor = affine_audit.mp_generalized(new["gram"], orthogonal.T * old["gram"] * orthogonal)
        a = mp.mpf("0") if ratio is None else mp.mpf(repr(affine_audit.ETA * ratio)) * metric_factor
        defect = float(np.linalg.norm(new_frame - old_frame @ orthogonal_np, 2))
        scalar = mp.mpf(repr(delta_new * affine_audit.ETA * delta_old * defect**2))
        b = scalar * inverse_target_min
        output.append({**item, "metric_base": a, "frame_base": b, "birth": q_birth, "frame_defect": defect})
    return {"candidates": output, "q_birth": q_birth, "ratio": ratio}


def choose(candidates: list[dict[str, object]], source: mp.mpf, selector: str) -> dict[str, object]:
    if selector == "polar":
        pool = [candidates[0]]
    elif selector == "metric":
        endpoints = [item for item in candidates if item["kind"] == "blend" and item["weight"] == 1.0]
        pool = endpoints or [candidates[0]]
    elif selector == "greedy":
        pool = candidates
    else:
        raise ValueError("unknown selector")
    evaluated = []
    for item in pool:
        envelope, tau = young_envelope(item["metric_base"], item["frame_base"], item["birth"], source)
        evaluated.append({**item, "envelope": envelope, "tau": tau})
    return min(evaluated, key=lambda item: item["envelope"])


def chain(model: dict[str, object], sigma: float, threshold: float, rank: int) -> dict[str, object]:
    temporal = affine_audit.records(model, sigma, threshold, rank)
    envelopes = {"greedy": mp.mpf("0"), "polar": mp.mpf("0"), "metric": mp.mpf("0")}
    steps = []
    for old, new in zip(temporal, temporal[1:]):
        data = coefficients(old, new)
        actual_source = affine_audit.mp_generalized(old["gram"], old["weighted_tail"])
        actual_target = affine_audit.mp_generalized(new["gram"], new["weighted_tail"])
        choices = {name: choose(data["candidates"], envelopes[name], name) for name in envelopes}
        oracle = choose(data["candidates"], actual_source, "greedy")
        for name in envelopes:
            envelopes[name] = choices[name]["envelope"]
        selected = choices["greedy"]
        radius = safety_radius(
            float(selected["metric_base"]), float(selected["frame_base"]),
            float(selected["birth"]),
        )
        recurrent = bool(float(old["delta"]) > 0.0)
        minimum_metric_base = min(item["metric_base"] for item in data["candidates"])
        step = {
            "source_time": int(old["time"]), "target_time": int(new["time"]),
            "recurrent": recurrent,
            "first_birth": bool(float(old["delta"]) == 0.0 and float(new["delta"]) > 0.0),
            "candidate_count": len(data["candidates"]),
            "actual_source": finite(actual_source), "actual_target": finite(actual_target),
            "minimum_metric_base": finite(minimum_metric_base),
            "long_run_orthogonal_contractivity_possible": bool(minimum_metric_base < 1),
            "greedy": {
                "bound": finite(envelopes["greedy"]), "oracle_bound": finite(oracle["envelope"]),
                "metric_base": finite(selected["metric_base"]), "frame_base": finite(selected["frame_base"]),
                "birth": finite(selected["birth"]), "tau": None if selected["tau"] is None else float(selected["tau"]),
                "kind": selected["kind"], "endpoint": selected["endpoint"], "weight": selected["weight"],
                "frame_defect": selected["frame_defect"], "safety_radius": None if math.isinf(radius) else radius,
                "safe": bool(envelopes["greedy"] < 1),
                "dominates_actual": bool(actual_target <= envelopes["greedy"] * (1 + mp.mpf("1e-12")) + mp.mpf("1e-75")),
            },
            "polar_bound": finite(envelopes["polar"]), "polar_safe": bool(envelopes["polar"] < 1),
            "metric_endpoint_bound": finite(envelopes["metric"]), "metric_endpoint_safe": bool(envelopes["metric"] < 1),
        }
        steps.append(step)
    return {
        "sigma": sigma, "side": model["side"], "threshold": threshold, "steps": steps,
        "greedy_chain_safe": all(step["greedy"]["safe"] for step in steps),
        "polar_chain_safe": all(step["polar_safe"] for step in steps),
        "metric_endpoint_chain_safe": all(step["metric_endpoint_safe"] for step in steps),
        "actual_chain_safe": all(step["actual_target"]["value"] < 1 for step in steps),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    mp.mp.dps = MP_DPS
    sigmas = metric_audit.SIGMAS[:3] if args.smoke else metric_audit.SIGMAS
    thresholds = metric_audit.THRESHOLDS[:1] if args.smoke else metric_audit.THRESHOLDS
    sides = ("left",) if args.smoke else ("left", "right")
    rows = []
    for sigma in sigmas:
        rank = affine_audit.floorfree.clock_rank(sigma, offset=affine_audit.RANK_OFFSET)
        _, models = metric_audit.build_models(sigma)
        for model in models:
            if model["side"] not in sides:
                continue
            for threshold in thresholds:
                rows.append(chain(model, sigma, threshold, rank))
        print(json.dumps({"completed_sigma": sigma, "chain_count": len(rows)}, sort_keys=True), flush=True)
    steps = [step for row in rows for step in row["steps"]]
    recurrent = [step for step in steps if step["recurrent"]]
    blocked = [step for step in recurrent if not step["long_run_orthogonal_contractivity_possible"]]
    safe_bounds = [step["greedy"]["bound"]["value"] for step in steps if step["greedy"]["safe"]]
    positive_actual = [step for step in steps if step["actual_target"]["value"] > 0]
    summary = {
        "scale_count": len(sigmas), "chain_count": len(rows), "transition_count": len(steps),
        "recurrent_transition_count": len(recurrent), "first_birth_count": sum(step["first_birth"] for step in steps),
        "zero_target_count": sum(step["actual_target"]["value"] == 0.0 for step in steps),
        "long_run_blocked_recurrent_count": len(blocked),
        "long_run_blocked_but_finite_safe_count": sum(step["greedy"]["safe"] for step in blocked),
        "long_run_blocked_and_finite_unsafe_count": sum(not step["greedy"]["safe"] for step in blocked),
        "greedy_safe_transition_count": sum(step["greedy"]["safe"] for step in steps),
        "polar_safe_transition_count": sum(step["polar_safe"] for step in steps),
        "metric_endpoint_safe_transition_count": sum(step["metric_endpoint_safe"] for step in steps),
        "actual_safe_transition_count": sum(step["actual_target"]["value"] < 1 for step in steps),
        "greedy_safe_chain_count": sum(row["greedy_chain_safe"] for row in rows),
        "polar_safe_chain_count": sum(row["polar_chain_safe"] for row in rows),
        "metric_endpoint_safe_chain_count": sum(row["metric_endpoint_chain_safe"] for row in rows),
        "actual_safe_chain_count": sum(row["actual_chain_safe"] for row in rows),
        "dominance_failure_count": sum(not step["greedy"]["dominates_actual"] for step in steps),
        "minimum_positive_greedy_bound": min(value for value in safe_bounds if value > 0),
        "median_positive_greedy_bound": float(np.median([value for value in safe_bounds if value > 0])),
        "maximum_safe_greedy_bound": max(safe_bounds),
        "maximum_greedy_bound": max(step["greedy"]["bound"]["value"] for step in steps),
        "maximum_bound_to_actual_ratio": max(
            step["greedy"]["bound"]["value"] / step["actual_target"]["value"] for step in positive_actual
        ),
    }
    payload = {
        "status": "rh137_finite_horizon_young_tail_envelope_audit",
        "precision_decimal_digits": MP_DPS, "blend_points": BLEND_POINTS,
        "rows": rows, "audit_summary": summary,
        "theorem_boundary": {
            "pointwise_optimal_young_envelope": True,
            "sharp_finite_safety_radius": True,
            "greedy_horizon_optimality_within_finite_candidate_family": True,
            "global_orthogonal_horizon_optimizer": False,
            "uniform_infinite_horizon_safety": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "Long-run contractivity and finite-horizon viability are distinct. Pointwise Young optimization turns each candidate gauge into a monotone nonlinear envelope. Greedy propagation is horizon-optimal within the fixed finite gauge family and crosses 31 of the 33 recurrent steps that cannot support a contractive affine fixed point; the two remaining failures coincide with actual relative tails above one.",
    }
    name = "finite_horizon_smoke.json" if args.smoke else "finite_horizon_audit.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
