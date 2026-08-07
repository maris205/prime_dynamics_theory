"""Verify RH-382 manifest membership, hashes, and source-lock identity."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
MANIFEST = ROOT / "results" / "dependency_manifest.json"
OUTPUT = ROOT / "results" / "archive_verification.json"
SHA256 = re.compile(r"^[0-9a-f]{64}$")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from experiments.build_archive import (  # noqa: E402
    LOCAL_MEMBERS,
    SOURCE_COMMITS,
    SOURCE_FILES,
    build_payload,
    digest,
    load_json,
    validated_result_source_map,
)
from two_scale_tail import CERTIFICATE_FIXTURE_SHA256, payload_sha256  # noqa: E402


def _safe_relative(relative: object) -> bool:
    if type(relative) is not str:
        return False
    path = Path(relative)
    return not path.is_absolute() and ".." not in path.parts


def _verify_map(base: Path, entries: object, label: str, failures: list[str]) -> int:
    if type(entries) is not dict:
        failures.append(f"{label}:not_an_object")
        return 0
    count = 0
    for relative, expected in entries.items():
        count += 1
        if not _safe_relative(relative):
            failures.append(f"{label}:{relative}:unsafe_path")
            continue
        if type(expected) is not str or not SHA256.fullmatch(expected):
            failures.append(f"{label}:{relative}:invalid_sha256")
            continue
        path = base / relative
        if not path.is_file():
            failures.append(f"{label}:{relative}:missing")
            continue
        if digest(path) != expected:
            failures.append(f"{label}:{relative}:hash_mismatch")
    return count


def verify_manifest(manifest: dict[str, object]) -> dict[str, object]:
    failures: list[str] = []
    expected_keys = {
        "status", "publication_file_count", "publication_artifacts",
        "external_input_count", "external_inputs", "source_commits",
        "result_source_lock_match", "release_blob_identity_pass",
        "source_digest_contract_pass", "exact_certificate_digest_pass",
        "semantic_pdf_match",
    }
    if type(manifest) is not dict or set(manifest) != expected_keys:
        failures.append("manifest:top_level_membership")
    if manifest.get("status") != "RH-382_fixed_publication_manifest":
        failures.append("manifest:status")

    local_entries = manifest.get("publication_artifacts")
    external_entries = manifest.get("external_inputs")
    local_count = _verify_map(ROOT, local_entries, "local", failures)
    external_count = _verify_map(WORKSPACE, external_entries, "external", failures)
    if type(manifest.get("publication_file_count")) is not int or manifest.get("publication_file_count") != local_count:
        failures.append("manifest:publication_file_count")
    if type(manifest.get("external_input_count")) is not int or manifest.get("external_input_count") != external_count:
        failures.append("manifest:external_input_count")
    if local_count != len(LOCAL_MEMBERS):
        failures.append("manifest:publication_membership_count")
    elif type(local_entries) is dict and set(local_entries) != set(LOCAL_MEMBERS):
        failures.append("manifest:publication_membership_set")
    if external_count != len(SOURCE_FILES):
        failures.append("manifest:external_membership_count")
    elif type(external_entries) is dict and set(external_entries) != set(SOURCE_FILES):
        failures.append("manifest:external_membership_set")
    if manifest.get("source_commits") != SOURCE_COMMITS:
        failures.append("manifest:source_commits")

    try:
        result = load_json(ROOT / "results/result.json")
        result_files = validated_result_source_map(result)
        source_locks = result["source_locks"]
        release_pass = source_locks.get("release_blob_identity_pass") is True
        digest_pass = source_locks.get("digest_contract_pass") is True
        certificate = result.get("certificate")
        certificate_pass = type(certificate) is dict and payload_sha256(certificate) == CERTIFICATE_FIXTURE_SHA256
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError, KeyError, TypeError) as exc:
        failures.append(f"result:invalid:{type(exc).__name__}")
        result_files = None
        release_pass = digest_pass = certificate_pass = False

    result_source_lock_match = result_files == external_entries
    if not result_source_lock_match or manifest.get("result_source_lock_match") is not True:
        failures.append("manifest:result_source_lock_match")
    if not release_pass or manifest.get("release_blob_identity_pass") is not True:
        failures.append("manifest:release_blob_identity_pass")
    if not digest_pass or manifest.get("source_digest_contract_pass") is not True:
        failures.append("manifest:source_digest_contract_pass")
    if not certificate_pass or manifest.get("exact_certificate_digest_pass") is not True:
        failures.append("manifest:exact_certificate_digest_pass")

    semantic_pdf_match = False
    if type(local_entries) is dict:
        semantic_pdf_match = local_entries.get("main.pdf") == local_entries.get("two-scale-prime-square-tail-expansion.pdf")
    if not semantic_pdf_match or manifest.get("semantic_pdf_match") is not True:
        failures.append("manifest:semantic_pdf_match")

    manifest_rebuild_match = False
    try:
        manifest_rebuild_match = manifest == build_payload()
    except (OSError, RuntimeError, ValueError, TypeError) as exc:
        failures.append(f"manifest:rebuild_error:{type(exc).__name__}")
    else:
        if not manifest_rebuild_match:
            failures.append("manifest:rebuild_mismatch")

    return {
        "status": "RH-382_archive_verified" if not failures else "RH-382_archive_failed",
        "publication_file_count": local_count,
        "external_input_count": external_count,
        "failure_count": len(failures),
        "failures": failures,
        "manifest_rebuild_match": manifest_rebuild_match,
        "result_source_lock_match": result_source_lock_match,
        "release_blob_identity_pass": release_pass,
        "source_digest_contract_pass": digest_pass,
        "exact_certificate_digest_pass": certificate_pass,
        "semantic_pdf_match": semantic_pdf_match,
    }


def main() -> None:
    try:
        manifest = load_json(MANIFEST)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        payload = {
            "status": "RH-382_archive_failed",
            "publication_file_count": 0,
            "external_input_count": 0,
            "failure_count": 1,
            "failures": [f"manifest:invalid:{type(exc).__name__}"],
            "manifest_rebuild_match": False,
            "result_source_lock_match": False,
            "release_blob_identity_pass": False,
            "source_digest_contract_pass": False,
            "exact_certificate_digest_pass": False,
            "semantic_pdf_match": False,
        }
    else:
        payload = verify_manifest(manifest)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(json.dumps(payload, sort_keys=True))
    if payload["failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
