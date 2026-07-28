#!/usr/bin/env python3
"""Generate and verify the TPC-168 separated-registry certificate."""

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
UPSTREAM = REPO / "papers" / "tpc-167-direct-additive-twist-parseval"
OUTPUT = PAPER / "experiments" / "tpc168_registry_sieve_audit.json"
SCHEMA = PAPER / "schemas" / "tpc168-registry-sieve-v1.schema.json"
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


def circle_distance(x: float, y: float) -> float:
    raw = abs(x - y) % 1.0
    return min(raw, 1.0 - raw)


def validate_top_level(obj: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if set(obj) != set(schema["properties"]):
        raise ValueError("strict top-level schema mismatch")
    if obj["schema"] != schema["properties"]["schema"]["const"]:
        raise ValueError("wrong schema id")
    if obj["status"] != "PASS":
        raise ValueError("non-PASS result")


def validate_semantics(obj: dict[str, Any]) -> None:
    theorem = obj["sampling_theorem"]
    registry = obj["registry_corollary"]
    selector = obj["selector_firewall"]
    boundary = obj["claim_boundary"]
    delta = theorem["fixture"]["delta"]
    if not (0 < delta <= 1):
        raise ValueError("delta lies outside the theorem domain")
    if registry["status"] != "PROVED_L1_ACTUAL_CORE_PHASE_METRIC_FINITE_REGISTRY":
        raise ValueError("wrong program status")
    if registry["analytic_norm"] != "L2_PHASE_REGISTRY":
        raise ValueError("wrong analytic norm")
    if registry["program_positive_L2"] is not False or registry["fixed_atom"] is not False:
        raise ValueError("registry average promoted to program L2 or fixed atom")
    if selector["not_meaning"] != "literal_mobius_twist_is_large":
        raise ValueError("coefficient selector fixture promoted to a Mobius lower bound")
    if selector["literal_mobius_lower_bound_claimed"] is not False:
        raise ValueError("coefficient selector fixture promoted to a Mobius lower bound")
    required_false = (
        "program_positive_L2",
        "fixed_atom",
        "distinguished_phase",
        "physical_phase_registry_supplied",
        "one_over_400",
        "prime_pair_lower_bound",
        "twin_prime_theorem",
    )
    if any(boundary[key] is not False for key in required_false):
        raise ValueError("claim boundary promotion")


def mutation_rejected(
    obj: dict[str, Any], path: tuple[str, ...], value: Any
) -> bool:
    clone = json.loads(json.dumps(obj))
    target: Any = clone
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    try:
        validate_semantics(clone)
    except ValueError:
        return True
    return False


def build() -> dict[str, Any]:
    upstream_path = UPSTREAM / "experiments" / "tpc167_parseval_audit.json"
    upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
    if upstream.get("status") != "PASS":
        raise ValueError("TPC-167 audit is not PASS")

    coefficients = [1, -2, 0, 3, -1, 2, 1, 0, -2]
    length = len(coefficients)
    energy = sum(abs(value) ** 2 for value in coefficients)
    registry = [0.013, 0.151, 0.289, 0.427, 0.565, 0.703, 0.841]
    delta = min(
        circle_distance(registry[i], registry[j])
        for i in range(len(registry))
        for j in range(i)
    )
    values = [
        sum(value * e(index * alpha) for index, value in enumerate(coefficients))
        for alpha in registry
    ]
    sample_energy = sum(abs(value) ** 2 for value in values)
    sampling_upper = (1.0 / delta + 4.0 * math.pi * (length - 1)) * energy

    threshold = 4.0
    bad_count = sum(abs(value) > threshold for value in values)
    count_upper = sampling_upper / (threshold * threshold)

    # Selector firewall fixture: the density theorem does not control phase zero.
    selector_length = 128
    selector_grid = [r / 128 for r in range(128)]
    selector_values = [
        abs(sum(e(index * alpha) for index in range(selector_length)))
        / selector_length
        for alpha in selector_grid
    ]
    distinguished_value = selector_values[0]
    density_threshold = 0.25
    selector_bad_count = sum(value > density_threshold for value in selector_values)

    result = {
        "schema": "tpc-168-registry-sieve-audit-v1",
        "status": "PASS",
        "hash_mode": HASH_MODE,
        "upstream": {
            "paper": "TPC-167",
            "audit_sha256": sha256(upstream_path),
            "main_tex_sha256": sha256(UPSTREAM / "main.tex"),
            "audit_status": upstream["status"],
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "sampling_theorem": {
            "export_id": "A168.separated_phase_sampling",
            "status": "PROVED_ANALYTIC_L2_PHASE_SAMPLING",
            "analytic_norm": "L2_PHASE_REGISTRY",
            "delta_domain": "0 < delta <= 1",
            "bound": "sum_j |P(alpha_j)|^2 <= (delta^(-1)+4*pi*(L-1))*sum_n|b_n|^2",
            "fixture": {
                "length": length,
                "registry_size": len(registry),
                "delta": delta,
                "coefficient_energy": energy,
                "sample_energy": sample_energy,
                "analytic_upper": sampling_upper,
                "threshold": threshold,
                "bad_count": bad_count,
                "bad_count_upper": count_upper,
            },
        },
        "registry_corollary": {
            "export_id": "A168.actual_core_registry_density",
            "status": "PROVED_L1_ACTUAL_CORE_PHASE_METRIC_FINITE_REGISTRY",
            "analytic_norm": "L2_PHASE_REGISTRY",
            "program_positive_L2": False,
            "fixed_atom": False,
            "general_bad_count": (
                "lambda^(-2)*(q^2/N^2)*(delta^(-1)+4*pi*(L_N-1))*E_N"
            ),
            "quasi_uniform_assumptions": "delta >= c/M and M >= theta*L_N",
            "bad_fraction": (
                "at_most_(c^(-1)+4*pi/theta)*(q/N+q^2/N^2)/lambda^2"
            ),
            "density_one_threshold": "lambda=(q/N)^(1/4)",
        },
        "selector_firewall": {
            "status": "PROVED_SCOPED_SELECTOR_NONIMPLICATION",
            "fixture": {
                "coefficient": "constant_one",
                "registry_size": len(selector_grid),
                "distinguished_phase": 0.0,
                "distinguished_normalized_value": distinguished_value,
                "threshold": density_threshold,
                "bad_count": selector_bad_count,
                "bad_fraction": selector_bad_count / len(selector_grid),
            },
            "meaning": "density_one_registry_control_does_not_identify_a_named_phase",
            "not_meaning": "literal_mobius_twist_is_large",
            "literal_mobius_lower_bound_claimed": False,
        },
        "route_decision": {
            "advance": "finite_separated_phase_registry_density",
            "original_pointwise_direct_twist_closed": False,
            "required_next": "selector_crosswalk_or_pointwise_phase_theorem",
        },
        "claim_boundary": {
            "actual_fixed_h0_core": True,
            "finite_registry_L2": True,
            "analytic_norm": "L2_PHASE_REGISTRY",
            "program_positive_L2": False,
            "fixed_atom": False,
            "all_but_sparse_registry_phases": True,
            "distinguished_phase": False,
            "physical_phase_registry_supplied": False,
            "one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "checks": {
            "upstream_pass": True,
            "registry_is_delta_separated": 0 < delta <= 1,
            "sampling_bound_holds": sample_energy <= sampling_upper + 1e-10,
            "bad_count_bound_holds": bad_count <= count_upper + 1e-10,
            "selector_distinguished_phase_is_bad": distinguished_value > density_threshold,
            "selector_bad_fraction_is_sparse": selector_bad_count / len(selector_grid) < 0.1,
            "selector_scope_not_promoted": True,
        },
        "mutation_regressions": {},
    }
    validate_top_level(result)
    validate_semantics(result)
    result["mutation_regressions"] = {
        "reject_registry_without_separation_certificate": mutation_rejected(
            result, ("sampling_theorem", "fixture", "delta"), 0
        ),
        "reject_density_one_as_all_phases": mutation_rejected(
            result, ("claim_boundary", "distinguished_phase"), True
        ),
        "reject_named_phase_from_counting_only": mutation_rejected(
            result, ("registry_corollary", "fixed_atom"), True
        ),
        "reject_coefficient_counterexample_as_mobius_lower_bound": mutation_rejected(
            result, ("selector_firewall", "literal_mobius_lower_bound_claimed"), True
        ),
        "reject_phase_registry_as_physical_occurrence_registry": mutation_rejected(
            result, ("claim_boundary", "physical_phase_registry_supplied"), True
        ),
        "reject_fixed_X_phase_power_as_one_over_400": mutation_rejected(
            result, ("claim_boundary", "one_over_400"), True
        ),
    }
    if not all(result["checks"].values()):
        raise AssertionError("TPC-168 check failed")
    if not all(result["mutation_regressions"].values()):
        raise AssertionError("TPC-168 mutation regression failed")
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
            raise SystemExit("TPC-168 CHECK FAIL: stale artifact")
        print("TPC-168 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, encoding="utf-8", newline="\n")
        print("TPC-168 GENERATE PASS")
    print(json.dumps({
        "registry_status": obj["registry_corollary"]["status"],
        "selector_status": obj["selector_firewall"]["status"],
        "pointwise_closed": obj["route_decision"]["original_pointwise_direct_twist_closed"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
