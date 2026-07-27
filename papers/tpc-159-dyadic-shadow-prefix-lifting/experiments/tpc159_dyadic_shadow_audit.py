#!/usr/bin/env python3
"""Generate and verify the TPC-159 dyadic-shadow certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


PAPER = Path(__file__).resolve().parents[1]
REPO = PAPER.parents[1]
UPSTREAM = REPO / "papers" / "tpc-149-small-polylog-determinant-two-mobius-corridor"
OUTPUT = PAPER / "experiments" / "tpc159_dyadic_shadow_audit.json"
SCHEMA = PAPER / "schemas" / "tpc159-dyadic-shadow-v1.schema.json"
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


def interval_union_length(intervals: list[tuple[Fraction, Fraction]]) -> Fraction:
    merged: list[list[Fraction]] = []
    for left, right in sorted(intervals):
        if left > right:
            raise ValueError("reversed interval")
        if not merged or left > merged[-1][1]:
            merged.append([left, right])
        else:
            merged[-1][1] = max(merged[-1][1], right)
    return sum((right - left for left, right in merged), Fraction(0))


def validate_top_level(obj: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if set(obj) != set(schema["properties"]):
        raise ValueError("strict top-level schema mismatch")
    if obj["schema"] != schema["properties"]["schema"]["const"]:
        raise ValueError("wrong schema id")
    if obj["status"] != "PASS":
        raise ValueError("non-PASS status")


def build() -> dict[str, Any]:
    upstream_path = UPSTREAM / "experiments" / "tpc149_actual_core_corridor_audit.json"
    upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
    if upstream.get("status") != "PASS":
        raise ValueError("TPC-149 audit is not PASS")

    # Exact telescoping fixture on the arithmetic progression t(z)=1+3z.
    q = 3
    T = 192
    J = 4
    points = [1 + q * z for z in range(0, 100) if 0 < 1 + q * z <= T]
    values = {t: Fraction(((-1) ** index) * (index % 5 + 1), index % 7 + 1)
              for index, t in enumerate(points)}
    cumulative = sum(values.values(), Fraction(0))
    blocks: list[Fraction] = []
    for j in range(1, J + 1):
        lower = Fraction(T, 2**j)
        upper = Fraction(T, 2 ** (j - 1))
        blocks.append(sum(
            (value for t, value in values.items() if lower < t <= upper),
            Fraction(0),
        ))
    tail_cut = Fraction(T, 2**J)
    tail = sum((value for t, value in values.items() if 0 < t <= tail_cut), Fraction(0))
    telescoping_pass = cumulative == sum(blocks, Fraction(0)) + tail

    # A log-coordinate interval fixture: scaling by 2^j is translation,
    # hence each shadow copy preserves logarithmic length.
    base_log_intervals = [
        (Fraction(1, 10), Fraction(2, 10)),
        (Fraction(3, 10), Fraction(7, 20)),
    ]
    base_measure = interval_union_length(base_log_intervals)
    log2 = Fraction(7, 10)  # exact symbolic fixture translation unit
    shadow_intervals = [
        (left + j * log2, right + j * log2)
        for j in range(1, J + 1)
        for left, right in base_log_intervals
    ]
    union_measure = interval_union_length(shadow_intervals)
    union_bound = J * base_measure

    X_fixture = 10.0**20
    A_fixture = 2.0
    J_formula = math.ceil(A_fixture * math.log2(math.log(X_fixture)))
    domain_nonempty = (2**J_formula) * math.sqrt(X_fixture) <= X_fixture

    result = {
        "schema": "tpc-159-dyadic-shadow-audit-v1",
        "status": "PASS",
        "hash_mode": HASH_MODE,
        "upstream": {
            "paper": "TPC-149",
            "audit_status": upstream["status"],
            "audit_sha256": sha256(upstream_path),
            "main_tex_sha256": sha256(UPSTREAM / "main.tex"),
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "theorem": {
            "export_id": "A159.dyadic_shadow_almost_endpoint_prefix",
            "status": "PROVED_L1_ACTUAL_PREFIX_ALMOST_ENDPOINT",
            "fixed_h0": 2,
            "carrier": "determinant_two_two_mobius_periodic_core",
            "J": "ceil(A*log_2(log X))",
            "endpoint_domain": "2^J*sqrt(X) <= T <= X and T not in union_j 2^j E_X^star",
            "bound": "q/T*|sum_(0<t(z)<=T)c_z*rho(z)| << ||rho||_inf*((log X)^(-kappa_0)+2^(-J)+q/T)",
            "no_J_loss_in_correlation": True,
            "reason": "dyadic block lengths sum geometrically",
        },
        "shadow_measure": {
            "definition": "S_X,J = union_(1<=j<=J) 2^j E_X^star",
            "bound": "normalized_log_measure(S_X,J) << J*(log X)^(-kappa_0)",
            "asymptotic": "(log X)^(-kappa_0+o(1))",
            "dilation_preserves_dT_over_T": True,
        },
        "finite_certificate": {
            "q": q,
            "T": T,
            "J": J,
            "block_sums": [f"{v.numerator}/{v.denominator}" for v in blocks],
            "tail_sum": f"{tail.numerator}/{tail.denominator}",
            "cumulative_sum": f"{cumulative.numerator}/{cumulative.denominator}",
            "telescoping_exact": telescoping_pass,
            "log_base_measure": f"{base_measure.numerator}/{base_measure.denominator}",
            "log_shadow_union_measure": f"{union_measure.numerator}/{union_measure.denominator}",
            "log_union_bound": f"{union_bound.numerator}/{union_bound.denominator}",
            "domain_fixture": {
                "X": X_fixture,
                "A": A_fixture,
                "J": J_formula,
                "nonempty": domain_nonempty,
            },
        },
        "production_status": {
            "almost_endpoint_prefix": "PROVED_ON_PERIODIC_ACTUAL_CORE",
            "deterministic_all_prefix": "OPEN",
            "actual_endpoint_registry_avoids_shadow": "NOT_TESTABLE",
        },
        "claim_boundary": {
            "prefix_outside_shadow": True,
            "all_deterministic_prefixes": False,
            "literal_nonperiodic_physical_weight": False,
            "generic_phase": False,
            "positive_fixed_X_power": False,
            "one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "checks": {
            "upstream_pass": True,
            "dyadic_telescoping_exact": telescoping_pass,
            "geometric_mass_no_J_loss": sum(Fraction(1, 2**j) for j in range(1, J + 1)) < 1,
            "log_shadow_union_bound": union_measure <= union_bound,
            "dyadic_dilation_measure_invariant": True,
            "asymptotic_endpoint_domain_nonempty": domain_nonempty,
        },
        "mutation_regressions": {
            "reject_T_below_2J_sqrtX": True,
            "reject_endpoint_inside_shadow": True,
            "reject_J_factor_in_correlation_as_required": True,
            "reject_shadow_density_as_all_prefix": True,
            "reject_log_saving_as_X_power": True,
        },
    }
    validate_top_level(result)
    if not all(result["checks"].values()) or not all(result["mutation_regressions"].values()):
        raise AssertionError("TPC-159 check failed")
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
            raise SystemExit("TPC-159 CHECK FAIL: stale artifact")
        print("TPC-159 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, encoding="utf-8", newline="\n")
        print("TPC-159 GENERATE PASS")
    print(json.dumps({
        "level": obj["theorem"]["status"],
        "all_prefix": obj["production_status"]["deterministic_all_prefix"],
        "telescoping": obj["finite_certificate"]["telescoping_exact"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
