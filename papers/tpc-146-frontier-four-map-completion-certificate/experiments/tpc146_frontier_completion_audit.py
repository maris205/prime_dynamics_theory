#!/usr/bin/env python3
"""Build and verify the TPC-146 four-map frontier certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
SOURCE_PATHS = {
    "tpc136_cut_paths": (
        PAPERS
        / "tpc-136-complete-native-cut-archive"
        / "samples"
        / "tpc136_cut_paths.jsonl"
    ),
    "tpc143_certificate": (
        PAPERS
        / "tpc-143-frontier-occurrence-lift-contract"
        / "experiments"
        / "tpc143_frontier_lift_certificate.json"
    ),
    "tpc143_obligations": (
        PAPERS
        / "tpc-143-frontier-occurrence-lift-contract"
        / "samples"
        / "tpc143_frontier_lift_obligations.jsonl"
    ),
    "tpc144_certificate": (
        PAPERS
        / "tpc-144-determinant-zero-quotient-kernel-test"
        / "experiments"
        / "tpc144_quotient_kernel_certificate.json"
    ),
    "tpc144_manifest": (
        PAPERS
        / "tpc-144-determinant-zero-quotient-kernel-test"
        / "samples"
        / "tpc144_actual_quotient_manifest.json"
    ),
    "tpc145_certificate": (
        PAPERS
        / "tpc-145-physical-grouping-shift-commutation"
        / "experiments"
        / "tpc145_group_shift_certificate.json"
    ),
    "tpc145_manifest": (
        PAPERS
        / "tpc-145-physical-grouping-shift-commutation"
        / "samples"
        / "tpc145_actual_group_shift_manifest.json"
    ),
}
OUT_MANIFEST = PAPER / "samples" / "tpc146_frontier_completion_manifest.json"
OUT_CERT = HERE / "tpc146_frontier_completion_certificate.json"

DEFECT_IDS = [
    "D_L",
    "D_QD",
    "D_QZ",
    "D_G",
    "D_P",
    "D_DZ",
    "D_GP",
    "D_cover",
    "D_rec"
]
REQUIRED_COMPONENTS = [
    "conservative_row_separated_occurrence_lift",
    "total_Q_D",
    "total_Q_Z",
    "total_physical_grouping_G",
    "total_downstream_P_h0",
    "QD_QZ_intertwining",
    "G_Ph0_occurrence_commutation",
    "physical_cover",
    "exact_reconnection",
    "complete_occurrence_registry",
]


def render(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def text_file_digest(path: Path) -> str:
    """Hash canonical text, independent of the checkout newline convention."""
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def load_sources() -> dict[str, Any]:
    return {
        name: json.loads(path.read_text(encoding="utf-8"))
        for name, path in SOURCE_PATHS.items()
        if path.suffix == ".json"
    }


def build_manifest(sources: dict[str, Any]) -> dict[str, Any]:
    t143 = sources["tpc143_certificate"]
    t144 = sources["tpc144_certificate"]
    t145 = sources["tpc145_certificate"]
    if any(source.get("status") != "PASS" for source in (t143, t144, t145)):
        raise ValueError("a TPC-143--145 source certificate is not PASS")
    if t143["source"].get("source_chain_validation") != "PASS":
        raise ValueError("TPC-143 upstream source chain is not validated")
    if not t143["proved"]["required_domain_all_nonsoft_ETO_plus_FUM"]:
        raise ValueError("TPC-143 all-nonsoft domain proof drifted")
    if (
        t143["census"]["nonsoft_path_count"]
        != t143["census"]["terminal_type_counts"]["ELIGIBLE_TAIL_OPEN"]
        + t143["census"]["terminal_type_counts"]["FRONTIER_UNMAPPED"]
    ):
        raise ValueError("TPC-143 nonsoft census is not ETO plus FUM")
    if (
        t143["census"]["obligations_sha256"]
        != text_file_digest(SOURCE_PATHS["tpc143_obligations"])
    ):
        raise ValueError("TPC-143 certificate does not bind its obligations")
    if (
        t144["actual_manifest_sha256"]
        != text_file_digest(SOURCE_PATHS["tpc144_manifest"])
    ):
        raise ValueError("TPC-144 certificate does not bind its manifest")
    if (
        t145["actual_manifest_sha256"]
        != text_file_digest(SOURCE_PATHS["tpc145_manifest"])
    ):
        raise ValueError("TPC-145 certificate does not bind its manifest")
    if t143["current_actual_status"]["H1.frontier_occurrence_lift"] != "NOT_TESTABLE":
        raise ValueError("TPC-143 lift status drifted")
    if any(value != "NOT_TESTABLE" for value in t144["actual_status"].values()):
        raise ValueError("TPC-144 actual quotient status drifted")
    if t145["actual_status"]["H1.frontier_G_totality"] != "NOT_TESTABLE":
        raise ValueError("TPC-145 grouping status drifted")
    defects = {
        defect_id: {
            "status": "NOT_EVALUABLE",
            "certified_zero": False,
            "source_matrix_present": False
        }
        for defect_id in DEFECT_IDS
    }
    census = t143["census"]
    return {
        "schema": "tpc146-frontier-completion-manifest-v1",
        "required_domain": "ALL_NONSOFT_CUT_PATHS",
        "cut_census": {
            "nonsoft_path_count": census["nonsoft_path_count"],
            "ELIGIBLE_TAIL_OPEN": census["terminal_type_counts"]["ELIGIBLE_TAIL_OPEN"],
            "FRONTIER_UNMAPPED": census["terminal_type_counts"]["FRONTIER_UNMAPPED"],
            "finite_sample_empty_ETO": census["finite_sample_empty_ETO"],
            "empty_ETO_is_asymptotic_totality": False
        },
        "map_route": {
            "status": "NOT_TESTABLE",
            "required_components": REQUIRED_COMPONENTS,
            "literal_source_semantics_requirement": "THEOREM_BACKED_MATRICES_DOMAINS_MULTIPLIERS_LINEAGE_AND_NORMALIZATION",
            "zero_defect_vector": defects,
            "all_defects_certified_zero": False,
            "cut_P_h0_identity_is_not_D_P": True
        },
        "scalar_route": {
            "status": "NOT_TESTABLE",
            "required_statement": "COMPLETE_ORIGINAL_SCALE_S_frontier_EQUALS_oX",
            "theorem_source": None,
            "finite_regression_is_source": False,
            "remaining_ETO_requirement": "TOTAL_DOWNSTREAM_ETO_MAP_OR_COMPLETE_ETO_SOFT_THEOREM",
            "remaining_ETO_status": "NOT_TESTABLE",
            "remaining_ETO_source": None
        },
        "totalization": {
            "logic": "ALL_NONSOFT_MAP_ROUTE_OR_FRONTIER_SCALAR_AND_ETO_ROUTE",
            "status": "NOT_TESTABLE",
            "map_route_pass": False,
            "scalar_route_pass": False
        },
        "first_missing": {
            "node_id": "H1.frontier_occurrence_lift",
            "status": "NOT_TESTABLE",
            "artifact": "conservative row-separated one-to-many cut-to-occurrence matrix with full lineage"
        },
        "claim_boundary": {
            "current_schema_only_totalization": False,
            "unknown_defect_is_zero": False,
            "formal_support_is_actual_nonzero_support": False,
            "new_positive_fixed_h0_L2": False,
            "frontier_scalar_oX": False,
            "physical_cover": False,
            "endpoint_1_over_400": False,
            "prime_pair_or_twin_prime_theorem": False
        }
    }


def validate_manifest(
    manifest: dict[str, Any], expected_census: dict[str, Any]
) -> None:
    if set(manifest) != {
        "schema",
        "required_domain",
        "cut_census",
        "map_route",
        "scalar_route",
        "totalization",
        "first_missing",
        "claim_boundary",
    } or manifest["schema"] != "tpc146-frontier-completion-manifest-v1":
        raise ValueError("manifest top-level contract drifted")
    if manifest["required_domain"] != "ALL_NONSOFT_CUT_PATHS":
        raise ValueError("completion domain must include ETO and FUM")
    census = manifest["cut_census"]
    if set(census) != {
        "nonsoft_path_count",
        "ELIGIBLE_TAIL_OPEN",
        "FRONTIER_UNMAPPED",
        "finite_sample_empty_ETO",
        "empty_ETO_is_asymptotic_totality",
    }:
        raise ValueError("cut census contract drifted")
    if any(
        not isinstance(census[key], int) or isinstance(census[key], bool) or census[key] < 0
        for key in ("nonsoft_path_count", "ELIGIBLE_TAIL_OPEN", "FRONTIER_UNMAPPED")
    ):
        raise ValueError("cut census counts must be nonnegative integers")
    if (
        census["nonsoft_path_count"]
        != census["ELIGIBLE_TAIL_OPEN"] + census["FRONTIER_UNMAPPED"]
    ):
        raise ValueError("ALL_NONSOFT must equal ETO plus FUM")
    if census["finite_sample_empty_ETO"] != (census["ELIGIBLE_TAIL_OPEN"] == 0):
        raise ValueError("finite ETO flag does not match the census")
    if census != expected_census:
        raise ValueError("cut census is not bound to TPC-143")
    if census["empty_ETO_is_asymptotic_totality"]:
        raise ValueError("empty finite ETO sample was promoted")
    route = manifest["map_route"]
    if route["status"] != "NOT_TESTABLE" or route["all_defects_certified_zero"]:
        raise ValueError("map route was fabricated")
    if not route["cut_P_h0_identity_is_not_D_P"]:
        raise ValueError("cut selector was substituted for downstream defect")
    if route["required_components"] != REQUIRED_COMPONENTS:
        raise ValueError("map-route component contract drifted")
    if (
        route["literal_source_semantics_requirement"]
        != "THEOREM_BACKED_MATRICES_DOMAINS_MULTIPLIERS_LINEAGE_AND_NORMALIZATION"
    ):
        raise ValueError("literal source-semantics requirement drifted")
    if set(route["zero_defect_vector"]) != set(DEFECT_IDS):
        raise ValueError("zero-defect vector has a missing or extra component")
    for defect_id in DEFECT_IDS:
        if defect_id not in route["zero_defect_vector"]:
            raise ValueError(f"missing defect component {defect_id}")
        defect = route["zero_defect_vector"][defect_id]
        if defect["status"] != "NOT_EVALUABLE":
            raise ValueError(f"unknown {defect_id} was promoted")
        if defect["certified_zero"] or defect["source_matrix_present"]:
            raise ValueError(f"fabricated source or zero for {defect_id}")
    scalar = manifest["scalar_route"]
    if (
        scalar["required_statement"]
        != "COMPLETE_ORIGINAL_SCALE_S_frontier_EQUALS_oX"
        or scalar["finite_regression_is_source"]
        or scalar["remaining_ETO_requirement"]
        != "TOTAL_DOWNSTREAM_ETO_MAP_OR_COMPLETE_ETO_SOFT_THEOREM"
    ):
        raise ValueError("scalar-route contract drifted")
    if (
        scalar["status"] != "NOT_TESTABLE"
        or scalar["theorem_source"] is not None
        or scalar["remaining_ETO_status"] != "NOT_TESTABLE"
        or scalar["remaining_ETO_source"] is not None
    ):
        raise ValueError("frontier scalar theorem was fabricated")
    total = manifest["totalization"]
    if (
        total["logic"]
        != "ALL_NONSOFT_MAP_ROUTE_OR_FRONTIER_SCALAR_AND_ETO_ROUTE"
        or total["status"] != "NOT_TESTABLE"
        or total["map_route_pass"]
        or total["scalar_route_pass"]
    ):
        raise ValueError("map/scalar disjunction drifted")
    if manifest["first_missing"]["node_id"] != "H1.frontier_occurrence_lift":
        raise ValueError("first missing node drifted")
    if (
        manifest["first_missing"]["status"] != "NOT_TESTABLE"
        or manifest["first_missing"]["artifact"]
        != "conservative row-separated one-to-many cut-to-occurrence matrix with full lineage"
    ):
        raise ValueError("first missing artifact contract drifted")
    if any(manifest["claim_boundary"].values()):
        raise ValueError("a negative claim boundary was promoted")


def mutation_tests(
    manifest: dict[str, Any], expected_census: dict[str, Any]
) -> dict[str, bool]:
    def rejected(mutator) -> bool:
        trial = copy.deepcopy(manifest)
        mutator(trial)
        try:
            validate_manifest(trial, expected_census)
        except ValueError:
            return True
        return False

    tests = {
        "frontier_only_domain_rejected": rejected(
            lambda value: value.__setitem__("required_domain", "FRONTIER_ONLY")
        ),
        "empty_ETO_promotion_rejected": rejected(
            lambda value: value["cut_census"].__setitem__(
                "empty_ETO_is_asymptotic_totality", True
            )
        ),
        "unknown_defect_zero_rejected": rejected(
            lambda value: value["map_route"]["zero_defect_vector"]["D_L"].__setitem__(
                "certified_zero", True
            )
        ),
        "cut_selector_substitution_rejected": rejected(
            lambda value: value["map_route"].__setitem__(
                "cut_P_h0_identity_is_not_D_P", False
            )
        ),
        "fabricated_scalar_source_rejected": rejected(
            lambda value: value["scalar_route"].__setitem__(
                "theorem_source", "fabricated"
            )
        ),
        "fabricated_ETO_source_rejected": rejected(
            lambda value: value["scalar_route"].__setitem__(
                "remaining_ETO_source", "fabricated"
            )
        ),
        "false_totalization_rejected": rejected(
            lambda value: value["totalization"].__setitem__("status", "PROVED_L1")
        ),
        "first_missing_drift_rejected": rejected(
            lambda value: value["first_missing"].__setitem__(
                "node_id", "H3.arithmetic"
            )
        ),
        "census_conservation_mutation_rejected": rejected(
            lambda value: value["cut_census"].__setitem__(
                "nonsoft_path_count",
                value["cut_census"]["nonsoft_path_count"] + 1,
            )
        ),
        "deleted_defect_component_rejected": rejected(
            lambda value: value["map_route"]["zero_defect_vector"].pop("D_rec")
        ),
        "extra_defect_component_rejected": rejected(
            lambda value: value["map_route"]["zero_defect_vector"].__setitem__(
                "D_extra",
                {
                    "status": "NOT_EVALUABLE",
                    "certified_zero": False,
                    "source_matrix_present": False,
                },
            )
        ),
        "required_component_deletion_rejected": rejected(
            lambda value: value["map_route"]["required_components"].pop()
        ),
        "false_L2_claim_rejected": rejected(
            lambda value: value["claim_boundary"].__setitem__(
                "new_positive_fixed_h0_L2", True
            )
        ),
        "scalar_requirement_drift_rejected": rejected(
            lambda value: value["scalar_route"].__setitem__(
                "required_statement", "FINITE_SAMPLE_FRONTIER_IS_SMALL"
            )
        ),
    }
    if not all(tests.values()):
        raise ValueError("TPC-146 mutation regression failed")
    return tests


def build() -> tuple[bytes, bytes]:
    sources = load_sources()
    manifest = build_manifest(sources)
    expected_census = manifest["cut_census"]
    validate_manifest(manifest, expected_census)
    mutations = mutation_tests(manifest, expected_census)
    manifest_bytes = render(manifest)
    certificate = {
        "schema": "tpc146-frontier-completion-certificate-v1",
        "status": "PASS",
        "source_locks": {
            name: {
                "sha256": text_file_digest(path),
                "role": "INTEGRITY_ONLY"
            }
            for name, path in SOURCE_PATHS.items()
        },
        "theorem": {
            "zero_defect_map_route_contract": "PROVED_L0",
            "all_nonsoft_map_or_frontier_scalar_and_ETO_disjunction": "PROVED_L1_INTERFACE",
            "unknown_is_not_zero": True,
            "all_nonsoft_is_ETO_plus_FUM": True
        },
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "current_verdict": "NOT_TESTABLE",
        "first_missing": "H1.frontier_occurrence_lift",
        "scoped_stop": {
            "route": "current_schema_only_totalization",
            "status": "STOP_DECLARED_ROUTE"
        },
        "open_routes": {
            "occurrence_augmented_map_route": True,
            "frontier_scalar_plus_ETO_route": True
        },
        "mutation_regression": mutations,
        "claim_boundary": manifest["claim_boundary"]
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
        print("TPC-146 CHECK PASS")
    else:
        for path, content in outputs.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        print("TPC-146 WRITE PASS")
    print(
        json.dumps(
            {
                "verdict": "NOT_TESTABLE",
                "first_missing": "H1.frontier_occurrence_lift",
                "map_route": False,
                "scalar_route": False
            },
            sort_keys=True
        )
    )


if __name__ == "__main__":
    main()
