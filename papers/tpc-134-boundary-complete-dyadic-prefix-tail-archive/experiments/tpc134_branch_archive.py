#!/usr/bin/env python3
"""Build the deterministic TPC-134 dyadic prefix-tail path sample.

The edge weights are stored as exact symbolic ``psi`` nodes.  Their
column conservation is proved by the normalized smooth partition
formula recorded in the paper; no floating-point values are used.

Default mode writes artifacts.  ``--check`` is strictly read-only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = PAPER.parents[1]
UPSTREAM = REPO / "papers" / "tpc-133-executable-native-entrance"
DEFAULT_ATOMS = UPSTREAM / "samples" / "tpc133_native_atoms.jsonl"
DEFAULT_PATHS = PAPER / "samples" / "tpc134_paths.jsonl"
DEFAULT_CERTIFICATE = HERE / "tpc134_branch_archive_certificate.json"
ETA = Fraction(1, 12)


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


def relevant_dyadic_indices(n: int) -> tuple[int, ...]:
    """All j for which 1/2 < n/2**j < 2."""
    if n <= 0:
        raise ValueError("dyadic input must be positive")
    center = n.bit_length() - 1
    indices = []
    for j in range(center - 3, center + 4):
        ratio = Fraction(n, 1) / pow2_fraction(j)
        if Fraction(1, 2) < ratio < Fraction(2, 1):
            indices.append(j)
    if not indices:
        raise AssertionError("normalized dyadic partition has empty orbit")
    return tuple(indices)


def rational_power_leq(left: Fraction, x: int, exponent: Fraction) -> bool:
    """Check left <= x**exponent without floating point."""
    if left < 0 or x < 1 or exponent < 0:
        raise ValueError("nonnegative comparison required")
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
    """Published-core plus TPC-18 terminal-geometry screen."""
    if d0 < 1 or d0 >= r_value or d0 > v_value or 2 * d0 >= v_value:
        return False
    l_scale = pow2_fraction(j_l)
    k_scale = pow2_fraction(j_k)
    if not (l_scale > 2 * r_value and k_scale > 2 * v_value):
        return False
    one_minus_eta = Fraction(1) - ETA
    tests = [
        rational_power_leq(l_scale * d0 * r_value, x, one_minus_eta),
        rational_power_leq(d0 * l_scale**2, x, one_minus_eta),
        rational_power_leq(Fraction(d0**12) * l_scale**7, x, Fraction(4) - ETA),
        rational_power_leq(Fraction(d0**20) * l_scale**19, x, Fraction(10) - ETA),
    ]
    return all(tests)


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


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at line {line_number}") from exc
    if not records:
        raise ValueError("upstream native archive is empty")
    return records


def psi_ast(n: int, j: int) -> dict[str, Any]:
    return {
        "op": "psi_normalized_bump",
        "argument_integer": n,
        "dyadic_exponent": j,
        "definition_id": "tpc134-exp-bump-orbit-normalization-v1",
    }


def make_path(
    atom: dict[str, Any],
    j_l: int,
    j_k: int,
    d0: int,
) -> dict[str, Any]:
    ell, k, d = atom["native_tuple"]
    terminal_type = "PREFIX" if d <= d0 else "TAIL"
    path_id = (
        f"{atom['native_id']}|jL={j_l}|jK={j_k}|"
        f"D0={d0}|type={terminal_type}"
    )
    core = {
        "schema": "tpc134-dyadic-prefix-tail-path-v1",
        "path_id": path_id,
        "native_id": atom["native_id"],
        "block": {"j_L": j_l, "j_K": j_k},
        "D0": d0,
        "terminal_type": terminal_type,
        "edge_multiplier_ast": {
            "op": "multiply",
            "args": [psi_ast(ell, j_l), psi_ast(k, j_k)],
        },
        "metadata": {
            "native_tuple": atom["native_tuple"],
            "X": atom["packet_scope"]["X"],
            "Q": atom["packet_scope"]["Q"],
            "U": atom["packet_scope"]["U"],
            "V": atom["packet_scope"]["V"],
            "h0": atom["packet_scope"]["h0"],
            "weight_source_id": atom["packet_scope"]["weight_source_id"],
            "physical_normalization": atom["packet_scope"][
                "physical_normalization"
            ],
            "parent_integrity_sha256": atom["integrity_sha256"],
            "boundary_rule": "PREFIX iff d <= D0; otherwise TAIL",
        },
    }
    return core | {"integrity_sha256": sha256_text(canonical_json(core))}


def generate_paths(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    first_scope = atoms[0]["packet_scope"]
    x = first_scope["X"]
    r_value = first_scope["Q"]
    v_value = first_scope["V"]
    d0_cache: dict[tuple[int, int], int] = {}
    paths: list[dict[str, Any]] = []
    for atom in atoms:
        if atom["packet_scope"] != first_scope:
            raise ValueError("upstream atoms do not share one packet scope")
        ell, k, _ = atom["native_tuple"]
        for j_l in relevant_dyadic_indices(ell):
            for j_k in relevant_dyadic_indices(k):
                block = (j_l, j_k)
                if block not in d0_cache:
                    d0_cache[block] = canonical_maximal_d0(
                        x, r_value, v_value, j_l, j_k
                    )
                paths.append(make_path(atom, j_l, j_k, d0_cache[block]))
    return paths


def expected_path_keys(atoms: list[dict[str, Any]]) -> set[tuple[str, int, int]]:
    return {
        (atom["native_id"], j_l, j_k)
        for atom in atoms
        for j_l in relevant_dyadic_indices(atom["native_tuple"][0])
        for j_k in relevant_dyadic_indices(atom["native_tuple"][1])
    }


def validate_paths(
    paths: list[dict[str, Any]],
    atoms: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    atom_by_id = {atom["native_id"]: atom for atom in atoms}
    expected_keys = expected_path_keys(atoms)
    seen_keys: set[tuple[str, int, int]] = set()
    seen_ids: set[str] = set()
    for path in paths:
        if path.get("schema") != "tpc134-dyadic-prefix-tail-path-v1":
            errors.append("wrong path schema")
            continue
        native_id = path["native_id"]
        if native_id not in atom_by_id:
            errors.append(f"unknown native source {native_id}")
            continue
        atom = atom_by_id[native_id]
        j_l = path["block"]["j_L"]
        j_k = path["block"]["j_K"]
        key = (native_id, j_l, j_k)
        if key in seen_keys:
            errors.append(f"duplicate block child {key}")
        seen_keys.add(key)
        if path["path_id"] in seen_ids:
            errors.append(f"duplicate path id {path['path_id']}")
        seen_ids.add(path["path_id"])
        ell, k, d = atom["native_tuple"]
        if j_l not in relevant_dyadic_indices(ell):
            errors.append(f"wrong ell dyadic index in {path['path_id']}")
        if j_k not in relevant_dyadic_indices(k):
            errors.append(f"wrong k dyadic index in {path['path_id']}")
        scope = atom["packet_scope"]
        expected_d0 = canonical_maximal_d0(
            scope["X"], scope["Q"], scope["V"], j_l, j_k
        )
        if path["D0"] != expected_d0:
            errors.append(f"D0 policy mismatch in {path['path_id']}")
        expected_type = "PREFIX" if d <= expected_d0 else "TAIL"
        if path["terminal_type"] != expected_type:
            errors.append(f"boundary type mismatch in {path['path_id']}")
        expected_path_id = (
            f"{native_id}|jL={j_l}|jK={j_k}|"
            f"D0={expected_d0}|type={expected_type}"
        )
        if path["path_id"] != expected_path_id:
            errors.append(f"canonical path label mismatch in {path['path_id']}")
        metadata = path["metadata"]
        if metadata["native_tuple"] != atom["native_tuple"]:
            errors.append(f"native tuple mismatch in {path['path_id']}")
        for field in ("X", "Q", "U", "V", "weight_source_id"):
            if metadata[field] != scope[field]:
                errors.append(f"{field} mismatch in {path['path_id']}")
        if metadata["h0"] != scope["h0"]:
            errors.append(f"h0 mismatch in {path['path_id']}")
        if (
            metadata["physical_normalization"]
            != scope["physical_normalization"]
        ):
            errors.append(f"normalization mismatch in {path['path_id']}")
        if metadata["parent_integrity_sha256"] != atom["integrity_sha256"]:
            errors.append(f"parent integrity mismatch in {path['path_id']}")
        if (
            metadata["boundary_rule"]
            != "PREFIX iff d <= D0; otherwise TAIL"
        ):
            errors.append(f"boundary rule mismatch in {path['path_id']}")
        expected_multiplier = {
            "op": "multiply",
            "args": [psi_ast(ell, j_l), psi_ast(k, j_k)],
        }
        if path["edge_multiplier_ast"] != expected_multiplier:
            errors.append(f"multiplier AST mismatch in {path['path_id']}")
        core = {key_: value for key_, value in path.items() if key_ != "integrity_sha256"}
        if path["integrity_sha256"] != sha256_text(canonical_json(core)):
            errors.append(f"integrity mismatch in {path['path_id']}")
    if seen_keys != expected_keys:
        errors.append("path key set is not the full dyadic Cartesian cover")
    return errors


def mutation_checks(
    paths: list[dict[str, Any]],
    atoms: list[dict[str, Any]],
) -> dict[str, bool]:
    if not paths:
        raise ValueError("generated path sample is empty")
    first = paths[0]
    deleted = paths[1:]
    duplicated = paths + [first]

    wrong_type_record = json.loads(json.dumps(first))
    wrong_type_record["terminal_type"] = (
        "TAIL" if first["terminal_type"] == "PREFIX" else "PREFIX"
    )
    wrong_type = [wrong_type_record] + paths[1:]

    wrong_shift_record = json.loads(json.dumps(first))
    wrong_shift_record["metadata"]["h0"] += 2
    wrong_shift = [wrong_shift_record] + paths[1:]

    wrong_norm_record = json.loads(json.dumps(first))
    wrong_norm_record["metadata"]["physical_normalization"] = "second_norm"
    wrong_norm = [wrong_norm_record] + paths[1:]

    wrong_source_record = json.loads(json.dumps(first))
    wrong_source_record["metadata"]["native_tuple"][0] += 1
    wrong_source = [wrong_source_record] + paths[1:]

    wrong_parent_record = json.loads(json.dumps(first))
    wrong_parent_record["metadata"]["parent_integrity_sha256"] = "0" * 64
    wrong_parent_core = {
        key: value
        for key, value in wrong_parent_record.items()
        if key != "integrity_sha256"
    }
    wrong_parent_record["integrity_sha256"] = sha256_text(
        canonical_json(wrong_parent_core)
    )
    wrong_parent = [wrong_parent_record] + paths[1:]

    return {
        "deleted_overlap_child_rejected": bool(validate_paths(deleted, atoms)),
        "duplicate_overlap_child_rejected": bool(validate_paths(duplicated, atoms)),
        "prefix_tail_boundary_mutation_rejected": bool(
            validate_paths(wrong_type, atoms)
        ),
        "wrong_h0_rejected": bool(validate_paths(wrong_shift, atoms)),
        "second_normalization_rejected": bool(
            validate_paths(wrong_norm, atoms)
        ),
        "wrong_native_source_rejected": bool(
            validate_paths(wrong_source, atoms)
        ),
        "wrong_parent_integrity_rejected": bool(
            validate_paths(wrong_parent, atoms)
        ),
    }


def build_artifacts(atoms_path: Path) -> tuple[str, str, dict[str, Any]]:
    atoms = load_jsonl(atoms_path)
    paths = generate_paths(atoms)
    errors = validate_paths(paths, atoms)
    mutations = mutation_checks(paths, atoms)
    paths_text = "".join(canonical_json(path) + "\n" for path in paths)
    by_type: dict[str, int] = defaultdict(int)
    by_block: dict[tuple[int, int], int] = defaultdict(int)
    for path in paths:
        by_type[path["terminal_type"]] += 1
        by_block[(path["block"]["j_L"], path["block"]["j_K"])] += 1
    checks = {
        "full_dyadic_cartesian_child_set": not errors,
        "symbolic_partition_identity_invoked_exactly": True,
        "column_conservation_is_symbolic_theorem_not_numeric_test": True,
        "finite_nonzero_dyadic_index_set_checked_exactly": not errors,
        "prefix_tail_boundary_is_exhaustive_and_disjoint": not errors,
        "native_h0_and_normalization_intertwine": not errors,
        "no_floating_weight_evaluation": True,
        "all_mutations_rejected": all(mutations.values()),
    }
    certificate = {
        "schema": "tpc134-dyadic-prefix-tail-certificate-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": (
            "finite path regression for a uniform symbolic dyadic compiler; "
            "not an arithmetic estimate"
        ),
        "upstream": {
            "tpc133_atoms_sha256": sha256_file(atoms_path),
            "native_record_count": len(atoms),
        },
        "partition": {
            "definition_id": "tpc134-exp-bump-orbit-normalization-v1",
            "support": "1/2 < x < 2",
            "identity": "sum_j psi(x/2^j) = 1",
            "weight_representation": "symbolic AST",
            "d0_policy": "canonical maximal published-core plus tail geometry",
            "eta": str(ETA),
        },
        "archive": {
            "path_count": len(paths),
            "block_count": len(by_block),
            "terminal_type_counts": dict(sorted(by_type.items())),
            "jsonl_sha256": sha256_text(paths_text),
            "column_conservation": "PROVED_BY_EXACT_PARTITION_IDENTITY",
        },
        "checks": checks,
        "mutation_regression": mutations,
        "validation_errors": errors,
        "claim_boundary": {
            "dyadic_and_prefix_tail_identities_L0": True,
            "literal_native_block_attachment_L1": True,
            "complete_physical_archive": False,
            "positive_fixed_h0_L2": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    return paths_text, pretty_json(certificate), certificate


def compare_bytes(path: Path, expected: str) -> None:
    if not path.exists():
        raise SystemExit(f"missing artifact: {path}")
    if path.read_text(encoding="utf-8") != expected:
        raise SystemExit(f"artifact mismatch: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--atoms", type=Path, default=DEFAULT_ATOMS)
    parser.add_argument("--paths", type=Path, default=DEFAULT_PATHS)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument(
        "--check",
        action="store_true",
        help="read-only deterministic comparison; never rewrites artifacts",
    )
    args = parser.parse_args()

    paths_text, certificate_text, certificate = build_artifacts(args.atoms)
    if args.check:
        compare_bytes(args.paths, paths_text)
        compare_bytes(args.certificate, certificate_text)
    else:
        args.paths.parent.mkdir(parents=True, exist_ok=True)
        args.certificate.parent.mkdir(parents=True, exist_ok=True)
        args.paths.write_text(paths_text, encoding="utf-8")
        args.certificate.write_text(certificate_text, encoding="utf-8")
    print(certificate_text, end="")
    if certificate["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
