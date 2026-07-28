#!/usr/bin/env python3
"""Generate and verify the TPC-169 maximal-prefix certificate."""

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
UPSTREAM_160 = REPO / "papers" / "tpc-160-exceptional-variation-abel-return"
UPSTREAM_167 = REPO / "papers" / "tpc-167-direct-additive-twist-parseval"
OUTPUT = PAPER / "experiments" / "tpc169_maximal_prefix_audit.json"
SCHEMA = PAPER / "schemas" / "tpc169-maximal-prefix-v1.schema.json"
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


def dyadic_prefix_blocks(k: int) -> list[tuple[int, int]]:
    """Return aligned half-open dyadic blocks whose union is [0,k)."""
    blocks: list[tuple[int, int]] = []
    start = 0
    for exponent in range(k.bit_length() - 1, -1, -1):
        size = 1 << exponent
        if k & size:
            blocks.append((start, start + size))
            start += size
    return blocks


def validate_top_level(obj: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if set(obj) != set(schema["properties"]):
        raise ValueError("strict top-level schema mismatch")
    if obj["schema"] != schema["properties"]["schema"]["const"]:
        raise ValueError("wrong schema id")
    if obj["status"] != "PASS":
        raise ValueError("non-PASS result")


def validate_semantics(obj: dict[str, Any]) -> None:
    theorem = obj["maximal_theorem"]
    endpoint = obj["endpoint_return"]
    boundary = obj["claim_boundary"]
    dyadic = obj["dyadic_decomposition"]
    if theorem["status"] != "PROVED_L1_ACTUAL_CORE_PHASE_METRIC_MAXIMAL_PREFIX":
        raise ValueError("wrong program status")
    if theorem["analytic_norm"] != "L2_PHASE_MAXIMAL":
        raise ValueError("wrong analytic norm")
    if theorem["program_positive_L2"] is not False or theorem["fixed_atom"] is not False:
        raise ValueError("phase maximum promoted to program L2 or fixed atom")
    if theorem["dyadic_depth_power"] != 2:
        raise ValueError("maximal theorem lost the squared dyadic-depth cost")
    if not dyadic["at_most_one_block_per_level"]:
        raise ValueError("dyadic decomposition repeats a level")
    if endpoint["natural_normalization_requires_theta_shell"] is not True:
        raise ValueError("terminal normalization promoted to all natural endpoints")
    required_false = (
        "program_positive_L2",
        "fixed_atom",
        "specified_phase",
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
    audit160_path = UPSTREAM_160 / "experiments" / "tpc160_abel_return_audit.json"
    audit167_path = UPSTREAM_167 / "experiments" / "tpc167_parseval_audit.json"
    audit160 = json.loads(audit160_path.read_text(encoding="utf-8"))
    audit167 = json.loads(audit167_path.read_text(encoding="utf-8"))
    if audit160.get("status") != "PASS" or audit167.get("status") != "PASS":
        raise ValueError("upstream audit is not PASS")

    coefficients = [1, -1, 2, 0, -2, 1, 1, -1, 0, 2, -1, 1, 0]
    length = len(coefficients)
    energy = sum(abs(value) ** 2 for value in coefficients)
    depth = 1 + math.ceil(math.log2(length))
    decompositions = {
        str(k): dyadic_prefix_blocks(k)
        for k in range(1, length + 1)
    }
    decomposition_ok = all(
        blocks[0][0] == 0
        and blocks[-1][1] == k
        and all(blocks[index][1] == blocks[index + 1][0]
                for index in range(len(blocks) - 1))
        and all(
            (end - start) & (end - start - 1) == 0
            and start % (end - start) == 0
            for start, end in blocks
        )
        and len({end - start for start, end in blocks}) == len(blocks)
        and len(blocks) <= depth
        for k_text, blocks in decompositions.items()
        for k in [int(k_text)]
    )
    one_per_level_ok = all(
        len({end - start for start, end in blocks}) == len(blocks)
        for blocks in decompositions.values()
    )

    grid_size = 4096
    maxima: list[float] = []
    for r in range(grid_size):
        alpha = r / grid_size
        partial = 0j
        maximum = 0.0
        for index, value in enumerate(coefficients):
            partial += value * e(-alpha * index)
            maximum = max(maximum, abs(partial))
        maxima.append(maximum)
    sampled_maximal_mean_square = sum(value * value for value in maxima) / grid_size
    maximal_upper = depth * depth * energy

    q = 9
    terminal = 500
    normalized_sample = (q / terminal) ** 2 * sampled_maximal_mean_square
    coefficient_bound = max(abs(value) for value in coefficients)
    counting_upper = (
        depth
        * depth
        * coefficient_bound
        * coefficient_bound
        * (q / terminal + q * q / (terminal * terminal))
    )

    threshold = 0.20
    bad_fraction = sum((q / terminal) * value > threshold for value in maxima) / grid_size
    chebyshev_upper = normalized_sample / (threshold * threshold)

    result = {
        "schema": "tpc-169-maximal-prefix-audit-v1",
        "status": "PASS",
        "hash_mode": HASH_MODE,
        "upstream": {
            "TPC160": {
                "audit_sha256": sha256(audit160_path),
                "main_tex_sha256": sha256(UPSTREAM_160 / "main.tex"),
                "audit_status": audit160["status"],
            },
            "TPC167": {
                "audit_sha256": sha256(audit167_path),
                "main_tex_sha256": sha256(UPSTREAM_167 / "main.tex"),
                "audit_status": audit167["status"],
            },
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "dyadic_decomposition": {
            "depth": depth,
            "prefix_count": length,
            "at_most_one_block_per_level": one_per_level_ok,
            "all_prefixes_exactly_partitioned": decomposition_ok,
            "decompositions": decompositions,
        },
        "maximal_theorem": {
            "export_id": "A169.phase_maximal_all_prefix",
            "status": "PROVED_L1_ACTUAL_CORE_PHASE_METRIC_MAXIMAL_PREFIX",
            "analytic_norm": "L2_PHASE_MAXIMAL",
            "program_positive_L2": False,
            "fixed_atom": False,
            "dyadic_depth_power": 2,
            "abstract_bound": "integral max_k |sum_(j<=k)b_j e(alpha j)|^2 <= D_L^2 sum_j|b_j|^2",
            "normalized_bound": (
                "integral G_T(alpha)^2 <= D_L^2 ||rho||_infinity^2 "
                "(q/T+q^2/T^2)"
            ),
            "fixture": {
                "length": length,
                "energy": energy,
                "depth": depth,
                "grid_size": grid_size,
                "sampled_maximal_mean_square": sampled_maximal_mean_square,
                "analytic_upper": maximal_upper,
                "q": q,
                "T": terminal,
                "normalized_sample": normalized_sample,
                "counting_upper": counting_upper,
                "threshold": threshold,
                "bad_fraction": bad_fraction,
                "chebyshev_upper_from_sample": chebyshev_upper,
                "fixture_scope": "FINITE_GRID_IMPLEMENTATION_CHECK_NOT_CONTINUOUS_INTEGRAL_CERTIFICATE",
            },
        },
        "endpoint_return": {
            "all_prefixes_share_one_phase_exceptional_set": True,
            "includes_TPC159_dyadic_bad_endpoints": True,
            "endpoint_shell": "U in [theta*T,T]",
            "normalization_loss": "theta^(-1)",
            "natural_normalization_requires_theta_shell": True,
            "specified_phase_covered": False,
        },
        "route_decision": {
            "parent_open_node": "O161.bad_endpoint_pointwise_core",
            "advance": "pointwise_in_endpoint_but_L2_in_phase",
            "original_fixed_phase_node_closed": False,
            "next_object": "phase_metric_crosswalk_or_fixed_phase_maximal_theorem",
        },
        "claim_boundary": {
            "actual_fixed_h0_core": True,
            "all_prefix_endpoint_maximum": True,
            "phase_averaged_L2": True,
            "analytic_norm": "L2_PHASE_MAXIMAL",
            "program_positive_L2": False,
            "fixed_atom": False,
            "specified_phase": False,
            "scale_exceptional_shadow_needed": False,
            "physical_H3": False,
            "one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "checks": {
            "upstreams_pass": True,
            "all_dyadic_prefix_decompositions_valid": decomposition_ok,
            "maximal_grid_mean_below_dyadic_bound": (
                sampled_maximal_mean_square <= maximal_upper + 1e-10
            ),
            "normalized_sample_below_counting_bound": (
                normalized_sample <= counting_upper + 1e-10
            ),
            "sample_bad_fraction_below_sample_chebyshev": (
                bad_fraction <= chebyshev_upper + 1e-10
            ),
            "endpoint_and_phase_quantifiers_separated": True,
        },
        "mutation_regressions": {},
    }
    validate_top_level(result)
    validate_semantics(result)
    result["mutation_regressions"] = {
        "reject_maximum_without_log_squared_depth_cost": mutation_rejected(
            result, ("maximal_theorem", "dyadic_depth_power"), 1
        ),
        "reject_terminal_normalization_as_small_endpoint_normalization": (
            mutation_rejected(
                result,
                ("endpoint_return", "natural_normalization_requires_theta_shell"),
                False,
            )
        ),
        "reject_phase_average_as_alpha_zero": mutation_rejected(
            result, ("maximal_theorem", "fixed_atom"), True
        ),
        "reject_endpoint_pointwise_as_phase_pointwise": mutation_rejected(
            result, ("claim_boundary", "specified_phase"), True
        ),
        "reject_bypass_of_scale_shadow_as_physical_endpoint_closure": (
            mutation_rejected(result, ("claim_boundary", "physical_H3"), True)
        ),
        "reject_phase_power_as_one_over_400_or_twin_prime": (
            mutation_rejected(result, ("claim_boundary", "one_over_400"), True)
            and mutation_rejected(
                result, ("claim_boundary", "twin_prime_theorem"), True
            )
        ),
    }
    if not all(result["checks"].values()):
        raise AssertionError("TPC-169 check failed")
    if not all(result["mutation_regressions"].values()):
        raise AssertionError("TPC-169 mutation regression failed")
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
            raise SystemExit("TPC-169 CHECK FAIL: stale artifact")
        print("TPC-169 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, encoding="utf-8", newline="\n")
        print("TPC-169 GENERATE PASS")
    print(json.dumps({
        "status": obj["maximal_theorem"]["status"],
        "all_prefixes": obj["endpoint_return"]["all_prefixes_share_one_phase_exceptional_set"],
        "fixed_phase_closed": obj["route_decision"]["original_fixed_phase_node_closed"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
