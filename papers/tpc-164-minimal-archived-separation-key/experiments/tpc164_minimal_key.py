#!/usr/bin/env python3
"""Exhaustively determine the smallest separating key in the TPC-153 archive."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PAPERS = PAPER.parent
REPO = PAPERS.parent

TPC153 = PAPERS / "tpc-153-canonical-cut-occurrence-shadow"
TPC163 = PAPERS / "tpc-163-source-locator-census-native-key-collision"
SHADOW = TPC153 / "samples" / "tpc153_cut_occurrence_shadow.jsonl"
TPC153_CERT = (
    TPC153 / "experiments" / "tpc153_cut_occurrence_shadow_certificate.json"
)
TPC163_CENSUS = TPC163 / "experiments" / "tpc163_source_census.json"
TPC163_AUDIT = TPC163 / "experiments" / "tpc163_source_census_audit.json"

SCHEMA = PAPER / "schemas" / "tpc164-minimal-key-v1.schema.json"
SAMPLE = PAPER / "samples" / "tpc164_minimal_key_witness.json"
CERT = HERE / "tpc164_minimal_key_certificate.json"
AUDIT = HERE / "tpc164_minimal_key_audit.json"

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCHEMA_ID = "tpc-164-minimal-archived-separation-key-v1"
FIELDS = ("ell", "k", "native_d", "jL", "jK", "D0", "reason", "type")
SELECTED = ("ell", "k", "native_d", "jL", "jK")


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def canonical_bytes(path: Path) -> bytes:
    text = normalize(path.read_text(encoding="utf-8"))
    if path.suffix == ".json":
        text = canonical_json(json.loads(text))
    elif not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def canonical_hash(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(normalize(path.read_text(encoding="utf-8")))
    if not isinstance(value, dict):
        raise ValueError(f"object expected: {path}")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    values: list[dict[str, Any]] = []
    for line in normalize(path.read_text(encoding="utf-8")).splitlines():
        if line.strip():
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError("JSONL row must be an object")
            values.append(value)
    return values


def source_lock(source_id: str, path: Path) -> dict[str, str]:
    return {
        "source_id": source_id,
        "path": rel(path),
        "canonical_utf8_lf_sha256": canonical_hash(path),
        "hash_mode": HASH_MODE,
        "hash_semantics": "INTEGRITY_ONLY",
    }


def archived_type(row: dict[str, Any]) -> str:
    native_d = int(row["lineage"]["native_tuple"][2])
    d0 = int(row["cut_classification"]["D0"])
    derived = "PREFIX" if native_d <= d0 else "TAIL"
    marker = row["source_cut_path_id"].rsplit("|type=", 1)[-1]
    if marker != derived:
        raise ValueError("derived cut type and archived identifier disagree")
    return derived


def feature_row(row: dict[str, Any]) -> dict[str, Any]:
    ell, k, native_d = row["lineage"]["native_tuple"]
    block = row["cut_classification"]["block"]
    return {
        "ell": int(ell),
        "k": int(k),
        "native_d": int(native_d),
        "jL": int(block["j_L"]),
        "jK": int(block["j_K"]),
        "D0": int(row["cut_classification"]["D0"]),
        "reason": row["cut_classification"]["frontier_reason"],
        "type": archived_type(row),
    }


def key_of(features: dict[str, Any], fields: Iterable[str]) -> tuple[Any, ...]:
    return tuple(features[field] for field in fields)


def key_stats(features: list[dict[str, Any]], fields: tuple[str, ...]) -> dict[str, int | bool]:
    counter = Counter(key_of(row, fields) for row in features)
    return {
        "distinct_key_count": len(counter),
        "maximum_multiplicity": max(counter.values()),
        "excess_rows_over_keys": len(features) - len(counter),
        "injective": len(counter) == len(features),
    }


def exhaustive_search(
    features: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[tuple[str, ...]], dict[int, int]]:
    records: list[dict[str, Any]] = []
    injective: list[tuple[str, ...]] = []
    injective_by_size: Counter[int] = Counter()
    for size in range(1, len(FIELDS) + 1):
        for fields in itertools.combinations(FIELDS, size):
            stats = key_stats(features, fields)
            records.append({"fields": list(fields), **stats})
            if stats["injective"]:
                injective.append(fields)
                injective_by_size[size] += 1
    return records, injective, dict(sorted(injective_by_size.items()))


def validate_candidate(
    cert: dict[str, Any],
    rows: list[dict[str, Any]],
    records: list[dict[str, Any]],
) -> None:
    if cert.get("schema") != SCHEMA_ID:
        raise ValueError("schema drift")
    if tuple(cert.get("selected_archived_key", ())) != SELECTED:
        raise ValueError("selected archived key drift")
    if cert.get("claim_boundary", {}).get("actual_occurrence_id_proved") is not False:
        raise ValueError("archive key promoted to occurrence ID")
    if cert.get("claim_boundary", {}).get(
        "canonical_minimal_representation_proved"
    ) is not False:
        raise ValueError("archive key promoted to canonical representation")
    expected_hashes = {
        item["source_id"]: item["canonical_utf8_lf_sha256"]
        for item in cert.get("source_locks", [])
    }
    actual_hashes = {
        "TPC153.shadow": canonical_hash(SHADOW),
        "TPC153.certificate": canonical_hash(TPC153_CERT),
        "TPC163.census": canonical_hash(TPC163_CENSUS),
        "TPC163.audit": canonical_hash(TPC163_AUDIT),
    }
    if expected_hashes != actual_hashes:
        raise ValueError("source lock drift")
    features = [feature_row(row) for row in rows]
    recomputed, injective, by_size = exhaustive_search(features)
    if recomputed != records:
        raise ValueError("exhaustive subset record drift")
    minimum = min(len(fields) for fields in injective)
    minimal = [fields for fields in injective if len(fields) == minimum]
    if minimum != 5 or minimal != [SELECTED] or by_size.get(5) != 1:
        raise ValueError("unique minimum separating key failed")


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    rows = load_jsonl(SHADOW)
    t153 = load_json(TPC153_CERT)
    t163 = load_json(TPC163_CENSUS)
    t163_audit = load_json(TPC163_AUDIT)
    if len(rows) != 2988 or t153.get("census", {}).get(
        "production_shadow_rows"
    ) != 2988:
        raise ValueError("TPC-153 row count drift")
    if t163_audit.get("status") != "PASS":
        raise ValueError("TPC-163 audit is not PASS")
    collision = t163.get("native_key_collision", {})
    if (
        collision.get("native_tuple_count") != 866
        or collision.get("excess_rows_over_native_keys") != 2122
    ):
        raise ValueError("TPC-163 collision theorem drift")
    path_ids = [row["source_cut_path_id"] for row in rows]
    if len(path_ids) != len(set(path_ids)):
        raise ValueError("source-cut path identifiers are not distinct")
    features = [feature_row(row) for row in rows]
    records, injective, by_size = exhaustive_search(features)
    minimum = min(len(fields) for fields in injective)
    minimal = [fields for fields in injective if len(fields) == minimum]
    if minimum != 5 or minimal != [SELECTED]:
        raise ValueError("expected unique five-field minimum not recovered")
    record_lookup = {
        tuple(record["fields"]): record for record in records
    }
    locks = [
        source_lock("TPC153.shadow", SHADOW),
        source_lock("TPC153.certificate", TPC153_CERT),
        source_lock("TPC163.census", TPC163_CENSUS),
        source_lock("TPC163.audit", TPC163_AUDIT),
    ]
    cert: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "scope": "FROZEN_TPC153_PRODUCTION_CUT_ARCHIVE",
        "source_locks": locks,
        "field_dictionary": list(FIELDS),
        "exhaustive_search": {
            "row_count": len(rows),
            "nonempty_subsets_tested": len(records),
            "minimum_cardinality": minimum,
            "minimum_key_count": len(minimal),
            "injective_key_count_by_cardinality": {
                str(size): count for size, count in by_size.items()
            },
        },
        "minimal_separating_keys": [list(fields) for fields in minimal],
        "selected_archived_key": list(SELECTED),
        "selected_key_statistics": record_lookup[SELECTED],
        "diagnostic_partial_keys": {
            "native_only": record_lookup[("ell", "k", "native_d")],
            "native_plus_reason": record_lookup[
                ("ell", "k", "native_d", "reason")
            ],
            "native_plus_jL": record_lookup[("ell", "k", "native_d", "jL")],
            "native_plus_jK": record_lookup[("ell", "k", "native_d", "jK")],
        },
        "all_subset_statistics": records,
        "claim_boundary": {
            "actual_occurrence_id_proved": False,
            "actual_active_support_proved": False,
            "canonical_minimal_representation_proved": False,
            "production_crosswalk_proved": False,
            "positive_fixed_X_L2": False,
            "twin_prime_theorem": False,
        },
    }
    target_native = (3, 171, 1)
    selected_rows = [
        (row, feature)
        for row, feature in zip(rows, features)
        if tuple(row["lineage"]["native_tuple"]) == target_native
    ]
    if len(selected_rows) != 4:
        raise ValueError("expected fourfold witness drift")
    sample_rows = []
    for row, feature in sorted(
        selected_rows, key=lambda item: key_of(item[1], SELECTED)
    ):
        sample_rows.append(
            {
                "source_cut_path_id": row["source_cut_path_id"],
                "field_values": feature,
                "native_key": list(key_of(feature, ("ell", "k", "native_d"))),
                "minimal_archived_key": list(key_of(feature, SELECTED)),
            }
        )
    sample = {
        "schema": "tpc-164-minimal-key-witness-v1",
        "scope": "PRODUCTION_ARCHIVE_EXCERPT",
        "native_collision": list(target_native),
        "rows": sample_rows,
        "statement": (
            "The unique minimum archived key separates this fourfold native "
            "collision; it is not an actual-occurrence identifier."
        ),
        "claim_boundary": {
            "actual_occurrence_data": False,
            "canonical_parent_data": False,
        },
    }
    validate_candidate(cert, rows, records)

    def rejected(mutator: Any) -> bool:
        candidate = copy.deepcopy(cert)
        mutator(candidate)
        try:
            validate_candidate(candidate, rows, records)
        except (KeyError, TypeError, ValueError):
            return True
        return False

    def source_drift(candidate: dict[str, Any]) -> None:
        candidate["source_locks"][0]["canonical_utf8_lf_sha256"] = "0" * 64

    def drop_jl(candidate: dict[str, Any]) -> None:
        candidate["selected_archived_key"] = [
            "ell", "k", "native_d", "jK"
        ]

    def drop_jk(candidate: dict[str, Any]) -> None:
        candidate["selected_archived_key"] = [
            "ell", "k", "native_d", "jL"
        ]

    def promote_occurrence(candidate: dict[str, Any]) -> None:
        candidate["claim_boundary"]["actual_occurrence_id_proved"] = True

    def promote_canonical(candidate: dict[str, Any]) -> None:
        candidate["claim_boundary"][
            "canonical_minimal_representation_proved"
        ] = True

    mutations = {
        "source_hash_drift_rejected": rejected(source_drift),
        "drop_jL_rejected": rejected(drop_jl),
        "drop_jK_rejected": rejected(drop_jk),
        "archive_key_to_occurrence_id_promotion_rejected": rejected(
            promote_occurrence
        ),
        "archive_key_to_canonical_representation_promotion_rejected": rejected(
            promote_canonical
        ),
    }
    if not all(mutations.values()):
        raise ValueError("mutation regression failed")
    audit = {
        "schema": "tpc-164-minimal-key-audit-v1",
        "status": "PASS",
        "certificate_sha256": hashlib.sha256(
            canonical_json(cert).encode("utf-8")
        ).hexdigest(),
        "checks": {
            "all_255_nonempty_field_subsets_recomputed": len(records) == 255,
            "unique_minimum_key_recomputed": minimal == [SELECTED],
            "all_2988_rows_separated": record_lookup[SELECTED][
                "distinct_key_count"
            ]
            == 2988,
            "source_locks_recomputed": True,
        },
        "mutation_regressions": mutations,
        "claim_boundary": cert["claim_boundary"],
    }
    return cert, sample, audit


def output_bytes(value: dict[str, Any]) -> bytes:
    return canonical_json(value).encode("utf-8")


def write_or_check(path: Path, value: dict[str, Any], check: bool) -> None:
    expected = output_bytes(value)
    if check:
        if not path.exists() or path.read_bytes() != expected:
            raise ValueError(f"generated artifact drift: {path}")
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(expected)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="recompute and require byte-identical generated artifacts",
    )
    args = parser.parse_args()
    cert, sample, audit = build()
    write_or_check(CERT, cert, args.check)
    write_or_check(SAMPLE, sample, args.check)
    write_or_check(AUDIT, audit, args.check)
    mode = "CHECK" if args.check else "GENERATE"
    summary = {
        "status": audit["status"],
        "rows": cert["exhaustive_search"]["row_count"],
        "subsets": cert["exhaustive_search"]["nonempty_subsets_tested"],
        "minimum_cardinality": cert["exhaustive_search"][
            "minimum_cardinality"
        ],
        "minimum_key_count": cert["exhaustive_search"]["minimum_key_count"],
        "selected_key": cert["selected_archived_key"],
    }
    print(f"TPC-164 {mode} PASS")
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
