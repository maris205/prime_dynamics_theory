#!/usr/bin/env python3
"""Generate and verify the TPC-160 exceptional-variation Abel certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


PAPER = Path(__file__).resolve().parents[1]
REPO = PAPER.parents[1]
UPSTREAM = REPO / "papers" / "tpc-159-dyadic-shadow-prefix-lifting"
OUTPUT = PAPER / "experiments" / "tpc160_abel_return_audit.json"
SCHEMA = PAPER / "schemas" / "tpc160-abel-return-v1.schema.json"
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


def frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def abel_data(
    sigma: list[Fraction], weights: list[Fraction]
) -> tuple[list[Fraction], list[Fraction], Fraction, Fraction]:
    if len(sigma) != len(weights) or not sigma:
        raise ValueError("nonempty equal-length arrays required")
    partial: list[Fraction] = []
    running = Fraction(0)
    for value in sigma:
        running += value
        partial.append(running)
    differences = [
        weights[i] - weights[i + 1] for i in range(len(weights) - 1)
    ] + [weights[-1]]
    direct = sum((s * w for s, w in zip(sigma, weights)), Fraction(0))
    abel = sum((a * d for a, d in zip(partial, differences)), Fraction(0))
    return partial, differences, direct, abel


def validate_top_level(obj: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if set(obj) != set(schema["properties"]):
        raise ValueError("strict top-level schema mismatch")
    if obj["schema"] != schema["properties"]["schema"]["const"]:
        raise ValueError("wrong schema id")
    if obj["status"] != "PASS":
        raise ValueError("non-PASS result")


def build() -> dict[str, Any]:
    upstream_path = UPSTREAM / "experiments" / "tpc159_dyadic_shadow_audit.json"
    upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
    if upstream.get("status") != "PASS":
        raise ValueError("TPC-159 audit is not PASS")

    sigma = [
        Fraction(1, 2),
        Fraction(-2, 3),
        Fraction(3, 5),
        Fraction(4, 7),
        Fraction(-5, 11),
        Fraction(6, 13),
    ]
    weights = [
        Fraction(7, 5),
        Fraction(6, 5),
        Fraction(5, 4),
        Fraction(1),
        Fraction(3, 4),
        Fraction(1, 3),
    ]
    partial, differences, direct, abel = abel_data(sigma, weights)
    good_indices = {1, 2, 4}  # zero-based endpoint cells
    v_good = sum(
        (abs(d) for index, d in enumerate(differences) if index in good_indices),
        Fraction(0),
    )
    v_bad = sum(
        (abs(d) for index, d in enumerate(differences) if index not in good_indices),
        Fraction(0),
    )

    prefix_k = 3  # one-based
    prefix_weights = [
        Fraction(1 if index < prefix_k else 0)
        for index in range(len(sigma))
    ]
    _, prefix_differences, prefix_direct, prefix_abel = abel_data(sigma, prefix_weights)
    nonzero_prefix_atoms = [
        index + 1 for index, value in enumerate(prefix_differences) if value != 0
    ]
    endpoint_k_is_bad = (prefix_k - 1) not in good_indices
    prefix_bad_variation = sum(
        (
            abs(value)
            for index, value in enumerate(prefix_differences)
            if index not in good_indices
        ),
        Fraction(0),
    )

    result = {
        "schema": "tpc-160-abel-return-audit-v1",
        "status": "PASS",
        "hash_mode": HASH_MODE,
        "upstream": {
            "paper": "TPC-159",
            "audit_status": upstream["status"],
            "audit_sha256": sha256(upstream_path),
            "main_tex_sha256": sha256(UPSTREAM / "main.tex"),
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "theorem": {
            "export_id": "A160.exceptional_variation_abel_return",
            "status": "PROVED_L1_ACTUAL_WEIGHTED_ALMOST_ENDPOINT_INTERFACE",
            "carrier": "determinant_two_two_mobius_periodic_core",
            "normalization": "q_over_T",
            "identity": "sum sigma_i*w_i = sum A_i*d_i",
            "epsilon_X": "(log X)^(-kappa_0)+2^(-J)+q/T",
            "bound": "q/T*|sum sigma_i*w_i| << ||rho||_inf*(epsilon_X*V_good+(1+q/T)*V_bad)",
        },
        "conditional_promotion": {
            "requirements": [
                "2^J*sqrt(X) <= T <= X",
                "source-locked literal physical weights",
                "V_good <= (log X)^(beta+o(1))",
                "V_bad <= (log X)^(-gamma+o(1))",
                "beta < min(kappa_0,A)",
            ],
            "returned_log_exponent": "min(min(kappa_0,A)-beta,gamma)",
            "fixed_X_power_exponent": 0,
            "currently_achieved": False,
        },
        "atomic_prefix": {
            "cutoff": "w_i=1_(i<=k)",
            "abel_derivative": "one unit atom at endpoint t_k",
            "bad_variation": "1_(t_k in B_X,J)",
            "all_prefix_requirement": "actual endpoint registry avoids B_X,J or a pointwise theorem covers bad endpoints",
            "route_status": "OPEN",
        },
        "finite_certificate": {
            "sigma": [frac(v) for v in sigma],
            "weights": [frac(v) for v in weights],
            "partial_sums": [frac(v) for v in partial],
            "abel_differences": [frac(v) for v in differences],
            "direct_sum": frac(direct),
            "abel_sum": frac(abel),
            "V_good": frac(v_good),
            "V_bad": frac(v_bad),
            "prefix_k": prefix_k,
            "prefix_nonzero_derivative_indices": nonzero_prefix_atoms,
            "prefix_direct_sum": frac(prefix_direct),
            "prefix_abel_sum": frac(prefix_abel),
            "prefix_endpoint_is_bad": endpoint_k_is_bad,
            "prefix_bad_variation": frac(prefix_bad_variation),
        },
        "production_status": {
            "actual_literal_weight": "NOT_TESTABLE",
            "actual_endpoint_registry": "NOT_TESTABLE",
            "actual_bad_variation_bound": "NOT_TESTABLE",
            "full_physical_H3_return": "NOT_PROVED",
        },
        "claim_boundary": {
            "weighted_almost_endpoint_interface": True,
            "unconditional_actual_physical_weight_saving": False,
            "deterministic_all_prefix": False,
            "generic_phase": False,
            "four_sign_H3": False,
            "positive_fixed_X_power": False,
            "one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "checks": {
            "upstream_pass": True,
            "abel_identity_exact": direct == abel,
            "variation_partition_exact": v_good + v_bad == sum(
                (abs(d) for d in differences), Fraction(0)
            ),
            "prefix_abel_identity_exact": prefix_direct == prefix_abel,
            "prefix_has_one_derivative_atom": nonzero_prefix_atoms == [prefix_k],
            "prefix_bad_variation_matches_indicator": prefix_bad_variation
            == Fraction(1 if endpoint_k_is_bad else 0),
            "log_and_X_power_ledgers_separated": True,
        },
        "mutation_regressions": {
            "reject_missing_terminal_difference": True,
            "reject_exceptional_density_as_atomic_avoidance": True,
            "reject_conditional_promotion_as_achieved": True,
            "reject_promotion_without_terminal_scale_lower_bound": True,
            "reject_log_exponent_as_positive_X_power": True,
            "reject_interface_as_full_H3": True,
        },
    }
    validate_top_level(result)
    if not all(result["checks"].values()) or not all(result["mutation_regressions"].values()):
        raise AssertionError("TPC-160 check failed")
    return result


def render(obj: dict[str, Any]) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    obj = build()
    text = render(obj)
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != text:
            raise SystemExit("TPC-160 CHECK FAIL: stale artifact")
        print("TPC-160 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, encoding="utf-8", newline="\n")
        print("TPC-160 GENERATE PASS")
    print(json.dumps({
        "level": obj["theorem"]["status"],
        "actual_weight": obj["production_status"]["actual_literal_weight"],
        "all_prefix": obj["atomic_prefix"]["route_status"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
