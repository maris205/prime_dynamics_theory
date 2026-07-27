#!/usr/bin/env python3
"""Deterministic TPC-145 occurrence-level grouping/shift audit."""

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
OUT_MANIFEST = PAPER / "samples" / "tpc145_actual_group_shift_manifest.json"
OUT_CERT = HERE / "tpc145_group_shift_certificate.json"

GROUPING_REQUIRED_FIELDS = [
    "physical_occurrence_id",
    "physical_group_id",
    "exact_reconstruction_multiplier",
    "physical_and_computational_multiplicity",
    "inverse_aggregation",
    "cover_class",
    "reconnection_destination",
    "source_and_target_shift_tags",
    "physical_normalization",
]
SELECTOR_REQUIRED_FIELDS = [
    "stage_id",
    "source_shift_tag",
    "target_shift_tag",
    "source_selector_domain",
    "target_selector_domain",
    "stage_matrix_edge",
    "shift_preservation_source",
]


def render(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def text_file_digest(path: Path) -> str:
    """Hash canonical text, independent of the checkout newline convention."""
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def aggregate_edges(
    source_ids: list[str],
    target_ids: list[str],
    edges: list[dict[str, Any]]
) -> list[list[Fraction]]:
    source_index = {value: index for index, value in enumerate(source_ids)}
    target_index = {value: index for index, value in enumerate(target_ids)}
    matrix = [
        [Fraction(0) for _ in source_ids]
        for _ in target_ids
    ]
    for edge in edges:
        matrix[target_index[edge["target"]]][source_index[edge["source"]]] += Fraction(
            edge["numerator"], edge.get("denominator", 1)
        )
    return matrix


def aggregate_commutes(
    source_ids: list[str],
    target_ids: list[str],
    source_shift: dict[str, int],
    target_shift: dict[str, int],
    edges: list[dict[str, Any]],
    h0: int
) -> bool:
    matrix = aggregate_edges(source_ids, target_ids, edges)
    for ti, target in enumerate(target_ids):
        for si, source in enumerate(source_ids):
            lhs = (1 if target_shift[target] == h0 else 0) * matrix[ti][si]
            rhs = matrix[ti][si] * (1 if source_shift[source] == h0 else 0)
            if lhs != rhs:
                return False
    return True


def pathwise_preserves(
    source_shift: dict[str, int],
    target_shift: dict[str, int],
    edges: list[dict[str, Any]],
    h0: int
) -> bool:
    for edge in edges:
        multiplier = Fraction(edge["numerator"], edge.get("denominator", 1))
        if not multiplier:
            continue
        source_selected = source_shift[edge["source"]] == h0
        target_selected = target_shift[edge["target"]] == h0
        if source_selected != target_selected:
            return False
    return True


def synthetic_tests() -> dict[str, Any]:
    source_ids = ["s_h0", "s_other"]
    target_ids = ["t_h0", "t_other"]
    source_shift = {"s_h0": 2, "s_other": 4}
    target_shift = {"t_h0": 2, "t_other": 4}
    good = [
        {"edge_id": "g1", "source": "s_h0", "target": "t_h0", "numerator": 1},
        {"edge_id": "g2", "source": "s_other", "target": "t_other", "numerator": 1}
    ]
    hidden = [
        {"edge_id": "b1", "source": "s_h0", "target": "t_other", "numerator": 1},
        {"edge_id": "b2", "source": "s_h0", "target": "t_other", "numerator": -1}
    ]
    if not aggregate_commutes(
        source_ids, target_ids, source_shift, target_shift, good, 2
    ):
        raise ValueError("good aggregate square should commute")
    if not pathwise_preserves(source_shift, target_shift, good, 2):
        raise ValueError("good occurrence edges should preserve shift")
    if not aggregate_commutes(
        source_ids, target_ids, source_shift, target_shift, hidden, 2
    ):
        raise ValueError("hidden leakage should cancel in aggregate matrix")
    if pathwise_preserves(source_shift, target_shift, hidden, 2):
        raise ValueError("row-separated audit must expose hidden leakage")
    return {
        "scope": "SYNTHETIC_L0_ONLY",
        "good_aggregate_commutes": True,
        "good_pathwise_preserves": True,
        "opposite_cross_shift_edges_cancel_in_aggregate": True,
        "row_separated_lift_detects_hidden_leakage": True
    }


def build_manifest(source: dict[str, Any]) -> dict[str, Any]:
    if source.get("status") != "PASS":
        raise ValueError("TPC-143 certificate is not PASS")
    if source["source"].get("source_chain_validation") != "PASS":
        raise ValueError("TPC-143 upstream source chain is not validated")
    if not source["proved"]["required_domain_all_nonsoft_ETO_plus_FUM"]:
        raise ValueError("TPC-143 all-nonsoft domain proof drifted")
    if source["census"]["obligations_sha256"] != text_file_digest(TPC143_OBLIGATIONS):
        raise ValueError("TPC-143 certificate does not bind its obligation archive")
    if source["proved"]["P_h0_cut_identity"] != "PROVED_L1":
        raise ValueError("TPC-143 cut selector status drifted")
    return {
        "schema": "tpc145-actual-group-shift-manifest-v1",
        "required_domain": "ALL_NONSOFT_CUT_PATHS",
        "cut_selector": {
            "map_id": "P_h0_cut",
            "h0": 2,
            "status": "PROVED_L1",
            "operator": "IDENTITY",
            "is_downstream_selector": False
        },
        "physical_grouping_G": {
            "status": "NOT_TESTABLE",
            "source_status": "NOT_TESTABLE",
            "actual_occurrence_edges": [],
            "required_fields": GROUPING_REQUIRED_FIELDS
        },
        "downstream_selector": {
            "map_id": "P_h0_downstream",
            "status": "NOT_TESTABLE",
            "source_status": "NOT_TESTABLE",
            "actual_stage_edges": [],
            "required_fields": SELECTOR_REQUIRED_FIELDS
        },
        "commuting_square": {
            "aggregate_status": "NOT_TESTABLE",
            "row_separated_status": "NOT_TESTABLE",
            "required_identity": "P_phys_G_EQUALS_G_P_source",
            "provenance_certificate": "ROW_SEPARATED_EDGEWISE_SHIFT_PRESERVATION"
        },
        "claim_boundary": {
            "cut_selector_is_downstream_selector": False,
            "aggregate_cancellation_is_pathwise_provenance": False,
            "new_positive_fixed_h0_L2": False,
            "physical_cover": False,
            "prime_pair_or_twin_prime_theorem": False
        }
    }


def validate_manifest(manifest: dict[str, Any]) -> None:
    if set(manifest) != {
        "schema",
        "required_domain",
        "cut_selector",
        "physical_grouping_G",
        "downstream_selector",
        "commuting_square",
        "claim_boundary",
    } or manifest["schema"] != "tpc145-actual-group-shift-manifest-v1":
        raise ValueError("manifest top-level contract drifted")
    if manifest["required_domain"] != "ALL_NONSOFT_CUT_PATHS":
        raise ValueError("G/P domain must include ETO and FUM")
    cut = manifest["cut_selector"]
    if cut != {
        "map_id": "P_h0_cut",
        "h0": 2,
        "status": "PROVED_L1",
        "operator": "IDENTITY",
        "is_downstream_selector": False,
    }:
        raise ValueError("proved cut selector was lost")
    grouping = manifest["physical_grouping_G"]
    if (
        grouping["status"] != "NOT_TESTABLE"
        or grouping["source_status"] != "NOT_TESTABLE"
        or grouping["actual_occurrence_edges"]
    ):
        raise ValueError("physical grouping was fabricated")
    if grouping["required_fields"] != GROUPING_REQUIRED_FIELDS:
        raise ValueError("physical grouping field contract drifted")
    selector = manifest["downstream_selector"]
    if (
        selector["status"] != "NOT_TESTABLE"
        or selector["source_status"] != "NOT_TESTABLE"
        or selector["actual_stage_edges"]
    ):
        raise ValueError("downstream shift stages were fabricated")
    if selector["required_fields"] != SELECTOR_REQUIRED_FIELDS:
        raise ValueError("downstream selector field contract drifted")
    square = manifest["commuting_square"]
    if (
        square["aggregate_status"] != "NOT_TESTABLE"
        or square["row_separated_status"] != "NOT_TESTABLE"
        or square["required_identity"] != "P_phys_G_EQUALS_G_P_source"
        or square["provenance_certificate"]
        != "ROW_SEPARATED_EDGEWISE_SHIFT_PRESERVATION"
    ):
        raise ValueError("commuting-square contract was promoted or changed")
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
        "cut_to_downstream_promotion_rejected": rejected(
            lambda value: value["cut_selector"].__setitem__(
                "is_downstream_selector", True
            )
        ),
        "fabricated_physical_edge_rejected": rejected(
            lambda value: value["physical_grouping_G"]["actual_occurrence_edges"].append(
                {"source": "x", "target": "y"}
            )
        ),
        "fabricated_stage_edge_rejected": rejected(
            lambda value: value["downstream_selector"]["actual_stage_edges"].append(
                {"source": "x", "target": "y"}
            )
        ),
        "aggregate_provenance_promotion_rejected": rejected(
            lambda value: value["claim_boundary"].__setitem__(
                "aggregate_cancellation_is_pathwise_provenance", True
            )
        ),
        "physical_source_promotion_rejected": rejected(
            lambda value: value["physical_grouping_G"].__setitem__(
                "source_status", "PROVED"
            )
        ),
        "aggregate_status_promotion_rejected": rejected(
            lambda value: value["commuting_square"].__setitem__(
                "aggregate_status", "PROVED_L1"
            )
        ),
        "row_separated_status_promotion_rejected": rejected(
            lambda value: value["commuting_square"].__setitem__(
                "row_separated_status", "PROVED_L1"
            )
        ),
        "deleted_grouping_field_rejected": rejected(
            lambda value: value["physical_grouping_G"]["required_fields"].pop()
        ),
        "false_physical_cover_rejected": rejected(
            lambda value: value["claim_boundary"].__setitem__(
                "physical_cover", True
            )
        ),
        "false_L2_claim_rejected": rejected(
            lambda value: value["claim_boundary"].__setitem__(
                "new_positive_fixed_h0_L2", True
            )
        ),
    }
    if not all(tests.values()):
        raise ValueError("TPC-145 mutation regression failed")
    return tests


def build() -> tuple[bytes, bytes]:
    source = json.loads(TPC143_CERT.read_text(encoding="utf-8"))
    manifest = build_manifest(source)
    validate_manifest(manifest)
    synthetic = synthetic_tests()
    mutations = mutation_tests(manifest)
    manifest_bytes = render(manifest)
    certificate = {
        "schema": "tpc145-group-shift-certificate-v1",
        "status": "PASS",
        "source": {
            "tpc143_certificate_sha256": text_file_digest(TPC143_CERT),
            "hash_is_integrity_only": True
        },
        "theorem": {
            "aggregate_commuting_square_block_criterion": "PROVED_L0",
            "row_separated_commutation_iff_edgewise_shift_preservation": "PROVED_L0",
            "P_h0_cut_identity": "PROVED_L1"
        },
        "synthetic_regression": synthetic,
        "actual_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "actual_status": {
            "H1.cut_Ph0": "PROVED_L1",
            "H1.frontier_G_totality": "NOT_TESTABLE",
            "H1.frontier_Ph0_downstream_totality": "NOT_TESTABLE",
            "H1.frontier_G_Ph0_commutation": "NOT_TESTABLE"
        },
        "scoped_stops": [
            {
                "route": "cut_h0_metadata_as_downstream_selector",
                "status": "STOP_DECLARED_ROUTE"
            },
            {
                "route": "aggregate_cancellation_as_shift_provenance",
                "status": "STOP_DECLARED_ROUTE"
            }
        ],
        "selected_occurrence_augmented_route_stopped": False,
        "mutation_regression": mutations,
        "claim_boundary": {
            "new_positive_fixed_h0_L2": False,
            "physical_cover": False,
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
        print("TPC-145 CHECK PASS")
    else:
        for path, content in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        print("TPC-145 WRITE PASS")
    print(
        json.dumps(
            {
                "P_cut": "PROVED_L1",
                "G": "NOT_TESTABLE",
                "P_downstream": "NOT_TESTABLE"
            },
            sort_keys=True
        )
    )


if __name__ == "__main__":
    main()
