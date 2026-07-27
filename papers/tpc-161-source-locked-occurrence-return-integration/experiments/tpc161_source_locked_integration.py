#!/usr/bin/env python3
"""Build and audit the deterministic TPC-161 integration snapshot.

This script is an administrative proof-interface audit.  It source-locks the
frozen TPC-151--160 artifacts, validates their declared semantics, constructs a
typed proof DAG, and enforces claim and endpoint-accounting firewalls.  It does
not turn source hashes, synthetic fixtures, or interface theorems into new
arithmetic evidence.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PAPER_DIR = HERE.parent
PAPERS_DIR = PAPER_DIR.parent
REPO_DIR = PAPERS_DIR.parent

MANIFEST_PATH = HERE / "tpc161_occurrence_return_manifest.json"
MANIFEST_SCHEMA_PATH = HERE / "tpc161_occurrence_return_manifest.schema.json"
AUDIT_PATH = HERE / "tpc161_occurrence_return_audit.json"
AUDIT_SCHEMA_PATH = HERE / "tpc161_occurrence_return_audit.schema.json"

MANIFEST_SCHEMA = "tpc-161-occurrence-return-integration-manifest-v1"
AUDIT_SCHEMA = "tpc-161-occurrence-return-integration-audit-v1"
HASH_MODE = "CANONICAL_UTF8_LF_V2"

STATUSES = {"PROVED", "OPEN", "NOT_TESTABLE", "STOPPED"}
NODE_TYPES = {"EVIDENCE", "TARGET", "ALL", "ANY_CLAUSE", "SCOPED_STOP"}
READINESS = {"READY", "MISSING", "BLOCKED_BY_PARENT", "NOT_APPLICABLE"}
ARITHMETIC_ROLES = {
    "ARITHMETIC_CORE",
    "ARITHMETIC_TARGET",
    "ARITHMETIC_NEGATIVE",
}
NINE_DEFECTS = (
    "D_L",
    "D_QD",
    "D_QZ",
    "D_G",
    "D_P",
    "D_DZ",
    "D_GP",
    "D_cover",
    "D_rec",
)
EXPECTED_ENDPOINT_CHARGES = {
    "ARITH.correlation_log_saving",
    "ARITH.dyadic_shadow",
    "PHYS.good_variation",
    "PHYS.bad_variation",
    "PHYS.phase_return",
    "PHYS.four_sign_reconnection",
}

SOURCE_SPECS = (
    (151, "TPC151.integration_script", "experiments/tpc151_source_locked_integration.py", "SCRIPT"),
    (151, "TPC151.integration_manifest", "experiments/tpc151_integration_manifest.json", "OUTPUT"),
    (151, "TPC151.integration_audit", "experiments/tpc151_source_locked_integration_audit.json", "OUTPUT"),
    (152, "TPC152.route_script", "experiments/tpc152_mvp5_route_audit.py", "SCRIPT"),
    (152, "TPC152.snapshot", "experiments/tpc152_mvp5_snapshot.json", "OUTPUT"),
    (152, "TPC152.route_audit", "experiments/tpc152_mvp5_route_audit.json", "OUTPUT"),
    (153, "TPC153.shadow_script", "experiments/tpc153_cut_occurrence_shadow.py", "SCRIPT"),
    (153, "TPC153.shadow_certificate", "experiments/tpc153_cut_occurrence_shadow_certificate.json", "OUTPUT"),
    (154, "TPC154.obstruction_script", "experiments/tpc154_completion_fiber_obstruction.py", "SCRIPT"),
    (154, "TPC154.obstruction_certificate", "experiments/tpc154_completion_fiber_obstruction_certificate.json", "OUTPUT"),
    (155, "TPC155.witness_script", "experiments/tpc155_occurrence_witness_verifier.py", "SCRIPT"),
    (155, "TPC155.witness_audit", "experiments/tpc155_occurrence_witness_audit.json", "OUTPUT"),
    (155, "TPC155.production_status", "samples/tpc155_production_witness_status.json", "OUTPUT"),
    (156, "TPC156.decision_script", "experiments/tpc156_h1_occurrence_decision.py", "SCRIPT"),
    (156, "TPC156.decision", "experiments/tpc156_h1_occurrence_decision.json", "OUTPUT"),
    (156, "TPC156.decision_audit", "experiments/tpc156_h1_occurrence_audit.json", "OUTPUT"),
    (157, "TPC157.weight_script", "experiments/tpc157_periodic_approximation_audit.py", "SCRIPT"),
    (157, "TPC157.weight_audit", "experiments/tpc157_periodic_approximation_audit.json", "OUTPUT"),
    (158, "TPC158.phase_script", "experiments/tpc158_phase_gate_audit.py", "SCRIPT"),
    (158, "TPC158.phase_audit", "experiments/tpc158_phase_gate_audit.json", "OUTPUT"),
    (159, "TPC159.prefix_script", "experiments/tpc159_dyadic_shadow_audit.py", "SCRIPT"),
    (159, "TPC159.prefix_audit", "experiments/tpc159_dyadic_shadow_audit.json", "OUTPUT"),
    (160, "TPC160.abel_script", "experiments/tpc160_abel_return_audit.py", "SCRIPT"),
    (160, "TPC160.abel_audit", "experiments/tpc160_abel_return_audit.json", "OUTPUT"),
)


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_source_bytes(path: Path) -> bytes:
    text = normalize_lf(path.read_text(encoding="utf-8"))
    if path.suffix == ".json":
        text = canonical_json(json.loads(text))
    return text.encode("utf-8")


def canonical_source_hash(path: Path) -> str:
    return sha256_bytes(canonical_source_bytes(path))


def find_paper(number: int) -> Path:
    matches = sorted(path for path in PAPERS_DIR.glob(f"tpc-{number}-*") if path.is_dir())
    if len(matches) != 1:
        raise FileNotFoundError(
            f"expected exactly one TPC-{number} directory; found {len(matches)}"
        )
    return matches[0]


def source_path(number: int, relative: str) -> Path:
    path = find_paper(number) / Path(relative)
    if not path.is_file():
        raise FileNotFoundError(f"missing frozen source: {path}")
    return path


def load_source_json(number: int, relative: str) -> dict[str, Any]:
    return json.loads(
        normalize_lf(source_path(number, relative).read_text(encoding="utf-8"))
    )


def build_source_locks() -> list[dict[str, Any]]:
    locks: list[dict[str, Any]] = []
    for number, source_id, relative, kind in SOURCE_SPECS:
        path = source_path(number, relative)
        locks.append(
            {
                "canonical_utf8_lf_sha256": canonical_source_hash(path),
                "kind": kind,
                "paper": f"TPC-{number}",
                "path": path.relative_to(REPO_DIR).as_posix(),
                "source_id": source_id,
            }
        )
    return locks


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_frozen_semantics() -> dict[str, Any]:
    """Validate the exact claims imported from the frozen source artifacts."""

    m151 = load_source_json(151, "experiments/tpc151_integration_manifest.json")
    a151 = load_source_json(
        151, "experiments/tpc151_source_locked_integration_audit.json"
    )
    s152 = load_source_json(152, "experiments/tpc152_mvp5_snapshot.json")
    a152 = load_source_json(152, "experiments/tpc152_mvp5_route_audit.json")
    c153 = load_source_json(
        153, "experiments/tpc153_cut_occurrence_shadow_certificate.json"
    )
    c154 = load_source_json(
        154, "experiments/tpc154_completion_fiber_obstruction_certificate.json"
    )
    a155 = load_source_json(
        155, "experiments/tpc155_occurrence_witness_audit.json"
    )
    p155 = load_source_json(
        155, "samples/tpc155_production_witness_status.json"
    )
    d156 = load_source_json(
        156, "experiments/tpc156_h1_occurrence_decision.json"
    )
    a156 = load_source_json(
        156, "experiments/tpc156_h1_occurrence_audit.json"
    )
    a157 = load_source_json(
        157, "experiments/tpc157_periodic_approximation_audit.json"
    )
    a158 = load_source_json(
        158, "experiments/tpc158_phase_gate_audit.json"
    )
    a159 = load_source_json(
        159, "experiments/tpc159_dyadic_shadow_audit.json"
    )
    a160 = load_source_json(
        160, "experiments/tpc160_abel_return_audit.json"
    )

    for label, payload in (
        ("TPC151 audit", a151),
        ("TPC152 audit", a152),
        ("TPC153 certificate", c153),
        ("TPC154 certificate", c154),
        ("TPC155 audit", a155),
        ("TPC156 audit", a156),
        ("TPC157 audit", a157),
        ("TPC158 audit", a158),
        ("TPC159 audit", a159),
        ("TPC160 audit", a160),
    ):
        require(payload["status"] == "PASS", f"{label} is not PASS")

    require(
        m151["progress_classification"]["new_positive_L2"] is False
        and m151["progress_classification"]["actual_fixed_power_achieved"] is False,
        "TPC151 positive-L2 boundary drifted",
    )
    require(
        s152["current_verdict"] == "NOT_TESTABLE"
        and s152["first_missing"]["node_id"] == "H1.frontier_occurrence_lift",
        "TPC152 anchor semantics drifted",
    )
    require(
        c153["theorem_exports"]["H1.cut_occurrence_shadow"]
        == "PROVED_L1_STRUCTURAL"
        and c153["theorem_exports"]["H1.frontier_occurrence_lift"]
        == "NOT_TESTABLE",
        "TPC153 shadow boundary drifted",
    )
    require(
        c154["theorem_exports"]["H1.current_artifacts_only_canonical_actual_lift"]
        == "STOP_DECLARED_ROUTE"
        and c154["theorem_exports"]["selected_augmented_route_stopped"] is False,
        "TPC154 scoped stop drifted",
    )
    require(
        a155["claim_boundary"]["actual_occurrence_lift_proved"] is False
        and p155["production_witness_present"] is False
        and p155["current_production_actual_witness_status"] == "NOT_TESTABLE",
        "TPC155 production witness boundary drifted",
    )
    require(
        d156["current_verdict"] == "NOT_TESTABLE"
        and d156["first_missing_selected_route"]
        == "H1.theorem_backed_occurrence_provenance_crosswalk"
        and tuple(d156["defects"].keys())
        == tuple(sorted((*NINE_DEFECTS, "D_occ"))),
        "TPC156 H1 decision drifted",
    )
    require(
        a157["theorem"]["status"]
        == "PROVED_L1_ACTUAL_CORE_WEIGHT_INTERFACE"
        and a157["production_status"]["literal_physical_weight_registry"]
        == "NOT_TESTABLE",
        "TPC157 weight-interface boundary drifted",
    )
    require(
        a158["major_arc"]["status"] == "PROVED_L1_ACTUAL_CORE_MAJOR_ARC"
        and a158["route_decision"]["production_phase_cell"] == "NOT_TESTABLE"
        and a158["minor_arc_projection"]["status"] == "PROVED_SCOPED_ROUTE_STOP",
        "TPC158 phase-gate boundary drifted",
    )
    require(
        a159["theorem"]["status"]
        == "PROVED_L1_ACTUAL_PREFIX_ALMOST_ENDPOINT"
        and a159["production_status"]["actual_endpoint_registry_avoids_shadow"]
        == "NOT_TESTABLE"
        and a159["claim_boundary"]["all_deterministic_prefixes"] is False,
        "TPC159 prefix boundary drifted",
    )
    require(
        a160["theorem"]["status"]
        == "PROVED_L1_ACTUAL_WEIGHTED_ALMOST_ENDPOINT_INTERFACE"
        and a160["conditional_promotion"]["currently_achieved"] is False
        and a160["conditional_promotion"]["fixed_X_power_exponent"] == 0
        and a160["production_status"]["actual_literal_weight"]
        == "NOT_TESTABLE"
        and a160["production_status"]["actual_endpoint_registry"]
        == "NOT_TESTABLE",
        "TPC160 Abel-interface boundary drifted",
    )

    return {
        "tpc151_anchor": {
            "first_missing": m151["first_missing"]["node_id"],
            "new_positive_L2": False,
            "status": "PASS",
        },
        "tpc152_anchor": {
            "current_verdict": s152["current_verdict"],
            "first_missing": s152["first_missing"]["node_id"],
            "status": "PASS",
        },
        "tpc153_shadow": {
            "status": c153["theorem_exports"]["H1.cut_occurrence_shadow"],
            "production_census": c153["census"]["production_terminal_type_counts"],
        },
        "tpc154_current_schema_route": {
            "selected_augmented_route_stopped": False,
            "status": "STOP_DECLARED_ROUTE",
        },
        "tpc155_production_witness": {
            "present": False,
            "status": "NOT_TESTABLE",
        },
        "tpc156_h1_decision": {
            "current_verdict": "NOT_TESTABLE",
            "first_missing": "H1.theorem_backed_occurrence_provenance_crosswalk",
        },
        "tpc157_weight_interface": {
            "production_weight_registry": "NOT_TESTABLE",
            "status": a157["theorem"]["status"],
        },
        "tpc158_phase_interface": {
            "production_phase_cell": "NOT_TESTABLE",
            "status": a158["major_arc"]["status"],
        },
        "tpc159_prefix": {
            "all_prefix": False,
            "status": a159["theorem"]["status"],
        },
        "tpc160_abel_interface": {
            "fixed_X_power_exponent": 0,
            "production_endpoint_registry": "NOT_TESTABLE",
            "production_weight": "NOT_TESTABLE",
            "status": a160["theorem"]["status"],
        },
    }


def registry_entry(
    key: str, status: str, description: str, source_ref: str
) -> dict[str, str]:
    return {
        "description": description,
        "key": key,
        "source_ref": source_ref,
        "status": status,
    }


def build_registries() -> dict[str, Any]:
    return {
        "artifacts": [
            registry_entry(
                "artifact.frozen_source_record",
                "READY",
                "canonical source-locked frozen evidence record",
                "TPC151--TPC160",
            ),
            registry_entry(
                "artifact.cut_occurrence_shadow",
                "READY",
                "canonical unit cut shadow on every archived nonsoft path",
                "TPC153.shadow_certificate",
            ),
            registry_entry(
                "artifact.theorem_backed_crosswalk",
                "MISSING",
                "actual row-level cut-to-occurrence provenance theorem",
                "TPC156.decision",
            ),
            registry_entry(
                "artifact.complete_FUM_scalar_oX",
                "MISSING",
                "complete original-scale FUM scalar o(X) theorem",
                "TPC156.decision",
            ),
            registry_entry(
                "artifact.ETO_disposition",
                "MISSING",
                "growing-scale theorem-backed ETO totalization or softness",
                "TPC156.decision",
            ),
            registry_entry(
                "artifact.literal_weight_registry",
                "MISSING",
                "source-locked literal physical multiplier on actual occurrences",
                "TPC157.weight_audit",
            ),
            registry_entry(
                "artifact.phase_cell_registry",
                "MISSING",
                "source-locked production phase cell and regime label",
                "TPC158.phase_audit",
            ),
            registry_entry(
                "artifact.endpoint_registry",
                "MISSING",
                "actual atomic endpoint registry with shadow membership",
                "TPC159.prefix_audit",
            ),
            registry_entry(
                "artifact.normalization_registry",
                "MISSING",
                "literal physical normalization and no-double-charge lineage",
                "TPC160.abel_audit",
            ),
            registry_entry(
                "artifact.periodic_actual_core",
                "READY",
                "determinant-two two-Mobius core with periodic multiplier",
                "TPC151.integration_manifest",
            ),
            registry_entry(
                "artifact.almost_endpoint_prefix",
                "READY",
                "periodic-core prefix outside the dyadic shadow",
                "TPC159.prefix_audit",
            ),
            registry_entry(
                "artifact.phase_projection_obstruction",
                "READY",
                "exact small-period projection obstruction on separated phase cells",
                "TPC158.phase_audit",
            ),
            registry_entry(
                "artifact.weighted_abel_interface",
                "READY",
                "exact Abel interface with good and bad variation",
                "TPC160.abel_audit",
            ),
        ],
        "carriers": [
            registry_entry(
                "carrier.all_nonsoft_cut_paths",
                "READY",
                "disjoint ETO union FUM source domain",
                "TPC153.shadow_certificate",
            ),
            registry_entry(
                "carrier.formal_completion_fibers",
                "READY",
                "maximal current-schema formal completion class",
                "TPC154.obstruction_certificate",
            ),
            registry_entry(
                "carrier.synthetic_witness_bundle",
                "READY",
                "L0 verifier fixture, not production evidence",
                "TPC155.witness_audit",
            ),
            registry_entry(
                "carrier.downstream_occurrences",
                "MISSING",
                "actual row-separated downstream occurrence carrier",
                "TPC156.decision",
            ),
            registry_entry(
                "carrier.determinant_two_two_mobius_core",
                "READY",
                "actual fixed-two quotient-Mobius periodic core",
                "TPC151.integration_manifest",
            ),
            registry_entry(
                "carrier.actual_h3_packet",
                "MISSING",
                "complete literal physical fixed-h0 packet",
                "TPC160.abel_audit",
            ),
        ],
        "normalizations": [
            registry_entry(
                "norm.physical_atomic",
                "READY",
                "literal physical atomic normalization",
                "TPC151.integration_manifest",
            ),
            registry_entry(
                "norm.q_over_N",
                "READY",
                "fiber-block normalization q/N",
                "TPC157.weight_audit",
            ),
            registry_entry(
                "norm.q_over_T",
                "READY",
                "cumulative fiber normalization q/T",
                "TPC159.prefix_audit",
            ),
            registry_entry(
                "norm.endpoint_amplitude",
                "MISSING",
                "full physical endpoint amplitude normalization",
                "TPC160.abel_audit",
            ),
        ],
        "scopes": [
            registry_entry(
                "scope.physical_nonsoft_cut",
                "READY",
                "archived physical ETO and FUM cut paths",
                "TPC153.shadow_certificate",
            ),
            registry_entry(
                "scope.current_schema_formal_completion",
                "READY",
                "formal completions determined only by current fields",
                "TPC154.obstruction_certificate",
            ),
            registry_entry(
                "scope.synthetic_witness_contract",
                "READY",
                "finite verifier soundness on a supplied bundle",
                "TPC155.witness_audit",
            ),
            registry_entry(
                "scope.h1_occurrence_augmented_route",
                "MISSING",
                "production theorem-backed occurrence crosswalk route",
                "TPC156.decision",
            ),
            registry_entry(
                "scope.actual_periodic_core_almost_scale",
                "READY",
                "actual fixed-two periodic core outside the source exceptional set",
                "TPC151.integration_manifest",
            ),
            registry_entry(
                "scope.actual_core_major_arc",
                "READY",
                "phase cells in the certified small-period major arcs",
                "TPC158.phase_audit",
            ),
            registry_entry(
                "scope.actual_core_minor_projection_obstruction",
                "READY",
                "separated phase cells stopped only for the small-period approximation route",
                "TPC158.phase_audit",
            ),
            registry_entry(
                "scope.actual_core_prefix_outside_shadow",
                "READY",
                "almost-endpoint prefixes outside the dyadic exceptional shadow",
                "TPC159.prefix_audit",
            ),
            registry_entry(
                "scope.actual_core_bad_endpoint",
                "READY",
                "actual periodic core at endpoints inside the dyadic bad set",
                "TPC159.prefix_audit",
            ),
            registry_entry(
                "scope.actual_core_weighted_almost_endpoint",
                "READY",
                "Abel-weighted periodic core with split variation",
                "TPC160.abel_audit",
            ),
            registry_entry(
                "scope.actual_fixed_h0_endpoint",
                "MISSING",
                "complete literal physical fixed-h0 endpoint synthesis",
                "INTEGRATION_DERIVED",
            ),
        ],
    }


def import_record(
    import_id: str,
    paper: str,
    source_export_id: str,
    status: str,
    evidence_level: str,
    scope_id: str,
    carrier_id: str,
    normalization_id: str,
    role: str,
    artifact_readiness: str,
    promotion_eligible: bool,
) -> dict[str, Any]:
    return {
        "artifact_readiness": artifact_readiness,
        "carrier_id": carrier_id,
        "evidence_level": evidence_level,
        "import_id": import_id,
        "normalization_id": normalization_id,
        "paper": paper,
        "promotion_eligible": promotion_eligible,
        "role": role,
        "scope_id": scope_id,
        "source_export_id": source_export_id,
        "status": status,
    }


def build_imports() -> list[dict[str, Any]]:
    return [
        import_record(
            "I151.actual_periodic_core",
            "TPC-151",
            "A149.actual_mobius_periodic_corridor",
            "PROVED",
            "L1_ACTUAL_CORE",
            "scope.actual_periodic_core_almost_scale",
            "carrier.determinant_two_two_mobius_core",
            "norm.q_over_N",
            "ARITHMETIC_CORE",
            "READY",
            False,
        ),
        import_record(
            "I152.mvp5_anchor",
            "TPC-152",
            "MVP5.NOT_TESTABLE",
            "NOT_TESTABLE",
            "L1_INTEGRATION",
            "scope.h1_occurrence_augmented_route",
            "carrier.downstream_occurrences",
            "norm.physical_atomic",
            "STRUCTURAL",
            "MISSING",
            False,
        ),
        import_record(
            "I153.cut_shadow",
            "TPC-153",
            "H1.cut_occurrence_shadow",
            "PROVED",
            "L1_STRUCTURAL",
            "scope.physical_nonsoft_cut",
            "carrier.all_nonsoft_cut_paths",
            "norm.physical_atomic",
            "STRUCTURAL",
            "READY",
            False,
        ),
        import_record(
            "I154.current_schema_stop",
            "TPC-154",
            "H1.current_artifacts_only_canonical_actual_lift",
            "STOPPED",
            "L0_SCHEMA_NEGATIVE",
            "scope.current_schema_formal_completion",
            "carrier.formal_completion_fibers",
            "norm.physical_atomic",
            "STRUCTURAL_NEGATIVE",
            "READY",
            False,
        ),
        import_record(
            "I155.witness_verifier",
            "TPC-155",
            "OccurrenceWitnessV1.verifier_internal_soundness",
            "PROVED",
            "L0_VERIFIER",
            "scope.synthetic_witness_contract",
            "carrier.synthetic_witness_bundle",
            "norm.physical_atomic",
            "STRUCTURAL",
            "READY",
            False,
        ),
        import_record(
            "I156.h1_crosswalk_decision",
            "TPC-156",
            "H1.theorem_backed_occurrence_provenance_crosswalk",
            "NOT_TESTABLE",
            "L1_STRUCTURAL_TARGET",
            "scope.h1_occurrence_augmented_route",
            "carrier.downstream_occurrences",
            "norm.physical_atomic",
            "STRUCTURAL",
            "MISSING",
            False,
        ),
        import_record(
            "I156.h1_typed_contract",
            "TPC-156",
            "H1.typed_map_scalar_contract",
            "PROVED",
            "L1_STRUCTURAL",
            "scope.h1_occurrence_augmented_route",
            "carrier.all_nonsoft_cut_paths",
            "norm.physical_atomic",
            "STRUCTURAL",
            "READY",
            False,
        ),
        import_record(
            "I157.weight_interface",
            "TPC-157",
            "A157.literal_weight_periodic_approximation",
            "PROVED",
            "L1_ACTUAL_CORE_WEIGHT_INTERFACE",
            "scope.actual_periodic_core_almost_scale",
            "carrier.determinant_two_two_mobius_core",
            "norm.q_over_N",
            "ARITHMETIC_CORE",
            "READY",
            False,
        ),
        import_record(
            "I158.major_arc",
            "TPC-158",
            "A158.additive_phase_major_arc",
            "PROVED",
            "L1_ACTUAL_CORE_MAJOR_ARC",
            "scope.actual_core_major_arc",
            "carrier.determinant_two_two_mobius_core",
            "norm.q_over_N",
            "ARITHMETIC_CORE",
            "READY",
            False,
        ),
        import_record(
            "I158.periodic_route_stop",
            "TPC-158",
            "N158.small_period_phase_projection_obstruction",
            "STOPPED",
            "L1_SCOPED_NEGATIVE",
            "scope.actual_core_minor_projection_obstruction",
            "carrier.determinant_two_two_mobius_core",
            "norm.q_over_N",
            "ARITHMETIC_NEGATIVE",
            "READY",
            False,
        ),
        import_record(
            "I159.almost_endpoint_prefix",
            "TPC-159",
            "A159.dyadic_shadow_almost_endpoint_prefix",
            "PROVED",
            "L1_ACTUAL_PREFIX_ALMOST_ENDPOINT",
            "scope.actual_core_prefix_outside_shadow",
            "carrier.determinant_two_two_mobius_core",
            "norm.q_over_T",
            "ARITHMETIC_CORE",
            "READY",
            False,
        ),
        import_record(
            "I160.abel_interface",
            "TPC-160",
            "A160.exceptional_variation_abel_return",
            "PROVED",
            "L1_ACTUAL_WEIGHTED_ALMOST_ENDPOINT_INTERFACE",
            "scope.actual_core_weighted_almost_endpoint",
            "carrier.determinant_two_two_mobius_core",
            "norm.q_over_T",
            "ARITHMETIC_CORE",
            "READY",
            False,
        ),
    ]


def node(
    node_id: str,
    node_type: str,
    status: str,
    role: str,
    program_level: str,
    parents: Iterable[str] = (),
    clauses: Iterable[Iterable[str]] = (),
    evidence_id: str = "INTEGRATION_DERIVED",
    scope_id: str = "scope.actual_fixed_h0_endpoint",
    carrier_id: str = "carrier.actual_h3_packet",
    normalization_id: str = "norm.endpoint_amplitude",
    required_artifact_id: str = "artifact.frozen_source_record",
    artifact_readiness: str = "READY",
) -> dict[str, Any]:
    return {
        "artifact_readiness": artifact_readiness,
        "carrier_id": carrier_id,
        "clauses": [list(clause) for clause in clauses],
        "evidence_id": evidence_id,
        "node_id": node_id,
        "node_type": node_type,
        "normalization_id": normalization_id,
        "parents": list(parents),
        "program_level": program_level,
        "required_artifact_id": required_artifact_id,
        "role": role,
        "scope_id": scope_id,
        "status": status,
    }


def build_nodes() -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = [
        node(
            "S153.cut_occurrence_shadow",
            "EVIDENCE",
            "PROVED",
            "STRUCTURAL",
            "L1_STRUCTURAL",
            evidence_id="I153.cut_shadow",
            scope_id="scope.physical_nonsoft_cut",
            carrier_id="carrier.all_nonsoft_cut_paths",
            normalization_id="norm.physical_atomic",
            required_artifact_id="artifact.cut_occurrence_shadow",
        ),
        node(
            "N154.current_schema_only_lift",
            "SCOPED_STOP",
            "STOPPED",
            "STRUCTURAL_NEGATIVE",
            "L0_SCHEMA_NEGATIVE",
            parents=("S153.cut_occurrence_shadow",),
            evidence_id="I154.current_schema_stop",
            scope_id="scope.current_schema_formal_completion",
            carrier_id="carrier.formal_completion_fibers",
            normalization_id="norm.physical_atomic",
            artifact_readiness="NOT_APPLICABLE",
        ),
        node(
            "C155.occurrence_witness_verifier",
            "EVIDENCE",
            "PROVED",
            "STRUCTURAL",
            "L0_VERIFIER",
            evidence_id="I155.witness_verifier",
            scope_id="scope.synthetic_witness_contract",
            carrier_id="carrier.synthetic_witness_bundle",
            normalization_id="norm.physical_atomic",
        ),
        node(
            "D156.h1_typed_contract",
            "EVIDENCE",
            "PROVED",
            "STRUCTURAL",
            "L1_STRUCTURAL",
            evidence_id="I156.h1_typed_contract",
            scope_id="scope.h1_occurrence_augmented_route",
            carrier_id="carrier.all_nonsoft_cut_paths",
            normalization_id="norm.physical_atomic",
        ),
        node(
            "A151.actual_periodic_core",
            "EVIDENCE",
            "PROVED",
            "ARITHMETIC_CORE",
            "L1_ACTUAL_CORE",
            evidence_id="I151.actual_periodic_core",
            scope_id="scope.actual_periodic_core_almost_scale",
            carrier_id="carrier.determinant_two_two_mobius_core",
            normalization_id="norm.q_over_N",
            required_artifact_id="artifact.periodic_actual_core",
        ),
        node(
            "A157.literal_weight_interface",
            "EVIDENCE",
            "PROVED",
            "ARITHMETIC_CORE",
            "L1_ACTUAL_CORE_WEIGHT_INTERFACE",
            parents=("A151.actual_periodic_core",),
            evidence_id="I157.weight_interface",
            scope_id="scope.actual_periodic_core_almost_scale",
            carrier_id="carrier.determinant_two_two_mobius_core",
            normalization_id="norm.q_over_N",
            required_artifact_id="artifact.periodic_actual_core",
        ),
        node(
            "A158.major_arc_interface",
            "EVIDENCE",
            "PROVED",
            "ARITHMETIC_CORE",
            "L1_ACTUAL_CORE_MAJOR_ARC",
            parents=("A157.literal_weight_interface",),
            evidence_id="I158.major_arc",
            scope_id="scope.actual_core_major_arc",
            carrier_id="carrier.determinant_two_two_mobius_core",
            normalization_id="norm.q_over_N",
            required_artifact_id="artifact.periodic_actual_core",
        ),
        node(
            "N158.small_period_projection_route",
            "SCOPED_STOP",
            "STOPPED",
            "ARITHMETIC_NEGATIVE",
            "L1_SCOPED_NEGATIVE",
            parents=("A157.literal_weight_interface",),
            evidence_id="I158.periodic_route_stop",
            scope_id="scope.actual_core_minor_projection_obstruction",
            carrier_id="carrier.determinant_two_two_mobius_core",
            normalization_id="norm.q_over_N",
            required_artifact_id="artifact.phase_projection_obstruction",
            artifact_readiness="NOT_APPLICABLE",
        ),
        node(
            "A159.almost_endpoint_prefix",
            "EVIDENCE",
            "PROVED",
            "ARITHMETIC_CORE",
            "L1_ACTUAL_PREFIX_ALMOST_ENDPOINT",
            parents=("A151.actual_periodic_core",),
            evidence_id="I159.almost_endpoint_prefix",
            scope_id="scope.actual_core_prefix_outside_shadow",
            carrier_id="carrier.determinant_two_two_mobius_core",
            normalization_id="norm.q_over_T",
            required_artifact_id="artifact.almost_endpoint_prefix",
        ),
        node(
            "A160.weighted_abel_interface",
            "EVIDENCE",
            "PROVED",
            "ARITHMETIC_CORE",
            "L1_ACTUAL_WEIGHTED_ALMOST_ENDPOINT_INTERFACE",
            parents=("A159.almost_endpoint_prefix",),
            evidence_id="I160.abel_interface",
            scope_id="scope.actual_core_weighted_almost_endpoint",
            carrier_id="carrier.determinant_two_two_mobius_core",
            normalization_id="norm.q_over_T",
            required_artifact_id="artifact.weighted_abel_interface",
        ),
        node(
            "O161.direct_additive_twist_core",
            "TARGET",
            "OPEN",
            "ARITHMETIC_TARGET",
            "L1_ACTUAL_CORE_TARGET",
            parents=("A151.actual_periodic_core",),
            scope_id="scope.actual_periodic_core_almost_scale",
            carrier_id="carrier.determinant_two_two_mobius_core",
            normalization_id="norm.q_over_N",
            required_artifact_id="artifact.periodic_actual_core",
        ),
        node(
            "O161.bad_endpoint_pointwise_core",
            "TARGET",
            "OPEN",
            "ARITHMETIC_TARGET",
            "L1_ACTUAL_PREFIX_TARGET",
            parents=(
                "A151.actual_periodic_core",
                "A159.almost_endpoint_prefix",
            ),
            scope_id="scope.actual_core_bad_endpoint",
            carrier_id="carrier.determinant_two_two_mobius_core",
            normalization_id="norm.q_over_T",
            required_artifact_id="artifact.periodic_actual_core",
        ),
        node(
            "H1.theorem_backed_occurrence_provenance_crosswalk",
            "TARGET",
            "NOT_TESTABLE",
            "STRUCTURAL",
            "L1_STRUCTURAL_TARGET",
            parents=(
                "S153.cut_occurrence_shadow",
                "C155.occurrence_witness_verifier",
                "D156.h1_typed_contract",
            ),
            evidence_id="I156.h1_crosswalk_decision",
            scope_id="scope.h1_occurrence_augmented_route",
            carrier_id="carrier.downstream_occurrences",
            normalization_id="norm.physical_atomic",
            required_artifact_id="artifact.theorem_backed_crosswalk",
            artifact_readiness="MISSING",
        ),
        node(
            "H1.frontier_occurrence_lift",
            "TARGET",
            "NOT_TESTABLE",
            "STRUCTURAL",
            "L1_STRUCTURAL_TARGET",
            parents=("H1.theorem_backed_occurrence_provenance_crosswalk",),
            scope_id="scope.h1_occurrence_augmented_route",
            carrier_id="carrier.downstream_occurrences",
            normalization_id="norm.physical_atomic",
            required_artifact_id="artifact.theorem_backed_crosswalk",
            artifact_readiness="BLOCKED_BY_PARENT",
        ),
    ]

    artifact_nodes = {
        "H1.frontier_QD_totality": ("literal determinant-fiber quotient",),
        "H1.frontier_QZ_totality": ("literal ordered zero-mode quotient",),
        "H1.frontier_G_totality": ("literal physical grouping",),
        "H1.frontier_P_h0_totality": ("downstream prescribed-shift selector",),
        "H1.frontier_cover_totality": ("production physical cover",),
        "H1.frontier_reconnection": ("production final reconnection",),
    }
    for node_id in artifact_nodes:
        nodes.append(
            node(
                node_id,
                "TARGET",
                "NOT_TESTABLE",
                "STRUCTURAL",
                "L1_STRUCTURAL_TARGET",
                parents=("H1.frontier_occurrence_lift",),
                scope_id="scope.h1_occurrence_augmented_route",
                carrier_id="carrier.downstream_occurrences",
                normalization_id="norm.physical_atomic",
                required_artifact_id="artifact.theorem_backed_crosswalk",
                artifact_readiness="BLOCKED_BY_PARENT",
            )
        )

    defect_parents = {
        "D_L": ("H1.frontier_occurrence_lift",),
        "D_QD": ("H1.frontier_QD_totality",),
        "D_QZ": ("H1.frontier_QZ_totality",),
        "D_G": ("H1.frontier_G_totality",),
        "D_P": ("H1.frontier_P_h0_totality",),
        "D_DZ": ("H1.frontier_QD_totality", "H1.frontier_QZ_totality"),
        "D_GP": ("H1.frontier_G_totality", "H1.frontier_P_h0_totality"),
        "D_cover": ("H1.frontier_cover_totality",),
        "D_rec": ("H1.frontier_reconnection",),
    }
    for defect_id in NINE_DEFECTS:
        nodes.append(
            node(
                f"H1.defect.{defect_id}",
                "TARGET",
                "NOT_TESTABLE",
                "STRUCTURAL",
                "L1_STRUCTURAL_TARGET",
                parents=defect_parents[defect_id],
                scope_id="scope.h1_occurrence_augmented_route",
                carrier_id="carrier.downstream_occurrences",
                normalization_id="norm.physical_atomic",
                required_artifact_id="artifact.theorem_backed_crosswalk",
                artifact_readiness="BLOCKED_BY_PARENT",
            )
        )

    nodes.extend(
        [
            node(
                "H1.frontier_occurrence_registry_totality",
                "TARGET",
                "NOT_TESTABLE",
                "PHYSICAL_REGISTRY",
                "L1_STRUCTURAL_TARGET",
                parents=(
                    "H1.frontier_occurrence_lift",
                    "H1.frontier_cover_totality",
                    "H1.frontier_reconnection",
                ),
                scope_id="scope.h1_occurrence_augmented_route",
                carrier_id="carrier.downstream_occurrences",
                normalization_id="norm.physical_atomic",
                required_artifact_id="artifact.theorem_backed_crosswalk",
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H1.map_clause",
                "ALL",
                "NOT_TESTABLE",
                "STRUCTURAL",
                "L1_STRUCTURAL_TARGET",
                parents=(
                    "H1.theorem_backed_occurrence_provenance_crosswalk",
                    *(f"H1.defect.{name}" for name in NINE_DEFECTS),
                    "H1.frontier_occurrence_registry_totality",
                ),
                scope_id="scope.h1_occurrence_augmented_route",
                carrier_id="carrier.downstream_occurrences",
                normalization_id="norm.physical_atomic",
                required_artifact_id="artifact.theorem_backed_crosswalk",
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H1.complete_FUM_scalar_oX",
                "TARGET",
                "NOT_TESTABLE",
                "ARITHMETIC_TARGET",
                "L1_ANALYTIC_TARGET",
                scope_id="scope.physical_nonsoft_cut",
                carrier_id="carrier.all_nonsoft_cut_paths",
                normalization_id="norm.physical_atomic",
                required_artifact_id="artifact.complete_FUM_scalar_oX",
                artifact_readiness="MISSING",
            ),
            node(
                "H1.theorem_backed_ETO_disposition",
                "TARGET",
                "NOT_TESTABLE",
                "STRUCTURAL",
                "L1_STRUCTURAL_TARGET",
                scope_id="scope.physical_nonsoft_cut",
                carrier_id="carrier.all_nonsoft_cut_paths",
                normalization_id="norm.physical_atomic",
                required_artifact_id="artifact.ETO_disposition",
                artifact_readiness="MISSING",
            ),
            node(
                "H1.scalar_clause",
                "ALL",
                "NOT_TESTABLE",
                "STRUCTURAL",
                "L1_TARGET",
                parents=(
                    "H1.complete_FUM_scalar_oX",
                    "H1.theorem_backed_ETO_disposition",
                ),
                scope_id="scope.physical_nonsoft_cut",
                carrier_id="carrier.all_nonsoft_cut_paths",
                normalization_id="norm.physical_atomic",
                required_artifact_id="artifact.complete_FUM_scalar_oX",
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H1.frontier_totalization",
                "ANY_CLAUSE",
                "NOT_TESTABLE",
                "STRUCTURAL",
                "L1_TARGET",
                clauses=(("H1.map_clause",), ("H1.scalar_clause",)),
                scope_id="scope.physical_nonsoft_cut",
                carrier_id="carrier.all_nonsoft_cut_paths",
                normalization_id="norm.physical_atomic",
                required_artifact_id="artifact.theorem_backed_crosswalk",
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
        ]
    )

    for node_id, artifact_id in (
        ("H9.literal_weight_registry", "artifact.literal_weight_registry"),
        ("H9.phase_cell_registry", "artifact.phase_cell_registry"),
        ("H9.endpoint_registry", "artifact.endpoint_registry"),
        ("H9.normalization_registry", "artifact.normalization_registry"),
    ):
        nodes.append(
            node(
                node_id,
                "TARGET",
                "NOT_TESTABLE",
                "PHYSICAL_REGISTRY",
                "L1_PHYSICAL_TARGET",
                required_artifact_id=artifact_id,
                artifact_readiness="MISSING",
            )
        )

    nodes.extend(
        [
            node(
                "H9.physical_registry",
                "ALL",
                "NOT_TESTABLE",
                "PHYSICAL_REGISTRY",
                "L1_PHYSICAL_TARGET",
                parents=(
                    "H1.frontier_occurrence_registry_totality",
                    "H9.literal_weight_registry",
                    "H9.phase_cell_registry",
                    "H9.endpoint_registry",
                    "H9.normalization_registry",
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H2.literal_weight_return",
                "ALL",
                "NOT_TESTABLE",
                "ARITHMETIC_TARGET",
                "L2_TARGET_POSITIVE",
                parents=(
                    "A157.literal_weight_interface",
                    "H9.literal_weight_registry",
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H2.phase_major_clause",
                "ALL",
                "NOT_TESTABLE",
                "ARITHMETIC_TARGET",
                "L2_TARGET_POSITIVE",
                parents=(
                    "A158.major_arc_interface",
                    "H9.phase_cell_registry",
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H2.phase_direct_clause",
                "ALL",
                "NOT_TESTABLE",
                "ARITHMETIC_TARGET",
                "L2_TARGET_POSITIVE",
                parents=(
                    "O161.direct_additive_twist_core",
                    "H9.phase_cell_registry",
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H2.phase_return",
                "ANY_CLAUSE",
                "NOT_TESTABLE",
                "ARITHMETIC_TARGET",
                "L2_TARGET_POSITIVE",
                clauses=(("H2.phase_major_clause",), ("H2.phase_direct_clause",)),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H4.endpoint_avoidance_clause",
                "ALL",
                "NOT_TESTABLE",
                "ARITHMETIC_TARGET",
                "L2_TARGET_POSITIVE",
                parents=(
                    "A159.almost_endpoint_prefix",
                    "H9.endpoint_registry",
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H4.endpoint_pointwise_clause",
                "ALL",
                "NOT_TESTABLE",
                "ARITHMETIC_TARGET",
                "L2_TARGET_POSITIVE",
                parents=(
                    "O161.bad_endpoint_pointwise_core",
                    "H9.endpoint_registry",
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H4.endpoint_return",
                "ANY_CLAUSE",
                "NOT_TESTABLE",
                "ARITHMETIC_TARGET",
                "L2_TARGET_POSITIVE",
                clauses=(
                    ("H4.endpoint_avoidance_clause",),
                    ("H4.endpoint_pointwise_clause",),
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H3.actual_packet_saving",
                "TARGET",
                "NOT_TESTABLE",
                "ARITHMETIC_TARGET",
                "L2_TARGET_POSITIVE",
                parents=(
                    "A160.weighted_abel_interface",
                    "H2.literal_weight_return",
                    "H2.phase_return",
                    "H4.endpoint_return",
                    "H9.normalization_registry",
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H5.complete_four_sign_return",
                "TARGET",
                "NOT_TESTABLE",
                "ARITHMETIC_TARGET",
                "L2_TARGET_POSITIVE",
                parents=(
                    "H3.actual_packet_saving",
                    "H1.frontier_occurrence_registry_totality",
                    "H9.physical_registry",
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H6.physical_cover",
                "ALL",
                "NOT_TESTABLE",
                "STRUCTURAL",
                "L1_STRUCTURAL_TARGET",
                parents=("H1.defect.D_cover",),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H7.fixed_h0_totality",
                "ALL",
                "NOT_TESTABLE",
                "STRUCTURAL",
                "L1_STRUCTURAL_TARGET",
                parents=("H1.defect.D_P",),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "H8.final_reconnection",
                "ALL",
                "NOT_TESTABLE",
                "STRUCTURAL",
                "L1_STRUCTURAL_TARGET",
                parents=(
                    "H1.defect.D_rec",
                    "H6.physical_cover",
                    "H7.fixed_h0_totality",
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
            node(
                "ROOT.selected_map_synthesis",
                "ALL",
                "NOT_TESTABLE",
                "ROOT",
                "L2_TARGET_POSITIVE",
                parents=(
                    "H1.map_clause",
                    "H2.literal_weight_return",
                    "H2.phase_return",
                    "H3.actual_packet_saving",
                    "H4.endpoint_return",
                    "H5.complete_four_sign_return",
                    "H6.physical_cover",
                    "H7.fixed_h0_totality",
                    "H8.final_reconnection",
                    "H9.physical_registry",
                ),
                artifact_readiness="BLOCKED_BY_PARENT",
            ),
        ]
    )
    return nodes


def node_map(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["node_id"]: item for item in nodes}


def dependencies(item: dict[str, Any]) -> list[str]:
    deps = list(item["parents"])
    for clause in item["clauses"]:
        deps.extend(clause)
    return sorted(set(deps))


def validate_dag(nodes: list[dict[str, Any]]) -> None:
    by_id = node_map(nodes)
    require(len(by_id) == len(nodes), "duplicate DAG node id")
    for item in nodes:
        require(item["status"] in STATUSES, f"invalid status for {item['node_id']}")
        require(item["node_type"] in NODE_TYPES, f"invalid node type for {item['node_id']}")
        require(
            item["artifact_readiness"] in READINESS,
            f"invalid readiness for {item['node_id']}",
        )
        for parent in dependencies(item):
            require(parent in by_id, f"unknown parent {parent} in {item['node_id']}")
        if item["node_type"] == "ALL":
            require(bool(item["parents"]) and not item["clauses"], "ill-typed ALL node")
        if item["node_type"] == "ANY_CLAUSE":
            require(
                not item["parents"] and len(item["clauses"]) >= 2,
                "ill-typed ANY_CLAUSE node",
            )
        if item["node_type"] in {"EVIDENCE", "TARGET", "SCOPED_STOP"}:
            require(not item["clauses"], "non-composite node has clauses")

    visiting: set[str] = set()
    done: set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in done:
            return
        require(node_id not in visiting, f"cycle at {node_id}")
        visiting.add(node_id)
        for parent in dependencies(by_id[node_id]):
            visit(parent)
        visiting.remove(node_id)
        done.add(node_id)

    for node_id in sorted(by_id):
        visit(node_id)

    for item in nodes:
        if item["node_type"] == "ALL":
            parent_statuses = [by_id[p]["status"] for p in item["parents"]]
            derived = (
                "PROVED"
                if all(status == "PROVED" for status in parent_statuses)
                else "NOT_TESTABLE"
                if any(status == "NOT_TESTABLE" for status in parent_statuses)
                else "OPEN"
                if any(status == "OPEN" for status in parent_statuses)
                else "STOPPED"
            )
            require(
                item["status"] == derived,
                f"ALL status mismatch for {item['node_id']}: {item['status']} != {derived}",
            )
        elif item["node_type"] == "ANY_CLAUSE":
            clause_statuses: list[str] = []
            for clause in item["clauses"]:
                statuses = [by_id[p]["status"] for p in clause]
                clause_statuses.append(
                    "PROVED"
                    if all(status == "PROVED" for status in statuses)
                    else "NOT_TESTABLE"
                    if any(status == "NOT_TESTABLE" for status in statuses)
                    else "OPEN"
                    if any(status == "OPEN" for status in statuses)
                    else "STOPPED"
                )
            derived = (
                "PROVED"
                if "PROVED" in clause_statuses
                else "NOT_TESTABLE"
                if "NOT_TESTABLE" in clause_statuses
                else "OPEN"
                if "OPEN" in clause_statuses
                else "STOPPED"
            )
            require(
                item["status"] == derived,
                f"ANY_CLAUSE status mismatch for {item['node_id']}",
            )


def ancestors(nodes: list[dict[str, Any]], start: str) -> set[str]:
    by_id = node_map(nodes)
    result: set[str] = set()
    stack = list(dependencies(by_id[start]))
    while stack:
        current = stack.pop()
        if current in result:
            continue
        result.add(current)
        stack.extend(dependencies(by_id[current]))
    return result


def nt_blockers(nodes: list[dict[str, Any]], start: str) -> set[str]:
    """Return minimal unavailable artifacts for a fixed ALL/target route."""

    by_id = node_map(nodes)
    memo: dict[str, set[str]] = {}

    def recurse(node_id: str) -> set[str]:
        if node_id in memo:
            return set(memo[node_id])
        item = by_id[node_id]
        if item["status"] != "NOT_TESTABLE":
            memo[node_id] = set()
            return set()
        if item["artifact_readiness"] == "MISSING":
            memo[node_id] = {node_id}
            return {node_id}
        result: set[str] = set()
        for parent in dependencies(item):
            result.update(recurse(parent))
        if not result:
            result.add(node_id)
        memo[node_id] = result
        return set(result)

    return recurse(start)


def open_dependencies(nodes: list[dict[str, Any]], start: str) -> set[str]:
    by_id = node_map(nodes)
    result: set[str] = set()
    seen: set[str] = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        item = by_id[current]
        if item["status"] == "OPEN":
            result.add(current)
        stack.extend(dependencies(item))
    return result


def antichain_record(
    nodes: list[dict[str, Any]], route_id: str
) -> dict[str, Any]:
    return {
        "minimal_not_testable_nodes": sorted(nt_blockers(nodes, route_id)),
        "open_nodes": sorted(open_dependencies(nodes, route_id)),
        "route_id": route_id,
        "selection_rule": "MINIMAL_MISSING_ARTIFACT_ANCESTORS_THEN_NODE_ID",
    }


def parent_ready_open(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = node_map(nodes)
    ready: list[dict[str, Any]] = []
    for item in nodes:
        deps = dependencies(item)
        if (
            item["status"] == "OPEN"
            and item["artifact_readiness"] == "READY"
            and deps
            and all(by_id[parent]["status"] == "PROVED" for parent in deps)
        ):
            ready.append(
                {
                    "artifact_readiness": "READY",
                    "node_id": item["node_id"],
                    "parents": deps,
                    "parents_all_proved": True,
                    "scope_id": item["scope_id"],
                    "status": "OPEN",
                }
            )
    return sorted(ready, key=lambda item: item["node_id"])


def build_h1_completion(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = node_map(nodes)
    return {
        "defect_vector": list(NINE_DEFECTS),
        "defects": [
            {
                "defect_id": name,
                "evaluable": False,
                "node_id": f"H1.defect.{name}",
                "status": by_id[f"H1.defect.{name}"]["status"],
                "zero_proved": False,
            }
            for name in NINE_DEFECTS
        ],
        "map_clause": {
            "node_id": "H1.map_clause",
            "operator": "ALL",
            "status": by_id["H1.map_clause"]["status"],
        },
        "occurrence_registry": {
            "compressed_as_D_occ": False,
            "independent_from_defect_vector": True,
            "node_id": "H1.frontier_occurrence_registry_totality",
            "status": by_id["H1.frontier_occurrence_registry_totality"]["status"],
        },
        "scalar_clause": {
            "node_id": "H1.scalar_clause",
            "operator": "ALL",
            "status": by_id["H1.scalar_clause"]["status"],
        },
        "totalization": {
            "clauses": ["H1.map_clause", "H1.scalar_clause"],
            "node_id": "H1.frontier_totalization",
            "operator": "ANY_CLAUSE",
            "status": by_id["H1.frontier_totalization"]["status"],
        },
    }


def build_routes() -> list[dict[str, Any]]:
    return [
        {
            "first_missing": None,
            "route_id": "current_schema_only_canonical_lift",
            "scope": "CURRENT_ARTIFACTS_ONLY",
            "selected": False,
            "state": "STOP_SCOPED",
            "stopped": True,
        },
        {
            "first_missing": "H1.theorem_backed_occurrence_provenance_crosswalk",
            "route_id": "occurrence_augmented_map",
            "scope": "PRODUCTION_THEOREM_BACKED_CROSSWALK",
            "selected": True,
            "state": "OPEN_NOT_TESTABLE",
            "stopped": False,
        },
        {
            "first_missing": "H1.complete_FUM_scalar_oX",
            "route_id": "scalar_plus_ETO",
            "scope": "COMPLETE_ORIGINAL_SCALE_FUM_AND_ETO",
            "selected": False,
            "state": "OPEN_NOT_TESTABLE",
            "stopped": False,
        },
        {
            "first_missing": None,
            "route_id": "direct_additive_twist_core",
            "scope": "ACTUAL_PERIODIC_CORE_ONLY",
            "selected": False,
            "state": "OPEN_PARENT_READY",
            "stopped": False,
        },
        {
            "first_missing": None,
            "route_id": "bad_endpoint_pointwise_core",
            "scope": "ACTUAL_PREFIX_CORE_ONLY",
            "selected": False,
            "state": "OPEN_PARENT_READY",
            "stopped": False,
        },
    ]


def build_firewall(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    by_id = node_map(nodes)
    transitive = sorted(ancestors(nodes, "H9.physical_registry"))
    arithmetic = [
        node_id for node_id in transitive if by_id[node_id]["role"] in ARITHMETIC_ROLES
    ]
    return {
        "arithmetic_ancestor_ids": arithmetic,
        "arithmetic_roles": sorted(ARITHMETIC_ROLES),
        "firewall_pass": not arithmetic,
        "policy": "H9_MUST_HAVE_NO_DIRECT_OR_TRANSITIVE_ARITHMETIC_ANCESTOR",
        "root_node": "H9.physical_registry",
        "transitive_ancestor_ids": transitive,
    }


def build_endpoint_ledger() -> dict[str, Any]:
    charges = [
        {
            "charge_id": "ARITH.correlation_log_saving",
            "owner_ledger": "arithmetic",
            "quantity_kind": "LOG_AMPLITUDE_SAVING",
            "state": "PROVED",
            "value": "(log X)^(-kappa_0+o(1))",
        },
        {
            "charge_id": "ARITH.dyadic_shadow",
            "owner_ledger": "arithmetic",
            "quantity_kind": "LOG_EXCEPTIONAL_MEASURE",
            "state": "PROVED",
            "value": "(log X)^(-kappa_0+o(1))",
        },
        {
            "charge_id": "PHYS.good_variation",
            "owner_ledger": "physical",
            "quantity_kind": "LOG_AMPLITUDE_COST",
            "state": "NOT_TESTABLE",
            "value": None,
        },
        {
            "charge_id": "PHYS.bad_variation",
            "owner_ledger": "physical",
            "quantity_kind": "ATOMIC_ENDPOINT_COST",
            "state": "NOT_TESTABLE",
            "value": None,
        },
        {
            "charge_id": "PHYS.phase_return",
            "owner_ledger": "physical",
            "quantity_kind": "PHASE_RETURN_COST",
            "state": "NOT_TESTABLE",
            "value": None,
        },
        {
            "charge_id": "PHYS.four_sign_reconnection",
            "owner_ledger": "physical",
            "quantity_kind": "RECONNECTION_COST",
            "state": "NOT_TESTABLE",
            "value": None,
        },
    ]
    return {
        "charge_registry": charges,
        "contract": "MVP1_FIXED_H0_NON_DUPLICATING_ENDPOINT_V3",
        "invariants": {
            "each_charge_has_exactly_one_owner": True,
            "full_synthesis_references_not_recharges": True,
            "log_power_not_converted_to_X_power": True,
            "no_charge_id_repeated": True,
            "physical_loss_registry_complete": False,
        },
        "ledgers": {
            "arithmetic": {
                "charge_ids": [
                    "ARITH.correlation_log_saving",
                    "ARITH.dyadic_shadow",
                ],
                "fixed_X_sigma": {"denominator": 1, "numerator": 0},
                "state": "INCOMPLETE",
            },
            "full_synthesis": {
                "charge_ids": [],
                "input_ledgers": ["arithmetic", "physical"],
                "net_fixed_X_slack": None,
                "state": "INCOMPLETE",
            },
            "physical": {
                "charge_ids": [
                    "PHYS.good_variation",
                    "PHYS.bad_variation",
                    "PHYS.phase_return",
                    "PHYS.four_sign_reconnection",
                ],
                "fixed_X_lambda_lower": None,
                "fixed_X_lambda_upper": None,
                "registry_complete": False,
                "state": "NOT_TESTABLE",
                "unknown_cost_policy": "UNKNOWN_IS_NOT_ZERO",
            },
        },
        "scale": "AMPLITUDE",
        "target": {
            "fixed_X_sigma_required": {"denominator": 400, "numerator": 1},
            "one_over_400_paid": False,
        },
    }


def validate_endpoint_ledger(ledger: dict[str, Any]) -> None:
    charges = ledger["charge_registry"]
    ids = [item["charge_id"] for item in charges]
    require(len(ids) == len(set(ids)), "duplicate endpoint charge id")
    require(
        set(ids) == EXPECTED_ENDPOINT_CHARGES,
        "canonical endpoint charge registry is incomplete or contains an extra id",
    )
    owners = {item["charge_id"]: item["owner_ledger"] for item in charges}
    seen: list[str] = []
    for ledger_id in ("arithmetic", "physical"):
        for charge_id in ledger["ledgers"][ledger_id]["charge_ids"]:
            require(charge_id in owners, f"unknown charge {charge_id}")
            require(owners[charge_id] == ledger_id, f"wrong owner for {charge_id}")
            seen.append(charge_id)
    require(sorted(seen) == sorted(ids), "not every endpoint charge used exactly once")
    require(
        ledger["ledgers"]["full_synthesis"]["charge_ids"] == [],
        "full synthesis recharged a child-ledger cost",
    )
    require(
        ledger["ledgers"]["arithmetic"]["fixed_X_sigma"]
        == {"numerator": 0, "denominator": 1},
        "log saving was promoted to a fixed-X power",
    )
    require(ledger["target"]["one_over_400_paid"] is False, "1/400 overclaim")
    require(
        ledger["invariants"]["physical_loss_registry_complete"] is False,
        "listed-charge contract was promoted to a complete physical registry",
    )


def build_manifest() -> dict[str, Any]:
    semantic_summary = validate_frozen_semantics()
    nodes = build_nodes()
    validate_dag(nodes)
    h1 = build_h1_completion(nodes)
    firewall = build_firewall(nodes)
    require(firewall["firewall_pass"], "H9 arithmetic firewall failed")
    endpoint = build_endpoint_ledger()
    validate_endpoint_ledger(endpoint)
    antichain_routes = (
        "H1.map_clause",
        "H1.scalar_clause",
        "H2.literal_weight_return",
        "H2.phase_major_clause",
        "H2.phase_direct_clause",
        "H4.endpoint_avoidance_clause",
        "H4.endpoint_pointwise_clause",
        "H9.physical_registry",
        "ROOT.selected_map_synthesis",
    )
    antichains = [antichain_record(nodes, route_id) for route_id in antichain_routes]
    ready_open = parent_ready_open(nodes)
    require(
        [item["node_id"] for item in ready_open]
        == [
            "O161.bad_endpoint_pointwise_core",
            "O161.direct_additive_twist_core",
        ],
        "parent-ready OPEN frontier drift",
    )

    return {
        "claim_boundary": {
            "all_deterministic_prefixes": False,
            "architecture_infeasible": False,
            "current_schema_stop_is_global": False,
            "fixed_X_positive_L2": False,
            "full_physical_H3": False,
            "one_over_400": False,
            "prime_pair_lower_bound": False,
            "production_occurrence_crosswalk": False,
            "production_phase_registry": False,
            "production_weight_registry": False,
            "source_hashes_are_theorem_evidence": False,
            "twin_prime_theorem": False,
        },
        "current_verdict": "NOT_TESTABLE",
        "endpoint_ledger_v3": endpoint,
        "first_missing": {
            "minimal_not_testable_nodes": [
                "H1.theorem_backed_occurrence_provenance_crosswalk"
            ],
            "node_id": "H1.theorem_backed_occurrence_provenance_crosswalk",
            "required_artifact_id": "artifact.theorem_backed_crosswalk",
            "route_id": "occurrence_augmented_map",
            "selection_rule": "SELECTED_ROUTE_THEN_MINIMAL_MISSING_ANCESTOR_THEN_NODE_ID",
            "status": "NOT_TESTABLE",
        },
        "h1_completion": h1,
        "h9_arithmetic_firewall": firewall,
        "imports": build_imports(),
        "minimal_not_testable_antichains": antichains,
        "nodes": nodes,
        "parent_ready_open_frontiers": ready_open,
        "progress_classification": {
            "actual_fixed_power_achieved": False,
            "actual_fixed_power_status": "NOT_PROVED",
            "actual_fixed_power_target_level": "L2_ACTUAL_POSITIVE",
            "current_schema_lift_route": "STOP_SCOPED",
            "new_positive_L2": False,
            "production_return_status": "NOT_TESTABLE",
            "strongest_arithmetic_export": "A159.almost_endpoint_prefix",
            "strongest_arithmetic_level": "L1_ACTUAL_PREFIX_ALMOST_ENDPOINT",
            "structural_shadow_level": "L1_STRUCTURAL",
        },
        "registries": build_registries(),
        "routes": build_routes(),
        "schema": MANIFEST_SCHEMA,
        "snapshot": {
            "date": "2026-07-28",
            "hash_mode": HASH_MODE,
            "selected_route": "occurrence_augmented_map",
            "source_hash_semantics": "INTEGRITY_ONLY",
            "source_range": "TPC-151--160",
        },
        "source_contract_summary": semantic_summary,
        "source_lock_policy": {
            "hash_semantics": "INTEGRITY_ONLY",
            "normalization": HASH_MODE,
            "source_hashes_prove_theorems": False,
        },
        "source_locks": build_source_locks(),
    }


def strict_object(properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "additionalProperties": False,
        "properties": properties,
        "required": list(properties),
        "type": "object",
    }


def string_array() -> dict[str, Any]:
    return {"items": {"type": "string"}, "type": "array"}


def manifest_schema() -> dict[str, Any]:
    registry_item = strict_object(
        {
            "description": {"type": "string"},
            "key": {"type": "string"},
            "source_ref": {"type": "string"},
            "status": {"enum": ["READY", "MISSING"]},
        }
    )
    source_lock = strict_object(
        {
            "canonical_utf8_lf_sha256": {
                "pattern": "^[0-9a-f]{64}$",
                "type": "string",
            },
            "kind": {"enum": ["SCRIPT", "OUTPUT"]},
            "paper": {"pattern": "^TPC-[0-9]+$", "type": "string"},
            "path": {"type": "string"},
            "source_id": {"type": "string"},
        }
    )
    import_item = strict_object(
        {
            "artifact_readiness": {"enum": sorted(READINESS)},
            "carrier_id": {"type": "string"},
            "evidence_level": {"type": "string"},
            "import_id": {"type": "string"},
            "normalization_id": {"type": "string"},
            "paper": {"type": "string"},
            "promotion_eligible": {"type": "boolean"},
            "role": {"type": "string"},
            "scope_id": {"type": "string"},
            "source_export_id": {"type": "string"},
            "status": {"enum": sorted(STATUSES)},
        }
    )
    node_item = strict_object(
        {
            "artifact_readiness": {"enum": sorted(READINESS)},
            "carrier_id": {"type": "string"},
            "clauses": {"items": string_array(), "type": "array"},
            "evidence_id": {"type": "string"},
            "node_id": {"type": "string"},
            "node_type": {"enum": sorted(NODE_TYPES)},
            "normalization_id": {"type": "string"},
            "parents": string_array(),
            "program_level": {"type": "string"},
            "required_artifact_id": {"type": "string"},
            "role": {"type": "string"},
            "scope_id": {"type": "string"},
            "status": {"enum": sorted(STATUSES)},
        }
    )
    route_item = strict_object(
        {
            "first_missing": {"type": ["string", "null"]},
            "route_id": {"type": "string"},
            "scope": {"type": "string"},
            "selected": {"type": "boolean"},
            "state": {"type": "string"},
            "stopped": {"type": "boolean"},
        }
    )
    defect_item = strict_object(
        {
            "defect_id": {"enum": list(NINE_DEFECTS)},
            "evaluable": {"type": "boolean"},
            "node_id": {"type": "string"},
            "status": {"enum": sorted(STATUSES)},
            "zero_proved": {"type": "boolean"},
        }
    )
    antichain_item = strict_object(
        {
            "minimal_not_testable_nodes": string_array(),
            "open_nodes": string_array(),
            "route_id": {"type": "string"},
            "selection_rule": {"type": "string"},
        }
    )
    frontier_item = strict_object(
        {
            "artifact_readiness": {"const": "READY"},
            "node_id": {"type": "string"},
            "parents": string_array(),
            "parents_all_proved": {"const": True},
            "scope_id": {"type": "string"},
            "status": {"const": "OPEN"},
        }
    )
    fraction = strict_object(
        {
            "denominator": {"minimum": 1, "type": "integer"},
            "numerator": {"type": "integer"},
        }
    )
    charge_item = strict_object(
        {
            "charge_id": {"type": "string"},
            "owner_ledger": {"enum": ["arithmetic", "physical"]},
            "quantity_kind": {"type": "string"},
            "state": {"enum": ["PROVED", "NOT_TESTABLE"]},
            "value": {"type": ["string", "null"]},
        }
    )
    source_summary = strict_object(
        {
            "tpc151_anchor": strict_object(
                {
                    "first_missing": {"type": "string"},
                    "new_positive_L2": {"const": False},
                    "status": {"const": "PASS"},
                }
            ),
            "tpc152_anchor": strict_object(
                {
                    "current_verdict": {"const": "NOT_TESTABLE"},
                    "first_missing": {"type": "string"},
                    "status": {"const": "PASS"},
                }
            ),
            "tpc153_shadow": strict_object(
                {
                    "production_census": strict_object(
                        {
                            "ELIGIBLE_TAIL_OPEN": {
                                "minimum": 0,
                                "type": "integer",
                            },
                            "FRONTIER_UNMAPPED": {
                                "minimum": 0,
                                "type": "integer",
                            },
                        }
                    ),
                    "status": {"const": "PROVED_L1_STRUCTURAL"},
                }
            ),
            "tpc154_current_schema_route": strict_object(
                {
                    "selected_augmented_route_stopped": {"const": False},
                    "status": {"const": "STOP_DECLARED_ROUTE"},
                }
            ),
            "tpc155_production_witness": strict_object(
                {
                    "present": {"const": False},
                    "status": {"const": "NOT_TESTABLE"},
                }
            ),
            "tpc156_h1_decision": strict_object(
                {
                    "current_verdict": {"const": "NOT_TESTABLE"},
                    "first_missing": {"type": "string"},
                }
            ),
            "tpc157_weight_interface": strict_object(
                {
                    "production_weight_registry": {"const": "NOT_TESTABLE"},
                    "status": {
                        "const": "PROVED_L1_ACTUAL_CORE_WEIGHT_INTERFACE"
                    },
                }
            ),
            "tpc158_phase_interface": strict_object(
                {
                    "production_phase_cell": {"const": "NOT_TESTABLE"},
                    "status": {"const": "PROVED_L1_ACTUAL_CORE_MAJOR_ARC"},
                }
            ),
            "tpc159_prefix": strict_object(
                {
                    "all_prefix": {"const": False},
                    "status": {
                        "const": "PROVED_L1_ACTUAL_PREFIX_ALMOST_ENDPOINT"
                    },
                }
            ),
            "tpc160_abel_interface": strict_object(
                {
                    "fixed_X_power_exponent": {"const": 0},
                    "production_endpoint_registry": {
                        "const": "NOT_TESTABLE"
                    },
                    "production_weight": {"const": "NOT_TESTABLE"},
                    "status": {
                        "const": "PROVED_L1_ACTUAL_WEIGHTED_ALMOST_ENDPOINT_INTERFACE"
                    },
                }
            ),
        }
    )
    schema = strict_object(
        {
            "claim_boundary": strict_object(
                {
                    key: {"type": "boolean"}
                    for key in (
                        "all_deterministic_prefixes",
                        "architecture_infeasible",
                        "current_schema_stop_is_global",
                        "fixed_X_positive_L2",
                        "full_physical_H3",
                        "one_over_400",
                        "prime_pair_lower_bound",
                        "production_occurrence_crosswalk",
                        "production_phase_registry",
                        "production_weight_registry",
                        "source_hashes_are_theorem_evidence",
                        "twin_prime_theorem",
                    )
                }
            ),
            "current_verdict": {"const": "NOT_TESTABLE"},
            "endpoint_ledger_v3": strict_object(
                {
                    "charge_registry": {"items": charge_item, "type": "array"},
                    "contract": {"type": "string"},
                    "invariants": strict_object(
                        {
                            "each_charge_has_exactly_one_owner": {"const": True},
                            "full_synthesis_references_not_recharges": {"const": True},
                            "log_power_not_converted_to_X_power": {"const": True},
                            "no_charge_id_repeated": {"const": True},
                            "physical_loss_registry_complete": {"const": False},
                        }
                    ),
                    "ledgers": strict_object(
                        {
                            "arithmetic": strict_object(
                                {
                                    "charge_ids": string_array(),
                                    "fixed_X_sigma": fraction,
                                    "state": {"type": "string"},
                                }
                            ),
                            "full_synthesis": strict_object(
                                {
                                    "charge_ids": string_array(),
                                    "input_ledgers": string_array(),
                                    "net_fixed_X_slack": {"type": "null"},
                                    "state": {"type": "string"},
                                }
                            ),
                            "physical": strict_object(
                                {
                                    "charge_ids": string_array(),
                                    "fixed_X_lambda_lower": {"type": "null"},
                                    "fixed_X_lambda_upper": {"type": "null"},
                                    "registry_complete": {"const": False},
                                    "state": {"type": "string"},
                                    "unknown_cost_policy": {"type": "string"},
                                }
                            ),
                        }
                    ),
                    "scale": {"const": "AMPLITUDE"},
                    "target": strict_object(
                        {
                            "fixed_X_sigma_required": fraction,
                            "one_over_400_paid": {"const": False},
                        }
                    ),
                }
            ),
            "first_missing": strict_object(
                {
                    "minimal_not_testable_nodes": string_array(),
                    "node_id": {"type": "string"},
                    "required_artifact_id": {"type": "string"},
                    "route_id": {"type": "string"},
                    "selection_rule": {"type": "string"},
                    "status": {"const": "NOT_TESTABLE"},
                }
            ),
            "h1_completion": strict_object(
                {
                    "defect_vector": string_array(),
                    "defects": {"items": defect_item, "type": "array"},
                    "map_clause": strict_object(
                        {
                            "node_id": {"type": "string"},
                            "operator": {"const": "ALL"},
                            "status": {"type": "string"},
                        }
                    ),
                    "occurrence_registry": strict_object(
                        {
                            "compressed_as_D_occ": {"const": False},
                            "independent_from_defect_vector": {"const": True},
                            "node_id": {"type": "string"},
                            "status": {"type": "string"},
                        }
                    ),
                    "scalar_clause": strict_object(
                        {
                            "node_id": {"type": "string"},
                            "operator": {"const": "ALL"},
                            "status": {"type": "string"},
                        }
                    ),
                    "totalization": strict_object(
                        {
                            "clauses": string_array(),
                            "node_id": {"type": "string"},
                            "operator": {"const": "ANY_CLAUSE"},
                            "status": {"type": "string"},
                        }
                    ),
                }
            ),
            "h9_arithmetic_firewall": strict_object(
                {
                    "arithmetic_ancestor_ids": string_array(),
                    "arithmetic_roles": string_array(),
                    "firewall_pass": {"const": True},
                    "policy": {"type": "string"},
                    "root_node": {"type": "string"},
                    "transitive_ancestor_ids": string_array(),
                }
            ),
            "imports": {"items": import_item, "type": "array"},
            "minimal_not_testable_antichains": {
                "items": antichain_item,
                "type": "array",
            },
            "nodes": {"items": node_item, "type": "array"},
            "parent_ready_open_frontiers": {
                "items": frontier_item,
                "type": "array",
            },
            "progress_classification": strict_object(
                {
                    "actual_fixed_power_achieved": {"const": False},
                    "actual_fixed_power_status": {"const": "NOT_PROVED"},
                    "actual_fixed_power_target_level": {"type": "string"},
                    "current_schema_lift_route": {"const": "STOP_SCOPED"},
                    "new_positive_L2": {"const": False},
                    "production_return_status": {"const": "NOT_TESTABLE"},
                    "strongest_arithmetic_export": {"type": "string"},
                    "strongest_arithmetic_level": {"type": "string"},
                    "structural_shadow_level": {"type": "string"},
                }
            ),
            "registries": strict_object(
                {
                    "artifacts": {"items": registry_item, "type": "array"},
                    "carriers": {"items": registry_item, "type": "array"},
                    "normalizations": {"items": registry_item, "type": "array"},
                    "scopes": {"items": registry_item, "type": "array"},
                }
            ),
            "routes": {"items": route_item, "type": "array"},
            "schema": {"const": MANIFEST_SCHEMA},
            "snapshot": strict_object(
                {
                    "date": {"type": "string"},
                    "hash_mode": {"const": HASH_MODE},
                    "selected_route": {"type": "string"},
                    "source_hash_semantics": {"const": "INTEGRITY_ONLY"},
                    "source_range": {"type": "string"},
                }
            ),
            "source_contract_summary": source_summary,
            "source_lock_policy": strict_object(
                {
                    "hash_semantics": {"const": "INTEGRITY_ONLY"},
                    "normalization": {"const": HASH_MODE},
                    "source_hashes_prove_theorems": {"const": False},
                }
            ),
            "source_locks": {"items": source_lock, "type": "array"},
        }
    )
    schema.update(
        {
            "$id": "https://example.invalid/tpc161-occurrence-return-manifest.schema.json",
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "TPC-161 source-locked occurrence-return integration manifest",
        }
    )
    return schema


def audit_schema() -> dict[str, Any]:
    bool_checks = (
        "all_source_locks_valid",
        "claim_boundary_intact",
        "clause_wise_antichains_exact",
        "current_schema_stop_scoped",
        "endpoint_v3_nonduplicating",
        "h1_map_scalar_separated",
        "h9_transitive_firewall_pass",
        "nine_defects_registry_independent",
        "parent_ready_open_frontiers_exact",
        "source_contracts_valid",
        "strict_schemas",
        "strongest_arithmetic_export_exact",
        "typed_dag_acyclic",
    )
    mutation_checks = (
        "reject_bad_endpoint_scope_mismatch",
        "reject_crosswalk_promotion",
        "reject_defect_omission",
        "reject_duplicate_endpoint_charge",
        "reject_evidence_status_mismatch",
        "reject_endpoint_charge_omission",
        "reject_h9_arithmetic_ancestor",
        "reject_log_to_X_power_conversion",
        "reject_minor_projection_scope_mismatch",
        "reject_occurrence_registry_compression",
        "reject_one_over_400_claim",
        "reject_positive_L2_claim",
        "reject_shadow_as_actual_lift",
        "reject_source_hash_as_theorem",
    )
    schema = strict_object(
        {
            "checks": strict_object({key: {"const": True} for key in bool_checks}),
            "claim_boundary": strict_object(
                {
                    "fixed_X_positive_L2": {"const": False},
                    "full_physical_H3": {"const": False},
                    "one_over_400": {"const": False},
                    "prime_pair_lower_bound": {"const": False},
                    "twin_prime_theorem": {"const": False},
                }
            ),
            "current_verdict": {"const": "NOT_TESTABLE"},
            "first_missing": {"type": "string"},
            "manifest_sha256": {
                "pattern": "^[0-9a-f]{64}$",
                "type": "string",
            },
            "mutation_regressions": strict_object(
                {key: {"const": True} for key in mutation_checks}
            ),
            "schema": {"const": AUDIT_SCHEMA},
            "status": {"const": "PASS"},
        }
    )
    schema.update(
        {
            "$id": "https://example.invalid/tpc161-occurrence-return-audit.schema.json",
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "TPC-161 occurrence-return integration audit",
        }
    )
    return schema


def assert_schema_strict(schema: Any) -> None:
    if isinstance(schema, dict):
        if schema.get("type") == "object":
            require(
                schema.get("additionalProperties") is False,
                "object schema is not strict",
            )
            require(
                set(schema.get("required", []))
                == set(schema.get("properties", {}).keys()),
                "strict schema does not require every declared property",
            )
        for value in schema.values():
            assert_schema_strict(value)
    elif isinstance(schema, list):
        for value in schema:
            assert_schema_strict(value)


def validate_manifest_shape(manifest: dict[str, Any], schema: dict[str, Any]) -> None:
    require(
        set(manifest) == set(schema["properties"]),
        "manifest top-level keys violate strict schema",
    )
    require(manifest["schema"] == MANIFEST_SCHEMA, "manifest schema mismatch")
    require(manifest["current_verdict"] == "NOT_TESTABLE", "verdict drift")
    require(
        manifest["first_missing"]["node_id"]
        == "H1.theorem_backed_occurrence_provenance_crosswalk",
        "first-missing drift",
    )
    registries = manifest["registries"]
    known = {
        name: {entry["key"] for entry in registries[name]}
        for name in ("artifacts", "carriers", "normalizations", "scopes")
    }
    import_ids = {item["import_id"] for item in manifest["imports"]}
    for item in manifest["imports"]:
        require(item["scope_id"] in known["scopes"], "unknown import scope")
        require(item["carrier_id"] in known["carriers"], "unknown import carrier")
        require(
            item["normalization_id"] in known["normalizations"],
            "unknown import normalization",
        )
    for item in manifest["nodes"]:
        require(item["scope_id"] in known["scopes"], "unknown node scope")
        require(item["carrier_id"] in known["carriers"], "unknown node carrier")
        require(
            item["normalization_id"] in known["normalizations"],
            "unknown node normalization",
        )
        require(
            item["required_artifact_id"] in known["artifacts"],
            "unknown node artifact",
        )
        require(
            item["evidence_id"] == "INTEGRATION_DERIVED"
            or item["evidence_id"] in import_ids,
            "unknown node evidence id",
        )
    imports_by_id = {item["import_id"]: item for item in manifest["imports"]}
    for item in manifest["nodes"]:
        if item["node_type"] == "EVIDENCE":
            require(
                item["evidence_id"] in imports_by_id
                and imports_by_id[item["evidence_id"]]["status"] == item["status"],
                f"evidence-status mismatch for {item['node_id']}",
            )
    validate_dag(manifest["nodes"])
    by_id = node_map(manifest["nodes"])
    require(
        by_id["H1.theorem_backed_occurrence_provenance_crosswalk"]["status"]
        == "NOT_TESTABLE"
        and by_id["H1.theorem_backed_occurrence_provenance_crosswalk"][
            "artifact_readiness"
        ]
        == "MISSING",
        "production crosswalk was promoted",
    )
    require(
        by_id["H1.frontier_occurrence_lift"]["status"] == "NOT_TESTABLE",
        "cut shadow was promoted to an actual occurrence lift",
    )
    require(
        by_id["O161.bad_endpoint_pointwise_core"]["scope_id"]
        == "scope.actual_core_bad_endpoint"
        and by_id["O161.bad_endpoint_pointwise_core"]["required_artifact_id"]
        == "artifact.periodic_actual_core",
        "bad-endpoint target has an outside-shadow scope or artifact",
    )
    require(
        by_id["N158.small_period_projection_route"]["scope_id"]
        == "scope.actual_core_minor_projection_obstruction"
        and by_id["N158.small_period_projection_route"][
            "required_artifact_id"
        ]
        == "artifact.phase_projection_obstruction",
        "small-period projection stop has a major-arc scope",
    )
    validate_endpoint_ledger(manifest["endpoint_ledger_v3"])
    require(
        manifest["h1_completion"]["defect_vector"] == list(NINE_DEFECTS),
        "nine-defect vector drift",
    )
    require(
        manifest["h1_completion"]["occurrence_registry"][
            "independent_from_defect_vector"
        ]
        and not manifest["h1_completion"]["occurrence_registry"][
            "compressed_as_D_occ"
        ],
        "occurrence registry compressed into defect vector",
    )
    require(
        manifest["h9_arithmetic_firewall"]["firewall_pass"]
        and not manifest["h9_arithmetic_firewall"]["arithmetic_ancestor_ids"],
        "H9 arithmetic firewall failed",
    )
    require(
        manifest["progress_classification"]["strongest_arithmetic_export"]
        == "A159.almost_endpoint_prefix"
        and manifest["progress_classification"]["new_positive_L2"] is False,
        "progress classifier drift",
    )
    require(
        not any(manifest["claim_boundary"].values()),
        "claim boundary contains an unsupported promotion",
    )


def mutation_regressions(manifest: dict[str, Any]) -> dict[str, bool]:
    def rejected(mutator: Any) -> bool:
        candidate = copy.deepcopy(manifest)
        mutator(candidate)
        try:
            validate_manifest_shape(candidate, manifest_schema())
        except (ValueError, KeyError):
            return True
        return False

    def set_node(candidate: dict[str, Any], node_id: str, field: str, value: Any) -> None:
        for item in candidate["nodes"]:
            if item["node_id"] == node_id:
                item[field] = value
                return
        raise KeyError(node_id)

    return {
        "reject_bad_endpoint_scope_mismatch": rejected(
            lambda c: set_node(
                c,
                "O161.bad_endpoint_pointwise_core",
                "scope_id",
                "scope.actual_core_prefix_outside_shadow",
            )
        ),
        "reject_crosswalk_promotion": rejected(
            lambda c: set_node(
                c,
                "H1.theorem_backed_occurrence_provenance_crosswalk",
                "status",
                "PROVED",
            )
        ),
        "reject_defect_omission": rejected(
            lambda c: c["h1_completion"]["defect_vector"].remove("D_GP")
        ),
        "reject_duplicate_endpoint_charge": rejected(
            lambda c: c["endpoint_ledger_v3"]["ledgers"]["physical"][
                "charge_ids"
            ].append("ARITH.correlation_log_saving")
        ),
        "reject_evidence_status_mismatch": rejected(
            lambda c: set_node(
                c,
                "D156.h1_typed_contract",
                "evidence_id",
                "I156.h1_crosswalk_decision",
            )
        ),
        "reject_endpoint_charge_omission": rejected(
            lambda c: (
                c["endpoint_ledger_v3"]["charge_registry"].pop(0),
                c["endpoint_ledger_v3"]["ledgers"]["arithmetic"]["charge_ids"].pop(
                    0
                ),
            )
        ),
        "reject_h9_arithmetic_ancestor": rejected(
            lambda c: c["h9_arithmetic_firewall"]["arithmetic_ancestor_ids"].append(
                "A159.almost_endpoint_prefix"
            )
        ),
        "reject_log_to_X_power_conversion": rejected(
            lambda c: c["endpoint_ledger_v3"]["ledgers"]["arithmetic"][
                "fixed_X_sigma"
            ].update({"numerator": 1})
        ),
        "reject_minor_projection_scope_mismatch": rejected(
            lambda c: set_node(
                c,
                "N158.small_period_projection_route",
                "scope_id",
                "scope.actual_core_major_arc",
            )
        ),
        "reject_occurrence_registry_compression": rejected(
            lambda c: c["h1_completion"]["occurrence_registry"].update(
                {"compressed_as_D_occ": True}
            )
        ),
        "reject_one_over_400_claim": rejected(
            lambda c: c["claim_boundary"].update({"one_over_400": True})
        ),
        "reject_positive_L2_claim": rejected(
            lambda c: c["progress_classification"].update(
                {"new_positive_L2": True}
            )
        ),
        "reject_shadow_as_actual_lift": rejected(
            lambda c: set_node(
                c,
                "H1.frontier_occurrence_lift",
                "status",
                "PROVED",
            )
        ),
        "reject_source_hash_as_theorem": rejected(
            lambda c: c["claim_boundary"].update(
                {"source_hashes_are_theorem_evidence": True}
            )
        ),
    }


def build_audit(
    manifest: dict[str, Any],
    manifest_text: str,
    m_schema: dict[str, Any],
    a_schema: dict[str, Any],
) -> dict[str, Any]:
    validate_manifest_shape(manifest, m_schema)
    assert_schema_strict(m_schema)
    assert_schema_strict(a_schema)
    mutations = mutation_regressions(manifest)
    require(all(mutations.values()), "a mutation regression was not rejected")
    antichain_lookup = {
        item["route_id"]: item for item in manifest["minimal_not_testable_antichains"]
    }
    require(
        antichain_lookup["H1.map_clause"]["minimal_not_testable_nodes"]
        == ["H1.theorem_backed_occurrence_provenance_crosswalk"],
        "map-clause antichain drift",
    )
    require(
        antichain_lookup["H1.scalar_clause"]["minimal_not_testable_nodes"]
        == [
            "H1.complete_FUM_scalar_oX",
            "H1.theorem_backed_ETO_disposition",
        ],
        "scalar-clause antichain drift",
    )
    return {
        "checks": {
            "all_source_locks_valid": all(
                canonical_source_hash(REPO_DIR / item["path"])
                == item["canonical_utf8_lf_sha256"]
                for item in manifest["source_locks"]
            ),
            "claim_boundary_intact": not any(manifest["claim_boundary"].values()),
            "clause_wise_antichains_exact": True,
            "current_schema_stop_scoped": (
                manifest["progress_classification"]["current_schema_lift_route"]
                == "STOP_SCOPED"
                and not manifest["claim_boundary"]["current_schema_stop_is_global"]
            ),
            "endpoint_v3_nonduplicating": True,
            "h1_map_scalar_separated": (
                manifest["h1_completion"]["map_clause"]["node_id"]
                != manifest["h1_completion"]["scalar_clause"]["node_id"]
            ),
            "h9_transitive_firewall_pass": manifest["h9_arithmetic_firewall"][
                "firewall_pass"
            ],
            "nine_defects_registry_independent": (
                len(manifest["h1_completion"]["defect_vector"]) == 9
                and manifest["h1_completion"]["occurrence_registry"][
                    "independent_from_defect_vector"
                ]
            ),
            "parent_ready_open_frontiers_exact": (
                len(manifest["parent_ready_open_frontiers"]) == 2
            ),
            "source_contracts_valid": True,
            "strict_schemas": True,
            "strongest_arithmetic_export_exact": (
                manifest["progress_classification"]["strongest_arithmetic_export"]
                == "A159.almost_endpoint_prefix"
            ),
            "typed_dag_acyclic": True,
        },
        "claim_boundary": {
            "fixed_X_positive_L2": False,
            "full_physical_H3": False,
            "one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "current_verdict": "NOT_TESTABLE",
        "first_missing": "H1.theorem_backed_occurrence_provenance_crosswalk",
        "manifest_sha256": sha256_bytes(manifest_text.encode("utf-8")),
        "mutation_regressions": mutations,
        "schema": AUDIT_SCHEMA,
        "status": "PASS",
    }


def compare_or_write(path: Path, text: str, check: bool) -> None:
    if check:
        if not path.is_file():
            raise SystemExit(f"MISSING: {path}")
        actual = normalize_lf(path.read_text(encoding="utf-8"))
        if actual != text:
            raise SystemExit(f"DRIFT: {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed deterministic artifacts without rewriting",
    )
    args = parser.parse_args()

    manifest = build_manifest()
    m_schema = manifest_schema()
    a_schema = audit_schema()
    manifest_text = canonical_json(manifest)
    audit = build_audit(manifest, manifest_text, m_schema, a_schema)
    audit_text = canonical_json(audit)

    outputs = (
        (MANIFEST_SCHEMA_PATH, canonical_json(m_schema)),
        (AUDIT_SCHEMA_PATH, canonical_json(a_schema)),
        (MANIFEST_PATH, manifest_text),
        (AUDIT_PATH, audit_text),
    )
    for path, text in outputs:
        compare_or_write(path, text, args.check)

    print(
        canonical_json(
            {
                "audit_sha256": sha256_bytes(audit_text.encode("utf-8")),
                "check_mode": args.check,
                "current_verdict": audit["current_verdict"],
                "first_missing": audit["first_missing"],
                "manifest_sha256": audit["manifest_sha256"],
                "status": audit["status"],
            }
        ),
        end="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
