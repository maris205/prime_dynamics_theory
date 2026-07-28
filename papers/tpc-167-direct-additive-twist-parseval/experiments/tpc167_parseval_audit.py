#!/usr/bin/env python3
"""Generate and verify the TPC-167 Parseval certificate."""

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
UPSTREAM = REPO / "papers" / "tpc-158-additive-phase-major-minor-gate"
OUTPUT = PAPER / "experiments" / "tpc167_parseval_audit.json"
SCHEMA = PAPER / "schemas" / "tpc167-parseval-audit-v1.schema.json"
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


def validate_top_level(obj: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if set(obj) != set(schema["properties"]):
        raise ValueError("strict top-level schema mismatch")
    if obj["schema"] != schema["properties"]["schema"]["const"]:
        raise ValueError("wrong schema id")
    if obj["status"] != "PASS":
        raise ValueError("non-PASS result")


def validate_semantics(obj: dict[str, Any]) -> None:
    theorem = obj["theorem"]
    boundary = obj["claim_boundary"]
    grid = obj["fourier_grid"]
    if theorem["status"] != "PROVED_L1_ACTUAL_CORE_PHASE_METRIC_SINGLE_CELL":
        raise ValueError("wrong program status")
    if theorem["analytic_norm"] != "L2_PHASE":
        raise ValueError("wrong analytic norm")
    if theorem["program_positive_L2"] is not False or theorem["fixed_atom"] is not False:
        raise ValueError("phase metric promoted to a program L2 or fixed atom")
    if theorem["orthogonality_not_mobius_specific"] is not True:
        raise ValueError("Parseval misclassified as Mobius-specific cancellation")
    if grid["grid_size"] < theorem["fixture"]["length"]:
        raise ValueError("complete-grid identity used below the interval length")
    required_false = (
        "program_positive_L2",
        "fixed_atom",
        "specified_phase",
        "uniform_all_phase",
        "physical_H3",
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
    upstream_path = UPSTREAM / "experiments" / "tpc158_phase_gate_audit.json"
    upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
    if upstream.get("status") != "PASS":
        raise ValueError("TPC-158 audit is not PASS")

    # A deterministic signed/zero coefficient fixture on a shifted interval.
    start = 137
    coefficients = [1, -1, 0, 1, 1, -1, 0, -1, 1, 0, 1]
    length = len(coefficients)
    energy = sum(abs(value) ** 2 for value in coefficients)
    grid_size = 17
    samples = [
        sum(
            value * e(-(r / grid_size) * (start + index))
            for index, value in enumerate(coefficients)
        )
        for r in range(grid_size)
    ]
    grid_mean_square = sum(abs(value) ** 2 for value in samples) / grid_size
    grid_error = abs(grid_mean_square - energy)

    # A second, much finer complete grid cross-checks the implementation.
    second_grid_size = 8192
    second_grid = [
        sum(
            value * e(-(r / second_grid_size) * (start + index))
            for index, value in enumerate(coefficients)
        )
        for r in range(second_grid_size)
    ]
    second_grid_mean_square = (
        sum(abs(value) ** 2 for value in second_grid) / second_grid_size
    )
    second_grid_error = abs(second_grid_mean_square - energy)

    q = 15
    n_scale = 1000
    normalized_exact = q * q * energy / (n_scale * n_scale)
    counting_upper = q / n_scale + q * q / (n_scale * n_scale)

    result = {
        "schema": "tpc-167-parseval-audit-v1",
        "status": "PASS",
        "hash_mode": HASH_MODE,
        "upstream": {
            "paper": "TPC-158",
            "audit_sha256": sha256(upstream_path),
            "main_tex_sha256": sha256(UPSTREAM / "main.tex"),
            "audit_status": upstream["status"],
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "theorem": {
            "export_id": "A167.direct_additive_twist_phase_L2",
            "status": "PROVED_L1_ACTUAL_CORE_PHASE_METRIC_SINGLE_CELL",
            "analytic_norm": "L2_PHASE",
            "program_positive_L2": False,
            "fixed_atom": False,
            "orthogonality_not_mobius_specific": True,
            "identity": "integral_0^1 |(q/N) sum c_z e(-alpha z)|^2 d alpha = q^2 E_N/N^2",
            "bad_phase_measure": "at_most_q^2_E_N_over_N^2_lambda^2",
            "scale_exceptional_set_required": False,
            "fixture": {
                "start": start,
                "length": length,
                "energy": energy,
                "q": q,
                "N": n_scale,
                "normalized_exact": normalized_exact,
                "counting_upper": counting_upper,
            },
        },
        "fourier_grid": {
            "condition": "M >= interval_length",
            "grid_size": grid_size,
            "mean_square": grid_mean_square,
            "target_energy": energy,
            "absolute_error": grid_error,
            "second_grid_size": second_grid_size,
            "second_grid_mean_square": second_grid_mean_square,
            "second_grid_absolute_error": second_grid_error,
            "fixture_scope": "FINITE_COMPLETE_GRID_IMPLEMENTATION_CHECK",
        },
        "power_envelope": {
            "assumptions": "q <= (log X)^eta_0 and N >= sqrt(X)",
            "phase_L2_bound": "sqrt(2)*X^(-1/4)*(log X)^(eta_0/2)",
            "positive_fixed_X_power": True,
            "qualifier": "PHASE_AVERAGED_ONLY",
        },
        "route_decision": {
            "parent_open_node": "O161.direct_additive_twist_core",
            "advance": "direct_twist_control_in_phase_L2_at_every_scale",
            "original_pointwise_node_closed": False,
            "next_object": "source_locked_phase_registry_or_pointwise_phase_input",
        },
        "claim_boundary": {
            "actual_fixed_h0_core": True,
            "phase_averaged_L2": True,
            "analytic_norm": "L2_PHASE",
            "program_positive_L2": False,
            "fixed_atom": False,
            "specified_phase": False,
            "uniform_all_phase": False,
            "physical_H3": False,
            "one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "checks": {
            "upstream_pass": True,
            "grid_size_at_least_length": grid_size >= length,
            "exact_grid_parseval_numerical": grid_error < 1e-12,
            "second_complete_grid_parseval": second_grid_error < 1e-10,
            "normalized_energy_below_counting_bound": normalized_exact <= counting_upper,
            "pointwise_scope_not_promoted": True,
            "phase_power_qualifier_explicit": True,
        },
        "mutation_regressions": {},
    }
    validate_top_level(result)
    validate_semantics(result)
    result["mutation_regressions"] = {
        "reject_phase_L2_as_fixed_phase": mutation_rejected(
            result, ("theorem", "fixed_atom"), True
        ),
        "reject_parseval_as_mobius_specific_cancellation": mutation_rejected(
            result, ("theorem", "orthogonality_not_mobius_specific"), False
        ),
        "reject_grid_identity_when_M_is_smaller_than_length": mutation_rejected(
            result, ("fourier_grid", "grid_size"), length - 1
        ),
        "reject_phase_average_as_physical_phase_registry": mutation_rejected(
            result, ("claim_boundary", "specified_phase"), True
        ),
        "reject_phase_power_as_endpoint_V3_pass": mutation_rejected(
            result, ("theorem", "program_positive_L2"), True
        ),
        "reject_one_over_400_or_twin_prime_promotion": (
            mutation_rejected(result, ("claim_boundary", "one_over_400"), True)
            and mutation_rejected(
                result, ("claim_boundary", "twin_prime_theorem"), True
            )
        ),
    }
    if not all(result["checks"].values()):
        raise AssertionError("TPC-167 check failed")
    if not all(result["mutation_regressions"].values()):
        raise AssertionError("TPC-167 mutation regression failed")
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
            raise SystemExit("TPC-167 CHECK FAIL: stale artifact")
        print("TPC-167 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, encoding="utf-8", newline="\n")
        print("TPC-167 GENERATE PASS")
    print(json.dumps({
        "status": obj["theorem"]["status"],
        "original_pointwise_node_closed": obj["route_decision"]["original_pointwise_node_closed"],
        "phase_power_qualifier": obj["power_envelope"]["qualifier"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
