#!/usr/bin/env python3
"""Deterministic TPC-144 quotient-kernel audit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
TPC143_CERT = (
    PAPERS
    / "tpc-143-frontier-occurrence-lift-contract"
    / "experiments"
    / "tpc143_frontier_lift_certificate.json"
)
TPC143_OBLIGATIONS = (
    PAPERS
    / "tpc-143-frontier-occurrence-lift-contract"
    / "samples"
    / "tpc143_frontier_lift_obligations.jsonl"
)
OUT_MANIFEST = PAPER / "samples" / "tpc144_actual_quotient_manifest.json"
OUT_CERT = HERE / "tpc144_quotient_kernel_certificate.json"

QD_REQUIRED_FIELDS = [
    "common_domain_column_ids_and_order",
    "canonical_parent_alpha_gamma_j",
    "row_ids_and_integer_slopes",
    "ordered_targets_x_y",
    "content",
    "signed_determinant_numerator",
    "exact_determinant_label",
    "inverse_aggregation_relation",
    "physical_multiplicity",
    "computational_multiplicity",
    "literal_parent_coefficient",
    "determinant_bin_target",
    "determinant_bin_exact_map_multiplier",
    "surjectivity_or_image_codomain_certificate",
]
QZ_REQUIRED_FIELDS = [
    "common_domain_column_ids_and_order",
    "outer_affine_key",
    "canonical_order_coordinate_and_rank",
    "arithmetic_sign",
    "outer_weight",
    "outer_reconstruction_multiplier",
    "factor_allocation_id",
    "retained_content_status",
    "content_remainder_destination",
    "zero_mode_output_record",
    "zero_mode_exact_map_multiplier",
    "surjectivity_or_image_codomain_certificate",
]


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        .encode("utf-8")
    )


def text_file_digest(path: Path) -> str:
    """Hash canonical text, independent of the checkout newline convention."""
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def rref(matrix: list[list[int | Fraction]]) -> tuple[tuple[Fraction, ...], ...]:
    a = [[Fraction(value) for value in row] for row in matrix]
    if not a:
        return tuple()
    rows, cols = len(a), len(a[0])
    if any(len(row) != cols for row in a):
        raise ValueError("ragged matrix")
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [value / scale for value in a[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = a[row][col]
            if factor:
                a[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(a[row], a[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    nonzero = [tuple(row) for row in a if any(row)]
    return tuple(nonzero)


def same_kernel(left: list[list[int]], right: list[list[int]]) -> bool:
    """Finite matrices have equal kernels iff their row spaces agree."""
    if left and right and len(left[0]) != len(right[0]):
        raise ValueError("kernel comparison requires a common domain")
    return rref(left) == rref(right)


def is_surjective_matrix(matrix: list[list[int]]) -> bool:
    return len(rref(matrix)) == len(matrix)


def rows_equal_up_to_permutation(
    left: list[list[int]], right: list[list[int]]
) -> bool:
    left_rows = sorted(tuple(Fraction(v) for v in row) for row in left)
    right_rows = sorted(tuple(Fraction(v) for v in row) for row in right)
    return left_rows == right_rows


def matvec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def scalar_total(matrix: list[list[int]], vector: list[int]) -> int:
    return sum(matvec(matrix, vector))


def synthetic_tests() -> dict[str, Any]:
    qd = [[1, 1, 0], [0, 0, 1]]
    qz_relabel = [[0, 0, 1], [1, 1, 0]]
    qz_bad = [[1, 0, 1], [0, 1, 0]]
    qd_identity = [[1, 0], [0, 1]]
    qz_shear = [[1, 1], [0, 1]]
    c = [2, -1, 3]
    if not all(is_surjective_matrix(q) for q in (qd, qz_relabel, qz_bad)):
        raise ValueError("kernel theorem fixture must use surjective quotients")
    if not same_kernel(qd, qz_relabel):
        raise ValueError("relabelled quotients should have equal kernels")
    if same_kernel(qd, qz_bad):
        raise ValueError("different partitions should have different kernels")
    if scalar_total(qd, c) != scalar_total(qz_bad, c):
        raise ValueError("incidence quotients should conserve the same scalar")
    if not same_kernel(qd_identity, qz_shear):
        raise ValueError("invertible quotients should have the same zero kernel")
    if rows_equal_up_to_permutation(qd_identity, qz_shear):
        raise ValueError("equal kernels must not be promoted to literal relabeling")
    return {
        "scope": "SYNTHETIC_L0_ONLY",
        "equal_kernel_relabel_case": True,
        "different_kernel_case_rejected": True,
        "same_scalar_does_not_imply_same_kernel": True,
        "surjectivity_precondition_checked": True,
        "same_kernel_does_not_imply_literal_row_relabeling": True,
        "same_scalar_value": scalar_total(qd, c),
        "qd_rref": [[str(v) for v in row] for row in rref(qd)],
        "qz_bad_rref": [[str(v) for v in row] for row in rref(qz_bad)]
    }


def build_manifest(source: dict[str, Any]) -> dict[str, Any]:
    if source.get("status") != "PASS":
        raise ValueError("TPC-143 certificate is not PASS")
    if source["source"].get("source_chain_validation") != "PASS":
        raise ValueError("TPC-143 upstream source chain is not validated")
    if not source["proved"]["required_domain_all_nonsoft_ETO_plus_FUM"]:
        raise ValueError("TPC-143 all-nonsoft domain proof drifted")
    if source["census"]["obligation_count"] != source["census"]["nonsoft_path_count"]:
        raise ValueError("TPC-143 obligation census is incomplete")
    if source["census"]["obligations_sha256"] != text_file_digest(TPC143_OBLIGATIONS):
        raise ValueError("TPC-143 certificate does not bind its obligation archive")
    if (
        sum(
            1
            for line in TPC143_OBLIGATIONS.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
        != source["census"]["obligation_count"]
    ):
        raise ValueError("TPC-143 obligation file count drifted")
    if source["current_actual_status"]["H1.frontier_occurrence_lift"] != "NOT_TESTABLE":
        raise ValueError("TPC-143 occurrence-lift status drifted")
    return {
        "schema": "tpc144-actual-quotient-manifest-v1",
        "required_domain": "ALL_NONSOFT_CUT_PATHS",
        "occurrence_lift_status": "NOT_TESTABLE",
        "quotients": {
            "Q_D": {
                "status": "NOT_TESTABLE",
                "source_status": "NOT_TESTABLE",
                "actual_map_edges": [],
                "required_fields": QD_REQUIRED_FIELDS
            },
            "Q_Z": {
                "status": "NOT_TESTABLE",
                "source_status": "NOT_TESTABLE",
                "actual_map_edges": [],
                "required_fields": QZ_REQUIRED_FIELDS
            }
        },
        "intertwining": {
            "J_QD_equals_QZ": "NOT_TESTABLE",
            "kernel_equality": "NOT_TESTABLE",
            "literal_fiber_relabeling": "NOT_TESTABLE"
        },
        "claim_boundary": {
            "current_cut_schema_derives_quotients": False,
            "one_scalar_equality_is_coefficientwise_intertwining": False,
            "formal_support_is_actual_nonzero_support": False,
            "new_positive_fixed_h0_L2": False,
            "prime_pair_or_twin_prime_theorem": False
        }
    }


def validate_manifest(manifest: dict[str, Any]) -> None:
    if set(manifest) != {
        "schema",
        "required_domain",
        "occurrence_lift_status",
        "quotients",
        "intertwining",
        "claim_boundary",
    } or manifest["schema"] != "tpc144-actual-quotient-manifest-v1":
        raise ValueError("manifest top-level contract drifted")
    if manifest["required_domain"] != "ALL_NONSOFT_CUT_PATHS":
        raise ValueError("quotient domain must include ETO and FUM")
    if manifest["occurrence_lift_status"] != "NOT_TESTABLE":
        raise ValueError("missing occurrence lift was promoted")
    if set(manifest["quotients"]) != {"Q_D", "Q_Z"}:
        raise ValueError("quotient set drifted")
    for name, required_fields in (
        ("Q_D", QD_REQUIRED_FIELDS),
        ("Q_Z", QZ_REQUIRED_FIELDS),
    ):
        quotient = manifest["quotients"][name]
        if quotient["status"] != "NOT_TESTABLE" or quotient["source_status"] != "NOT_TESTABLE":
            raise ValueError(f"actual {name} was fabricated")
        if quotient["actual_map_edges"]:
            raise ValueError(f"actual {name} edges are unavailable")
        if quotient["required_fields"] != required_fields:
            raise ValueError(f"{name} field contract drifted")
    if set(manifest["intertwining"]) != {
        "J_QD_equals_QZ",
        "kernel_equality",
        "literal_fiber_relabeling",
    } or any(value != "NOT_TESTABLE" for value in manifest["intertwining"].values()):
        raise ValueError("intertwining was promoted without quotients")
    if any(manifest["claim_boundary"].values()):
        raise ValueError("a negative claim boundary was promoted")


def mutation_tests(manifest: dict[str, Any]) -> dict[str, bool]:
    def rejected(mutator) -> bool:
        trial = copy.deepcopy(manifest)
        mutator(trial)
        try:
            validate_manifest(trial)
        except ValueError:
            return True
        return False

    tests = {
        "frontier_only_domain_rejected": rejected(
            lambda value: value.__setitem__("required_domain", "FRONTIER_ONLY")
        ),
        "fabricated_QD_rejected": rejected(
            lambda value: value["quotients"]["Q_D"].__setitem__("status", "PROVED")
        ),
        "fabricated_QZ_edge_rejected": rejected(
            lambda value: value["quotients"]["Q_Z"]["actual_map_edges"].append(
                {"source": "x", "target": "y"}
            )
        ),
        "scalar_intertwining_promotion_rejected": rejected(
            lambda value: value["claim_boundary"].__setitem__(
                "one_scalar_equality_is_coefficientwise_intertwining", True
            )
        ),
        "kernel_promotion_rejected": rejected(
            lambda value: value["intertwining"].__setitem__(
                "kernel_equality", "PROVED_L1"
            )
        ),
        "literal_relabeling_promotion_rejected": rejected(
            lambda value: value["intertwining"].__setitem__(
                "literal_fiber_relabeling", "PROVED_L1"
            )
        ),
        "deleted_QD_field_rejected": rejected(
            lambda value: value["quotients"]["Q_D"]["required_fields"].pop()
        ),
        "promoted_QZ_source_rejected": rejected(
            lambda value: value["quotients"]["Q_Z"].__setitem__(
                "source_status", "PROVED"
            )
        ),
    }
    if not all(tests.values()):
        raise ValueError("TPC-144 mutation regression failed")
    return tests


def render(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def build() -> tuple[bytes, bytes]:
    source = json.loads(TPC143_CERT.read_text(encoding="utf-8"))
    manifest = build_manifest(source)
    validate_manifest(manifest)
    synthetic = synthetic_tests()
    mutations = mutation_tests(manifest)
    manifest_bytes = render(manifest)
    certificate = {
        "schema": "tpc144-quotient-kernel-certificate-v1",
        "status": "PASS",
        "source": {
            "tpc143_certificate_sha256": text_file_digest(TPC143_CERT),
            "hash_is_integrity_only": True
        },
        "theorem": {
            "surjective_quotient_isomorphism_iff_equal_kernels": "PROVED_L0",
            "full_kernel_criterion_requires_surjective_quotients": True,
            "restricted_range_required_when_occurrence_map_not_surjective": True,
            "literal_relabeling_iff_allowed_weighted_row_permutation": "PROVED_L0"
        },
        "synthetic_regression": synthetic,
        "actual_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "actual_status": {
            "H1.frontier_QD_totality": "NOT_TESTABLE",
            "H1.frontier_QZ_totality": "NOT_TESTABLE",
            "H1.frontier_QD_QZ_intertwining": "NOT_TESTABLE"
        },
        "scoped_stop": {
            "route": "schema_or_scalar_only_QD_QZ_derivation",
            "status": "STOP_DECLARED_ROUTE",
            "occurrence_augmented_route_stopped": False
        },
        "mutation_regression": mutations,
        "claim_boundary": {
            "new_positive_fixed_h0_L2": False,
            "frontier_scalar_oX": False,
            "endpoint_1_over_400": False,
            "prime_pair_or_twin_prime_theorem": False
        }
    }
    return manifest_bytes, render(certificate)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest, certificate = build()
    outputs = {OUT_MANIFEST: manifest, OUT_CERT: certificate}
    if args.check:
        for path, expected in outputs.items():
            if not path.exists() or path.read_bytes() != expected:
                raise SystemExit(f"DRIFT: {path}")
        print("TPC-144 CHECK PASS")
    else:
        for path, content in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        print("TPC-144 WRITE PASS")
    print(
        json.dumps(
            {
                "QD": "NOT_TESTABLE",
                "QZ": "NOT_TESTABLE",
                "kernel_theorem": "PROVED_L0"
            },
            sort_keys=True
        )
    )


if __name__ == "__main__":
    main()
