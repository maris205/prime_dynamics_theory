#!/usr/bin/env python3
"""Build the deterministic TPC-151 source-locked integration manifest.

The audit is deliberately administrative.  It validates canonical source
hashes, typed imports, a route-specific proof DAG, endpoint bookkeeping, and
the exact first-missing pointer.  It does not estimate an arithmetic sum.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER_DIR = HERE.parent
PAPERS_DIR = PAPER_DIR.parent
SCHEMA_PATH = HERE / "tpc151_integration_manifest.schema.json"
MANIFEST_PATH = HERE / "tpc151_integration_manifest.json"
AUDIT_PATH = HERE / "tpc151_source_locked_integration_audit.json"

TPC141_DIR = PAPERS_DIR / "tpc-141-source-locked-cut-arithmetic-integration"
TPC141_MANIFEST = TPC141_DIR / "experiments" / "tpc141_batch_manifest.json"
TPC141_SCHEMA = TPC141_DIR / "experiments" / "tpc141_batch_manifest.schema.json"
TPC142_DIR = PAPERS_DIR / "tpc-142-mvp4-source-locked-route-decision"
TPC142_SNAPSHOT = TPC142_DIR / "experiments" / "tpc142_mvp4_snapshot.json"
TPC142_SCHEMA = TPC142_DIR / "experiments" / "tpc142_mvp4_snapshot.schema.json"

SCHEMA_NAME = "tpc-151-source-locked-frontier-quotient-integration-v1"
HASH_MODE = "CANONICAL_UTF8_LF_V2"
VALID_STATUSES = {"PROVED", "CONDITIONAL", "OPEN", "NOT_TESTABLE", "REFUTED"}
VALID_LEVELS = {
    "L0_MODEL",
    "L1_STRUCTURAL",
    "L1_ACTUAL_CORE",
    "L1_CONDITIONAL",
    "L1_NEGATIVE",
    "L2_TARGET_POSITIVE",
    "L2_ACTUAL_POSITIVE",
}
VALID_ROLES = {
    "STRUCTURAL",
    "PHYSICAL_SYNTHESIS",
    "ARITHMETIC_SHADOW",
    "ARITHMETIC_TARGET",
    "ARITHMETIC_NEGATIVE",
    "ROOT",
}
ARITHMETIC_ROLES = {
    "ARITHMETIC_SHADOW",
    "ARITHMETIC_TARGET",
    "ARITHMETIC_NEGATIVE",
}
SOURCE_SUFFIXES = {".tex", ".md", ".bib", ".py", ".json", ".jsonl"}
FRONTIER_TOTALIZATION_LOGIC = (
    "ALL_NONSOFT_MAP_ROUTE_OR_FRONTIER_SCALAR_AND_ETO_ROUTE"
)
REQUIRED_ARTIFACT_CONTRACTS = {
    "H1.frontier_occurrence_lift": (
        "a conservative row-separated one-to-many lift on every "
        "ELIGIBLE_TAIL_OPEN and FRONTIER_UNMAPPED path, with exact "
        "occurrence, stage, parent, multiplier, native, h0, "
        "normalization and support-status lineage"
    ),
    "H1.frontier_totalization": (
        "either (i) the selected all-nonsoft map route with a zero "
        "four-map defect vector and complete typed sources on every ETO "
        "and FUM path, or (ii) the scalar-plus-ETO route with both a "
        "complete original-frontier S_frontier(X)=o(X) theorem and a "
        "theorem-backed disposition of every ETO path via total maps or "
        "a complete original-scale soft theorem"
    ),
    "H1.actual_carrier": (
        "a complete occurrence-resolved actual carrier on every ETO and "
        "FUM path in the inherited physical atomic normalization"
    ),
    "G150.actual_corridor_return": (
        "scope-matched literal physical weights and generic phases, a "
        "deterministic all-prefix theorem or valid non-atomic selector, "
        "and the complete four-sign return on the actual fixed-h0 carrier"
    ),
    "H3.actual_packet_saving": (
        "a scope-matched actual fixed-h0 physical-packet theorem with "
        "positive fixed-X-power sigma_raw at least 1/400"
    ),
    "H5.det_zero": (
        "an actual determinant and zero-mode exponent pair on completed "
        "occurrence fibers with source-matched normalization"
    ),
    "H6.physical_cover": (
        "a complete theorem-backed physical cover of all actual active "
        "occurrences with exact disjoint-cover lineage"
    ),
    "H7.fixed_h0_totality": (
        "actual downstream fixed-h0 selector totality on every active "
        "occurrence, not the cut-stage identity"
    ),
    "H8.final_reconnection": (
        "exact physical hard-packet reconnection with literal weights, "
        "signs, phases and all-prefix lineage"
    ),
    "H9.physical_registry": (
        "a complete actual occurrence registry plus an H2--H5-independent "
        "theorem-backed physical-amplitude upper certificate "
        "Lambda_phys<1/400"
    ),
    "ROOT.endpoint_synthesis": (
        "a scope-matched H1--H9 conjunction, sigma_raw>=1/400, "
        "Lambda_phys<1/400 and sigma_raw-Lambda_phys>0"
    ),
}
PROGRESS_CLASSIFICATION = {
    "structural_achieved_level": "L1_STRUCTURAL",
    "actual_core_arithmetic_achieved_level": "L1_ACTUAL_CORE",
    "actual_fixed_power_target_level": "L2_ACTUAL_POSITIVE",
    "actual_fixed_power_status": "NOT_PROVED",
    "actual_fixed_power_achieved": False,
    "new_structural_L1": True,
    "new_actual_core_L1": True,
    "new_positive_L2": False,
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(payload: Any) -> str:
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_source_bytes(path: Path) -> bytes:
    """Return a cross-platform canonical representation of a source file."""

    text = normalize_lf(path.read_text(encoding="utf-8"))
    if path.suffix == ".json":
        return canonical_json(json.loads(text)).encode("utf-8")
    return text.encode("utf-8")


def canonical_source_hash(path: Path) -> str:
    return sha256_bytes(canonical_source_bytes(path))


def canonical_json_file(path: Path) -> tuple[dict[str, Any], str]:
    rendered = canonical_json(
        json.loads(normalize_lf(path.read_text(encoding="utf-8")))
    )
    return json.loads(rendered), rendered


def parse_fraction(record: dict[str, int] | None) -> Fraction | None:
    if record is None:
        return None
    denominator = record["denominator"]
    if denominator <= 0:
        raise ValueError("fraction denominator must be positive")
    return Fraction(record["numerator"], denominator)


def fraction_record(value: Fraction | None) -> dict[str, int] | None:
    if value is None:
        return None
    return {"numerator": value.numerator, "denominator": value.denominator}


def find_source_dir(number: int) -> Path:
    matches = sorted(
        path for path in PAPERS_DIR.glob(f"tpc-{number}-*") if path.is_dir()
    )
    if len(matches) != 1:
        raise FileNotFoundError(
            f"expected exactly one frozen TPC-{number} directory, "
            f"found {len(matches)}"
        )
    return matches[0]


def source_inventory(directory: Path) -> list[Path]:
    required = [
        directory / "main.tex",
        directory / "README.md",
        directory / "references.bib",
    ]
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(f"{directory.name} lacks {path.name}")
    files = [
        path
        for path in directory.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix in SOURCE_SUFFIXES
    ]
    return sorted(set(files), key=lambda path: path.relative_to(directory).as_posix())


def source_bundle(number: int) -> dict[str, Any]:
    directory = find_source_dir(number)
    files = source_inventory(directory)
    hashes = {
        path.relative_to(directory).as_posix(): canonical_source_hash(path)
        for path in files
    }
    identity = {
        "paper": f"TPC-{number}",
        "directory": directory.name,
        "hash_mode": HASH_MODE,
        "files": hashes,
    }
    return {
        **identity,
        "bundle_sha256": sha256_bytes(
            canonical_json(identity).encode("utf-8")
        ),
    }


def experiment_json(number: int, name: str) -> dict[str, Any]:
    path = find_source_dir(number) / "experiments" / name
    if not path.is_file():
        raise FileNotFoundError(f"TPC-{number} lacks source contract {name}")
    payload, _ = canonical_json_file(path)
    return payload


def source_contracts() -> dict[str, Any]:
    c143 = experiment_json(143, "tpc143_frontier_lift_certificate.json")
    c144 = experiment_json(144, "tpc144_quotient_kernel_certificate.json")
    c145 = experiment_json(145, "tpc145_group_shift_certificate.json")
    c146 = experiment_json(146, "tpc146_frontier_completion_certificate.json")
    c147 = experiment_json(147, "tpc147_periodic_reassembly_audit.json")
    c148 = experiment_json(148, "tpc148_quotient_lift_audit.json")
    c149 = experiment_json(149, "tpc149_actual_core_corridor_audit.json")
    c150 = experiment_json(150, "tpc150_actual_return_manifest.json")

    if (
        c143["status"] != "PASS"
        or c143["first_missing"]["node_id"]
        != "H1.frontier_occurrence_lift"
        or c143["proved"]["P_h0_cut_identity"] != "PROVED_L1"
        or c143["scoped_stop"]["route"]
        != "current_schema_only_downstream_label_derivation"
        or c143["scoped_stop"]["status"] != "STOP_DECLARED_ROUTE"
        or c143["scoped_stop"]["selected_augmented_route_stopped"]
    ):
        raise ValueError("TPC-143 source contract drift")
    if (
        c144["status"] != "PASS"
        or set(c144["actual_status"].values()) != {"NOT_TESTABLE"}
        or c144["scoped_stop"]["status"] != "STOP_DECLARED_ROUTE"
    ):
        raise ValueError("TPC-144 source contract drift")
    if (
        c145["status"] != "PASS"
        or c145["actual_status"]["H1.cut_Ph0"] != "PROVED_L1"
        or c145["actual_status"]["H1.frontier_G_totality"]
        != "NOT_TESTABLE"
        or c145["actual_status"]["H1.frontier_Ph0_downstream_totality"]
        != "NOT_TESTABLE"
    ):
        raise ValueError("TPC-145 source contract drift")
    if (
        c146["status"] != "PASS"
        or c146["current_verdict"] != "NOT_TESTABLE"
        or c146["first_missing"] != "H1.frontier_occurrence_lift"
        or not c146["theorem"]["all_nonsoft_is_ETO_plus_FUM"]
        or c146["theorem"][
            "all_nonsoft_map_or_frontier_scalar_and_ETO_disjunction"
        ] != "PROVED_L1_INTERFACE"
        or not c146["open_routes"]["occurrence_augmented_map_route"]
        or not c146["open_routes"]["frontier_scalar_plus_ETO_route"]
    ):
        raise ValueError("TPC-146 source contract drift")
    theorem147 = c147["derived_theorem"]
    if (
        c147["status"] != "PASS"
        or theorem147["node_id"] != "A147.periodic_residue_reassembly"
        or theorem147["status"] != "PROVED"
        or theorem147["promotion_eligible"]
    ):
        raise ValueError("TPC-147 source contract drift")
    exports148 = {record["node_id"]: record for record in c148["exports"]}
    if (
        c148["status"] != "PASS"
        or exports148["A148.quotient_mobius_lift"]["status"] != "PROVED"
        or exports148["A148.nonpretentious_stability"]["status"] != "PROVED"
    ):
        raise ValueError("TPC-148 source contract drift")
    theorem149 = c149["theorem"]
    if (
        c149["status"] != "PASS"
        or theorem149["node_id"]
        != "A149.actual_mobius_periodic_corridor"
        or theorem149["program_level"] != "L1_ACTUAL_CORE"
        or theorem149["scope_id"]
        != "scope.actual_fixed_two_mobius_periodic_core_almost_scale"
        or theorem149["full_H3_scope_match"]
        or theorem149["promotion_eligible"]
        or c149["claim_boundary"]["positive_X_power"]
    ):
        raise ValueError("TPC-149 source contract drift")
    nodes150 = {record["node_id"]: record for record in c150["nodes"]}
    if (
        nodes150["N150.deterministic_prefix_nonimplication"]["status"]
        != "PROVED"
        or nodes150["G150.actual_corridor_return"]["status"]
        != "NOT_TESTABLE"
        or c150["route_status"]["first_missing"]
        != "H1.frontier_occurrence_lift"
        or c150["route_status"]["positive_L2"]
    ):
        raise ValueError("TPC-150 source contract drift")

    return {
        "TPC-143": {
            "P_h0_cut": "PROVED_L1",
            "occurrence_lift": "NOT_TESTABLE",
            "first_missing": "H1.frontier_occurrence_lift",
            "schema_nonidentifiability_scope": (
                "CURRENT_MAXIMAL_FORMAL_SCHEMA_COMPLETION_CLASS_ONLY"
            ),
            "actual_carrier_impossibility": False,
            "selected_augmented_route_stopped": False,
        },
        "TPC-144": {
            "QD_totality": "NOT_TESTABLE",
            "QZ_totality": "NOT_TESTABLE",
            "intertwining": "NOT_TESTABLE",
        },
        "TPC-145": {
            "P_h0_cut": "PROVED_L1",
            "G_totality": "NOT_TESTABLE",
            "P_h0_downstream_totality": "NOT_TESTABLE",
        },
        "TPC-146": {
            "frontier_totalization": "NOT_TESTABLE",
            "first_missing": "H1.frontier_occurrence_lift",
            "totalization_logic": FRONTIER_TOTALIZATION_LOGIC,
            "interface_status": "PROVED_L1_INTERFACE",
            "map_route_open": True,
            "frontier_scalar_plus_ETO_route_open": True,
        },
        "TPC-147": {
            "node_id": theorem147["node_id"],
            "status": theorem147["status"],
            "promotion_eligible": theorem147["promotion_eligible"],
        },
        "TPC-148": {
            "quotient_lift": exports148["A148.quotient_mobius_lift"]["status"],
            "nonpretentious_stability": exports148[
                "A148.nonpretentious_stability"
            ]["status"],
        },
        "TPC-149": {
            "node_id": theorem149["node_id"],
            "status": theorem149["status"],
            "program_level": theorem149["program_level"],
            "scope_id": theorem149["scope_id"],
            "full_H3_scope_match": theorem149["full_H3_scope_match"],
            "promotion_eligible": theorem149["promotion_eligible"],
            "fixed_X_power_positive": False,
        },
        "TPC-150": {
            "prefix_nonimplication": nodes150[
                "N150.deterministic_prefix_nonimplication"
            ]["status"],
            "actual_corridor_return": nodes150[
                "G150.actual_corridor_return"
            ]["status"],
            "first_missing": c150["route_status"]["first_missing"],
        },
    }


def anchor_chain() -> dict[str, Any]:
    for path in (
        TPC141_MANIFEST,
        TPC141_SCHEMA,
        TPC142_SNAPSHOT,
        TPC142_SCHEMA,
    ):
        if not path.is_file():
            raise FileNotFoundError(f"missing upstream anchor {path}")

    manifest141, rendered141 = canonical_json_file(TPC141_MANIFEST)
    snapshot142, rendered142 = canonical_json_file(TPC142_SNAPSHOT)
    embedded = snapshot142["snapshot"]["source_manifest_sha256"]
    actual = sha256_bytes(rendered141.encode("utf-8"))
    if embedded != actual:
        raise ValueError("TPC-142 no longer anchors the canonical TPC-141 manifest")
    if snapshot142["current_verdict"] != "NOT_TESTABLE":
        raise ValueError("unexpected TPC-142 verdict")
    if snapshot142["first_missing"]["node_id"] != "H1.frontier_totalization":
        raise ValueError("unexpected TPC-142 first-missing anchor")
    if manifest141["snapshot"]["source_hash_semantics"] != "INTEGRITY_ONLY":
        raise ValueError("TPC-141 source hash semantics drift")

    return {
        "hash_mode": HASH_MODE,
        "hash_semantics": "INTEGRITY_ONLY",
        "tpc141_manifest_sha256": actual,
        "tpc141_schema_sha256": canonical_source_hash(TPC141_SCHEMA),
        "tpc142_snapshot_sha256": sha256_bytes(rendered142.encode("utf-8")),
        "tpc142_schema_sha256": canonical_source_hash(TPC142_SCHEMA),
        "tpc142_embedded_tpc141_hash_verified": True,
        "prior_verdict": snapshot142["current_verdict"],
        "prior_first_missing": snapshot142["first_missing"]["node_id"],
    }


def scope_registry() -> dict[str, dict[str, Any]]:
    return {
        "scope.physical_nonsoft_cut": {
            "fixed_h0": True,
            "coverage": "ALL_NONSOFT_CUT_PATHS_ETO_PLUS_FUM",
            "support": "FORMAL_SUPPORT_ENVELOPE",
        },
        "scope.frontier_completion_model": {
            "fixed_h0": True,
            "coverage": "SYNTHETIC_OR_CONDITIONAL_COMPLETION",
            "support": "TYPED_COMPLETION",
        },
        "scope.actual_fixed_two_mobius_periodic_core_almost_scale": {
            "fixed_h0": True,
            "coverage": "SMALL_POLYLOG_PERIODIC_CORE_ALMOST_SCALE",
            "support": "ACTUAL_MOBIUS_CORE_NOT_FULL_PHYSICAL_PACKET",
        },
        "scope.actual_h3": {
            "fixed_h0": True,
            "coverage": "FULL_ACTUAL_PHYSICAL_H3_PACKET",
            "support": "ACTUAL_ACTIVE_SUPPORT",
        },
        "scope.physical_hard_packet": {
            "fixed_h0": True,
            "coverage": "FULL_HARD_PACKET",
            "support": "ACTUAL_ACTIVE_SUPPORT",
        },
    }


def carrier_registry() -> dict[str, dict[str, Any]]:
    return {
        "carrier.all_nonsoft_cut_paths": {
            "classes": ["ELIGIBLE_TAIL_OPEN", "FRONTIER_UNMAPPED"],
            "sample_eto_may_be_empty": True,
        },
        "carrier.downstream_occurrences": {
            "row_separated": True,
            "current_status": "MISSING",
        },
        "carrier.fixed_two_mobius_periodic_core": {
            "shift": 2,
            "physical_return_complete": False,
        },
        "carrier.actual_h3_packet": {"physical_return_complete": False},
        "carrier.physical_hard_packet": {"physical_return_complete": False},
    }


def normalization_registry() -> dict[str, dict[str, Any]]:
    return {
        "norm.physical_atomic": {
            "scale": "AMPLITUDE",
            "determinant_label_is_normalization": False,
        },
        "norm.almost_scale_cesaro_core": {
            "scale": "CESARO_CORRELATION",
            "physical_atomic_crosswalk": "OPEN",
        },
    }


def export(
    export_id: str,
    paper: str,
    status: str,
    level: str,
    direction: str,
    role: str,
    scope_id: str,
    carrier_id: str,
    normalization_id: str,
    coverage: str,
    *,
    promotion_eligible: bool = False,
    x_power_sigma: Fraction | None = None,
) -> dict[str, Any]:
    return {
        "export_id": export_id,
        "paper": paper,
        "status": status,
        "program_level": level,
        "direction": direction,
        "role": role,
        "scope_id": scope_id,
        "carrier_id": carrier_id,
        "normalization_id": normalization_id,
        "coverage": coverage,
        "promotion_eligible": promotion_eligible,
        "x_power_sigma": fraction_record(x_power_sigma),
    }


def build_exports() -> list[dict[str, Any]]:
    pc = "scope.physical_nonsoft_cut"
    cc = "carrier.all_nonsoft_cut_paths"
    pa = "norm.physical_atomic"
    model = "scope.frontier_completion_model"
    occ = "carrier.downstream_occurrences"
    core = "scope.actual_fixed_two_mobius_periodic_core_almost_scale"
    core_carrier = "carrier.fixed_two_mobius_periodic_core"
    cnorm = "norm.almost_scale_cesaro_core"
    return [
        export(
            "ANCHOR.N135.eligible_only_stop", "TPC-142", "PROVED",
            "L1_NEGATIVE", "NEGATIVE", "STRUCTURAL", pc, cc, pa,
            "COMPLETE_DECLARED_ROUTE_CELL",
        ),
        export(
            "ANCHOR.N138.shift_one_stop", "TPC-142", "PROVED",
            "L1_NEGATIVE", "NEGATIVE", "ARITHMETIC_NEGATIVE", pc, cc, pa,
            "COMPLETE_DECLARED_ROUTE_CELL",
        ),
        export(
            "S143.cut_shift_selector", "TPC-143", "PROVED",
            "L1_STRUCTURAL", "POSITIVE", "STRUCTURAL", pc, cc, pa,
            "P_H0_CUT_IDENTITY_ONLY",
        ),
        export(
            "N143.schema_nonidentifiability", "TPC-143", "PROVED",
            "L1_NEGATIVE", "NEGATIVE", "STRUCTURAL", pc, cc, pa,
            "COMPLETE_DECLARED_ROUTE_CELL",
        ),
        export(
            "G143.frontier_occurrence_lift", "TPC-143", "NOT_TESTABLE",
            "L1_STRUCTURAL", "NEUTRAL", "STRUCTURAL", pc, cc, pa,
            "ALL_NONSOFT_CUT_PATHS_ETO_PLUS_FUM",
        ),
        export(
            "C144.QD_interface", "TPC-144", "PROVED",
            "L0_MODEL", "POSITIVE", "STRUCTURAL", model, occ, pa,
            "ABSTRACT_TYPED_INTERFACE",
        ),
        export(
            "C144.QZ_interface", "TPC-144", "PROVED",
            "L0_MODEL", "POSITIVE", "STRUCTURAL", model, occ, pa,
            "ABSTRACT_TYPED_INTERFACE",
        ),
        export(
            "N144.schema_only_QD_QZ", "TPC-144", "PROVED",
            "L1_NEGATIVE", "NEGATIVE", "STRUCTURAL", pc, cc, pa,
            "COMPLETE_DECLARED_ROUTE_CELL",
        ),
        export(
            "C145.GP_commuting_square", "TPC-145", "PROVED",
            "L0_MODEL", "POSITIVE", "STRUCTURAL", model, occ, pa,
            "ROW_SEPARATED_ABSTRACT_INTERFACE",
        ),
        export(
            "S145.cut_Ph0_identity", "TPC-145", "PROVED",
            "L1_STRUCTURAL", "POSITIVE", "STRUCTURAL", pc, cc, pa,
            "P_H0_CUT_IDENTITY_ONLY",
        ),
        export(
            "N145.aggregate_cancellation_stop", "TPC-145", "PROVED",
            "L1_NEGATIVE", "NEGATIVE", "STRUCTURAL", pc, cc, pa,
            "COMPLETE_DECLARED_ROUTE_CELL",
        ),
        export(
            "C146.four_map_contract", "TPC-146", "PROVED",
            "L1_STRUCTURAL", "POSITIVE", "STRUCTURAL", pc, cc, pa,
            "ALL_NONSOFT_MAP_OR_FRONTIER_SCALAR_AND_ETO_CONTRACT",
        ),
        export(
            "N146.current_schema_totalization_stop", "TPC-146", "PROVED",
            "L1_NEGATIVE", "NEGATIVE", "STRUCTURAL", pc, cc, pa,
            "COMPLETE_DECLARED_ROUTE_CELL",
        ),
        export(
            "A147.periodic_residue_reassembly", "TPC-147", "PROVED",
            "L1_STRUCTURAL", "POSITIVE", "ARITHMETIC_SHADOW",
            core, core_carrier, cnorm, "FIXED_TWO_PERIODIC_CORE",
        ),
        export(
            "A148.quotient_mobius_lift", "TPC-148", "PROVED",
            "L0_MODEL", "POSITIVE", "ARITHMETIC_SHADOW",
            core, core_carrier, cnorm, "EXACT_QUOTIENT_LIFT_IDENTITY",
        ),
        export(
            "A148.nonpretentious_stability", "TPC-148", "PROVED",
            "L1_ACTUAL_CORE", "POSITIVE", "ARITHMETIC_SHADOW",
            core, core_carrier, cnorm, "NONPRETENTIOUSNESS_INPUT",
        ),
        export(
            "A149.actual_mobius_periodic_corridor", "TPC-149", "PROVED",
            "L1_ACTUAL_CORE", "POSITIVE", "ARITHMETIC_SHADOW",
            core, core_carrier, cnorm,
            "ACTUAL_FIXED_TWO_MOBIUS_PERIODIC_CORE_ALMOST_SCALE",
            promotion_eligible=False,
            x_power_sigma=Fraction(0),
        ),
        export(
            "G150.actual_corridor_return", "TPC-150", "NOT_TESTABLE",
            "L2_TARGET_POSITIVE", "NEUTRAL", "ARITHMETIC_TARGET",
            "scope.actual_h3", "carrier.actual_h3_packet", pa,
            "FULL_ACTUAL_PHYSICAL_RETURN",
        ),
        export(
            "N150.deterministic_prefix_nonimplication", "TPC-150", "PROVED",
            "L1_NEGATIVE", "NEGATIVE", "ARITHMETIC_NEGATIVE",
            "scope.actual_h3", "carrier.actual_h3_packet", pa,
            "COMPLETE_DECLARED_ROUTE_CELL",
        ),
    ]


def build_imports(exports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "import_id": f"I151.{record['export_id']}",
            "source_export": record["export_id"],
            "status": record["status"],
            "program_level": record["program_level"],
            "direction": record["direction"],
            "role": record["role"],
            "scope_id": record["scope_id"],
            "carrier_id": record["carrier_id"],
            "normalization_id": record["normalization_id"],
            "coverage": record["coverage"],
            "within_scope_proof_edge": record["status"] == "PROVED",
            "promotion_edge_to_actual_h3": False,
        }
        for record in exports
    ]


def validate_imports(
    exports: list[dict[str, Any]],
    imports: list[dict[str, Any]],
) -> None:
    by_id = {record["export_id"]: record for record in exports}
    if len(by_id) != len(exports):
        raise ValueError("duplicate export id")
    seen: set[str] = set()
    exact_fields = (
        "status",
        "program_level",
        "direction",
        "role",
        "scope_id",
        "carrier_id",
        "normalization_id",
        "coverage",
    )
    for record in imports:
        if record["import_id"] in seen:
            raise ValueError("duplicate import id")
        seen.add(record["import_id"])
        source = by_id.get(record["source_export"])
        if source is None:
            raise ValueError("import references unknown export")
        if any(record[field] != source[field] for field in exact_fields):
            raise ValueError("typed import does not exactly match export")
        if (
            record["within_scope_proof_edge"]
            and source["status"] != "PROVED"
        ):
            raise ValueError("non-proved export was used as a proof edge")
        if (
            record["promotion_edge_to_actual_h3"]
            and not source["promotion_eligible"]
        ):
            raise ValueError("shadow-only export was promoted to actual H3")


def node(
    node_id: str,
    gate: str,
    status: str,
    level: str,
    role: str,
    structural: bool,
    scope_match: bool,
    parents: tuple[str, ...] = (),
    source_export: str | None = None,
    required_artifact: str = "",
) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "gate": gate,
        "status": status,
        "program_level": level,
        "role": role,
        "structural": structural,
        "scope_match": scope_match,
        "parents": list(parents),
        "source_export": source_export,
        "required_artifact": required_artifact,
    }


def build_nodes() -> list[dict[str, Any]]:
    return [
        node(
            "S143.cut_shift_selector", "H1.cut", "PROVED", "L1_STRUCTURAL",
            "STRUCTURAL", True, True, source_export="S143.cut_shift_selector",
        ),
        node(
            "N143.schema_nonidentifiability", "H1.cut", "PROVED", "L1_NEGATIVE",
            "STRUCTURAL", True, True,
            source_export="N143.schema_nonidentifiability",
        ),
        node(
            "H1.frontier_occurrence_lift", "H1", "NOT_TESTABLE",
            "L1_STRUCTURAL", "STRUCTURAL", True, True,
            ("S143.cut_shift_selector", "N143.schema_nonidentifiability"),
            "G143.frontier_occurrence_lift",
            REQUIRED_ARTIFACT_CONTRACTS["H1.frontier_occurrence_lift"],
        ),
        node(
            "C144.QD_interface", "H1.interface", "PROVED", "L0_MODEL",
            "STRUCTURAL", True, True,
            source_export="C144.QD_interface",
        ),
        node(
            "C144.QZ_interface", "H1.interface", "PROVED", "L0_MODEL",
            "STRUCTURAL", True, True,
            source_export="C144.QZ_interface",
        ),
        node(
            "H1.frontier_QD_totality", "H1", "NOT_TESTABLE",
            "L1_STRUCTURAL", "STRUCTURAL", True, True,
            ("H1.frontier_occurrence_lift", "C144.QD_interface"),
            required_artifact="actual path-total determinant quotient",
        ),
        node(
            "H1.frontier_QZ_totality", "H1", "NOT_TESTABLE",
            "L1_STRUCTURAL", "STRUCTURAL", True, True,
            ("H1.frontier_occurrence_lift", "C144.QZ_interface"),
            required_artifact="actual path-total zero-mode quotient",
        ),
        node(
            "H1.frontier_QD_QZ_intertwining", "H1", "NOT_TESTABLE",
            "L1_STRUCTURAL", "STRUCTURAL", True, True,
            ("H1.frontier_QD_totality", "H1.frontier_QZ_totality"),
            required_artifact="kernel/fiber equivalence with exact multipliers",
        ),
        node(
            "C145.GP_commuting_square", "H1.interface", "PROVED", "L0_MODEL",
            "STRUCTURAL", True, True,
            source_export="C145.GP_commuting_square",
        ),
        node(
            "S145.cut_Ph0_identity", "H1.cut", "PROVED", "L1_STRUCTURAL",
            "STRUCTURAL", True, True,
            source_export="S145.cut_Ph0_identity",
        ),
        node(
            "H1.frontier_G_totality", "H1", "NOT_TESTABLE",
            "L1_STRUCTURAL", "STRUCTURAL", True, True,
            ("H1.frontier_occurrence_lift", "C145.GP_commuting_square"),
            required_artifact="actual occurrence-resolved physical grouping",
        ),
        node(
            "H1.frontier_Ph0_totality", "H1", "NOT_TESTABLE",
            "L1_STRUCTURAL", "STRUCTURAL", True, True,
            (
                "H1.frontier_occurrence_lift",
                "C145.GP_commuting_square",
                "S145.cut_Ph0_identity",
            ),
            required_artifact="actual downstream prescribed-shift selector",
        ),
        node(
            "H1.frontier_GP_commutation", "H1", "NOT_TESTABLE",
            "L1_STRUCTURAL", "STRUCTURAL", True, True,
            ("H1.frontier_G_totality", "H1.frontier_Ph0_totality"),
            required_artifact="row-separated edgewise shift preservation",
        ),
        node(
            "C146.four_map_contract", "H1.interface", "PROVED",
            "L1_STRUCTURAL", "STRUCTURAL", True, True,
            source_export="C146.four_map_contract",
        ),
        node(
            "H1.frontier_totalization", "H1", "NOT_TESTABLE",
            "L1_STRUCTURAL", "STRUCTURAL", True, True,
            (
                "C146.four_map_contract",
                "H1.frontier_QD_QZ_intertwining",
                "H1.frontier_GP_commutation",
            ),
            required_artifact=REQUIRED_ARTIFACT_CONTRACTS[
                "H1.frontier_totalization"
            ],
        ),
        node(
            "H1.actual_carrier", "H1", "NOT_TESTABLE", "L1_STRUCTURAL",
            "STRUCTURAL", True, True, ("H1.frontier_totalization",),
            required_artifact=REQUIRED_ARTIFACT_CONTRACTS[
                "H1.actual_carrier"
            ],
        ),
        node(
            "A147.periodic_residue_reassembly", "H3.core", "PROVED",
            "L1_STRUCTURAL", "ARITHMETIC_SHADOW", False, True,
            source_export="A147.periodic_residue_reassembly",
        ),
        node(
            "A148.quotient_mobius_lift", "H3.core", "PROVED", "L0_MODEL",
            "ARITHMETIC_SHADOW", False, True,
            source_export="A148.quotient_mobius_lift",
        ),
        node(
            "A148.nonpretentious_stability", "H3.core", "PROVED",
            "L1_ACTUAL_CORE", "ARITHMETIC_SHADOW", False, True,
            source_export="A148.nonpretentious_stability",
        ),
        node(
            "A149.actual_mobius_periodic_corridor", "H3.core", "PROVED",
            "L1_ACTUAL_CORE", "ARITHMETIC_SHADOW", False, True,
            (
                "A147.periodic_residue_reassembly",
                "A148.quotient_mobius_lift",
                "A148.nonpretentious_stability",
            ),
            "A149.actual_mobius_periodic_corridor",
        ),
        node(
            "G150.actual_corridor_return", "H3", "NOT_TESTABLE",
            "L2_TARGET_POSITIVE", "ARITHMETIC_TARGET", False, True,
            ("A149.actual_mobius_periodic_corridor", "H1.actual_carrier"),
            "G150.actual_corridor_return",
            required_artifact=REQUIRED_ARTIFACT_CONTRACTS[
                "G150.actual_corridor_return"
            ],
        ),
        node(
            "H2.signed_resonance", "H2", "OPEN", "L2_TARGET_POSITIVE",
            "ARITHMETIC_TARGET", False, True, ("H1.actual_carrier",),
            required_artifact="literal signed resonance replacement",
        ),
        node(
            "H3.actual_packet_saving", "H3", "OPEN", "L2_TARGET_POSITIVE",
            "ARITHMETIC_TARGET", False, True, ("G150.actual_corridor_return",),
            required_artifact=REQUIRED_ARTIFACT_CONTRACTS[
                "H3.actual_packet_saving"
            ],
        ),
        node(
            "H4.complete_tail", "H4", "OPEN", "L2_TARGET_POSITIVE",
            "ARITHMETIC_TARGET", False, True, ("H1.actual_carrier",),
            required_artifact="complete original-scale high/ultra/boundary return",
        ),
        node(
            "H5.det_zero", "H5", "NOT_TESTABLE", "L2_TARGET_POSITIVE",
            "ARITHMETIC_TARGET", False, True, ("H1.actual_carrier",),
            required_artifact=REQUIRED_ARTIFACT_CONTRACTS["H5.det_zero"],
        ),
        node(
            "H6.physical_cover", "H6", "NOT_TESTABLE", "L1_STRUCTURAL",
            "STRUCTURAL", True, True, ("H1.actual_carrier",),
            required_artifact=REQUIRED_ARTIFACT_CONTRACTS[
                "H6.physical_cover"
            ],
        ),
        node(
            "H7.fixed_h0_totality", "H7", "NOT_TESTABLE", "L1_STRUCTURAL",
            "STRUCTURAL", True, True, ("H1.actual_carrier",),
            required_artifact=REQUIRED_ARTIFACT_CONTRACTS[
                "H7.fixed_h0_totality"
            ],
        ),
        node(
            "H8.final_reconnection", "H8", "NOT_TESTABLE", "L1_STRUCTURAL",
            "STRUCTURAL", True, True,
            ("H1.actual_carrier", "H6.physical_cover", "H7.fixed_h0_totality"),
            required_artifact=REQUIRED_ARTIFACT_CONTRACTS[
                "H8.final_reconnection"
            ],
        ),
        node(
            "H9.physical_registry", "H9", "NOT_TESTABLE", "L1_STRUCTURAL",
            "PHYSICAL_SYNTHESIS", True, True,
            (
                "H1.actual_carrier",
                "H6.physical_cover",
                "H7.fixed_h0_totality",
                "H8.final_reconnection",
            ),
            required_artifact=REQUIRED_ARTIFACT_CONTRACTS[
                "H9.physical_registry"
            ],
        ),
        node(
            "ROOT.endpoint_synthesis", "ROOT", "CONDITIONAL",
            "L1_CONDITIONAL", "ROOT", False, True,
            (
                "H1.actual_carrier",
                "H2.signed_resonance",
                "H3.actual_packet_saving",
                "H4.complete_tail",
                "H5.det_zero",
                "H6.physical_cover",
                "H7.fixed_h0_totality",
                "H8.final_reconnection",
                "H9.physical_registry",
            ),
            required_artifact=REQUIRED_ARTIFACT_CONTRACTS[
                "ROOT.endpoint_synthesis"
            ],
        ),
    ]


def topo_order(graph: dict[str, tuple[str, ...]]) -> list[str]:
    indegree = {node_id: 0 for node_id in graph}
    children = {node_id: [] for node_id in graph}
    for node_id, parents in graph.items():
        for parent in parents:
            if parent not in graph:
                raise ValueError(f"unknown DAG parent {parent}")
            indegree[node_id] += 1
            children[parent].append(node_id)
    queue = sorted(node_id for node_id, degree in indegree.items() if degree == 0)
    order: list[str] = []
    while queue:
        node_id = queue.pop(0)
        order.append(node_id)
        for child in sorted(children[node_id]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort()
    if len(order) != len(graph):
        raise ValueError("cyclic proof DAG")
    return order


def ancestor_closure(
    graph: dict[str, tuple[str, ...]],
    node_id: str,
    *,
    include_self: bool = False,
) -> set[str]:
    if node_id not in graph:
        raise ValueError(f"unknown closure root {node_id}")
    seen = {node_id} if include_self else set()
    stack = list(graph[node_id])
    while stack:
        parent = stack.pop()
        if parent in seen:
            continue
        seen.add(parent)
        stack.extend(graph[parent])
    return seen


def validate_nodes(
    nodes: list[dict[str, Any]],
    exports: list[dict[str, Any]],
) -> tuple[dict[str, tuple[str, ...]], list[str]]:
    by_id = {record["node_id"]: record for record in nodes}
    if len(by_id) != len(nodes):
        raise ValueError("duplicate node id")
    export_ids = {record["export_id"] for record in exports}
    for record in nodes:
        if record["status"] not in VALID_STATUSES:
            raise ValueError("unknown node status")
        if record["program_level"] not in VALID_LEVELS:
            raise ValueError("unknown program level")
        if record["role"] not in VALID_ROLES:
            raise ValueError("unknown node role")
        if (
            record["status"] == "PROVED"
            and record["program_level"] == "L2_TARGET_POSITIVE"
        ):
            raise ValueError("target-only L2 label cannot be marked proved")
        if (
            record["source_export"] is not None
            and record["source_export"] not in export_ids
        ):
            raise ValueError("node references unknown export")
    for node_id, required_artifact in REQUIRED_ARTIFACT_CONTRACTS.items():
        if node_id not in by_id:
            raise ValueError(f"missing required-artifact contract node {node_id}")
        if by_id[node_id]["required_artifact"] != required_artifact:
            raise ValueError(
                f"compressed or drifted required artifact for {node_id}"
            )
    graph = {
        node_id: tuple(record["parents"])
        for node_id, record in by_id.items()
    }
    order = topo_order(graph)

    h9_ancestors = ancestor_closure(graph, "H9.physical_registry")
    if any(by_id[node_id]["role"] in ARITHMETIC_ROLES for node_id in h9_ancestors):
        raise ValueError("H9 has a direct or indirect arithmetic-role dependency")
    if any(
        by_id[node_id]["gate"].split(".", 1)[0] in {"H2", "H3", "H4", "H5"}
        for node_id in h9_ancestors
    ):
        raise ValueError("H9 has a direct or indirect arithmetic-gate dependency")
    return graph, order


def minimal_missing_set(
    nodes: list[dict[str, Any]],
    graph: dict[str, tuple[str, ...]],
    order: list[str],
    root: str,
) -> dict[str, Any] | None:
    by_id = {record["node_id"]: record for record in nodes}
    active = ancestor_closure(graph, root, include_self=True)
    missing = {
        node_id
        for node_id in active
        if by_id[node_id]["status"] == "NOT_TESTABLE"
        or not by_id[node_id]["scope_match"]
    }
    if not missing:
        return None
    minimal = {
        node_id
        for node_id in missing
        if not (ancestor_closure(graph, node_id) & missing)
    }
    position = {node_id: index for index, node_id in enumerate(order)}
    ordered = sorted(minimal, key=lambda node_id: (position[node_id], node_id))
    first = by_id[ordered[0]]
    return {
        "node_id": first["node_id"],
        "gate": first["gate"],
        "status": first["status"],
        "program_level": first["program_level"],
        "required_artifact": first["required_artifact"],
        "minimal_missing_set": ordered,
        "active_node_count": len(active),
        "selection_rule": "MINIMAL_MISSING_ANCESTORS_THEN_CANONICAL_TOPOLOGY",
    }


def route_universe() -> dict[str, Any]:
    route_ids = [
        "eligible_only_tpc17_18_compiler",
        "quantitative_shift1_reparameterization",
        "current_schema_only_downstream_label_derivation",
        "schema_only_QD_QZ_derivation",
        "aggregate_cancellation_shift_provenance",
        "atomic_deterministic_prefix_transfer",
        "occurrence_lift_quotient_mobius_return",
    ]
    stops = {
        "eligible_only_tpc17_18_compiler": (
            "ANCHOR.N135.eligible_only_stop", "registry.eligible-v1"
        ),
        "quantitative_shift1_reparameterization": (
            "ANCHOR.N138.shift_one_stop", "registry.shift1-v1"
        ),
        "current_schema_only_downstream_label_derivation": (
            "N143.schema_nonidentifiability", "registry.schema-only-v1"
        ),
        "schema_only_QD_QZ_derivation": (
            "N144.schema_only_QD_QZ", "registry.qdqz-schema-v1"
        ),
        "aggregate_cancellation_shift_provenance": (
            "N145.aggregate_cancellation_stop", "registry.aggregate-gp-v1"
        ),
        "atomic_deterministic_prefix_transfer": (
            "N150.deterministic_prefix_nonimplication",
            "registry.atomic-prefix-v1"
        ),
    }
    return {
        "routes": route_ids,
        "selected_route": "occurrence_lift_quotient_mobius_return",
        "selected_root": "ROOT.endpoint_synthesis",
        "typed_alternative": None,
        "typed_alternative_crosswalk": None,
        "universe_completeness": {
            "status": "OPEN",
            "source_export": None,
            "scope": "DECLARED_TESTED_ROUTE_CELLS_NOT_ALL_CONCEIVABLE_ROUTES",
        },
        "stops": _route_stop_records(route_ids, stops),
    }


def _route_stop_records(
    route_ids: list[str],
    stops: dict[str, tuple[str, str]],
) -> dict[str, dict[str, Any]]:
    exports = {record["export_id"]: record for record in build_exports()}
    records: dict[str, dict[str, Any]] = {}
    for route_id in route_ids:
        if route_id not in stops:
            records[route_id] = {
                "stopped": False,
                "source_export": None,
                "scope_id": "scope.actual_h3",
                "carrier_id": "carrier.actual_h3_packet",
                "normalization_id": "norm.physical_atomic",
                "coverage": "OPEN_SELECTED_ROUTE",
                "registry_id": "registry.occurrence-quotient-v1",
            }
            continue
        export_id, registry_id = stops[route_id]
        source = exports[export_id]
        records[route_id] = {
            "stopped": True,
            "source_export": export_id,
            "scope_id": source["scope_id"],
            "carrier_id": source["carrier_id"],
            "normalization_id": source["normalization_id"],
            "coverage": source["coverage"],
            "registry_id": registry_id,
        }
    return records


def validate_routes(
    routes: dict[str, Any],
    exports: list[dict[str, Any]],
) -> None:
    universe = set(routes["routes"])
    if not universe or routes["selected_route"] not in universe:
        raise ValueError("selected route lies outside declared universe")
    if set(routes["stops"]) != universe:
        raise ValueError("stop map is not an exact declared-route cover")
    by_export = {record["export_id"]: record for record in exports}
    for route_id, record in routes["stops"].items():
        if record["stopped"]:
            source = by_export.get(record["source_export"])
            if source is None or source["direction"] != "NEGATIVE":
                raise ValueError(f"route stop {route_id} lacks a negative export")
            if record["coverage"] != "COMPLETE_DECLARED_ROUTE_CELL":
                raise ValueError("route stop lacks complete cell coverage")
            for field in (
                "scope_id",
                "carrier_id",
                "normalization_id",
                "coverage",
            ):
                if record[field] != source[field]:
                    raise ValueError("route stop does not exactly match export")
            if not all(
                record[field]
                for field in (
                    "scope_id",
                    "carrier_id",
                    "normalization_id",
                    "registry_id",
                )
            ):
                raise ValueError("route stop lacks typed metadata")
    completeness = routes["universe_completeness"]
    if completeness["status"] == "PROVED" and not completeness["source_export"]:
        raise ValueError("proved route-universe completeness lacks a source")
    alternative = routes["typed_alternative"]
    if alternative is not None:
        selected = routes["selected_route"]
        if alternative not in universe or alternative == selected:
            raise ValueError("invalid typed alternative")
        if not routes["stops"][selected]["stopped"]:
            raise ValueError("reroute lacks a selected-route stop")
        if routes["stops"][alternative]["stopped"]:
            raise ValueError("typed alternative is already stopped")
        if not routes["typed_alternative_crosswalk"]:
            raise ValueError("reroute lacks a theorem-backed crosswalk")
        if (
            routes["stops"][alternative]["registry_id"]
            == routes["stops"][selected]["registry_id"]
        ):
            raise ValueError("reroute did not use a fresh registry")


def physical_endpoint_state(
    threshold: Fraction,
    upper: Fraction | None,
    lower: Fraction | None,
    registry_complete: bool,
) -> str:
    if not registry_complete:
        return "INCOMPLETE"
    if lower is not None and lower >= threshold:
        return "EQUALITY_STOP" if lower == threshold else "LOWER_STOP"
    if upper is None:
        return "INCOMPLETE"
    if upper < threshold:
        return "STRICT_PASS"
    return "NO_PASS_CERTIFICATE"


def endpoint_ledgers(registry_complete: bool = False) -> dict[str, Any]:
    threshold = Fraction(1, 400)
    physical_state = physical_endpoint_state(
        threshold, None, None, registry_complete
    )
    return {
        "contract": "MVP1-FIXED-H0-SPLIT-ENDPOINT-V2",
        "scale": "AMPLITUDE",
        "arithmetic": {
            "sigma_required": fraction_record(threshold),
            "sigma_actual_lower": None,
            "best_shadow_x_power_sigma": fraction_record(Fraction(0)),
            "state": "INCOMPLETE",
            "log_saving_pays_fixed_power": False,
        },
        "physical": {
            "lambda_required_strict_upper": fraction_record(threshold),
            "lambda_phys_upper": None,
            "lambda_phys_lower": None,
            "registry_complete": registry_complete,
            "state": physical_state,
            "unknown_cost_policy": "UNKNOWN_IS_NOT_ZERO",
            "upper_at_or_above_is_stop_without_lower": False,
            "determinant_reserve_reusable": False,
        },
        "full_synthesis": {
            "strict_net_slack": None,
            "state": "INCOMPLETE",
        },
    }


def gate_projection() -> dict[str, dict[str, Any]]:
    return {
        "H1": {
            "status": "NOT_TESTABLE", "evidence": "L1_STRUCTURAL",
            "structural": True, "scope_match": True,
            "source_node": "H1.actual_carrier",
        },
        "H2": {
            "status": "OPEN", "evidence": "L2_TARGET_POSITIVE",
            "structural": False, "scope_match": True,
            "source_node": "H2.signed_resonance",
        },
        "H3": {
            "status": "OPEN", "evidence": "L2_TARGET_POSITIVE",
            "structural": False, "scope_match": True,
            "source_node": "H3.actual_packet_saving",
        },
        "H4": {
            "status": "OPEN", "evidence": "L2_TARGET_POSITIVE",
            "structural": False, "scope_match": True,
            "source_node": "H4.complete_tail",
        },
        "H5": {
            "status": "NOT_TESTABLE", "evidence": "L2_TARGET_POSITIVE",
            "structural": False, "scope_match": True,
            "source_node": "H5.det_zero",
        },
        "H6": {
            "status": "NOT_TESTABLE", "evidence": "L1_STRUCTURAL",
            "structural": True, "scope_match": True,
            "source_node": "H6.physical_cover",
        },
        "H7": {
            "status": "NOT_TESTABLE", "evidence": "L1_STRUCTURAL",
            "structural": True, "scope_match": True,
            "source_node": "H7.fixed_h0_totality",
        },
        "H8": {
            "status": "NOT_TESTABLE", "evidence": "L1_STRUCTURAL",
            "structural": True, "scope_match": True,
            "source_node": "H8.final_reconnection",
        },
        "H9": {
            "status": "NOT_TESTABLE", "evidence": "L1_STRUCTURAL",
            "structural": True, "scope_match": True,
            "source_node": "H9.physical_registry",
        },
    }


def build_manifest() -> dict[str, Any]:
    anchor = anchor_chain()
    bundles = {f"TPC-{number}": source_bundle(number) for number in range(143, 151)}
    exports = build_exports()
    imports = build_imports(exports)
    validate_imports(exports, imports)
    nodes = build_nodes()
    graph, order = validate_nodes(nodes, exports)
    routes = route_universe()
    validate_routes(routes, exports)
    first = minimal_missing_set(
        nodes, graph, order, routes["selected_root"]
    )
    if first is None or first["node_id"] != "H1.frontier_occurrence_lift":
        raise ValueError("unexpected current first-missing node")

    return {
        "schema": SCHEMA_NAME,
        "snapshot": {
            "date": "2026-07-27",
            "source_range": "TPC-143--150",
            "hash_mode": HASH_MODE,
            "source_hash_semantics": "INTEGRITY_ONLY",
            "identity_rule": "EXACT_TYPED_KEYS_NOT_HASH_IDENTITIES",
            "selected_route": routes["selected_route"],
        },
        "anchor_chain": anchor,
        "source_bundles": bundles,
        "source_contracts": source_contracts(),
        "scope_registry": scope_registry(),
        "carrier_registry": carrier_registry(),
        "normalization_registry": normalization_registry(),
        "exports": exports,
        "imports": imports,
        "nodes": nodes,
        "proof_dag": {
            "parents": {
                node_id: list(parents)
                for node_id, parents in graph.items()
            },
            "topological_order": order,
            "selected_root": routes["selected_root"],
            "active_nodes_derived_not_declared": True,
            "H9_role_and_gate_independent": True,
        },
        "route_universe": routes,
        "frontier_contract": {
            "domain": "ALL_NONSOFT_CUT_PATHS_ETO_PLUS_FUM",
            "totalization_logic": FRONTIER_TOTALIZATION_LOGIC,
            "sample_counts": {
                "ELIGIBLE_TAIL_OPEN": 0,
                "FRONTIER_UNMAPPED": 2988,
            },
            "empty_sample_class_implies_asymptotic_empty": False,
            "occurrence_lift": {
                "map_id": "L_X",
                "one_to_many": True,
                "row_separated": True,
                "column_conservation": "1^T L_X = 1^T",
                "status": "NOT_TESTABLE",
            },
            "cut_selector": {
                "map_id": "P_h0_cut",
                "status": "PROVED_L1",
                "equals_identity": True,
                "is_downstream_selector": False,
            },
            "map_route": {
                "defect_vector": [
                    "D_L", "D_QD", "D_QZ", "D_G", "D_P",
                    "D_DZ", "D_GP", "D_cover", "D_reconnection",
                ],
                "zero_defect_proved": False,
            },
            "scalar_route": {
                "frontier_required": (
                    "S_frontier(X)=o(X) on the complete original scale"
                ),
                "eligible_tail_required": (
                    "theorem-backed total maps or a complete ETO soft theorem"
                ),
                "frontier_scalar_proved": False,
                "eligible_tail_disposed": False,
                "pass": False,
            },
            "full_carrier_totalized": False,
        },
        "arithmetic_corridor": {
            "scope_id": (
                "scope.actual_fixed_two_mobius_periodic_core_almost_scale"
            ),
            "quotient_identity": (
                "t=aD(z), t+2=sV(z), "
                "mu(D(z))mu(V(z))=G_a(t)G_s(t+2)"
            ),
            "status": "PROVED_L1_ACTUAL_CORE",
            "promotion_eligible": False,
            "x_power_sigma": fraction_record(Fraction(0)),
            "missing_physical_return": [
                "actual_physical_weight",
                "generic_phase",
                "all_prefix_selector",
                "complete_four_sign_return",
            ],
            "positive_L2": False,
        },
        "occurrence_registry": {
            "status": "INCOMPLETE",
            "complete": False,
            "required_domain": "ALL_NONSOFT_CUT_PATHS_ETO_PLUS_FUM",
            "unknown_tokens_are_zero": False,
            "joint_replacements_require_exact_disjoint_cover": True,
            "energy_to_amplitude_halving_count": 1,
            "determinant_reserve_is_physical_token": False,
        },
        "endpoint_ledgers": endpoint_ledgers(False),
        "gate_projection": gate_projection(),
        "first_missing": first,
        "progress_classification": copy.deepcopy(PROGRESS_CLASSIFICATION),
        "claim_boundary": {
            "source_hashes_prove_theorems": False,
            "P_h0_cut_is_downstream_P_h0": False,
            "schema_nonidentifiability_is_actual_carrier_impossibility": False,
            "empty_sample_ETO_is_asymptotic_empty": False,
            "actual_core_is_full_H3": False,
            "log_saving_pays_one_over_400": False,
            "positive_L2": False,
            "physical_endpoint_pass": False,
            "arithmetic_target_pass": False,
            "full_endpoint_pass": False,
            "arithmetic_frontier": False,
            "hard_packet_oX": False,
            "prime_pair_theorem": False,
            "twin_prime_theorem": False,
        },
    }


def validate_manifest(manifest: dict[str, Any]) -> dict[str, bool]:
    schema = json.loads(
        normalize_lf(SCHEMA_PATH.read_text(encoding="utf-8"))
    )
    if set(manifest) != set(schema["required"]):
        raise ValueError("manifest top-level fields differ from schema contract")
    if manifest["schema"] != SCHEMA_NAME:
        raise ValueError("manifest schema mismatch")
    if manifest["snapshot"]["hash_mode"] != HASH_MODE:
        raise ValueError("source hash mode drift")
    if manifest["snapshot"]["source_hash_semantics"] != "INTEGRITY_ONLY":
        raise ValueError("source hashes were assigned proof semantics")
    node_schema = schema["properties"]["nodes"]["items"]
    for record in manifest["nodes"]:
        if set(record) != set(node_schema["required"]):
            raise ValueError("node fields differ from schema contract")
    frontier_schema = schema["properties"]["frontier_contract"]
    if set(manifest["frontier_contract"]) != set(frontier_schema["required"]):
        raise ValueError("frontier fields differ from schema contract")
    scalar_schema = frontier_schema["properties"]["scalar_route"]
    if set(manifest["frontier_contract"]["scalar_route"]) != set(
        scalar_schema["required"]
    ):
        raise ValueError("scalar-route fields differ from schema contract")
    progress_schema = schema["properties"]["progress_classification"]
    if set(manifest["progress_classification"]) != set(
        progress_schema["required"]
    ):
        raise ValueError(
            "progress-classification fields differ from schema contract"
        )
    if manifest["progress_classification"] != PROGRESS_CLASSIFICATION:
        raise ValueError("progress classification is ambiguous or stale")
    if len(manifest["source_bundles"]) != 8:
        raise ValueError("source-lock must contain TPC-143--150")
    for number in range(143, 151):
        record = manifest["source_bundles"].get(f"TPC-{number}")
        if record is None or record["hash_mode"] != HASH_MODE:
            raise ValueError("source bundle absent or noncanonical")
        if len(record["bundle_sha256"]) != 64:
            raise ValueError("invalid source bundle hash")
    if manifest["source_contracts"] != source_contracts():
        raise ValueError("typed source-contract summary is stale")
    if not manifest["anchor_chain"]["tpc142_embedded_tpc141_hash_verified"]:
        raise ValueError("upstream anchor chain is not verified")

    validate_imports(manifest["exports"], manifest["imports"])
    graph, order = validate_nodes(manifest["nodes"], manifest["exports"])
    if manifest["proof_dag"]["parents"] != {
        node_id: list(parents) for node_id, parents in graph.items()
    }:
        raise ValueError("proof DAG differs from node parents")
    if manifest["proof_dag"]["topological_order"] != order:
        raise ValueError("topological order is not canonical")
    validate_routes(manifest["route_universe"], manifest["exports"])
    first = minimal_missing_set(
        manifest["nodes"],
        graph,
        order,
        manifest["proof_dag"]["selected_root"],
    )
    if first != manifest["first_missing"]:
        raise ValueError("first-missing record is stale")
    if first is None or first["node_id"] != "H1.frontier_occurrence_lift":
        raise ValueError("occurrence lift is not the first missing object")
    if first["minimal_missing_set"] != ["H1.frontier_occurrence_lift"]:
        raise ValueError("unexpected minimal missing antichain")

    frontier = manifest["frontier_contract"]
    if frontier["domain"] != "ALL_NONSOFT_CUT_PATHS_ETO_PLUS_FUM":
        raise ValueError("frontier contract dropped eligible-tail paths")
    if frontier["sample_counts"]["ELIGIBLE_TAIL_OPEN"] != 0:
        raise ValueError("frozen sample count drift")
    if frontier["empty_sample_class_implies_asymptotic_empty"]:
        raise ValueError("empty ETO sample was promoted to an asymptotic theorem")
    if frontier["cut_selector"]["is_downstream_selector"]:
        raise ValueError("cut selector was promoted to downstream P_h0")
    if (
        frontier["totalization_logic"]
        != FRONTIER_TOTALIZATION_LOGIC
    ):
        raise ValueError("frontier disjunction drift")
    scalar_route = frontier["scalar_route"]
    scalar_route_pass = (
        scalar_route["frontier_scalar_proved"]
        and scalar_route["eligible_tail_disposed"]
    )
    if scalar_route["pass"] != scalar_route_pass:
        raise ValueError(
            "frontier scalar theorem was accepted without an ETO disposition"
        )
    if frontier["full_carrier_totalized"]:
        raise ValueError("frontier was falsely totalized")
    corridor = manifest["arithmetic_corridor"]
    if (
        corridor["status"] != "PROVED_L1_ACTUAL_CORE"
        or corridor["promotion_eligible"]
        or parse_fraction(corridor["x_power_sigma"]) != 0
        or corridor["positive_L2"]
    ):
        raise ValueError("actual core corridor was promoted to positive L2")
    endpoint = manifest["endpoint_ledgers"]
    if parse_fraction(endpoint["arithmetic"]["sigma_required"]) != Fraction(1, 400):
        raise ValueError("arithmetic 1/400 contract drift")
    if parse_fraction(
        endpoint["physical"]["lambda_required_strict_upper"]
    ) != Fraction(1, 400):
        raise ValueError("physical 1/400 contract drift")
    if endpoint["physical"]["state"] != "INCOMPLETE":
        raise ValueError("current physical endpoint falsely closed")
    if endpoint["full_synthesis"]["state"] != "INCOMPLETE":
        raise ValueError("current full endpoint falsely closed")
    if any(manifest["claim_boundary"].values()):
        raise ValueError("claim boundary contains a false positive")
    if manifest["gate_projection"]["H1"]["status"] != "NOT_TESTABLE":
        raise ValueError("H1 was falsely closed")
    return {
        "schema_fields": True,
        "canonical_utf8_lf_v2_sources": True,
        "upstream_anchor_chain": True,
        "source_contracts_recomputed": True,
        "source_hashes_integrity_only": True,
        "typed_imports_exact": True,
        "required_artifact_contracts_exact": True,
        "progress_target_and_achievement_separated": True,
        "active_ancestor_closure": True,
        "minimal_missing_antichain": True,
        "occurrence_lift_first_missing": True,
        "all_nonsoft_eto_plus_fum": True,
        "frontier_scalar_requires_ETO": True,
        "cut_selector_not_downstream": True,
        "H9_transitively_arithmetic_independent": True,
        "actual_core_not_positive_L2": True,
        "split_one_over_400_ledgers": True,
        "route_stop_scopes_exact": True,
        "claim_boundary": True,
    }


def mutation_regressions(manifest: dict[str, Any]) -> dict[str, bool]:
    results: dict[str, bool] = {}
    text_lf = "alpha\nbeta\n"
    text_crlf = text_lf.replace("\n", "\r\n")
    results["eol_normalization_stable"] = (
        normalize_lf(text_lf) == normalize_lf(text_crlf)
    )
    left = {"b": 2, "a": 1}
    right = {"a": 1, "b": 2}
    results["json_key_order_stable"] = canonical_json(left) == canonical_json(right)
    results["source_content_drift_detected"] = (
        sha256_bytes(normalize_lf("a\n").encode())
        != sha256_bytes(normalize_lf("b\n").encode())
    )

    bad_imports = copy.deepcopy(manifest["imports"])
    bad_imports[0]["normalization_id"] = "norm.wrong"
    try:
        validate_imports(manifest["exports"], bad_imports)
    except ValueError:
        results["typed_import_mismatch_rejected"] = True
    else:
        results["typed_import_mismatch_rejected"] = False

    bad_manifest = copy.deepcopy(manifest)
    progress = bad_manifest["progress_classification"]
    progress["actual_fixed_power"] = progress.pop(
        "actual_fixed_power_target_level"
    )
    progress.pop("actual_fixed_power_status")
    progress.pop("actual_fixed_power_achieved")
    try:
        validate_manifest(bad_manifest)
    except ValueError:
        results["ambiguous_actual_fixed_power_field_rejected"] = True
    else:
        results["ambiguous_actual_fixed_power_field_rejected"] = False

    bad_nodes = copy.deepcopy(manifest["nodes"])
    for record in bad_nodes:
        if record["node_id"] == "H1.frontier_totalization":
            record["required_artifact"] = (
                "zero four-map defect vector or a complete original-scale "
                "S_frontier=o(X) theorem"
            )
    try:
        validate_nodes(bad_nodes, manifest["exports"])
    except ValueError:
        results[
            "frontier_totalization_without_ETO_artifact_rejected"
        ] = True
    else:
        results[
            "frontier_totalization_without_ETO_artifact_rejected"
        ] = False

    bad_nodes = copy.deepcopy(manifest["nodes"])
    for record in bad_nodes:
        if record["node_id"] == "H9.physical_registry":
            record["required_artifact"] = (
                "complete occurrence registry and independent physical "
                "Lambda upper certificate"
            )
    try:
        validate_nodes(bad_nodes, manifest["exports"])
    except ValueError:
        results["endpoint_required_artifact_compression_rejected"] = True
    else:
        results["endpoint_required_artifact_compression_rejected"] = False

    bad_nodes = copy.deepcopy(manifest["nodes"])
    for record in bad_nodes:
        if record["node_id"] == "H8.final_reconnection":
            record["parents"].append("A149.actual_mobius_periodic_corridor")
    try:
        validate_nodes(bad_nodes, manifest["exports"])
    except ValueError:
        results["H9_indirect_arithmetic_dependency_rejected"] = True
    else:
        results["H9_indirect_arithmetic_dependency_rejected"] = False

    bad_nodes = copy.deepcopy(manifest["nodes"])
    for record in bad_nodes:
        if record["node_id"] == "A149.actual_mobius_periodic_corridor":
            record["program_level"] = "L2_TARGET_POSITIVE"
    try:
        validate_nodes(bad_nodes, manifest["exports"])
    except ValueError:
        results["actual_core_pseudo_L2_rejected"] = True
    else:
        results["actual_core_pseudo_L2_rejected"] = False

    threshold = Fraction(1, 400)
    results["endpoint_strict_upper_pass"] = (
        physical_endpoint_state(
            threshold, Fraction(1, 500), None, True
        ) == "STRICT_PASS"
    )
    results["endpoint_upper_failure_not_stop"] = (
        physical_endpoint_state(
            threshold, Fraction(1, 300), None, True
        ) == "NO_PASS_CERTIFICATE"
    )
    results["endpoint_equality_lower_stop"] = (
        physical_endpoint_state(
            threshold, None, threshold, True
        ) == "EQUALITY_STOP"
    )
    results["unknown_endpoint_not_zero"] = (
        physical_endpoint_state(threshold, None, None, False) == "INCOMPLETE"
    )

    bad_routes = copy.deepcopy(manifest["route_universe"])
    bad_routes["universe_completeness"]["status"] = "PROVED"
    try:
        validate_routes(bad_routes, manifest["exports"])
    except ValueError:
        results["unproved_universe_completeness_rejected"] = True
    else:
        results["unproved_universe_completeness_rejected"] = False

    bad_routes = copy.deepcopy(manifest["route_universe"])
    stopped = next(
        record
        for record in bad_routes["stops"].values()
        if record["stopped"]
    )
    stopped["scope_id"] = "scope.wrong"
    try:
        validate_routes(bad_routes, manifest["exports"])
    except ValueError:
        results["route_stop_scope_mismatch_rejected"] = True
    else:
        results["route_stop_scope_mismatch_rejected"] = False

    bad_manifest = copy.deepcopy(manifest)
    scalar_route = bad_manifest["frontier_contract"]["scalar_route"]
    scalar_route["frontier_scalar_proved"] = True
    scalar_route["pass"] = True
    try:
        validate_manifest(bad_manifest)
    except ValueError:
        results["frontier_scalar_without_ETO_rejected"] = True
    else:
        results["frontier_scalar_without_ETO_rejected"] = False

    bad_manifest = copy.deepcopy(manifest)
    bad_manifest["claim_boundary"][
        "schema_nonidentifiability_is_actual_carrier_impossibility"
    ] = True
    try:
        validate_manifest(bad_manifest)
    except ValueError:
        results["schema_nonidentifiability_promotion_rejected"] = True
    else:
        results["schema_nonidentifiability_promotion_rejected"] = False

    first = manifest["first_missing"]
    results["descendant_cannot_preempt_missing_ancestor"] = (
        first["minimal_missing_set"] == ["H1.frontier_occurrence_lift"]
    )
    results["empty_eto_sample_not_total"] = (
        not manifest["frontier_contract"][
            "empty_sample_class_implies_asymptotic_empty"
        ]
    )
    results["cut_selector_promotion_rejected"] = (
        not manifest["frontier_contract"]["cut_selector"][
            "is_downstream_selector"
        ]
    )
    results["log_shadow_does_not_pay_endpoint"] = (
        parse_fraction(
            manifest["endpoint_ledgers"]["arithmetic"][
                "best_shadow_x_power_sigma"
            ]
        ) == 0
        and manifest["endpoint_ledgers"]["arithmetic"][
            "log_saving_pays_fixed_power"
        ] is False
    )
    return results


def build_audit(
    manifest: dict[str, Any],
    manifest_rendered: str,
) -> dict[str, Any]:
    checks = validate_manifest(manifest)
    regressions = mutation_regressions(manifest)
    status = all(checks.values()) and all(regressions.values())
    return {
        "schema": "tpc-151-source-locked-integration-audit-v1",
        "status": "PASS" if status else "FAIL",
        "manifest_sha256": sha256_bytes(manifest_rendered.encode("utf-8")),
        "hash_mode": HASH_MODE,
        "checks": checks,
        "mutation_regressions": regressions,
        "first_missing": manifest["first_missing"],
        "progress_classification": manifest["progress_classification"],
        "claim_boundary": manifest["claim_boundary"],
    }


def write_canonical(path: Path, rendered: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(rendered)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare committed deterministic artifacts without writing",
    )
    args = parser.parse_args()

    manifest = build_manifest()
    manifest_rendered = canonical_json(manifest)
    audit = build_audit(manifest, manifest_rendered)
    audit_rendered = canonical_json(audit)
    if args.check:
        for path, expected in (
            (MANIFEST_PATH, manifest_rendered),
            (AUDIT_PATH, audit_rendered),
        ):
            if not path.is_file():
                raise SystemExit(f"missing certificate: {path.name}")
            existing = normalize_lf(path.read_text(encoding="utf-8"))
            if existing != expected:
                raise SystemExit(f"certificate mismatch: {path.name}")
    else:
        write_canonical(MANIFEST_PATH, manifest_rendered)
        write_canonical(AUDIT_PATH, audit_rendered)
    print(audit_rendered, end="")
    if audit["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
