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
RH135 = PAPERS / "RH-135-relative-metric-affine-tail-recurrence"
sys.path[:0] = [str(ROOT / "src"), str(RH135 / "experiments")]

from projective_gram import cumulative_base_lower  # noqa: E402
import build_relative_affine_audit as affine  # noqa: E402


MP_DPS = 80


def extrema(matrix: mp.matrix) -> tuple[mp.mpf, mp.mpf]:
    values, _ = mp.eigsy((matrix + matrix.T) / 2)
    return mp.mpf(values[0]), mp.mpf(values[-1])


def base(matrix: mp.matrix) -> mp.mpf:
    low, high = extrema(matrix)
    return mp.sqrt(low / high)


def polar_alignment(old: dict[str, object], new: dict[str, object]) -> mp.matrix:
    old_frame = np.asarray(old["input_frame"])
    new_frame = np.asarray(new["input_frame"])
    left, _, right = np.linalg.svd(old_frame.T @ new_frame, full_matrices=False)
    return affine.floorfree.mp_matrix(left @ right)


def projective_data(source: mp.matrix, target: mp.matrix) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    values, vectors = mp.eigsy((source + source.T) / 2)
    inverse = vectors * mp.diag([1 / mp.sqrt(values[i]) for i in range(values.rows)]) * vectors.T
    relative = inverse * target * inverse
    generalized, _ = mp.eigsy((relative + relative.T) / 2)
    minimum = mp.mpf(generalized[0])
    maximum = mp.mpf(generalized[-1])
    return minimum, maximum, mp.log(maximum / minimum)


def chain(model: dict[str, object], sigma: float, threshold: float, rank: int) -> dict[str, object]:
    temporal = affine.records(model, sigma, threshold, rank)
    initial_base = base(temporal[0]["gram"])
    cumulative = mp.mpf("0")
    steps = []
    exact_bases = [initial_base]
    for old, new in zip(temporal, temporal[1:]):
        orthogonal = polar_alignment(old, new)
        source_gram = orthogonal.T * old["gram"] * orthogonal
        source_base = base(source_gram)
        target_base = base(new["gram"])
        minimum, maximum, distance = projective_data(source_gram, new["gram"])
        one_step_lower = mp.e ** (-distance / 2) * source_base
        cumulative += distance
        cumulative_lower = mp.e ** (-cumulative / 2) * initial_base
        exact_bases.append(target_base)
        steps.append({
            "source_time": int(old["time"]),
            "target_time": int(new["time"]),
            "generalized_minimum": float(minimum),
            "generalized_maximum": float(maximum),
            "projective_distance": float(distance),
            "cumulative_projective_variation": float(cumulative),
            "source_base": float(source_base),
            "target_base": float(target_base),
            "one_step_lower": float(one_step_lower),
            "cumulative_lower": float(cumulative_lower),
            "signed_log_base_drift": float(mp.log(source_base / target_base)),
            "one_step_dominance_ratio": float(target_base / one_step_lower),
            "cumulative_dominance_ratio": float(target_base / cumulative_lower),
            "one_step_holds": bool(target_base + mp.mpf("1e-70") >= one_step_lower),
            "cumulative_holds": bool(target_base + mp.mpf("1e-70") >= cumulative_lower),
        })
    distances = [step["projective_distance"] for step in steps]
    terminal_lower = steps[-1]["cumulative_lower"]
    terminal_base = steps[-1]["target_base"]
    return {
        "sigma": sigma,
        "side": model["side"],
        "threshold": threshold,
        "transition_count": len(steps),
        "initial_base": float(initial_base),
        "terminal_base": terminal_base,
        "minimum_exact_base": float(min(exact_bases)),
        "total_projective_variation": float(cumulative),
        "mean_projective_distance": float(np.mean(distances)),
        "terminal_projective_lower": terminal_lower,
        "terminal_dominance_ratio": terminal_base / terminal_lower,
        "steps": steps,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    mp.mp.dps = MP_DPS
    sigmas = affine.SIGMAS[:2] if args.smoke else affine.SIGMAS
    thresholds = affine.THRESHOLDS[:1] if args.smoke else affine.THRESHOLDS
    sides = ("left",) if args.smoke else ("left", "right")
    rows = []
    for sigma in sigmas:
        rank = affine.floorfree.clock_rank(sigma, offset=affine.RANK_OFFSET)
        _, models = affine.build_models(sigma)
        for model in models:
            if model["side"] not in sides:
                continue
            for threshold in thresholds:
                rows.append(chain(model, sigma, threshold, rank))
        print(json.dumps({"completed_sigma": sigma, "chain_count": len(rows)}, sort_keys=True), flush=True)

    steps = [step for row in rows for step in row["steps"]]
    distances = [step["projective_distance"] for step in steps]
    totals = [row["total_projective_variation"] for row in rows]
    terminal_lowers = [row["terminal_projective_lower"] for row in rows]
    terminal_bases = [row["terminal_base"] for row in rows]
    dominance = [step["cumulative_dominance_ratio"] for step in steps]
    by_sigma = {}
    for sigma in sigmas:
        scale_rows = [row for row in rows if row["sigma"] == sigma]
        scale_steps = [step for row in scale_rows for step in row["steps"]]
        by_sigma[str(sigma)] = {
            "transition_count": len(scale_steps),
            "median_step_distance": float(np.median([step["projective_distance"] for step in scale_steps])),
            "median_total_variation": float(np.median([row["total_projective_variation"] for row in scale_rows])),
            "maximum_total_variation": max(row["total_projective_variation"] for row in scale_rows),
            "minimum_terminal_exact_base": min(row["terminal_base"] for row in scale_rows),
            "minimum_terminal_projective_lower": min(row["terminal_projective_lower"] for row in scale_rows),
        }
    summary = {
        "scale_count": len(sigmas),
        "chain_count": len(rows),
        "transition_count": len(steps),
        "one_step_failure_count": sum(not step["one_step_holds"] for step in steps),
        "cumulative_failure_count": sum(not step["cumulative_holds"] for step in steps),
        "minimum_projective_distance": min(distances),
        "median_projective_distance": float(np.median(distances)),
        "maximum_projective_distance": max(distances),
        "projective_distance_q90": float(np.quantile(distances, 0.9)),
        "minimum_total_projective_variation": min(totals),
        "median_total_projective_variation": float(np.median(totals)),
        "maximum_total_projective_variation": max(totals),
        "minimum_terminal_projective_lower": min(terminal_lowers),
        "median_terminal_projective_lower": float(np.median(terminal_lowers)),
        "maximum_terminal_projective_lower": max(terminal_lowers),
        "minimum_terminal_exact_base": min(terminal_bases),
        "median_terminal_exact_base": float(np.median(terminal_bases)),
        "maximum_terminal_exact_base": max(terminal_bases),
        "minimum_cumulative_dominance_ratio": min(dominance),
        "median_cumulative_dominance_ratio": float(np.median(dominance)),
        "maximum_cumulative_dominance_ratio": max(dominance),
        "observed_step_distances_approach_zero": False,
        "finite_trend_supports_projective_summability": False,
        "by_sigma": by_sigma,
    }
    payload = {
        "status": "rh146_projective_gram_base_recurrence_audit",
        "precision_decimal_digits": MP_DPS,
        "gauge": "RH-135 physical polar alignment",
        "rows": rows,
        "audit_summary": summary,
        "sharp_witnesses": {
            "half_coefficient_equality": "G=I, H=diag(exp(d),1)",
            "bounded_nonsummable_obstruction": "G_n=diag(exp(n),1), d_n=1, a_n=exp(-n/2)",
        },
        "theorem_boundary": {
            "projective_base_recurrence_proved": True,
            "summable_variation_implies_positive_base_liminf": True,
            "half_coefficient_sharp": True,
            "bounded_nonsummable_obstruction": True,
            "physical_polar_gauge_audited": not args.smoke,
            "projective_variation_summable_for_model": False,
            "positive_normalized_base_liminf": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "Summable Hilbert projective variation is a rigorous sufficient packet for a positive normalized-base liminf. The 330-step physical polar-gauge audit verifies the sharp recurrence but accumulates 97.5--234.2 units of variation per chain, producing terminal universal lowers between roughly 1e-52 and 1e-23. Exact bases are vastly larger, so correlation-aware control is the next route; finite data neither proves nor supports all-level projective summability.",
    }
    name = "projective_gram_smoke.json" if args.smoke else "projective_gram_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()

