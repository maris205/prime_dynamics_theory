#!/usr/bin/env python3
"""Generate and verify the TPC-172/MVP7 dynamic route decision."""

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
REPO = PAPERS.parent
SNAPSHOT = HERE / "tpc172_mvp7_snapshot.json"
AUDIT = HERE / "tpc172_mvp7_route_audit.json"
SNAPSHOT_SCHEMA = PAPER / "schemas" / "tpc172-mvp7-snapshot-v1.schema.json"
AUDIT_SCHEMA = PAPER / "schemas" / "tpc172-mvp7-audit-v1.schema.json"
HASH_MODE = "CANONICAL_UTF8_LF_V2"
SOURCE_LOCKED = "SOURCE_LOCKED"
SYNTHETIC = "SYNTHETIC_REACHABILITY"
ORDERED_VALID_VERDICTS = [
    "GO",
    "ARCHITECTURE_INFEASIBLE",
    "REROUTE",
    "STOP_ROUTE",
    "NOT_TESTABLE",
    "ARITHMETIC_FRONTIER",
    "OPEN",
]

REQUIRED_BLOCKERS = [
    "H1.source_backed_local_occurrence_edge_family",
    "H1.actual_active_support_certificate",
    "H1.canonical_minimal_representation_certificate",
    "H9.literal_weight_registry",
    "H9.phase_cell_registry",
    "H9.endpoint_registry",
    "H9.normalization_registry",
]
REQUIRED_OPEN = [
    "O161.bad_endpoint_pointwise_fixed_atom",
    "O161.direct_additive_twist_fixed_atom",
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_bytes(path: Path) -> bytes:
    text = normalize_lf(path.read_text(encoding="utf-8"))
    if path.suffix == ".json":
        text = canonical_json(json.loads(text))
    elif not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def payload_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def paper_dir(number: int) -> Path:
    matches = sorted(path for path in PAPERS.glob(f"tpc-{number}-*") if path.is_dir())
    if len(matches) != 1:
        raise FileNotFoundError(
            f"expected exactly one TPC-{number} directory; found {len(matches)}"
        )
    return matches[0]


def repo_relative(path: Path) -> str:
    return path.resolve().relative_to(REPO.resolve()).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(normalize_lf(path.read_text(encoding="utf-8")))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def source_record(
    source_id: str,
    path: Path,
    *,
    claim_type: str,
    scope_id: str,
    from_route: str | None = None,
    to_route: str | None = None,
    statement: str,
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "evidence_kind": "SOURCE_LOCKED_ROUTE_RESULT",
        "proof_semantics": "SCOPED_SOURCE_RESULT",
        "claim_type": claim_type,
        "scope_id": scope_id,
        "from_route": from_route,
        "to_route": to_route,
        "path": repo_relative(path),
        "canonical_utf8_lf_sha256": sha256(path),
        "statement": statement,
    }


def source_lock(source_id: str, path: Path, kind: str) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "path": repo_relative(path),
        "kind": kind,
        "canonical_utf8_lf_sha256": sha256(path),
        "hash_semantics": "INTEGRITY_ONLY",
    }


def production_evidence_registry() -> dict[str, dict[str, Any]]:
    tpc154 = (
        paper_dir(154)
        / "experiments"
        / "tpc154_completion_fiber_obstruction_certificate.json"
    )
    tpc170 = (
        paper_dir(170)
        / "experiments"
        / "tpc170_metric_corridor_audit.json"
    )
    payload154 = load_json(tpc154)
    payload170 = load_json(tpc170)
    if (
        payload154.get("status") != "PASS"
        or payload154.get("theorem_exports", {}).get(
            "H1.current_artifacts_only_canonical_actual_lift"
        )
        != "STOP_DECLARED_ROUTE"
        or payload154.get("obstruction_scope", {}).get(
            "stopped_route"
        )
        != "CURRENT_ARTIFACTS_ONLY_CANONICAL_ACTUAL_LIFT_DERIVATION"
        or payload154.get("obstruction_scope", {}).get(
            "actual_carrier_impossibility_proved"
        )
        is not False
    ):
        raise ValueError("TPC-154 route-stop payload drift")
    atom170 = payload170.get("fixed_atom_stop", {})
    if (
        payload170.get("status") != "PASS"
        or atom170.get("status")
        != "PROVED_SCOPED_METRIC_TO_ATOM_NONIMPLICATION"
        or atom170.get("quantifier_proved") != "LEBESGUE_AE_FIXED_PHASE"
        or atom170.get("quantifier_not_proved")
        != "NAMED_FIXED_ATOM_OR_SCALE_DEPENDENT_SELECTOR"
        or atom170.get("not_a_literal_mobius_lower_bound") is not True
    ):
        raise ValueError("TPC-170 arithmetic scoped-stop payload drift")
    return {
        "TPC154.current_schema_only_lift": source_record(
            "TPC154.current_schema_only_lift",
            tpc154,
            claim_type="ARCHITECTURE_ROUTE_CELL_STOP",
            scope_id="CURRENT_ARCHIVE_FIELDS_ONLY",
            from_route="current_schema_only_canonical_lift",
            statement=(
                "Only canonical actual-lift recovery from the current archive "
                "fields is stopped."
            ),
        ),
        "TPC170.uncontrolled_atomic_promotion": source_record(
            "TPC170.uncontrolled_atomic_promotion",
            tpc170,
            claim_type="ARITHMETIC_METHOD_SCOPED_STOP",
            scope_id="UNCONTROLLED_ATOMIC_PROMOTION_ONLY",
            from_route="phase_metric_uncontrolled_atomic",
            statement=(
                "Metric almost-every-phase control does not imply control on an "
                "arbitrary atomic registry."
            ),
        ),
    }


def find_171_files() -> dict[str, Path]:
    directory = paper_dir(171)
    files = {
        "script": directory / "experiments" / "tpc171_source_locked_integration.py",
        "manifest": directory / "experiments" / "tpc171_integration_manifest.json",
        "audit": directory / "experiments" / "tpc171_integration_audit.json",
        "manifest_schema": directory
        / "schemas"
        / "tpc171-integration-manifest-v1.schema.json",
        "audit_schema": directory
        / "schemas"
        / "tpc171-integration-audit-v1.schema.json",
        "main": directory / "main.tex",
    }
    if any(not path.is_file() for path in files.values()):
        raise FileNotFoundError("TPC-171 bundle is incomplete")
    return files


def expected_snapshot_source_locks() -> list[dict[str, Any]]:
    files171 = find_171_files()
    tpc154 = (
        paper_dir(154)
        / "experiments"
        / "tpc154_completion_fiber_obstruction_certificate.json"
    )
    tpc170 = (
        paper_dir(170)
        / "experiments"
        / "tpc170_metric_corridor_audit.json"
    )
    return [
        source_lock("TPC171.integration_script", files171["script"], "SCRIPT"),
        source_lock("TPC171.manifest", files171["manifest"], "OUTPUT"),
        source_lock("TPC171.audit", files171["audit"], "OUTPUT"),
        source_lock("TPC171.manifest_schema", files171["manifest_schema"], "SCHEMA"),
        source_lock("TPC171.audit_schema", files171["audit_schema"], "SCHEMA"),
        source_lock("TPC171.main", files171["main"], "LATEX"),
        source_lock("TPC154.route_stop", tpc154, "OUTPUT"),
        source_lock("TPC170.atomic_stop", tpc170, "OUTPUT"),
    ]


def rational(value: dict[str, Any]) -> Fraction:
    if set(value) != {"numerator", "denominator"}:
        raise ValueError("rational fields drift")
    denominator = value["denominator"]
    numerator = value["numerator"]
    if (
        not isinstance(numerator, int)
        or not isinstance(denominator, int)
        or denominator <= 0
    ):
        raise ValueError("invalid rational")
    return Fraction(numerator, denominator)


def validate_evidence_registry(
    state: dict[str, Any], mode: str, *, verify_files: bool
) -> None:
    registry = state["classifier_evidence_registry"]
    if not isinstance(registry, dict):
        raise ValueError("classifier evidence registry is not an object")
    used: set[str] = set()

    architecture = state["route_families"]["architecture"]
    for route_id, route in architecture["records"].items():
        source_id = route["source_export"]
        if not route["stopped"]:
            if source_id is not None:
                raise ValueError("open architecture route has stop evidence")
            continue
        if not source_id or source_id not in registry:
            raise ValueError("stopped architecture route lacks registered evidence")
        record = registry[source_id]
        used.add(source_id)
        if (
            record["claim_type"] != "ARCHITECTURE_ROUTE_CELL_STOP"
            or record["from_route"] != route_id
            or record["scope_id"] != route["scope_id"]
        ):
            raise ValueError("architecture stop evidence has wrong type or scope")

    completeness = architecture["universe_completeness"]
    if completeness["status"] == "PROVED":
        source_id = completeness["source_export"]
        if not source_id or source_id not in registry:
            raise ValueError("route completeness lacks registered evidence")
        record = registry[source_id]
        used.add(source_id)
        if (
            record["claim_type"] != "ARCHITECTURE_UNIVERSE_COMPLETENESS"
            or record["scope_id"] != completeness["scope"]
        ):
            raise ValueError("wrong completeness evidence")
    elif completeness["source_export"] is not None:
        raise ValueError("unproved completeness has an evidence label")

    alternative = architecture["typed_alternative"]
    crosswalk = architecture["typed_alternative_crosswalk"]
    if alternative is not None:
        if alternative not in architecture["records"]:
            raise ValueError("typed alternative is not an architecture route")
        selected = architecture["selected_route"]
        if alternative == selected:
            raise ValueError("alternative equals selected route")
        if not crosswalk or crosswalk not in registry:
            raise ValueError("alternative lacks typed crosswalk")
        record = registry[crosswalk]
        used.add(crosswalk)
        selected_record = architecture["records"][selected]
        alternative_record = architecture["records"][alternative]
        if (
            record["claim_type"] != "ARCHITECTURE_ROUTE_CROSSWALK"
            or record["from_route"] != selected
            or record["to_route"] != alternative
            or selected_record["route_kind"] != "ARCHITECTURE_ROUTE"
            or alternative_record["route_kind"] != "ARCHITECTURE_ROUTE"
            or alternative_record["registry_id"] == selected_record["registry_id"]
            or not alternative_record["fresh_registry"]
        ):
            raise ValueError("invalid architecture reroute crosswalk")
    elif crosswalk is not None:
        raise ValueError("crosswalk supplied without an alternative")

    if mode == SOURCE_LOCKED:
        if registry != production_evidence_registry():
            raise ValueError("production classifier evidence registry drift")
        for source_id, record in registry.items():
            if (
                record["evidence_kind"] != "SOURCE_LOCKED_ROUTE_RESULT"
                or record["proof_semantics"] != "SCOPED_SOURCE_RESULT"
            ):
                raise ValueError("synthetic evidence entered production classifier")
            if verify_files:
                path = REPO / record["path"]
                if (
                    not path.is_file()
                    or sha256(path) != record["canonical_utf8_lf_sha256"]
                ):
                    raise ValueError("classifier evidence hash drift")
    elif mode == SYNTHETIC:
        for record in registry.values():
            if (
                record["evidence_kind"] != "SYNTHETIC_ASSUMED_PREDICATE"
                or record["proof_semantics"] != "NONE_SYNTHETIC_REACHABILITY_ONLY"
                or record["path"] is not None
                or record["canonical_utf8_lf_sha256"] is not None
            ):
                raise ValueError("source theorem evidence entered synthetic mode")
    else:
        raise ValueError("invalid classifier evidence mode")

    # Extra production records are permitted only when they describe the
    # arithmetic scoped stop; they may never be consumed as architecture proof.
    allowed_unused = {
        source_id
        for source_id, record in registry.items()
        if record["claim_type"] == "ARITHMETIC_METHOD_SCOPED_STOP"
    }
    if set(registry) - used - allowed_unused:
        raise ValueError("classifier evidence registry has unused records")


def validate_state(state: dict[str, Any], *, verify_files: bool = True) -> None:
    required = {
        "evidence_mode",
        "route_families",
        "typed_frontiers",
        "endpoint_state",
        "classifier_evidence_registry",
    }
    if set(state) != required:
        raise ValueError("classifier state fields drift")
    mode = state["evidence_mode"]
    route_families = state["route_families"]
    if set(route_families) != {"architecture", "arithmetic_subroutes"}:
        raise ValueError("route-family fields drift")
    architecture = route_families["architecture"]
    arithmetic = route_families["arithmetic_subroutes"]
    if sum(
        bool(record["selected"]) for record in architecture["records"].values()
    ) != 1:
        raise ValueError("architecture selection is not unique")
    selected = architecture["selected_route"]
    if (
        selected not in architecture["records"]
        or not architecture["records"][selected]["selected"]
    ):
        raise ValueError("selected architecture route drift")
    if any(
        record["route_kind"] != "ARCHITECTURE_ROUTE"
        for record in architecture["records"].values()
    ):
        raise ValueError("arithmetic subroute entered architecture universe")
    if any(
        record["route_kind"] != "ARITHMETIC_SUBROUTE"
        for record in arithmetic["records"].values()
    ):
        raise ValueError("architecture route entered arithmetic methods")
    if arithmetic["architecture_reroute_eligible"]:
        raise ValueError("arithmetic method made reroute eligible")
    for route in architecture["records"].values():
        if route["stopped"] != route["state"].startswith("STOP"):
            raise ValueError("route stopped/state mismatch")

    frontiers = state["typed_frontiers"]
    if set(frontiers) != {
        "minimal_not_testable_antichain",
        "parent_ready_open_frontier",
    }:
        raise ValueError("typed frontier fields drift")
    blockers = frontiers["minimal_not_testable_antichain"]
    opens = frontiers["parent_ready_open_frontier"]
    if len(blockers) != len(set(blockers)) or len(opens) != len(set(opens)):
        raise ValueError("duplicate frontier node")
    if set(blockers) & set(opens):
        raise ValueError("NOT_TESTABLE and OPEN frontiers merged")

    endpoint = state["endpoint_state"]
    required_endpoint = {
        "root_status",
        "all_active_requirements_proved",
        "structural_complete",
        "physical_registry_complete",
        "named_fixed_atom_proved",
        "deterministic_endpoint_proved",
        "all_remaining_open_are_positive_L2_arithmetic",
        "named_fixed_atom_sigma",
        "sigma_required",
        "physical_loss_upper",
        "strict_net_slack",
        "literal_gate_complete",
    }
    if set(endpoint) != required_endpoint:
        raise ValueError("endpoint classifier fields drift")
    sigma = rational(endpoint["named_fixed_atom_sigma"])
    required_sigma = rational(endpoint["sigma_required"])
    if required_sigma != Fraction(1, 400):
        raise ValueError("endpoint target is not 1/400")
    if endpoint["strict_net_slack"] is not None:
        slack = rational(endpoint["strict_net_slack"])
        if endpoint["physical_loss_upper"] is None:
            raise ValueError("slack supplied without physical loss")
        loss = rational(endpoint["physical_loss_upper"])
        if slack != sigma - loss - required_sigma:
            raise ValueError("strict endpoint slack arithmetic drift")
    if endpoint["all_active_requirements_proved"] and endpoint["root_status"] != "PROVED":
        raise ValueError("active requirements/root status mismatch")
    if endpoint["root_status"] == "PROVED" and not endpoint[
        "all_active_requirements_proved"
    ]:
        raise ValueError("proved root without proved requirements")

    validate_evidence_registry(state, mode, verify_files=verify_files)


def valid_classify(state: dict[str, Any]) -> str:
    endpoint = state["endpoint_state"]
    architecture = state["route_families"]["architecture"]
    selected = architecture["records"][architecture["selected_route"]]
    blockers = state["typed_frontiers"]["minimal_not_testable_antichain"]
    opens = state["typed_frontiers"]["parent_ready_open_frontier"]

    if (
        endpoint["all_active_requirements_proved"]
        and endpoint["root_status"] == "PROVED"
        and endpoint["literal_gate_complete"]
        and endpoint["strict_net_slack"] is not None
        and rational(endpoint["strict_net_slack"]) > 0
    ):
        return "GO"

    if (
        architecture["universe_completeness"]["status"] == "PROVED"
        and all(record["stopped"] for record in architecture["records"].values())
    ):
        return "ARCHITECTURE_INFEASIBLE"

    if selected["stopped"]:
        if architecture["typed_alternative"] is not None:
            return "REROUTE"
        return "STOP_ROUTE"

    if blockers:
        return "NOT_TESTABLE"

    if (
        endpoint["structural_complete"]
        and endpoint["physical_registry_complete"]
        and endpoint["named_fixed_atom_proved"]
        and endpoint["deterministic_endpoint_proved"]
        and not endpoint["all_active_requirements_proved"]
        and endpoint["all_remaining_open_are_positive_L2_arithmetic"]
        and opens
    ):
        return "ARITHMETIC_FRONTIER"

    return "OPEN"


def classify(state: dict[str, Any], *, verify_files: bool = True) -> str:
    try:
        validate_state(state, verify_files=verify_files)
    except (ValueError, FileNotFoundError, KeyError, TypeError):
        return "INVALID"
    return valid_classify(state)


def current_state(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "evidence_mode": SOURCE_LOCKED,
        "route_families": copy.deepcopy(snapshot["route_families"]),
        "typed_frontiers": {
            "minimal_not_testable_antichain": [
                item["node_id"]
                for item in snapshot["typed_frontiers"][
                    "minimal_not_testable_antichain"
                ]
            ],
            "parent_ready_open_frontier": [
                item["node_id"]
                for item in snapshot["typed_frontiers"]["parent_ready_open_frontier"]
            ],
        },
        "endpoint_state": copy.deepcopy(snapshot["endpoint_classifier_state"]),
        "classifier_evidence_registry": copy.deepcopy(
            snapshot["classifier_evidence_registry"]
        ),
    }


def build_snapshot() -> dict[str, Any]:
    files171 = find_171_files()
    manifest171 = load_json(files171["manifest"])
    audit171 = load_json(files171["audit"])
    if (
        manifest171["schema"]
        != "tpc-171-source-locked-occurrence-phase-return-integration-v1"
        or manifest171["current_verdict"] != "NOT_TESTABLE"
        or audit171["status"] != "PASS"
        or audit171["manifest_sha256"] != payload_sha256(manifest171)
    ):
        raise ValueError("TPC-171 source state is not valid")
    if manifest171["first_missing"]["node_id"] != REQUIRED_BLOCKERS[0]:
        raise ValueError("TPC-171 first missing drift")
    blockers = [
        item["node_id"]
        for item in manifest171["typed_frontiers"]["minimal_not_testable_antichain"]
    ]
    opens = [
        item["node_id"]
        for item in manifest171["typed_frontiers"]["parent_ready_open_frontier"]
    ]
    if blockers != REQUIRED_BLOCKERS or opens != REQUIRED_OPEN:
        raise ValueError("TPC-171 frontier drift")

    boundary171 = manifest171["claim_boundary"]
    if any(boundary171.values()):
        raise ValueError("TPC-171 claim boundary contains a promotion")
    arithmetic171 = manifest171["arithmetic_state"]
    if (
        arithmetic171["program_positive_L2"]
        or arithmetic171["named_fixed_atom"]
        or arithmetic171["production_phase_registry"]
    ):
        raise ValueError("TPC-171 phase metric promoted")

    tpc154 = (
        paper_dir(154)
        / "experiments"
        / "tpc154_completion_fiber_obstruction_certificate.json"
    )
    tpc170 = (
        paper_dir(170)
        / "experiments"
        / "tpc170_metric_corridor_audit.json"
    )
    evidence = production_evidence_registry()

    architecture171 = manifest171["route_families"]["architecture"]
    architecture_records = copy.deepcopy(architecture171["records"])
    for route_id, record in architecture_records.items():
        record["fresh_registry"] = route_id != "current_schema_only_canonical_lift"
    arithmetic171_routes = copy.deepcopy(
        manifest171["route_families"]["arithmetic_subroutes"]
    )

    route_families = {
        "architecture": {
            "selected_route": architecture171["selected_route"],
            "selected_root": architecture171["selected_root"],
            "records": architecture_records,
            "universe_completeness": copy.deepcopy(
                architecture171["universe_completeness"]
            ),
            "typed_alternative": architecture171["typed_alternative"],
            "typed_alternative_crosswalk": architecture171[
                "typed_alternative_crosswalk"
            ],
        },
        "arithmetic_subroutes": arithmetic171_routes,
    }

    ledger = manifest171["endpoint_ledger_v4"]
    endpoint_state = {
        "root_status": "NOT_TESTABLE",
        "all_active_requirements_proved": False,
        "structural_complete": False,
        "physical_registry_complete": False,
        "named_fixed_atom_proved": False,
        "deterministic_endpoint_proved": False,
        "all_remaining_open_are_positive_L2_arithmetic": False,
        "named_fixed_atom_sigma": copy.deepcopy(
            ledger["arithmetic"]["named_fixed_atom_sigma"]
        ),
        "sigma_required": copy.deepcopy(ledger["arithmetic"]["sigma_required"]),
        "physical_loss_upper": None,
        "strict_net_slack": None,
        "literal_gate_complete": False,
    }

    locks = expected_snapshot_source_locks()

    snapshot = {
        "schema": "tpc-172-mvp7-occurrence-phase-atomic-route-snapshot-v1",
        "snapshot": {
            "date": "2026-07-28",
            "hash_mode": HASH_MODE,
            "hash_semantics": "INTEGRITY_ONLY",
            "classifier_evidence_mode": SOURCE_LOCKED,
            "source_manifest": repo_relative(files171["manifest"]),
            "source_manifest_sha256": sha256(files171["manifest"]),
            "source_manifest_payload_sha256": payload_sha256(manifest171),
            "snapshot_schema_sha256": sha256(SNAPSHOT_SCHEMA),
        },
        "source_locks": locks,
        "imported_state": {
            "tpc171_verdict": manifest171["current_verdict"],
            "tpc171_first_missing": manifest171["first_missing"]["node_id"],
            "structural_roots": REQUIRED_BLOCKERS[:3],
            "H9_registry_roots": REQUIRED_BLOCKERS[3:],
            "strongest_arithmetic_export": arithmetic171["strongest_export"],
            "strongest_arithmetic_level": arithmetic171["strongest_level"],
            "analytic_norm": arithmetic171["analytic_norm"],
            "phase_quantifier": arithmetic171["phase_quantifier"],
            "endpoint_quantifier": arithmetic171["endpoint_quantifier"],
            "program_positive_L2": arithmetic171["program_positive_L2"],
            "named_fixed_atom": arithmetic171["named_fixed_atom"],
            "production_phase_registry": arithmetic171[
                "production_phase_registry"
            ],
        },
        "quantifier_projection": {
            "proved": {
                "carrier_axis": "EXPLICIT_PACKET_CORRIDOR",
                "phase_axis": "LEBESGUE_AE_FIXED_PHASE",
                "endpoint_axis": "ALL_PREFIX_THETA_SHELL",
                "scale_axis": "EVENTUALLY_PRESCRIBED_SCHEDULE",
                "decay_axis": "FIXED_X_POWER_PHASE_METRIC",
                "support_axis": "ACTUAL_CORE",
            },
            "required": {
                "carrier_axis": "ACTUAL_FIXED_H0_PACKET",
                "phase_axis": "NAMED_FIXED_ATOM",
                "endpoint_axis": "DETERMINISTIC_ALL_PREFIX",
                "scale_axis": "DETERMINISTIC_ALL_SCALE",
                "decay_axis": "FIXED_X_POWER_FIXED_ATOM",
                "support_axis": "ACTUAL_ACTIVE_SUPPORT",
            },
            "promotion_complete": False,
            "failed_axes": [
                "carrier_axis",
                "phase_axis",
                "endpoint_axis",
                "scale_axis",
                "decay_axis",
                "support_axis",
            ],
        },
        "route_families": route_families,
        "typed_frontiers": copy.deepcopy(manifest171["typed_frontiers"]),
        "endpoint_ledger_v4": copy.deepcopy(ledger),
        "endpoint_classifier_state": endpoint_state,
        "classifier_evidence_registry": evidence,
        "ordered_valid_verdicts": ORDERED_VALID_VERDICTS,
        "classifier_contract": {
            "outer_invalid": True,
            "architecture_routes_only_can_reroute": True,
            "fresh_registry_required_for_reroute": True,
            "typed_crosswalk_required_for_reroute": True,
            "architecture_infeasible_requires_complete_universe": True,
            "arithmetic_frontier_requires_structural_and_physical_completion": True,
            "source_hashes_are_integrity_only": True,
            "synthetic_reachability_is_not_theorem_evidence": True,
        },
        "next_forced_objects": {
            "structural": REQUIRED_BLOCKERS[:3],
            "physical_registries": REQUIRED_BLOCKERS[3:],
            "arithmetic_alternatives": REQUIRED_OPEN,
            "metric_bridge": "H2.metric_fixed_atom_crosswalk",
        },
        "current_verdict": "NOT_TESTABLE",
        "progress_classification": {
            "new_structural_localization": True,
            "new_actual_core_phase_metric_all_prefix_corridor": True,
            "new_named_fixed_atom_theorem": False,
            "new_actual_active_support": False,
            "new_program_positive_L2": False,
            "strict_one_over_400": False,
        },
        "claim_boundary": {
            "source_hashes_prove_theorems": False,
            "frozen_zero_edge_census_is_actual_nonexistence": False,
            "archive_address_is_occurrence_identity": False,
            "formal_gluing_is_production_totality": False,
            "phase_metric_is_named_fixed_atom": False,
            "all_prefix_metric_is_deterministic_physical_endpoint": False,
            "metric_fixed_X_power_is_program_positive_L2": False,
            "uncontrolled_atomic_stop_kills_direct_twist": False,
            "arithmetic_subroute_is_architecture_route": False,
            "route_universe_complete": False,
            "architecture_infeasible": False,
            "reroute": False,
            "go": False,
            "strict_one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
    }
    state = current_state(snapshot)
    if classify(state) != "NOT_TESTABLE":
        raise ValueError("current classifier result drift")
    return snapshot


def validate_schema_top(value: dict[str, Any], schema_path: Path) -> None:
    schema = load_json(schema_path)
    if set(value) != set(schema["properties"]):
        raise ValueError(f"strict top-level schema mismatch: {schema_path.name}")
    if value["schema"] != schema["properties"]["schema"]["const"]:
        raise ValueError("schema id drift")


def validate_snapshot(snapshot: dict[str, Any], *, verify_sources: bool = True) -> None:
    validate_schema_top(snapshot, SNAPSHOT_SCHEMA)
    if snapshot["snapshot"]["hash_semantics"] != "INTEGRITY_ONLY":
        raise ValueError("source hashes promoted to theorem evidence")
    if snapshot["ordered_valid_verdicts"] != ORDERED_VALID_VERDICTS:
        raise ValueError("valid-verdict precedence drift")
    if snapshot["current_verdict"] != "NOT_TESTABLE":
        raise ValueError("current verdict drift")
    if any(snapshot["claim_boundary"].values()):
        raise ValueError("claim boundary contains promotion")
    if snapshot["imported_state"]["tpc171_first_missing"] != REQUIRED_BLOCKERS[0]:
        raise ValueError("imported first missing drift")
    if (
        snapshot["imported_state"]["structural_roots"] != REQUIRED_BLOCKERS[:3]
        or snapshot["imported_state"]["H9_registry_roots"] != REQUIRED_BLOCKERS[3:]
    ):
        raise ValueError("imported blocker roots drift")
    if (
        snapshot["imported_state"]["program_positive_L2"]
        or snapshot["imported_state"]["named_fixed_atom"]
        or snapshot["imported_state"]["production_phase_registry"]
    ):
        raise ValueError("phase-metric import promoted")
    projection = snapshot["quantifier_projection"]
    if (
        projection["proved"]["phase_axis"] != "LEBESGUE_AE_FIXED_PHASE"
        or projection["required"]["phase_axis"] != "NAMED_FIXED_ATOM"
        or projection["promotion_complete"]
        or set(projection["failed_axes"]) != set(projection["proved"])
    ):
        raise ValueError("quantifier projection drift")
    blockers = [
        item["node_id"]
        for item in snapshot["typed_frontiers"]["minimal_not_testable_antichain"]
    ]
    opens = [
        item["node_id"]
        for item in snapshot["typed_frontiers"]["parent_ready_open_frontier"]
    ]
    if blockers != REQUIRED_BLOCKERS or opens != REQUIRED_OPEN:
        raise ValueError("snapshot frontier drift")
    blocker_records = {
        item["node_id"]: item
        for item in snapshot["typed_frontiers"]["minimal_not_testable_antichain"]
    }
    if blocker_records[
        "H1.source_backed_local_occurrence_edge_family"
    ]["quantifier_signature"]["support_axis"] != "SOURCE_BACKED_LOCAL_SUPPORT":
        raise ValueError("local occurrence edge promoted to active support")
    registry_axes = {
        "H9.literal_weight_registry": (
            "LITERAL_WEIGHT_REGISTRY",
            "NOT_APPLICABLE",
            "NOT_APPLICABLE",
        ),
        "H9.phase_cell_registry": (
            "PHYSICAL_PHASE_REGISTRY",
            "NAMED_FIXED_ATOM",
            "NOT_APPLICABLE",
        ),
        "H9.endpoint_registry": (
            "PHYSICAL_ENDPOINT_REGISTRY",
            "NOT_APPLICABLE",
            "DETERMINISTIC_ALL_PREFIX",
        ),
        "H9.normalization_registry": (
            "PHYSICAL_NORMALIZATION_REGISTRY",
            "NOT_APPLICABLE",
            "NOT_APPLICABLE",
        ),
    }
    for node_id, (carrier_axis, phase_axis, endpoint_axis) in registry_axes.items():
        signature = blocker_records[node_id]["quantifier_signature"]
        if (
            signature["carrier_axis"] != carrier_axis
            or signature["phase_axis"] != phase_axis
            or signature["endpoint_axis"] != endpoint_axis
            or signature["decay_axis"] != "NONE"
        ):
            raise ValueError("physical data registry carries theorem decay")
    ledger = snapshot["endpoint_ledger_v4"]
    if ledger["arithmetic"]["named_fixed_atom_sigma"] != {
        "numerator": 0,
        "denominator": 1,
    }:
        raise ValueError("metric power promoted to named fixed atom")
    if ledger["full_synthesis"]["one_over_400_paid"]:
        raise ValueError("1/400 marked paid")
    if any(
        item["quantity_kind"].startswith("FIXED_X_POWER_PHASE")
        and item["eligible_for_named_fixed_atom"]
        for item in ledger["charge_registry"]
    ):
        raise ValueError("metric charge promoted")
    state = current_state(snapshot)
    validate_state(state, verify_files=verify_sources)
    if classify(state, verify_files=verify_sources) != "NOT_TESTABLE":
        raise ValueError("snapshot does not classify NOT_TESTABLE")
    if verify_sources:
        if snapshot["source_locks"] != expected_snapshot_source_locks():
            raise ValueError("snapshot source-lock coverage or metadata drift")
        for record in snapshot["source_locks"]:
            if record["hash_semantics"] != "INTEGRITY_ONLY":
                raise ValueError("source lock has theorem semantics")
            path = REPO / record["path"]
            if (
                not path.is_file()
                or sha256(path) != record["canonical_utf8_lf_sha256"]
            ):
                raise ValueError("snapshot source hash drift")
        source_manifest = REPO / snapshot["snapshot"]["source_manifest"]
        if (
            sha256(source_manifest)
            != snapshot["snapshot"]["source_manifest_sha256"]
            or payload_sha256(load_json(source_manifest))
            != snapshot["snapshot"]["source_manifest_payload_sha256"]
        ):
            raise ValueError("source manifest lock drift")
        if sha256(SNAPSHOT_SCHEMA) != snapshot["snapshot"]["snapshot_schema_sha256"]:
            raise ValueError("snapshot schema hash drift")


def synthetic_evidence(
    source_id: str,
    claim_type: str,
    scope_id: str,
    *,
    from_route: str | None = None,
    to_route: str | None = None,
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "evidence_kind": "SYNTHETIC_ASSUMED_PREDICATE",
        "proof_semantics": "NONE_SYNTHETIC_REACHABILITY_ONLY",
        "claim_type": claim_type,
        "scope_id": scope_id,
        "from_route": from_route,
        "to_route": to_route,
        "path": None,
        "canonical_utf8_lf_sha256": None,
        "statement": "Synthetic reachability predicate; not theorem evidence.",
    }


def synthetic_state(
    *,
    root_status: str = "OPEN",
    blockers: bool = False,
    opens: bool = True,
    selected_stopped: bool = False,
    alternative: bool = False,
    complete_universe: bool = False,
    all_routes_stopped: bool = False,
    structural_complete: bool = False,
    physical_complete: bool = False,
    fixed_atom: bool = False,
    deterministic_endpoint: bool = False,
    arithmetic_only_open: bool = False,
    go: bool = False,
) -> dict[str, Any]:
    records = {
        "map": {
            "route_kind": "ARCHITECTURE_ROUTE",
            "state": "STOP_SCOPED" if selected_stopped or all_routes_stopped else "OPEN",
            "stopped": selected_stopped or all_routes_stopped,
            "selected": True,
            "root_node": "ROOT.map",
            "scope_id": "SYNTHETIC_MAP",
            "source_export": "synthetic.stop.map"
            if selected_stopped or all_routes_stopped
            else None,
            "registry_id": "registry.map",
            "fresh_registry": True,
        },
        "scalar": {
            "route_kind": "ARCHITECTURE_ROUTE",
            "state": "STOP_SCOPED" if all_routes_stopped else "OPEN",
            "stopped": all_routes_stopped,
            "selected": False,
            "root_node": "ROOT.scalar",
            "scope_id": "SYNTHETIC_SCALAR",
            "source_export": "synthetic.stop.scalar" if all_routes_stopped else None,
            "registry_id": "registry.scalar",
            "fresh_registry": True,
        },
    }
    registry: dict[str, Any] = {}
    if records["map"]["stopped"]:
        registry["synthetic.stop.map"] = synthetic_evidence(
            "synthetic.stop.map",
            "ARCHITECTURE_ROUTE_CELL_STOP",
            "SYNTHETIC_MAP",
            from_route="map",
        )
    if records["scalar"]["stopped"]:
        registry["synthetic.stop.scalar"] = synthetic_evidence(
            "synthetic.stop.scalar",
            "ARCHITECTURE_ROUTE_CELL_STOP",
            "SYNTHETIC_SCALAR",
            from_route="scalar",
        )
    completeness = {
        "status": "PROVED" if complete_universe else "NOT_PROVED",
        "source_export": "synthetic.complete" if complete_universe else None,
        "scope": "SYNTHETIC_ARCHITECTURE_UNIVERSE",
    }
    if complete_universe:
        registry["synthetic.complete"] = synthetic_evidence(
            "synthetic.complete",
            "ARCHITECTURE_UNIVERSE_COMPLETENESS",
            "SYNTHETIC_ARCHITECTURE_UNIVERSE",
        )
    typed_alternative = "scalar" if alternative else None
    typed_crosswalk = "synthetic.crosswalk" if alternative else None
    if alternative:
        registry["synthetic.crosswalk"] = synthetic_evidence(
            "synthetic.crosswalk",
            "ARCHITECTURE_ROUTE_CROSSWALK",
            "SYNTHETIC_MAP_TO_SCALAR",
            from_route="map",
            to_route="scalar",
        )
    sigma = {"numerator": 1, "denominator": 100} if go else {
        "numerator": 0,
        "denominator": 1,
    }
    loss = {"numerator": 1, "denominator": 1000} if go else None
    slack = {"numerator": 13, "denominator": 2000} if go else None
    return {
        "evidence_mode": SYNTHETIC,
        "route_families": {
            "architecture": {
                "selected_route": "map",
                "selected_root": "ROOT.map",
                "records": records,
                "universe_completeness": completeness,
                "typed_alternative": typed_alternative,
                "typed_alternative_crosswalk": typed_crosswalk,
            },
            "arithmetic_subroutes": {
                "records": {
                    "method": {
                        "route_kind": "ARITHMETIC_SUBROUTE",
                        "state": "OPEN",
                        "scope_id": "SYNTHETIC_METHOD",
                    }
                },
                "architecture_reroute_eligible": False,
            },
        },
        "typed_frontiers": {
            "minimal_not_testable_antichain": ["H.synthetic"] if blockers else [],
            "parent_ready_open_frontier": ["A.synthetic"] if opens else [],
        },
        "endpoint_state": {
            "root_status": "PROVED" if go else root_status,
            "all_active_requirements_proved": go,
            "structural_complete": structural_complete or go,
            "physical_registry_complete": physical_complete or go,
            "named_fixed_atom_proved": fixed_atom or go,
            "deterministic_endpoint_proved": deterministic_endpoint or go,
            "all_remaining_open_are_positive_L2_arithmetic": arithmetic_only_open,
            "named_fixed_atom_sigma": sigma,
            "sigma_required": {"numerator": 1, "denominator": 400},
            "physical_loss_upper": loss,
            "strict_net_slack": slack,
            "literal_gate_complete": go,
        },
        "classifier_evidence_registry": registry,
    }


def reachability_scenarios() -> dict[str, str]:
    states = {
        "GO": synthetic_state(go=True, opens=False),
        "ARCHITECTURE_INFEASIBLE": synthetic_state(
            complete_universe=True, all_routes_stopped=True
        ),
        "REROUTE": synthetic_state(selected_stopped=True, alternative=True),
        "STOP_ROUTE": synthetic_state(selected_stopped=True),
        "NOT_TESTABLE": synthetic_state(blockers=True),
        "ARITHMETIC_FRONTIER": synthetic_state(
            structural_complete=True,
            physical_complete=True,
            fixed_atom=True,
            deterministic_endpoint=True,
            arithmetic_only_open=True,
        ),
        "OPEN": synthetic_state(),
    }
    outcomes = {
        expected: classify(state, verify_files=False)
        for expected, state in states.items()
    }
    if outcomes != {name: name for name in ORDERED_VALID_VERDICTS}:
        raise ValueError(f"classifier reachability drift: {outcomes}")
    malformed = copy.deepcopy(states["NOT_TESTABLE"])
    malformed["route_families"]["architecture"]["records"]["map"][
        "route_kind"
    ] = "ARITHMETIC_SUBROUTE"
    outcomes["INVALID"] = classify(malformed, verify_files=False)
    if outcomes["INVALID"] != "INVALID":
        raise ValueError("INVALID is unreachable")
    return outcomes


def mutation_rejected(snapshot: dict[str, Any], mutate: Any) -> bool:
    clone = copy.deepcopy(snapshot)
    mutate(clone)
    try:
        validate_snapshot(clone, verify_sources=True)
    except (ValueError, FileNotFoundError, KeyError, TypeError):
        return True
    return False


def build_audit(snapshot: dict[str, Any]) -> dict[str, Any]:
    validate_snapshot(snapshot)
    scenarios = reachability_scenarios()

    mutations = {
        "reject_source_hash_as_theorem": mutation_rejected(
            snapshot,
            lambda value: value["snapshot"].__setitem__(
                "hash_semantics", "THEOREM_EVIDENCE"
            ),
        ),
        "reject_source_hash_drift": mutation_rejected(
            snapshot,
            lambda value: value["source_locks"][0].__setitem__(
                "canonical_utf8_lf_sha256", "0" * 64
            ),
        ),
        "reject_phase_ae_as_named_atom": mutation_rejected(
            snapshot,
            lambda value: value["quantifier_projection"]["proved"].__setitem__(
                "phase_axis", "NAMED_FIXED_ATOM"
            ),
        ),
        "reject_metric_power_as_program_L2": mutation_rejected(
            snapshot,
            lambda value: value["imported_state"].__setitem__(
                "program_positive_L2", True
            ),
        ),
        "reject_metric_charge_as_fixed_atom": mutation_rejected(
            snapshot,
            lambda value: value["endpoint_ledger_v4"]["charge_registry"][
                0
            ].__setitem__("eligible_for_named_fixed_atom", True),
        ),
        "reject_local_edge_as_active_support": mutation_rejected(
            snapshot,
            lambda value: next(
                item
                for item in value["typed_frontiers"][
                    "minimal_not_testable_antichain"
                ]
                if item["node_id"]
                == "H1.source_backed_local_occurrence_edge_family"
            )["quantifier_signature"].__setitem__(
                "support_axis", "ACTUAL_ACTIVE_SUPPORT"
            ),
        ),
        "reject_H9_registry_decay_promotion": mutation_rejected(
            snapshot,
            lambda value: next(
                item
                for item in value["typed_frontiers"][
                    "minimal_not_testable_antichain"
                ]
                if item["node_id"] == "H9.phase_cell_registry"
            )["quantifier_signature"].__setitem__(
                "decay_axis", "FIXED_X_POWER_FIXED_ATOM"
            ),
        ),
        "reject_arithmetic_method_as_architecture": mutation_rejected(
            snapshot,
            lambda value: value["route_families"]["architecture"]["records"].__setitem__(
                "direct_twist",
                {
                    "route_kind": "ARITHMETIC_SUBROUTE",
                    "state": "OPEN",
                    "stopped": False,
                    "selected": False,
                    "root_node": None,
                    "scope_id": "NAMED_FIXED_PHASE",
                    "source_export": None,
                    "registry_id": "registry.fake",
                    "fresh_registry": True,
                },
            ),
        ),
        "reject_arithmetic_method_reroute": mutation_rejected(
            snapshot,
            lambda value: value["route_families"]["arithmetic_subroutes"].__setitem__(
                "architecture_reroute_eligible", True
            ),
        ),
        "reject_unproved_route_universe": mutation_rejected(
            snapshot,
            lambda value: value["route_families"]["architecture"][
                "universe_completeness"
            ].__setitem__("status", "PROVED"),
        ),
        "reject_fabricated_stop_label": mutation_rejected(
            snapshot,
            lambda value: value["route_families"]["architecture"]["records"][
                "occurrence_augmented_map"
            ].update(
                {
                    "state": "STOP_SCOPED",
                    "stopped": True,
                    "source_export": "theorem.fabricated",
                }
            ),
        ),
        "reject_uncontrolled_atom_stop_as_direct_twist_stop": mutation_rejected(
            snapshot,
            lambda value: value["claim_boundary"].__setitem__(
                "uncontrolled_atomic_stop_kills_direct_twist", True
            ),
        ),
        "reject_blocker_collapse": mutation_rejected(
            snapshot,
            lambda value: value["typed_frontiers"].__setitem__(
                "minimal_not_testable_antichain",
                value["typed_frontiers"]["minimal_not_testable_antichain"][:1],
            ),
        ),
        "reject_open_nt_merge": mutation_rejected(
            snapshot,
            lambda value: value["typed_frontiers"][
                "parent_ready_open_frontier"
            ].append(
                copy.deepcopy(
                    value["typed_frontiers"]["minimal_not_testable_antichain"][0]
                )
            ),
        ),
        "reject_named_atom_sigma_promotion": mutation_rejected(
            snapshot,
            lambda value: value["endpoint_ledger_v4"]["arithmetic"].__setitem__(
                "named_fixed_atom_sigma", {"numerator": 1, "denominator": 10}
            ),
        ),
        "reject_one_over_400_without_literal_gate": mutation_rejected(
            snapshot,
            lambda value: value["endpoint_ledger_v4"]["full_synthesis"].__setitem__(
                "one_over_400_paid", True
            ),
        ),
        "reject_verdict_promotion": mutation_rejected(
            snapshot,
            lambda value: value.__setitem__("current_verdict", "GO"),
        ),
    }
    if not all(mutations.values()):
        raise ValueError(
            f"mutation regression escaped: {[k for k, ok in mutations.items() if not ok]}"
        )

    return {
        "schema": "tpc-172-mvp7-occurrence-phase-atomic-route-audit-v1",
        "status": "PASS",
        "snapshot_sha256": payload_sha256(snapshot),
        "checks": {
            "dynamic_tpc171_source_lock": True,
            "source_hashes_integrity_only": True,
            "six_axis_projection_preserved": True,
            "phase_metric_not_named_fixed_atom": True,
            "architecture_arithmetic_route_types_disjoint": True,
            "arithmetic_methods_not_reroute_eligible": True,
            "typed_blockers_and_open_frontier_separate": True,
            "fresh_registry_and_crosswalk_required": True,
            "route_universe_completeness_required": True,
            "endpoint_v4_literal_gate_preserved": True,
            "metric_power_not_fixed_atom_power": True,
            "all_classifier_verdicts_reachable": True,
        },
        "mutation_regressions": mutations,
        "scenario_verdicts": scenarios,
        "current_verdict": "NOT_TESTABLE",
        "first_missing": REQUIRED_BLOCKERS[0],
        "claim_boundary": copy.deepcopy(snapshot["claim_boundary"]),
    }


def validate_audit(audit: dict[str, Any], snapshot: dict[str, Any]) -> None:
    validate_schema_top(audit, AUDIT_SCHEMA)
    if audit["status"] != "PASS":
        raise ValueError("audit status is not PASS")
    if audit["snapshot_sha256"] != payload_sha256(snapshot):
        raise ValueError("snapshot hash drift")
    if not all(audit["checks"].values()) or not all(
        audit["mutation_regressions"].values()
    ):
        raise ValueError("audit contains failed checks")
    expected_scenarios = {
        **{name: name for name in ORDERED_VALID_VERDICTS},
        "INVALID": "INVALID",
    }
    if audit["scenario_verdicts"] != expected_scenarios:
        raise ValueError("scenario verdict drift")
    if audit["claim_boundary"] != snapshot["claim_boundary"]:
        raise ValueError("audit claim boundary drift")


def write_or_check(path: Path, value: Any, check: bool) -> None:
    expected = canonical_json(value)
    if check:
        if normalize_lf(path.read_text(encoding="utf-8")) != expected:
            raise ValueError(f"generated artifact drift: {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(expected, encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    snapshot = build_snapshot()
    validate_snapshot(snapshot)
    audit = build_audit(snapshot)
    validate_audit(audit, snapshot)
    write_or_check(SNAPSHOT, snapshot, args.check)
    write_or_check(AUDIT, audit, args.check)
    print(
        "PASS: TPC-172/MVP7 dynamic classifier; "
        f"verdict={snapshot['current_verdict']}; "
        f"first_missing={audit['first_missing']}"
    )


if __name__ == "__main__":
    main()
