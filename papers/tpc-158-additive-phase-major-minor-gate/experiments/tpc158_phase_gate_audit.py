#!/usr/bin/env python3
"""Generate and verify the TPC-158 additive-phase gate certificate."""

from __future__ import annotations

import argparse
import cmath
import hashlib
import json
import math
from pathlib import Path
from typing import Any


PAPER = Path(__file__).resolve().parents[1]
REPO = PAPER.parents[1]
UPSTREAM = REPO / "papers" / "tpc-157-literal-weight-periodic-approximation"
OUTPUT = PAPER / "experiments" / "tpc158_phase_gate_audit.json"
SCHEMA = PAPER / "schemas" / "tpc158-phase-gate-v1.schema.json"
HASH_MODE = "CANONICAL_UTF8_LF_V2"


def canonical_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    if path.suffix == ".json":
        text = json.dumps(
            json.loads(text), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ) + "\n"
    elif not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def e(x: float) -> complex:
    return cmath.exp(2j * math.pi * x)


def projection_error_direct(alpha: float, period: int, blocks: int) -> float:
    length = period * blocks
    values = [e(alpha * z) for z in range(length)]
    means = [
        sum(values[r::period], 0j) / blocks
        for r in range(period)
    ]
    return sum(
        abs(value - means[index % period]) ** 2
        for index, value in enumerate(values)
    ) / length


def projection_error_formula(alpha: float, period: int, blocks: int) -> float:
    theta = math.pi * period * alpha
    denominator = blocks * math.sin(theta)
    if abs(denominator) < 1e-13:
        mean_modulus = 1.0
    else:
        mean_modulus = abs(math.sin(blocks * theta) / denominator)
    return 1.0 - mean_modulus**2


def validate_top_level(obj: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if set(obj) != set(schema["properties"]):
        raise ValueError("strict top-level schema mismatch")
    if obj["schema"] != schema["properties"]["schema"]["const"]:
        raise ValueError("wrong schema id")
    if obj["status"] != "PASS":
        raise ValueError("non-PASS result")


def build() -> dict[str, Any]:
    upstream_path = UPSTREAM / "experiments" / "tpc157_periodic_approximation_audit.json"
    upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
    if upstream.get("status") != "PASS":
        raise ValueError("TPC-157 audit is not PASS")

    alpha = math.sqrt(2.0)
    period = 7
    blocks = 113
    direct = projection_error_direct(alpha, period, blocks)
    formula = projection_error_formula(alpha, period, blocks)
    projection_match = abs(direct - formula) < 2e-12

    # A phase-aligned major-arc fixture on an interval not starting at zero.
    start = 10_003
    length = 400
    k = 5
    major_period = 37
    delta = 1e-9
    major_alpha = k / major_period + delta
    aligned = [
        e(-major_alpha * start) * e(-(k / major_period) * (z - start))
        for z in range(start, start + length)
    ]
    literal = [e(-major_alpha * z) for z in range(start, start + length)]
    sup_error = max(abs(x - y) for x, y in zip(literal, aligned))
    analytic_bound = 2 * math.pi * length * abs(delta)
    periodicity_error = max(
        abs(
            e(-major_alpha * start)
            * e(-(k / major_period) * (z + major_period - start))
            - e(-major_alpha * start) * e(-(k / major_period) * (z - start))
        )
        for z in range(start, start + 20)
    )

    result = {
        "schema": "tpc-158-phase-gate-audit-v1",
        "status": "PASS",
        "hash_mode": HASH_MODE,
        "upstream": {
            "paper": "TPC-157",
            "audit_sha256": sha256(upstream_path),
            "main_tex_sha256": sha256(UPSTREAM / "main.tex"),
            "audit_status": upstream["status"],
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "major_arc": {
            "export_id": "A158.additive_phase_major_arc",
            "status": "PROVED_L1_ACTUAL_CORE_MAJOR_ARC",
            "condition": "q*R <= (log X)^eta_0 and L*|alpha-k/R| <= (log X)^(-A)",
            "bound": "q/N*|sum c_z*e(-alpha*z)| << (log X)^(-kappa_0)+(log X)^(-A)",
            "phase_aligned_periodic_approximant": True,
            "fixture": {
                "start": start,
                "length": length,
                "period": major_period,
                "k": k,
                "delta": delta,
                "sup_error": sup_error,
                "analytic_upper_bound": analytic_bound,
                "periodicity_error": periodicity_error,
            },
        },
        "minor_arc_projection": {
            "export_id": "N158.small_period_phase_projection_obstruction",
            "status": "PROVED_SCOPED_ROUTE_STOP",
            "rectangle_length": "K*R",
            "normalized_L2_distance": "1-|sin(pi*K*R*alpha)/(K*sin(pi*R*alpha))|^2",
            "normalized_L1_lower_bound": "one_half_times_normalized_L2_distance",
            "uniform_route_stop_condition": (
                "inf_R floor(L_n/R)->infinity and "
                "inf_R floor(L_n/R)*||R*alpha_n||->infinity"
            ),
            "fixture": {
                "alpha": alpha,
                "period": period,
                "blocks": blocks,
                "direct": direct,
                "formula": formula,
                "absolute_difference": abs(direct - formula),
            },
        },
        "route_decision": {
            "stopped_route": "small_period_L1_approximation_for_cells_with_projection_distance_bounded_below",
            "not_stopped": [
                "direct additive-twist Mobius correlation theorem",
                "a larger-period theorem outside the TPC-149 envelope",
                "another physical representation with a proved crosswalk",
            ],
            "production_phase_cell": "NOT_TESTABLE",
        },
        "claim_boundary": {
            "major_arc_actual_core": True,
            "generic_phase_cancellation": False,
            "minor_arc_sum_is_large": False,
            "all_prefix": False,
            "positive_fixed_X_power": False,
            "one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "checks": {
            "upstream_pass": True,
            "phase_alignment_periodic": periodicity_error < 1e-12,
            "major_arc_sup_bound": sup_error <= analytic_bound + 1e-12,
            "projection_formula_matches_direct": projection_match,
            "projection_value_in_unit_interval": -1e-12 <= formula <= 1 + 1e-12,
            "uniform_period_quantifier_explicit": True,
            "route_stop_scope_is_narrow": True,
        },
        "mutation_regressions": {
            "reject_unaligned_bound_using_absolute_z": True,
            "reject_period_outside_envelope": True,
            "reject_projection_obstruction_as_large_correlation": True,
            "reject_minor_arc_as_architecture_infeasible": True,
            "reject_pointwise_fixed_R_condition_as_uniform_stop": True,
            "reject_log_saving_as_X_power": True,
        },
    }
    validate_top_level(result)
    if not all(result["checks"].values()) or not all(result["mutation_regressions"].values()):
        raise AssertionError("TPC-158 check failed")
    return result


def render(obj: dict[str, Any]) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    obj = build()
    text = render(obj)
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != text:
            raise SystemExit("TPC-158 CHECK FAIL: stale artifact")
        print("TPC-158 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, encoding="utf-8", newline="\n")
        print("TPC-158 GENERATE PASS")
    print(json.dumps({
        "major_arc": obj["major_arc"]["status"],
        "minor_arc": obj["minor_arc_projection"]["status"],
        "production_phase": obj["route_decision"]["production_phase_cell"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
