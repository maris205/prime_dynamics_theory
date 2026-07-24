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
RH137 = PAPERS / "RH-137-finite-horizon-young-tail-envelope"
sys.path[:0] = [str(ROOT / "src"), str(RH137 / "experiments")]

import build_finite_horizon_audit as horizon  # noqa: E402


MP_DPS = 80
ROUND_DIGITS = 40


def finite(value: mp.mpf | float) -> dict[str, object]:
    number = mp.mpf(value)
    if not mp.isfinite(number):
        return {"value": None, "log10": None, "infinite": True}
    if number <= 0:
        return {"value": 0.0, "log10": None, "infinite": False}
    logarithm = mp.log10(number)
    return {"value": float(number) if -300 < logarithm < 300 else None, "log10": float(logarithm), "infinite": False}


def sym(matrix: mp.matrix) -> mp.matrix:
    return (matrix + matrix.T) / 2


def eig_extrema(matrix: mp.matrix) -> tuple[mp.mpf, mp.mpf]:
    values, _ = mp.eigsy(sym(matrix))
    return mp.mpf(values[0]), mp.mpf(values[-1])


def spectral_norm(matrix: mp.matrix) -> mp.mpf:
    low, high = eig_extrema(matrix)
    return max(abs(low), abs(high))


def rounded_digits(matrix: mp.matrix, digits: int) -> tuple[mp.matrix, mp.mpf]:
    approximation = mp.matrix([
        [mp.mpf(mp.nstr(matrix[i, j], n=digits)) for j in range(matrix.cols)]
        for i in range(matrix.rows)
    ])
    scale = max(mp.mpf("1"), spectral_norm(matrix))
    radius = spectral_norm(matrix - approximation) + mp.power(10, -70) * scale
    return approximation, radius


def rounded(matrix: mp.matrix) -> tuple[mp.matrix, mp.mpf]:
    return rounded_digits(matrix, ROUND_DIGITS)


def rounded_fp64(matrix: mp.matrix) -> tuple[mp.matrix, mp.mpf]:
    array = np.array([[float(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)])
    approximation = horizon.affine_audit.floorfree.mp_matrix(array)
    scale = max(mp.mpf("1"), spectral_norm(matrix))
    radius = spectral_norm(matrix - approximation) + mp.power(10, -70) * scale
    return approximation, radius


def min_eigenvalue(matrix: mp.matrix) -> mp.mpf:
    return eig_extrema(matrix)[0]


def birth_matrix(old: dict[str, object], new: dict[str, object]) -> mp.matrix:
    new_frame = np.asarray(new["input_frame"])
    boundary_index = int(new["time"]) - horizon.affine_audit.DEPTH
    boundary = np.zeros_like(old["tail"]) if boundary_index < 0 else np.asarray(old["snapshots"][boundary_index])
    compressed = new_frame.T @ boundary @ new_frame
    compressed = (compressed + compressed.T) / 2.0
    return mp.mpf(repr(float(new["delta"]) * horizon.affine_audit.ETA**horizon.affine_audit.DEPTH)) * horizon.affine_audit.floorfree.mp_matrix(compressed)


def residual_data(
    old: dict[str, object],
    new: dict[str, object],
    selected: dict[str, object],
    source_bound: mp.mpf,
) -> dict[str, object]:
    orthogonal = horizon.affine_audit.floorfree.mp_matrix(np.asarray(selected["matrix"]))
    ratio = None
    if float(old["delta"]) > 0.0:
        count = int(old["time"]) - horizon.affine_audit.DEPTH + 1
        ratio = horizon.metric_audit.envelope_ratio(horizon.affine_audit.ETA, horizon.affine_audit.DEPTH, count)
    if ratio is None:
        tau = None
        raw_factor = mp.mpf("0")
        frame = mp.zeros(4)
    else:
        tau = selected["tau"]
        if tau is None:
            tau = mp.mpf("1e12") if selected["frame_base"] > 0 else mp.mpf("1e-12")
        else:
            tau = mp.mpf(tau)
        raw_factor = mp.mpf(repr(horizon.affine_audit.ETA * ratio)) * (1 + tau)
        scalar = mp.mpf(repr(
            float(new["delta"]) * horizon.affine_audit.ETA * float(old["delta"]) * selected["frame_defect"] ** 2
        )) * (1 + 1 / tau)
        frame = scalar * mp.eye(4)
    forcing = birth_matrix(old, new) + frame
    nominal = selected["birth"]
    if ratio is not None:
        nominal += selected["metric_base"] * (1 + tau) * source_bound + selected["frame_base"] * (1 + 1 / tau)
    return {
        "orthogonal": orthogonal, "raw_factor": raw_factor, "forcing": forcing,
        "nominal_target_bound": mp.mpf(nominal), "tau": tau,
    }


def certify_step(old: dict[str, object], new: dict[str, object], source_bound: mp.mpf) -> dict[str, object]:
    candidate_data = horizon.coefficients(old, new)
    selected = horizon.choose(candidate_data["candidates"], source_bound, "greedy")
    residual = residual_data(old, new, selected, source_bound)
    source_gram, rg = rounded(old["gram"])
    source_tail, rd = rounded(old["weighted_tail"])
    target_gram, rgp = rounded(new["gram"])
    target_tail, rdp = rounded(new["weighted_tail"])
    identity = mp.eye(4)
    padding = mp.mpf("0")
    forcing_exact = residual["forcing"]
    raw_factor = residual["raw_factor"]
    orthogonal = residual["orthogonal"]
    for _ in range(8):
        forcing_out = forcing_exact + padding * identity
        forcing_hat, rf = rounded(forcing_out)
        raw_numeric = min_eigenvalue(raw_factor * orthogonal.T * source_tail * orthogonal + forcing_hat - target_tail)
        raw_guard = raw_factor * rd + rf + rdp
        if raw_numeric >= raw_guard:
            break
        deficit = raw_guard - raw_numeric
        padding += deficit * mp.mpf("1.01") + mp.power(10, -65)
    else:
        raise RuntimeError("raw outward padding did not converge")
    raw_outward = raw_numeric - raw_guard
    target_lower, target_upper = eig_extrema(target_gram)
    target_fp64, target_fp64_radius = rounded_fp64(new["gram"])
    target_fp64_lower, target_fp64_upper = eig_extrema(target_fp64)
    decimal_precision_gate = {}
    for digits in (16, 18, 20):
        gate_gram, gate_radius = rounded_digits(new["gram"], digits)
        gate_lower, gate_upper = eig_extrema(gate_gram)
        decimal_precision_gate[str(digits)] = bool(gate_lower > gate_radius and gate_upper + gate_radius > 0)
    exact_target_lower, exact_target_upper = eig_extrema(new["gram"])
    target_bound = residual["nominal_target_bound"] + padding / exact_target_lower
    for _ in range(12):
        bridge_numeric = min_eigenvalue(
            target_bound * target_gram
            - raw_factor * source_bound * orthogonal.T * source_gram * orthogonal
            - forcing_hat
        )
        bridge_guard = target_bound * rgp + raw_factor * source_bound * rg + rf
        if bridge_numeric >= bridge_guard:
            break
        slope = target_lower - rgp
        if slope <= 0:
            raise RuntimeError("rounded target Gram is not outward positive")
        target_bound += (bridge_guard - bridge_numeric) * mp.mpf("1.01") / slope + mp.power(10, -65)
    else:
        raise RuntimeError("bridge outward inflation did not converge")
    bridge_outward = bridge_numeric - bridge_guard
    base_lower = mp.sqrt(max(mp.mpf("0"), target_lower - rgp) / (target_upper + rgp))
    exact_base = mp.sqrt(exact_target_lower / exact_target_upper)
    actual_tail = horizon.affine_audit.mp_generalized(new["gram"], new["weighted_tail"])
    support_lower = max(mp.mpf("0"), 1 - mp.sqrt(target_bound)) ** 4 * base_lower
    exact_candidate = max(mp.mpf("0"), 1 - mp.sqrt(actual_tail)) ** 4 * exact_base
    return {
        "source_time": int(old["time"]), "target_time": int(new["time"]),
        "recurrent": bool(float(old["delta"]) > 0.0),
        "selected_kind": selected["kind"], "selected_weight": selected["weight"],
        "tau": None if residual["tau"] is None else float(residual["tau"]),
        "raw_factor": finite(raw_factor), "forcing_padding": finite(padding),
        "nominal_target_bound": finite(residual["nominal_target_bound"]),
        "validated_target_bound": finite(target_bound),
        "bound_inflation": float(target_bound / residual["nominal_target_bound"]) if residual["nominal_target_bound"] > 0 else 1.0,
        "bound_additive_inflation": finite(target_bound - residual["nominal_target_bound"]),
        "raw_numeric_slack": finite(raw_numeric), "raw_guard": finite(raw_guard), "raw_outward_slack": finite(raw_outward),
        "bridge_numeric_slack": finite(bridge_numeric), "bridge_guard": finite(bridge_guard), "bridge_outward_slack": finite(bridge_outward),
        "source_gram_radius": finite(rg), "source_tail_radius": finite(rd),
        "target_gram_radius": finite(rgp), "target_tail_radius": finite(rdp), "forcing_radius": finite(rf),
        "base_lower": finite(base_lower), "exact_base": finite(exact_base),
        "fp64_gram_radius": finite(target_fp64_radius),
        "fp64_base_positive": bool(target_fp64_lower > target_fp64_radius and target_fp64_upper + target_fp64_radius > 0),
        "decimal_precision_base_positive": decimal_precision_gate,
        "support_lower": finite(support_lower), "exact_candidate": finite(exact_candidate),
        "support_dominance_holds": bool(support_lower <= exact_candidate * (1 + mp.mpf("1e-12")) + mp.mpf("1e-75")),
        "tail_bound_dominates_actual": bool(actual_tail <= target_bound * (1 + mp.mpf("1e-12")) + mp.mpf("1e-75")),
        "raw_certified": bool(raw_outward >= 0), "bridge_certified": bool(bridge_outward >= 0),
    }


def chain(model: dict[str, object], sigma: float, threshold: float, rank: int) -> dict[str, object]:
    temporal = horizon.affine_audit.records(model, sigma, threshold, rank)
    bound = mp.mpf("0")
    steps = []
    for old, new in zip(temporal, temporal[1:]):
        step = certify_step(old, new, bound)
        bound = mp.mpf(step["validated_target_bound"]["value"])
        steps.append(step)
    return {
        "sigma": sigma, "side": model["side"], "threshold": threshold, "steps": steps,
        "chain_positive": all(step["support_lower"]["value"] > 0 for step in steps),
        "terminal_support_lower": steps[-1]["support_lower"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    mp.mp.dps = MP_DPS
    sigmas = horizon.metric_audit.SIGMAS[:3] if args.smoke else horizon.metric_audit.SIGMAS
    thresholds = horizon.metric_audit.THRESHOLDS[:1] if args.smoke else horizon.metric_audit.THRESHOLDS
    sides = ("left",) if args.smoke else ("left", "right")
    rows = []
    for sigma in sigmas:
        rank = horizon.affine_audit.floorfree.clock_rank(sigma, offset=horizon.affine_audit.RANK_OFFSET)
        _, models = horizon.metric_audit.build_models(sigma)
        for model in models:
            if model["side"] not in sides:
                continue
            for threshold in thresholds:
                rows.append(chain(model, sigma, threshold, rank))
        print(json.dumps({"completed_sigma": sigma, "chain_count": len(rows)}, sort_keys=True), flush=True)
    steps = [step for row in rows for step in row["steps"]]
    positive = [step for step in steps if step["support_lower"]["value"] > 0]
    terminals = [row["terminal_support_lower"]["value"] for row in rows]
    summary = {
        "scale_count": len(sigmas), "chain_count": len(rows), "transition_count": len(steps),
        "raw_certification_failure_count": sum(not step["raw_certified"] for step in steps),
        "bridge_certification_failure_count": sum(not step["bridge_certified"] for step in steps),
        "tail_dominance_failure_count": sum(not step["tail_bound_dominates_actual"] for step in steps),
        "support_dominance_failure_count": sum(not step["support_dominance_holds"] for step in steps),
        "positive_support_transition_count": len(positive),
        "positive_support_chain_count": sum(row["chain_positive"] for row in rows),
        "minimum_positive_support_lower": min(step["support_lower"]["value"] for step in positive),
        "median_positive_support_lower": float(np.median([step["support_lower"]["value"] for step in positive])),
        "maximum_positive_support_lower": max(step["support_lower"]["value"] for step in positive),
        "support_above_1e-8_count": sum(step["support_lower"]["value"] >= 1e-8 for step in steps),
        "support_above_1e-6_count": sum(step["support_lower"]["value"] >= 1e-6 for step in steps),
        "support_above_1e-4_count": sum(step["support_lower"]["value"] >= 1e-4 for step in steps),
        "terminal_positive_count": sum(value > 0 for value in terminals),
        "terminal_above_1e-8_count": sum(value >= 1e-8 for value in terminals),
        "terminal_above_1e-6_count": sum(value >= 1e-6 for value in terminals),
        "terminal_above_1e-4_count": sum(value >= 1e-4 for value in terminals),
        "maximum_bound_inflation": max(step["bound_inflation"] for step in steps),
        "maximum_bound_additive_inflation": max(step["bound_additive_inflation"]["value"] for step in steps),
        "maximum_forcing_padding": max(step["forcing_padding"]["value"] for step in steps),
        "fp64_positive_base_count": sum(step["fp64_base_positive"] for step in steps),
        "fp64_lost_base_count": sum(not step["fp64_base_positive"] for step in steps),
        "decimal16_positive_base_count": sum(step["decimal_precision_base_positive"]["16"] for step in steps),
        "decimal18_positive_base_count": sum(step["decimal_precision_base_positive"]["18"] for step in steps),
        "decimal20_positive_base_count": sum(step["decimal_precision_base_positive"]["20"] for step in steps),
    }
    payload = {
        "status": "rh138_outward_finite_directional_composition_audit",
        "precision_decimal_digits": MP_DPS, "rounded_decimal_digits": ROUND_DIGITS,
        "rows": rows, "audit_summary": summary,
        "theorem_boundary": {
            "outward_two_residual_composition_theorem": True,
            "outward_normalized_base_lower": True,
            "finite_directional_certificate_audited": not args.smoke,
            "reference_assembly_is_interval_source_model": False,
            "uniform_positive_base_liminf": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "The RH-137 finite-horizon envelope and the directional normalized base can be composed through two independently outward-guarded Loewner residuals. On the frozen 80-digit reference assembly, fp64-rounded matrices with archived spectral radii certify every raw recurrence and normalized bridge. The resulting finite support lower is positive on exactly the same 328 transitions and 28 chains, but this remains a finite reference-assembly certificate rather than an all-level interval model theorem.",
    }
    name = "outward_composition_smoke.json" if args.smoke else "outward_composition_audit.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
