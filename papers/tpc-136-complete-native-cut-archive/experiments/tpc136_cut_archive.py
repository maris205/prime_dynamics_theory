#!/usr/bin/env python3
"""Compose the TPC-133--135 artifacts into the TPC-136 cut archive.

The cut is complete even when later carrier maps are absent: every
upstream path is retained as exactly one of soft, open, or frontier.
The program separately audits totality of four downstream partial maps.

Default mode writes deterministic artifacts.  ``--check`` performs
only byte comparisons and never rewrites.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
REPO = PAPER.parents[1]
TPC134 = (
    REPO
    / "papers"
    / "tpc-134-boundary-complete-dyadic-prefix-tail-archive"
)
TPC135 = REPO / "papers" / "tpc-135-tpc17-tpc18-block-frontier"
DEFAULT_PATHS = TPC134 / "samples" / "tpc134_paths.jsonl"
DEFAULT_FRONTIER = TPC135 / "samples" / "tpc135_frontier_manifest.json"
DEFAULT_FRONTIER_CERT = (
    TPC135 / "experiments" / "tpc135_domain_cover_certificate.json"
)
DEFAULT_CUT_PATHS = PAPER / "samples" / "tpc136_cut_paths.jsonl"
DEFAULT_MAPS = PAPER / "samples" / "tpc136_downstream_maps.json"
DEFAULT_CERTIFICATE = HERE / "tpc136_cut_archive_certificate.json"
TERMINAL_TYPES = {
    "ELIGIBLE_PREFIX_SOFT",
    "ELIGIBLE_TAIL_OPEN",
    "FRONTIER_UNMAPPED",
}
MAP_IDS = (
    "determinant_fiber_QD",
    "zero_mode_order_QZ",
    "physical_grouping_G",
    "fixed_h0_downstream_selector",
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def pretty_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            values.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at line {line_number}") from exc
    if not values:
        raise ValueError("upstream path archive is empty")
    return values


def validate_frontier_chain(
    paths_path: Path,
    frontier_path: Path,
    frontier_certificate_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    paths = load_jsonl(paths_path)
    frontier = load_json(frontier_path)
    certificate = load_json(frontier_certificate_path)
    if certificate.get("status") != "PASS":
        raise ValueError("TPC-135 certificate is not PASS")
    if certificate["upstream"]["tpc134_paths_sha256"] != sha256_file(paths_path):
        raise ValueError("TPC-135 certificate does not bind the current TPC-134 paths")
    frontier_text = frontier_path.read_text(encoding="utf-8")
    if certificate["census"]["manifest_sha256"] != sha256_text(frontier_text):
        raise ValueError("TPC-135 certificate does not bind the frontier manifest")
    return paths, frontier, certificate


def block_reasons(frontier: dict[str, Any]) -> dict[tuple[int, int], str]:
    result: dict[tuple[int, int], str] = {}
    for block in frontier["blocks"]:
        key = (block["j_L"], block["j_K"])
        if key in result:
            raise ValueError("duplicate block in frontier manifest")
        result[key] = block["reason"]
    return result


def make_cut_path(
    path: dict[str, Any],
    reason: str,
) -> dict[str, Any]:
    if reason == "ELIGIBLE":
        if path["terminal_type"] == "PREFIX":
            cut_type = "ELIGIBLE_PREFIX_SOFT"
            soft_source: dict[str, Any] | None = {
                "paper": "TPC-17",
                "theorem": "cumulative-divisor-prefix-cancellation",
                "scope": "published-Maynard-core with fixed eta margin",
                "normalization": path["metadata"]["physical_normalization"],
            }
        else:
            cut_type = "ELIGIBLE_TAIL_OPEN"
            soft_source = None
    else:
        cut_type = "FRONTIER_UNMAPPED"
        soft_source = None
    cut_path_id = f"cut|{path['path_id']}"
    core = {
        "schema": "tpc136-cut-path-v1",
        "cut_path_id": cut_path_id,
        "upstream_path_id": path["path_id"],
        "native_id": path["native_id"],
        "cut_terminal_type": cut_type,
        "edge_multiplier_ast": path["edge_multiplier_ast"],
        "metadata": {
            **path["metadata"],
            "block": path["block"],
            "D0": path["D0"],
            "upstream_integrity_sha256": path["integrity_sha256"],
            "frontier_reason": None if reason == "ELIGIBLE" else reason,
        },
        "soft_theorem_source": soft_source,
    }
    return core | {"integrity_sha256": sha256_text(canonical_json(core))}


def generate_cut_paths(
    paths: list[dict[str, Any]],
    frontier: dict[str, Any],
) -> list[dict[str, Any]]:
    reasons = block_reasons(frontier)
    cut_paths: list[dict[str, Any]] = []
    for path in paths:
        key = (path["block"]["j_L"], path["block"]["j_K"])
        if key not in reasons:
            raise ValueError(f"frontier manifest misses block {key}")
        cut_paths.append(make_cut_path(path, reasons[key]))
    return cut_paths


def build_map_manifest(cut_paths: list[dict[str, Any]]) -> dict[str, Any]:
    h0_values = {path["metadata"]["h0"] for path in cut_paths}
    if len(h0_values) != 1:
        raise ValueError("cut archive does not have one inherited fixed h0")
    required_h0 = next(iter(h0_values))
    return {
        "schema": "tpc136-downstream-map-manifest-v1",
        "maps": [
            {
                "map_id": map_id,
                "status": "NOT_TESTABLE",
                "source_status": "NOT_TESTABLE",
                "source": "",
                "required_domain": "ALL_NONSOFT_CUT_PATHS",
                "required_h0": required_h0,
                "totality_definition": (
                    "ROW_SEPARATED_MATRIX_EQUIVALENT_TO_PATH_TOTALITY"
                ),
                "domain_cut_path_ids": [],
            }
            for map_id in MAP_IDS
        ],
    }


def validate_cut_paths(
    cut_paths: list[dict[str, Any]],
    upstream_paths: list[dict[str, Any]],
    frontier: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    upstream_by_id = {path["path_id"]: path for path in upstream_paths}
    reasons = block_reasons(frontier)
    seen_upstream: set[str] = set()
    seen_cut: set[str] = set()
    for cut in cut_paths:
        if cut.get("schema") != "tpc136-cut-path-v1":
            errors.append("wrong cut path schema")
            continue
        upstream_id = cut["upstream_path_id"]
        if upstream_id not in upstream_by_id:
            errors.append(f"unknown upstream path {upstream_id}")
            continue
        if upstream_id in seen_upstream:
            errors.append(f"duplicate upstream path {upstream_id}")
        seen_upstream.add(upstream_id)
        if cut["cut_path_id"] in seen_cut:
            errors.append(f"duplicate cut path {cut['cut_path_id']}")
        seen_cut.add(cut["cut_path_id"])
        upstream = upstream_by_id[upstream_id]
        key = (upstream["block"]["j_L"], upstream["block"]["j_K"])
        expected = make_cut_path(upstream, reasons[key])
        if cut != expected:
            errors.append(f"cut record mismatch for {upstream_id}")
        if cut["cut_terminal_type"] not in TERMINAL_TYPES:
            errors.append(f"unknown terminal type for {upstream_id}")
        if cut["cut_terminal_type"] == "ELIGIBLE_PREFIX_SOFT":
            if not cut["soft_theorem_source"]:
                errors.append(f"soft path lacks theorem source for {upstream_id}")
        elif cut["soft_theorem_source"] is not None:
            errors.append(f"nonsoft path has a soft theorem source for {upstream_id}")
    if seen_upstream != set(upstream_by_id):
        errors.append("cut archive does not contain exactly one child per upstream path")
    return errors


def validate_map_manifest(
    maps: dict[str, Any],
    cut_paths: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    if maps.get("schema") != "tpc136-downstream-map-manifest-v1":
        errors.append("wrong map manifest schema")
        return errors
    map_records = maps.get("maps", [])
    ids = [record.get("map_id") for record in map_records]
    if tuple(ids) != MAP_IDS:
        errors.append("map ids or order do not match the declared route")
    nonsoft = {
        path["cut_path_id"]
        for path in cut_paths
        if path["cut_terminal_type"] != "ELIGIBLE_PREFIX_SOFT"
    }
    all_cut_ids = {path["cut_path_id"] for path in cut_paths}
    h0_values = {path["metadata"]["h0"] for path in cut_paths}
    if len(h0_values) != 1:
        errors.append("cut archive does not have one inherited fixed h0")
        required_h0 = None
    else:
        required_h0 = next(iter(h0_values))
    for record in map_records:
        domain_list = record.get("domain_cut_path_ids", [])
        domain = set(domain_list)
        if len(domain) != len(domain_list):
            errors.append(f"duplicate map-domain id for {record.get('map_id')}")
        if not domain.issubset(all_cut_ids):
            errors.append(f"unknown map-domain id for {record.get('map_id')}")
        if record.get("required_domain") != "ALL_NONSOFT_CUT_PATHS":
            errors.append(f"wrong path-totality contract for {record.get('map_id')}")
        if record.get("required_h0") != required_h0:
            errors.append(f"wrong fixed-h0 contract for {record.get('map_id')}")
        if (
            record.get("totality_definition")
            != "ROW_SEPARATED_MATRIX_EQUIVALENT_TO_PATH_TOTALITY"
        ):
            errors.append(f"wrong totality definition for {record.get('map_id')}")
        if record.get("status") == "PROVED":
            if record.get("source_status") != "PROVED":
                errors.append(
                    f"proved map lacks proved source status for {record.get('map_id')}"
                )
            if not record.get("source"):
                errors.append(f"proved map lacks source for {record.get('map_id')}")
            if not nonsoft.issubset(domain):
                errors.append(f"proved map is not path-total for {record.get('map_id')}")
        elif record.get("status") == "NOT_TESTABLE":
            if record.get("source_status") != "NOT_TESTABLE":
                errors.append(
                    f"untestable map has promoted source for {record.get('map_id')}"
                )
            if record.get("source"):
                errors.append(
                    f"untestable map has unsupported source for {record.get('map_id')}"
                )
        else:
            errors.append(f"invalid map status for {record.get('map_id')}")
    return errors


def map_totality_summary(
    maps: dict[str, Any],
    cut_paths: list[dict[str, Any]],
) -> dict[str, Any]:
    nonsoft = {
        path["cut_path_id"]
        for path in cut_paths
        if path["cut_terminal_type"] != "ELIGIBLE_PREFIX_SOFT"
    }
    summary: dict[str, Any] = {}
    for record in maps["maps"]:
        domain = set(record["domain_cut_path_ids"])
        missing = sorted(nonsoft - domain)
        summary[record["map_id"]] = {
            "status": record["status"],
            "source_status": record["source_status"],
            "required_domain": record["required_domain"],
            "required_h0": record["required_h0"],
            "totality_definition": record["totality_definition"],
            "path_total": not missing,
            "matrix_operator_total": not missing,
            "missing_nonsoft_path_count": len(missing),
            "first_missing_cut_path_ids": missing[:3],
            "aggregated_scalar_totality": (
                "NOT_EVALUATED_AND_NOT_A_PROVENANCE_CERTIFICATE"
            ),
        }
    return summary


def totality_semantics_regression() -> dict[str, bool]:
    """Separate row-level zero from a cancelling aggregated scalar."""
    omitted_row_entries = (1, -1)
    matrix_zero = all(entry == 0 for entry in omitted_row_entries)
    aggregated_zero = sum(omitted_row_entries) == 0
    return {
        "row_separated_matrix_is_nonzero": not matrix_zero,
        "aggregated_scalar_can_cancel": aggregated_zero,
        "aggregated_zero_not_promoted_to_path_total": (
            aggregated_zero and not matrix_zero
        ),
    }


def mutation_checks(
    cut_paths: list[dict[str, Any]],
    upstream_paths: list[dict[str, Any]],
    frontier: dict[str, Any],
    maps: dict[str, Any],
) -> dict[str, bool]:
    first = cut_paths[0]

    deleted = cut_paths[1:]
    duplicated = cut_paths + [first]

    wrong_type_record = json.loads(json.dumps(first))
    wrong_type_record["cut_terminal_type"] = "ELIGIBLE_PREFIX_SOFT"
    wrong_type = [wrong_type_record] + cut_paths[1:]

    unsupported_soft_record = json.loads(json.dumps(first))
    unsupported_soft_record["soft_theorem_source"] = {
        "paper": "",
        "theorem": "",
        "scope": "",
        "normalization": "",
    }
    unsupported_soft = [unsupported_soft_record] + cut_paths[1:]

    wrong_shift_record = json.loads(json.dumps(first))
    wrong_shift_record["metadata"]["h0"] += 2
    wrong_shift = [wrong_shift_record] + cut_paths[1:]

    false_total_maps = json.loads(json.dumps(maps))
    false_total_maps["maps"][0]["status"] = "PROVED"
    false_total_maps["maps"][0]["source_status"] = "PROVED"
    false_total_maps["maps"][0]["source"] = "unsupported-claim"

    false_source_maps = json.loads(json.dumps(maps))
    false_source_maps["maps"][-1]["source_status"] = "PROVED"
    false_source_maps["maps"][-1]["source"] = "unsupported-fixed-h0-source"

    wrong_h0_maps = json.loads(json.dumps(maps))
    wrong_h0_maps["maps"][-1]["required_h0"] += 2

    wrong_totality_maps = json.loads(json.dumps(maps))
    wrong_totality_maps["maps"][0][
        "totality_definition"
    ] = "AGGREGATED_SCALAR_ZERO"

    return {
        "deleted_cut_path_rejected": bool(
            validate_cut_paths(deleted, upstream_paths, frontier)
        ),
        "duplicate_cut_path_rejected": bool(
            validate_cut_paths(duplicated, upstream_paths, frontier)
        ),
        "terminal_type_mutation_rejected": bool(
            validate_cut_paths(wrong_type, upstream_paths, frontier)
        ),
        "unsupported_soft_label_rejected": bool(
            validate_cut_paths(unsupported_soft, upstream_paths, frontier)
        ),
        "wrong_h0_rejected": bool(
            validate_cut_paths(wrong_shift, upstream_paths, frontier)
        ),
        "false_total_map_rejected": bool(
            validate_map_manifest(false_total_maps, cut_paths)
        ),
        "unsupported_fixed_h0_source_rejected": bool(
            validate_map_manifest(false_source_maps, cut_paths)
        ),
        "wrong_fixed_h0_contract_rejected": bool(
            validate_map_manifest(wrong_h0_maps, cut_paths)
        ),
        "aggregated_scalar_totality_promotion_rejected": bool(
            validate_map_manifest(wrong_totality_maps, cut_paths)
        ),
    }


def build_artifacts(
    paths_path: Path,
    frontier_path: Path,
    frontier_certificate_path: Path,
) -> tuple[str, str, str, dict[str, Any]]:
    paths, frontier, frontier_certificate = validate_frontier_chain(
        paths_path, frontier_path, frontier_certificate_path
    )
    cut_paths = generate_cut_paths(paths, frontier)
    maps = build_map_manifest(cut_paths)
    cut_errors = validate_cut_paths(cut_paths, paths, frontier)
    map_errors = validate_map_manifest(maps, cut_paths)
    mutations = mutation_checks(cut_paths, paths, frontier, maps)
    totality = map_totality_summary(maps, cut_paths)
    totality_semantics = totality_semantics_regression()
    terminal_counts = Counter(path["cut_terminal_type"] for path in cut_paths)
    cut_text = "".join(canonical_json(path) + "\n" for path in cut_paths)
    maps_text = pretty_json(maps)
    checks = {
        "exactly_one_cut_record_per_upstream_path": not cut_errors,
        "native_h0_and_normalization_preserved": not cut_errors,
        "soft_paths_have_typed_theorem_sources": not cut_errors,
        "frontier_paths_are_retained_not_deleted": terminal_counts[
            "FRONTIER_UNMAPPED"
        ]
        > 0,
        "downstream_map_manifest_consistent": not map_errors,
        "all_downstream_totality_failures_reported": all(
            not record["path_total"] for record in totality.values()
        ),
        "all_four_map_sources_remain_not_testable": all(
            record["source_status"] == "NOT_TESTABLE"
            for record in totality.values()
        ),
        "fixed_h0_selector_source_remains_not_testable": totality[
            "fixed_h0_downstream_selector"
        ]["source_status"]
        == "NOT_TESTABLE",
        "matrix_and_path_totality_agree": all(
            record["matrix_operator_total"] == record["path_total"]
            for record in totality.values()
        ),
        "aggregated_scalar_false_positive_regression_passes": all(
            totality_semantics.values()
        ),
        "all_mutations_rejected": all(mutations.values()),
    }
    certificate = {
        "schema": "tpc136-cut-archive-certificate-v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "scope": (
            "complete native archive to the first unsupported cut; "
            "not a complete downstream actual-carrier archive"
        ),
        "upstream": {
            "tpc134_paths_sha256": sha256_file(paths_path),
            "tpc135_frontier_manifest_sha256": sha256_file(frontier_path),
            "tpc135_certificate_sha256": sha256_file(
                frontier_certificate_path
            ),
            "tpc135_status": frontier_certificate["status"],
        },
        "cut_archive": {
            "upstream_path_count": len(paths),
            "cut_path_count": len(cut_paths),
            "terminal_type_counts": dict(sorted(terminal_counts.items())),
            "jsonl_sha256": sha256_text(cut_text),
            "column_conservation": "INHERITED_EXACTLY_FROM_TPC134",
            "scalar_identity": (
                "B = eligible_prefix_soft + eligible_tail_open "
                "+ frontier_unmapped"
            ),
        },
        "downstream_totality": totality,
        "totality_semantics_regression": totality_semantics,
        "checks": checks,
        "mutation_regression": mutations,
        "validation_errors": {
            "cut_paths": cut_errors,
            "maps": map_errors,
        },
        "route_verdict": {
            "H1_native_entrance": "PROVED_L1",
            "H1_dyadic_prefix_archive": "PROVED_L1",
            "H1_native_cut": "PROVED_L1",
            "eligible_only_cover": "STOP_DECLARED_COMPILER",
            "H1_actual_carrier": "NOT_TESTABLE",
            "first_missing": (
                "frontier totalization or a theorem-backed complete "
                "frontier soft estimate, followed by total QD/QZ/G/h0 maps"
            ),
        },
        "claim_boundary": {
            "cut_archive_L0_L1": True,
            "new_positive_fixed_h0_L2": False,
            "frontier_scalar_bound": False,
            "complete_H1_actual_carrier": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    return cut_text, maps_text, pretty_json(certificate), certificate


def compare_bytes(path: Path, expected: str) -> None:
    if not path.exists():
        raise SystemExit(f"missing artifact: {path}")
    if path.read_text(encoding="utf-8") != expected:
        raise SystemExit(f"artifact mismatch: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths", type=Path, default=DEFAULT_PATHS)
    parser.add_argument("--frontier", type=Path, default=DEFAULT_FRONTIER)
    parser.add_argument(
        "--frontier-certificate",
        type=Path,
        default=DEFAULT_FRONTIER_CERT,
    )
    parser.add_argument("--cut-paths", type=Path, default=DEFAULT_CUT_PATHS)
    parser.add_argument("--maps", type=Path, default=DEFAULT_MAPS)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument(
        "--check",
        action="store_true",
        help="read-only deterministic comparison; never rewrites artifacts",
    )
    args = parser.parse_args()

    cut_text, maps_text, certificate_text, certificate = build_artifacts(
        args.paths, args.frontier, args.frontier_certificate
    )
    if args.check:
        compare_bytes(args.cut_paths, cut_text)
        compare_bytes(args.maps, maps_text)
        compare_bytes(args.certificate, certificate_text)
    else:
        args.cut_paths.parent.mkdir(parents=True, exist_ok=True)
        args.maps.parent.mkdir(parents=True, exist_ok=True)
        args.certificate.parent.mkdir(parents=True, exist_ok=True)
        args.cut_paths.write_text(cut_text, encoding="utf-8")
        args.maps.write_text(maps_text, encoding="utf-8")
        args.certificate.write_text(certificate_text, encoding="utf-8")
    print(certificate_text, end="")
    if certificate["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
