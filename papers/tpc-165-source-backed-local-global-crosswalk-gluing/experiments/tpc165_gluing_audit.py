#!/usr/bin/env python3
"""Build and audit the TPC-165 finite local-to-global gluing interface."""

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

TPC163 = PAPERS / "tpc-163-source-locator-census-native-key-collision"
TPC164 = PAPERS / "tpc-164-minimal-archived-separation-key"
TPC163_CENSUS = TPC163 / "experiments" / "tpc163_source_census.json"
TPC163_AUDIT = TPC163 / "experiments" / "tpc163_source_census_audit.json"
TPC164_CERT = TPC164 / "experiments" / "tpc164_minimal_key_certificate.json"
TPC164_AUDIT = TPC164 / "experiments" / "tpc164_minimal_key_audit.json"

SCHEMA = PAPER / "schemas" / "tpc165-local-global-gluing-v1.schema.json"
SAMPLE = PAPER / "samples" / "tpc165_synthetic_local_patches.json"
CERT = HERE / "tpc165_gluing_certificate.json"
AUDIT = HERE / "tpc165_gluing_audit.json"

HASH_MODE = "CANONICAL_UTF8_LF_V2"
SCHEMA_ID = "tpc-165-local-global-crosswalk-gluing-v1"


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


def source_lock(source_id: str, path: Path) -> dict[str, str]:
    return {
        "source_id": source_id,
        "path": rel(path),
        "canonical_utf8_lf_sha256": canonical_hash(path),
        "hash_mode": HASH_MODE,
        "hash_semantics": "INTEGRITY_ONLY",
    }


def fraction(record: dict[str, Any]) -> Fraction:
    numerator = record.get("numerator")
    denominator = record.get("denominator")
    if not isinstance(numerator, int) or not isinstance(denominator, int):
        raise ValueError("exact rational weight required")
    if denominator <= 0:
        raise ValueError("positive denominator required")
    return Fraction(numerator, denominator)


def row_lookup(fixture: dict[str, Any]) -> dict[tuple[str, str, str], dict[str, Any]]:
    lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    for patch in fixture["patches"]:
        patch_id = patch["patch_id"]
        for cut, rows in patch["local_rows_by_cut"].items():
            if cut not in patch["cut_keys"] or not rows:
                raise ValueError("local patch totality failed")
            for row in rows:
                key = (patch_id, cut, row["local_row_id"])
                if key in lookup:
                    raise ValueError("duplicate local row identifier")
                fraction(row["weight"])
                lookup[key] = row
    return lookup


def validate_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    if fixture.get("evidence_mode") != "SYNTHETIC_REACHABILITY":
        raise ValueError("synthetic fixture mode required")
    if fixture.get("theorem_semantics") is not False:
        raise ValueError("synthetic fixture cannot carry theorem semantics")
    cuts = fixture["cut_universe"]
    if len(cuts) != len(set(cuts)):
        raise ValueError("duplicate cut key")
    patches = fixture["patches"]
    patch_ids = [patch["patch_id"] for patch in patches]
    if len(patch_ids) != len(set(patch_ids)):
        raise ValueError("duplicate patch identifier")
    patch_by_id = {patch["patch_id"]: patch for patch in patches}
    covered = {
        cut for patch in patches for cut in patch["cut_keys"]
    }
    if covered != set(cuts):
        raise ValueError("patch cover is not total")
    lookup = row_lookup(fixture)
    for patch in patches:
        if set(patch["local_rows_by_cut"]) != set(patch["cut_keys"]):
            raise ValueError("local row family domain drift")
        for cut, rows in patch["local_rows_by_cut"].items():
            if sum((fraction(row["weight"]) for row in rows), Fraction()) != 1:
                raise ValueError(f"local column sum is not one: {cut}")

    maps: dict[tuple[str, str, str], dict[str, str]] = {}
    for record in fixture["overlap_maps"]:
        left = record["from_patch"]
        right = record["to_patch"]
        cut = record["cut_key"]
        if left == right or left not in patch_by_id or right not in patch_by_id:
            raise ValueError("invalid overlap patch pair")
        if cut not in patch_by_id[left]["cut_keys"] or cut not in patch_by_id[
            right
        ]["cut_keys"]:
            raise ValueError("overlap map outside patch intersection")
        key = (left, right, cut)
        if key in maps:
            raise ValueError("duplicate oriented overlap map")
        mapping = record["row_bijection"]
        left_ids = {
            row["local_row_id"]
            for row in patch_by_id[left]["local_rows_by_cut"][cut]
        }
        right_ids = {
            row["local_row_id"]
            for row in patch_by_id[right]["local_rows_by_cut"][cut]
        }
        if set(mapping) != left_ids or set(mapping.values()) != right_ids:
            raise ValueError("overlap map is not a bijection")
        for source_id, target_id in mapping.items():
            source = lookup[(left, cut, source_id)]
            target = lookup[(right, cut, target_id)]
            if source["typed_payload"] != target["typed_payload"]:
                raise ValueError("typed payload is not preserved")
            if fraction(source["weight"]) != fraction(target["weight"]):
                raise ValueError("exact weight is not preserved")
        maps[key] = mapping
        maps[(right, left, cut)] = {
            target: source for source, target in mapping.items()
        }

    for left_index, left in enumerate(patch_ids):
        for right in patch_ids[left_index + 1 :]:
            overlap = set(patch_by_id[left]["cut_keys"]) & set(
                patch_by_id[right]["cut_keys"]
            )
            for cut in overlap:
                if (left, right, cut) not in maps:
                    raise ValueError("missing overlap bijection")

    for first in patch_ids:
        for second in patch_ids:
            for third in patch_ids:
                common = (
                    set(patch_by_id[first]["cut_keys"])
                    & set(patch_by_id[second]["cut_keys"])
                    & set(patch_by_id[third]["cut_keys"])
                )
                for cut in common:
                    if first == second or second == third or first == third:
                        continue
                    direct = maps[(first, third, cut)]
                    first_leg = maps[(first, second, cut)]
                    second_leg = maps[(second, third, cut)]
                    for local_id, direct_target in direct.items():
                        if second_leg[first_leg[local_id]] != direct_target:
                            raise ValueError("triple-overlap cocycle failed")

    parent: dict[tuple[str, str, str], tuple[str, str, str]] = {
        key: key for key in lookup
    }

    def find(key: tuple[str, str, str]) -> tuple[str, str, str]:
        while parent[key] != key:
            parent[key] = parent[parent[key]]
            key = parent[key]
        return key

    def union(
        left: tuple[str, str, str], right: tuple[str, str, str]
    ) -> None:
        root_left = find(left)
        root_right = find(right)
        if root_left != root_right:
            parent[root_right] = root_left

    for (left, right, cut), mapping in maps.items():
        if left < right:
            for source_id, target_id in mapping.items():
                union(
                    (left, cut, source_id),
                    (right, cut, target_id),
                )
    classes: dict[tuple[str, str, str], list[tuple[str, str, str]]] = {}
    for key in lookup:
        classes.setdefault(find(key), []).append(key)
    global_by_cut: dict[str, list[tuple[str, str, str]]] = {
        cut: [] for cut in cuts
    }
    for root, members in classes.items():
        member_cuts = {member[1] for member in members}
        if len(member_cuts) != 1:
            raise ValueError("gluing merged rows from different cuts")
        cut = next(iter(member_cuts))
        payloads = [lookup[member]["typed_payload"] for member in members]
        weights = [fraction(lookup[member]["weight"]) for member in members]
        if any(payload != payloads[0] for payload in payloads[1:]):
            raise ValueError("payload failed to descend")
        if any(weight != weights[0] for weight in weights[1:]):
            raise ValueError("weight failed to descend")
        global_by_cut[cut].append(root)
    for cut, roots in global_by_cut.items():
        if sum(
            (fraction(lookup[root]["weight"]) for root in roots), Fraction()
        ) != 1:
            raise ValueError(f"global column sum is not one: {cut}")
    return {
        "validation": "PASS",
        "cut_count": len(cuts),
        "patch_count": len(patches),
        "local_row_copy_count": len(lookup),
        "global_formal_row_count": len(classes),
        "global_column_sums_are_one": True,
        "overlap_bijections_complete": True,
        "cocycle_satisfied": True,
    }


def base_fixture() -> dict[str, Any]:
    def row(local_id: str, symbol: str, address: list[int]) -> dict[str, Any]:
        return {
            "local_row_id": local_id,
            "weight": {"numerator": 1, "denominator": 1, "ring": "Q"},
            "typed_payload": {
                "formal_occurrence_symbol": symbol,
                "archived_source_address": address,
                "semantic_class": "FORMAL_OCCURRENCE_ROW",
                "actual_occurrence_semantics": False,
                "actual_active_support": "UNDECIDED",
                "canonical_minimal_representation": "UNDECIDED",
            },
        }

    return {
        "schema": "tpc-165-synthetic-local-patches-v1",
        "evidence_mode": "SYNTHETIC_REACHABILITY",
        "theorem_semantics": False,
        "cut_universe": ["c1", "c2", "c3"],
        "patches": [
            {
                "patch_id": "U1",
                "cut_keys": ["c1", "c2"],
                "local_rows_by_cut": {
                    "c1": [row("u1-r1", "omega-1", [11, 21, 1, 2, 3])],
                    "c2": [row("u1-r2", "omega-2", [12, 22, 1, 3, 4])],
                },
            },
            {
                "patch_id": "U2",
                "cut_keys": ["c2", "c3"],
                "local_rows_by_cut": {
                    "c2": [row("u2-r2", "omega-2", [12, 22, 1, 3, 4])],
                    "c3": [row("u2-r3", "omega-3", [13, 23, 1, 4, 5])],
                },
            },
        ],
        "overlap_maps": [
            {
                "from_patch": "U1",
                "to_patch": "U2",
                "cut_key": "c2",
                "row_bijection": {"u1-r2": "u2-r2"},
            }
        ],
        "claim_boundary": {
            "synthetic_only": True,
            "production_local_patch": False,
            "actual_active_support": False,
            "canonical_minimal_representation": False,
        },
    }


def triangle_fixture() -> dict[str, Any]:
    patches = []
    for patch_id in ("A", "B", "C"):
        rows = []
        for suffix in ("0", "1"):
            rows.append(
                {
                    "local_row_id": f"{patch_id}-{suffix}",
                    "weight": {
                        "numerator": 1,
                        "denominator": 2,
                        "ring": "Q",
                    },
                    "typed_payload": {
                        "formal_occurrence_symbol": "same-payload",
                        "archived_source_address": [1, 1, 1, 1, 1],
                        "semantic_class": "FORMAL_OCCURRENCE_ROW",
                        "actual_occurrence_semantics": False,
                        "actual_active_support": "UNDECIDED",
                        "canonical_minimal_representation": "UNDECIDED",
                    },
                }
            )
        patches.append(
            {
                "patch_id": patch_id,
                "cut_keys": ["c"],
                "local_rows_by_cut": {"c": rows},
            }
        )
    return {
        "schema": "tpc-165-synthetic-cocycle-regression-v1",
        "evidence_mode": "SYNTHETIC_REACHABILITY",
        "theorem_semantics": False,
        "cut_universe": ["c"],
        "patches": patches,
        "overlap_maps": [
            {
                "from_patch": "A",
                "to_patch": "B",
                "cut_key": "c",
                "row_bijection": {"A-0": "B-0", "A-1": "B-1"},
            },
            {
                "from_patch": "A",
                "to_patch": "C",
                "cut_key": "c",
                "row_bijection": {"A-0": "C-0", "A-1": "C-1"},
            },
            {
                "from_patch": "B",
                "to_patch": "C",
                "cut_key": "c",
                "row_bijection": {"B-0": "C-0", "B-1": "C-1"},
            },
        ],
        "claim_boundary": {"synthetic_only": True},
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    if cert.get("schema") != SCHEMA_ID:
        raise ValueError("certificate schema drift")
    locks = {
        item["source_id"]: item["canonical_utf8_lf_sha256"]
        for item in cert.get("source_locks", [])
    }
    expected = {
        "TPC163.census": canonical_hash(TPC163_CENSUS),
        "TPC163.audit": canonical_hash(TPC163_AUDIT),
        "TPC164.certificate": canonical_hash(TPC164_CERT),
        "TPC164.audit": canonical_hash(TPC164_AUDIT),
    }
    if locks != expected:
        raise ValueError("source-lock drift")
    production = cert.get("production_status", {})
    if production.get("source_backed_local_edge_count") != 0:
        raise ValueError("production local edges fabricated")
    if production.get("local_patch_family_status") != "NOT_TESTABLE":
        raise ValueError("production local-patch status promoted")
    gates = cert.get("three_gate_separation", {})
    if set(gates) != {
        "formal_occurrence_totality",
        "actual_active_support",
        "canonical_minimal_representation",
    }:
        raise ValueError("three-gate interface drift")
    if any(gates[name]["production_status"] != "NOT_TESTABLE" for name in gates):
        raise ValueError("production gate promoted")


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    t163 = load_json(TPC163_CENSUS)
    t163_audit = load_json(TPC163_AUDIT)
    t164 = load_json(TPC164_CERT)
    t164_audit = load_json(TPC164_AUDIT)
    if t163_audit.get("status") != "PASS" or t164_audit.get("status") != "PASS":
        raise ValueError("upstream audit is not PASS")
    if t163.get("production_crosswalk_edge_census", {}).get(
        "theorem_backed_edge_count"
    ) != 0:
        raise ValueError("TPC-163 production edge census drift")
    if t164.get("selected_archived_key") != [
        "ell", "k", "native_d", "jL", "jK"
    ]:
        raise ValueError("TPC-164 archive key drift")
    fixture = base_fixture()
    fixture_result = validate_fixture(fixture)
    triangle = triangle_fixture()
    validate_fixture(triangle)
    locks = [
        source_lock("TPC163.census", TPC163_CENSUS),
        source_lock("TPC163.audit", TPC163_AUDIT),
        source_lock("TPC164.certificate", TPC164_CERT),
        source_lock("TPC164.audit", TPC164_AUDIT),
    ]
    cert: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "source_locks": locks,
        "formal_gluing_theorem": {
            "local_totality": (
                "Every cut in every patch has a finite nonempty local row "
                "family."
            ),
            "overlap_bijections": (
                "Local rows over each pairwise overlap are related by exact "
                "typed weight-preserving bijections."
            ),
            "cocycle": (
                "The overlap bijections satisfy identity, inverse, and "
                "triple-overlap composition."
            ),
            "typed_payload_preservation": True,
            "exact_column_conservation": (
                "Local rational column sums equal to one descend to global "
                "rational column sums equal to one."
            ),
            "conclusion": (
                "The quotient gives a global formal row family, unique up to "
                "the unique typed isomorphism commuting with all local maps."
            ),
            "theorem_level": "PROVED_L0_FORMAL",
        },
        "production_status": {
            "source_backed_local_edge_count": 0,
            "local_patch_family_status": "NOT_TESTABLE",
            "overlap_cocycle_status": "NOT_TESTABLE",
            "formal_occurrence_totality": "NOT_TESTABLE",
            "reason": (
                "TPC-163 finds no theorem-backed production actual-occurrence "
                "edge in the frozen declared corpus."
            ),
        },
        "synthetic_nonvacuity": {
            "evidence_mode": "SYNTHETIC_REACHABILITY",
            "theorem_semantics": False,
            **fixture_result,
        },
        "three_gate_separation": {
            "formal_occurrence_totality": {
                "production_status": "NOT_TESTABLE",
                "meaning": "every archived cut has at least one glued formal row",
            },
            "actual_active_support": {
                "production_status": "NOT_TESTABLE",
                "meaning": "the glued row is present with nonzero physical coefficient",
            },
            "canonical_minimal_representation": {
                "production_status": "NOT_TESTABLE",
                "meaning": "the actual carrier has an independently proved canonical or minimal parent",
            },
        },
        "claim_boundary": {
            "synthetic_fixture_is_production_evidence": False,
            "formal_gluing_implies_actual_active_support": False,
            "formal_gluing_implies_canonical_minimal_representation": False,
            "occurrence_witness_verifier_pass_implies_active_support": False,
            "occurrence_witness_verifier_pass_implies_canonical_minimality": False,
            "production_crosswalk_proved": False,
            "positive_fixed_X_L2": False,
            "twin_prime_theorem": False,
        },
    }
    validate_certificate(cert)

    def fixture_rejected(mutator: Any, candidate: dict[str, Any] | None = None) -> bool:
        value = copy.deepcopy(fixture if candidate is None else candidate)
        mutator(value)
        try:
            validate_fixture(value)
        except (KeyError, TypeError, ValueError):
            return True
        return False

    def delete_overlap(value: dict[str, Any]) -> None:
        value["overlap_maps"] = []

    def change_payload(value: dict[str, Any]) -> None:
        value["patches"][1]["local_rows_by_cut"]["c2"][0][
            "typed_payload"
        ]["formal_occurrence_symbol"] = "drift"

    def change_weight(value: dict[str, Any]) -> None:
        value["patches"][1]["local_rows_by_cut"]["c2"][0]["weight"] = {
            "numerator": 2,
            "denominator": 1,
            "ring": "Q",
        }

    def promote_fixture(value: dict[str, Any]) -> None:
        value["theorem_semantics"] = True

    bad_triangle = copy.deepcopy(triangle)

    def break_cocycle(value: dict[str, Any]) -> None:
        value["overlap_maps"][1]["row_bijection"] = {
            "A-0": "C-1",
            "A-1": "C-0",
        }

    def cert_rejected(mutator: Any) -> bool:
        value = copy.deepcopy(cert)
        mutator(value)
        try:
            validate_certificate(value)
        except (KeyError, TypeError, ValueError):
            return True
        return False

    def fabricate_production(value: dict[str, Any]) -> None:
        value["production_status"]["source_backed_local_edge_count"] = 1

    def promote_support(value: dict[str, Any]) -> None:
        value["three_gate_separation"]["actual_active_support"][
            "production_status"
        ] = "PROVED"

    mutations = {
        "missing_overlap_bijection_rejected": fixture_rejected(delete_overlap),
        "overlap_payload_drift_rejected": fixture_rejected(change_payload),
        "overlap_weight_drift_rejected": fixture_rejected(change_weight),
        "synthetic_to_theorem_promotion_rejected": fixture_rejected(
            promote_fixture
        ),
        "triple_overlap_cocycle_break_rejected": fixture_rejected(
            break_cocycle, bad_triangle
        ),
        "fabricated_production_local_edge_rejected": cert_rejected(
            fabricate_production
        ),
        "active_support_gate_promotion_rejected": cert_rejected(
            promote_support
        ),
    }
    if not all(mutations.values()):
        raise ValueError("mutation regression failed")
    audit = {
        "schema": "tpc-165-local-global-gluing-audit-v1",
        "status": "PASS",
        "certificate_sha256": hashlib.sha256(
            canonical_json(cert).encode("utf-8")
        ).hexdigest(),
        "synthetic_fixture_sha256": hashlib.sha256(
            canonical_json(fixture).encode("utf-8")
        ).hexdigest(),
        "checks": {
            "upstream_source_locks_recomputed": True,
            "synthetic_two_patch_gluing_nonvacuous": True,
            "exact_column_conservation_recomputed": True,
            "three_gate_separation_preserved": True,
            "production_local_edge_count_remains_zero": True,
        },
        "mutation_regressions": mutations,
        "claim_boundary": cert["claim_boundary"],
    }
    return cert, fixture, audit


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
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    cert, fixture, audit = build()
    write_or_check(CERT, cert, args.check)
    write_or_check(SAMPLE, fixture, args.check)
    write_or_check(AUDIT, audit, args.check)
    mode = "CHECK" if args.check else "GENERATE"
    print(f"TPC-165 {mode} PASS")
    print(
        json.dumps(
            {
                "status": audit["status"],
                "synthetic_global_rows": cert["synthetic_nonvacuity"][
                    "global_formal_row_count"
                ],
                "production_local_edges": cert["production_status"][
                    "source_backed_local_edge_count"
                ],
                "production_status": cert["production_status"][
                    "local_patch_family_status"
                ],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
