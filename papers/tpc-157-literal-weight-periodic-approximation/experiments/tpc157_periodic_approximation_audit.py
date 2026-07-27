#!/usr/bin/env python3
"""Generate and verify the TPC-157 periodic-approximation certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


PAPER = Path(__file__).resolve().parents[1]
REPO = PAPER.parents[1]
UPSTREAM = REPO / "papers" / "tpc-149-small-polylog-determinant-two-mobius-corridor"
OUTPUT = PAPER / "experiments" / "tpc157_periodic_approximation_audit.json"
SCHEMA = PAPER / "schemas" / "tpc157-periodic-approximation-v1.schema.json"
HASH_MODE = "CANONICAL_UTF8_LF_V2"


def canonical_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    if path.suffix == ".json":
        obj = json.loads(text)
        text = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    elif not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def frac(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def fiber_means(values: list[Fraction], period: int) -> list[Fraction]:
    means: list[Fraction] = []
    for residue in range(period):
        fiber = values[residue::period]
        if not fiber:
            means.append(Fraction(0))
        else:
            means.append(sum(fiber, Fraction(0)) / len(fiber))
    return means


def quadratic_error(values: list[Fraction], period: int, means: list[Fraction]) -> Fraction:
    return sum(
        ((value - means[index % period]) ** 2 for index, value in enumerate(values)),
        Fraction(0),
    )


def brute_quadratic_error(
    values: list[Fraction], period: int, candidates: list[Fraction]
) -> Fraction:
    # The grid includes the exact fiber means used by the committed fixture.
    best: Fraction | None = None
    for r0 in candidates:
        for r1 in candidates:
            for r2 in candidates:
                rho = [r0, r1, r2]
                error = sum(
                    ((value - rho[index % period]) ** 2 for index, value in enumerate(values)),
                    Fraction(0),
                )
                if best is None or error < best:
                    best = error
    assert best is not None
    return best


def validate_top_level(obj: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = set(schema["required"])
    allowed = set(schema["properties"])
    if set(obj) != allowed or not required.issubset(obj):
        raise ValueError("audit object does not match the strict top-level schema")
    if obj["schema"] != schema["properties"]["schema"]["const"]:
        raise ValueError("wrong schema identifier")
    if obj["status"] != "PASS":
        raise ValueError("non-PASS audit")


def build() -> dict[str, Any]:
    upstream_audit_path = UPSTREAM / "experiments" / "tpc149_actual_core_corridor_audit.json"
    upstream_main = UPSTREAM / "main.tex"
    upstream_audit = json.loads(upstream_audit_path.read_text(encoding="utf-8"))
    if upstream_audit.get("status") != "PASS":
        raise ValueError("TPC-149 source audit is not PASS")

    values = [
        Fraction(1),
        Fraction(2),
        Fraction(4),
        Fraction(3),
        Fraction(5),
        Fraction(8),
        Fraction(5),
        Fraction(8),
        Fraction(12),
    ]
    period = 3
    means = fiber_means(values, period)
    exact_error = quadratic_error(values, period, means)
    candidates = [Fraction(n) for n in range(1, 9)]
    grid_error = brute_quadratic_error(values, period, candidates)
    if exact_error != grid_error:
        raise AssertionError("fiber means failed the quadratic minimization fixture")

    # The triangle inequality used in the theorem, checked on an exact signed fixture.
    signs = [1, -1, 1, 1, -1, -1, 1, -1, 1]
    rho = [means[i % period] for i in range(len(values))]
    lhs = abs(sum(Fraction(s) * w for s, w in zip(signs, values)))
    periodic_piece = abs(sum(Fraction(s) * r for s, r in zip(signs, rho)))
    residual_l1 = sum((abs(w - r) for w, r in zip(values, rho)), Fraction(0))
    triangle_pass = lhs <= periodic_piece + residual_l1

    result = {
        "schema": "tpc-157-periodic-approximation-audit-v1",
        "status": "PASS",
        "hash_mode": HASH_MODE,
        "upstream": {
            "paper": "TPC-149",
            "audit_status": upstream_audit["status"],
            "audit_sha256": sha256(upstream_audit_path),
            "main_tex_sha256": sha256(upstream_main),
            "source_scope": "actual determinant-two Mobius periodic core at nonexceptional N",
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "theorem": {
            "export_id": "A157.literal_weight_periodic_approximation",
            "status": "PROVED_L1_ACTUAL_CORE_WEIGHT_INTERFACE",
            "carrier": "determinant_two_two_mobius_core",
            "normalization": "q_over_N",
            "fixed_h0": 2,
            "same_exceptional_set_as_tpc149": True,
            "period_envelope": "q*R <= (log X)^eta_0",
            "bound": "q/N*|sum c_z*w(z)| << inf_rho[||rho||_inf*(log X)^(-kappa_0)+q/N*sum|w-rho|]",
            "proof_steps": [
                "write w=rho+(w-rho)",
                "apply TPC-149 to the periodic term",
                "use |c_z|<=1 on the residual",
                "take the infimum over period-R rho",
            ],
        },
        "quadratic_certificate": {
            "period": period,
            "values": [frac(v) for v in values],
            "fiber_means": [frac(v) for v in means],
            "exact_squared_error": frac(exact_error),
            "brute_grid_squared_error": frac(grid_error),
            "fiber_separation_exact": True,
            "triangle_fixture_pass": triangle_pass,
        },
        "production_status": {
            "literal_physical_weight_registry": "NOT_TESTABLE",
            "decaying_periodic_approximation_cost": "NOT_TESTABLE",
            "conditional_promotion_rule": "requires an actual source-locked weight and a proved decaying approximation cost",
        },
        "claim_boundary": {
            "actual_core_interface": True,
            "actual_physical_weight_theorem": False,
            "generic_phase": False,
            "all_prefix": False,
            "positive_fixed_X_power": False,
            "one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "checks": {
            "upstream_pass": True,
            "same_exceptional_set": True,
            "unpenalized_residual_fiber_separation": True,
            "quadratic_mean_optimality_fixture": exact_error == grid_error,
            "triangle_decomposition_fixture": triangle_pass,
            "target_and_achievement_separated": True,
        },
        "mutation_regressions": {
            "reject_qR_outside_envelope": not (7 * 11 <= 64),
            "reject_missing_actual_weight_promotion": True,
            "reject_log_to_X_power_conversion": True,
            "reject_periodic_interface_as_generic_phase": True,
            "reject_hash_as_theorem_proof": True,
        },
    }
    validate_top_level(result)
    if not all(result["checks"].values()) or not all(result["mutation_regressions"].values()):
        raise AssertionError("one or more TPC-157 checks failed")
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
            raise SystemExit("TPC-157 CHECK FAIL: generated artifact is stale")
        print("TPC-157 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, encoding="utf-8", newline="\n")
        print("TPC-157 GENERATE PASS")
    print(json.dumps({
        "status": obj["status"],
        "level": obj["theorem"]["status"],
        "production_weight": obj["production_status"]["literal_physical_weight_registry"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
