#!/usr/bin/env python3
"""Audit the exact eligible/frontier partition used by TPC-135.

This program classifies the actual committed TPC-134 path sample.  It
does not evaluate any arithmetic coefficient and it never infers that
the frontier scalar is large.  The negative result is only a
coefficientwise coverage defect for the eligible-only compiler.

Default mode writes deterministic JSON.  ``--check`` is read-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = PAPER.parents[1]
UPSTREAM = (
    REPO
    / "papers"
    / "tpc-134-boundary-complete-dyadic-prefix-tail-archive"
)
DEFAULT_PATHS = UPSTREAM / "samples" / "tpc134_paths.jsonl"
DEFAULT_MANIFEST = PAPER / "samples" / "tpc135_frontier_manifest.json"
DEFAULT_CERTIFICATE = HERE / "tpc135_domain_cover_certificate.json"
ETA = Fraction(1, 12)
REASONS = (
    "ELIGIBLE",
    "L_TOO_LOW",
    "K_TOO_LOW",
    "NO_TAIL_ROOM",
    "PUBLISHED_PROFILE_FAIL",
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def pretty_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pow2_fraction(exponent: int) -> Fraction:
    if exponent >= 0:
        return Fraction(1 << exponent, 1)
    return Fraction(1, 1 << (-exponent))


def rational_power_leq(left: Fraction, x: int, exponent: Fraction) -> bool:
    p, q = exponent.numerator, exponent.denominator
    return pow(left.numerator, q) <= pow(x, p) * pow(left.denominator, q)


def d0_admissible(
    d0: int,
    x: int,
    r_value: int,
    v_value: int,
    j_l: int,
    j_k: int,
) -> bool:
    if d0 < 1 or d0 >= r_value or d0 > v_value or 2 * d0 >= v_value:
        return False
    l_scale = pow2_fraction(j_l)
    k_scale = pow2_fraction(j_k)
    if not (l_scale > 2 * r_value and k_scale > 2 * v_value):
        return False
    return all(
        [
            rational_power_leq(
                l_scale * d0 * r_value,
                x,
                Fraction(1) - ETA,
            ),
            rational_power_leq(
                d0 * l_scale**2,
                x,
                Fraction(1) - ETA,
            ),
            rational_power_leq(
                Fraction(d0**12) * l_scale**7,
                x,
                Fraction(4) - ETA,
            ),
            rational_power_leq(
                Fraction(d0**20) * l_scale**19,
                x,
                Fraction(10) - ETA,
            ),
        ]
    )


def canonical_maximal_d0(
    x: int,
    r_value: int,
    v_value: int,
    j_l: int,
    j_k: int,
) -> int:
    for d0 in range((v_value - 1) // 2, 0, -1):
        if d0_admissible(d0, x, r_value, v_value, j_l, j_k):
            return d0
    return 0


def classify_block(
    x: int,
    r_value: int,
    v_value: int,
    j_l: int,
    j_k: int,
    d0: int,
) -> str:
    l_scale = pow2_fraction(j_l)
    k_scale = pow2_fraction(j_k)
    if l_scale <= 2 * r_value:
        return "L_TOO_LOW"
    if k_scale <= 2 * v_value:
        return "K_TOO_LOW"
    if (v_value - 1) // 2 < 1:
        return "NO_TAIL_ROOM"
    if d0 == 0:
        return "PUBLISHED_PROFILE_FAIL"
    if not d0_admissible(d0, x, r_value, v_value, j_l, j_k):
        raise ValueError("positive D0 is not admissible")
    return "ELIGIBLE"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    paths: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            paths.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at line {line_number}") from exc
    if not paths:
        raise ValueError("upstream path archive is empty")
    return paths


def build_manifest(paths: list[dict[str, Any]]) -> dict[str, Any]:
    first = paths[0]
    metadata = first["metadata"]
    x = metadata["X"]
    r_value = metadata["Q"]
    v_value = metadata["V"]
    blocks: dict[tuple[int, int], dict[str, Any]] = {}
    for path in paths:
        if path["metadata"]["h0"] != metadata["h0"]:
            raise ValueError("mixed h0 scopes")
        for field in ("X", "Q", "U", "V", "weight_source_id"):
            if path["metadata"][field] != metadata[field]:
                raise ValueError(f"mixed {field} scopes")
        if (
            path["metadata"]["physical_normalization"]
            != metadata["physical_normalization"]
        ):
            raise ValueError("mixed physical normalizations")
        j_l = path["block"]["j_L"]
        j_k = path["block"]["j_K"]
        key = (j_l, j_k)
        expected_d0 = canonical_maximal_d0(
            x, r_value, v_value, j_l, j_k
        )
        if path["D0"] != expected_d0:
            raise ValueError("upstream D0 does not match canonical maximal policy")
        reason = classify_block(
            x, r_value, v_value, j_l, j_k, expected_d0
        )
        if key not in blocks:
            blocks[key] = {
                "j_L": j_l,
                "j_K": j_k,
                "D0": expected_d0,
                "reason": reason,
                "path_count": 0,
            }
        elif blocks[key]["reason"] != reason:
            raise ValueError("one block received two eligibility reasons")
        blocks[key]["path_count"] += 1

    paths_by_native: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for path in paths:
        paths_by_native[path["native_id"]].append(path)
    witness_id = None
    witness_paths: list[dict[str, Any]] = []
    for native_id in sorted(paths_by_native):
        candidates = paths_by_native[native_id]
        candidate_reasons = {
            blocks[(path["block"]["j_L"], path["block"]["j_K"])]["reason"]
            for path in candidates
        }
        if candidate_reasons == {"L_TOO_LOW"}:
            witness_id = native_id
            witness_paths = candidates
            break
    if witness_id is None:
        raise ValueError("sample contains no all-low-L frontier witness")

    block_list = [blocks[key] for key in sorted(blocks)]
    return {
        "schema": "tpc135-domain-cover-manifest-v1",
        "scope": {
            "X": x,
            "h0": metadata["h0"],
            "R": r_value,
            "V": v_value,
            "eta": str(ETA),
            "physical_normalization": metadata["physical_normalization"],
            "route": "published-Maynard-core plus TPC-18 tail geometry",
        },
        "blocks": block_list,
        "witness": {
            "native_id": witness_id,
            "column_kind": "FORMAL_SUPPORT_ENVELOPE_COLUMN",
            "native_coefficient_nonzero_status": "UNDECIDED",
            "path_count": len(witness_paths),
            "child_blocks": sorted(
                [
                    [path["block"]["j_L"], path["block"]["j_K"]]
                    for path in witness_paths
                ]
            ),
            "all_child_reasons": ["L_TOO_LOW"],
            "eligible_symbolic_column_sum": "0",
            "full_symbolic_column_sum": "1",
            "interpretation": (
                "formal coefficientwise coverage witness only; "
                "the arithmetic coefficient may vanish and "
                "no scalar lower bound is asserted"
            ),
        },
        "frontier_scalar_bound_present": False,
    }


def validate_manifest(
    manifest: dict[str, Any],
    paths: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema") != "tpc135-domain-cover-manifest-v1":
        errors.append("wrong manifest schema")
        return errors
    if manifest.get("frontier_scalar_bound_present") is not False:
        errors.append("frontier scalar bound must remain absent")
    scope = manifest["scope"]
    block_by_key = {
        (block["j_L"], block["j_K"]): block for block in manifest["blocks"]
    }
    path_counts = Counter(
        (path["block"]["j_L"], path["block"]["j_K"]) for path in paths
    )
    if set(block_by_key) != set(path_counts):
        errors.append("block manifest does not exactly cover path blocks")
    for key, count in path_counts.items():
        if key not in block_by_key:
            continue
        block = block_by_key[key]
        expected_d0 = canonical_maximal_d0(
            scope["X"], scope["R"], scope["V"], key[0], key[1]
        )
        expected_reason = classify_block(
            scope["X"],
            scope["R"],
            scope["V"],
            key[0],
            key[1],
            expected_d0,
        )
        if block["D0"] != expected_d0:
            errors.append(f"D0 mismatch for block {key}")
        if block["reason"] != expected_reason:
            errors.append(f"reason mismatch for block {key}")
        if block["path_count"] != count:
            errors.append(f"path count mismatch for block {key}")
    witness = manifest["witness"]
    if witness.get("column_kind") != "FORMAL_SUPPORT_ENVELOPE_COLUMN":
        errors.append("witness must remain a formal support-envelope column")
    if witness.get("native_coefficient_nonzero_status") != "UNDECIDED":
        errors.append("witness arithmetic coefficient must remain undecided")
    witness_paths = [
        path for path in paths if path["native_id"] == witness["native_id"]
    ]
    if not witness_paths:
        errors.append("witness native id has no paths")
    witness_reasons = {
        block_by_key[(path["block"]["j_L"], path["block"]["j_K"])]["reason"]
        for path in witness_paths
        if (path["block"]["j_L"], path["block"]["j_K"]) in block_by_key
    }
    if witness_reasons != {"L_TOO_LOW"}:
        errors.append("witness is not supported only on the low-L frontier")
    if witness.get("eligible_symbolic_column_sum") != "0":
        errors.append("eligible witness sum must be zero")
    if witness.get("full_symbolic_column_sum") != "1":
        errors.append("full witness sum must be one")
    return errors


def synthetic_regressions() -> dict[str, bool]:
    x = 1 << 84
    r_value = 1 << 21
    v_value = 1 << 10
    j_l = 38
    j_k = 46
    d0 = canonical_maximal_d0(x, r_value, v_value, j_l, j_k)
    return {
        "large_scale_eligible_case_exists": d0 > 0
        and classify_block(x, r_value, v_value, j_l, j_k, d0)
        == "ELIGIBLE",
        "low_L_case_rejected": classify_block(
            x, r_value, v_value, 21, j_k, 0
        )
        == "L_TOO_LOW",
        "low_K_case_rejected": classify_block(
            x, r_value, v_value, j_l, 10, 0
        )
        == "K_TOO_LOW",
        "maximal_policy_is_maximal": d0 > 0
        and not d0_admissible(d0 + 1, x, r_value, v_value, j_l, j_k),
    }


def mutation_checks(
    manifest: dict[str, Any],
    paths: list[dict[str, Any]],
) -> dict[str, bool]:
    first_block = manifest["blocks"][0]

    wrong_reason = json.loads(json.dumps(manifest))
    wrong_reason["blocks"][0]["reason"] = (
        "ELIGIBLE" if first_block["reason"] != "ELIGIBLE" else "L_TOO_LOW"
    )

    missing_block = json.loads(json.dumps(manifest))
    missing_block["blocks"] = missing_block["blocks"][1:]

    false_scalar = json.loads(json.dumps(manifest))
    false_scalar["frontier_scalar_bound_present"] = True

    false_witness = json.loads(json.dumps(manifest))
    false_witness["witness"]["eligible_symbolic_column_sum"] = "1"

    false_nonzero = json.loads(json.dumps(manifest))
    false_nonzero["witness"]["native_coefficient_nonzero_status"] = "PROVED_NONZERO"

    return {
        "wrong_reason_rejected": bool(validate_manifest(wrong_reason, paths)),
        "missing_block_rejected": bool(validate_manifest(missing_block, paths)),
        "unsupported_scalar_claim_rejected": bool(
            validate_manifest(false_scalar, paths)
        ),
        "false_eligible_cover_witness_rejected": bool(
            validate_manifest(false_witness, paths)
        ),
        "false_nonzero_coefficient_promotion_rejected": bool(
            validate_manifest(false_nonzero, paths)
        ),
    }


def build_artifacts(paths_path: Path) -> tuple[str, str, dict[str, Any]]:
    paths = load_jsonl(paths_path)
    manifest = build_manifest(paths)
    errors = validate_manifest(manifest, paths)
    synthetic = synthetic_regressions()
    mutations = mutation_checks(manifest, paths)
    reason_counts = Counter(block["reason"] for block in manifest["blocks"])
    eligible_paths = sum(
        block["path_count"]
        for block in manifest["blocks"]
        if block["reason"] == "ELIGIBLE"
    )
    frontier_paths = len(paths) - eligible_paths
    checks = {
        "block_partition_exhaustive_and_disjoint": not errors,
        "canonical_maximal_integer_D0_policy": True,
        "committed_support_envelope_sample_has_frontier_column": not errors,
        "eligible_only_column_cover_refuted_on_witness": not errors,
        "witness_numeric_coefficient_remains_undecided": (
            manifest["witness"]["native_coefficient_nonzero_status"]
            == "UNDECIDED"
        ),
        "no_frontier_scalar_largeness_claim": True,
        "synthetic_boundary_regressions_pass": all(synthetic.values()),
        "all_mutations_rejected": all(mutations.values()),
    }
    manifest_text = pretty_json(manifest)
    certificate = {
        "schema": "tpc135-domain-cover-certificate-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": (
            "coefficientwise eligible/frontier cover audit; "
            "not an estimate of the frontier scalar"
        ),
        "upstream": {
            "tpc134_paths_sha256": sha256_file(paths_path),
            "path_count": len(paths),
        },
        "policy": {
            "name": "canonical maximal integer D0",
            "eta": str(ETA),
            "route": "published Maynard core only",
            "reasons": list(REASONS),
        },
        "census": {
            "block_reason_counts": dict(sorted(reason_counts.items())),
            "eligible_path_count": eligible_paths,
            "frontier_path_count": frontier_paths,
            "manifest_sha256": sha256_text(manifest_text),
        },
        "witness": manifest["witness"],
        "checks": checks,
        "synthetic_regression": synthetic,
        "mutation_regression": mutations,
        "validation_errors": errors,
        "route_verdict": {
            "eligible_only_coefficientwise_compiler": "STOP_DECLARED_ROUTE",
            "frontier_scalar_oX": "NOT_PROVED",
            "alternative_frontier_route": "OPEN",
            "full_H1_actual_carrier": "NOT_TESTABLE",
        },
        "claim_boundary": {
            "set_partition_L0": True,
            "scoped_coverage_obstruction_L1": True,
            "new_positive_fixed_h0_L2": False,
            "scalar_frontier_lower_bound": False,
            "witness_numeric_coefficient_nonzero": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    return manifest_text, pretty_json(certificate), certificate


def compare_bytes(path: Path, expected: str) -> None:
    if not path.exists():
        raise SystemExit(f"missing artifact: {path}")
    if path.read_text(encoding="utf-8") != expected:
        raise SystemExit(f"artifact mismatch: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths", type=Path, default=DEFAULT_PATHS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument(
        "--check",
        action="store_true",
        help="read-only deterministic comparison; never rewrites artifacts",
    )
    args = parser.parse_args()

    manifest_text, certificate_text, certificate = build_artifacts(args.paths)
    if args.check:
        compare_bytes(args.manifest, manifest_text)
        compare_bytes(args.certificate, certificate_text)
    else:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.certificate.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(manifest_text, encoding="utf-8")
        args.certificate.write_text(certificate_text, encoding="utf-8")
    print(certificate_text, end="")
    if certificate["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
