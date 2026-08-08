"""Verify RH-389 archive membership, hashes, source identity, and replay gates."""

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

for directory in (ROOT, ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from experiments import build_result, build_schema, source_locks  # noqa: E402
from experiments.build_archive import (  # noqa: E402
    LOCAL_MEMBERS,
    REMOTE_DIGESTS,
    SOURCE_COMMITS,
    build_payload,
    digest,
    external_payload_exclusion,
    offline_remote_replay,
    validated_remote_locks,
    validated_result_git_source_map,
)
from experiments.verify_tao_source import loads_strict  # noqa: E402
from terminal_log_capacity.core import exact_equal, payload_sha256  # noqa: E402


BOOLEAN_KEYS = (
    "result_rebuild_match",
    "schema_rebuild_match",
    "result_source_lock_match",
    "release_blob_identity_pass",
    "source_digest_contract_pass",
    "logical_source_digest_pass",
    "exact_certificate_digest_pass",
    "remote_lock_exact_pass",
    "offline_remote_zero_requests",
    "remote_payload_excluded",
    "semantic_pdf_match",
)


def _safe_relative(relative: object) -> bool:
    if type(relative) is not str:
        return False
    path = Path(relative)
    return not path.is_absolute() and ".." not in path.parts


def _verify_map(base: Path, entries: object, label: str, failures: list[str]) -> int:
    if type(entries) is not dict:
        failures.append(f"{label}:not_an_object")
        return 0
    for relative, expected in entries.items():
        if not _safe_relative(relative):
            failures.append(f"{label}:{relative}:unsafe_path")
        elif type(expected) is not str or not SHA256.fullmatch(expected):
            failures.append(f"{label}:{relative}:invalid_sha256")
        else:
            try:
                path = base / relative
                if not path.is_file():
                    failures.append(f"{label}:{relative}:missing")
                elif digest(path) != expected:
                    failures.append(f"{label}:{relative}:hash_mismatch")
            except (OSError, ValueError):
                failures.append(f"{label}:unsafe_or_invalid_path")
    return len(entries)


def _failure_payload(failure: str) -> dict[str, object]:
    if type(failure) is not str:
        raise TypeError("archive failure label must be text")
    return {
        "status": "RH-389_archive_failed",
        "publication_file_count": 0,
        "release_stage_file_count": 0,
        "external_git_input_count": 0,
        "remote_logical_input_count": 0,
        "failure_count": 1,
        "failures": [failure],
        "manifest_rebuild_match": False,
        **{key: False for key in BOOLEAN_KEYS},
    }


def verify_manifest(manifest: object) -> dict[str, object]:
    if type(manifest) is not dict:
        return _failure_payload("manifest:top_level_not_an_object")
    failures: list[str] = []
    expected_keys = {
        "status", "publication_file_count", "publication_artifacts",
        "release_stage_file_count", "external_git_input_count", "external_git_inputs",
        "remote_logical_input_count", "remote_source_lock_sha256",
        "logical_source_digest", "source_commits", "offline_remote_replay", *BOOLEAN_KEYS,
    }
    if set(manifest) != expected_keys:
        failures.append("manifest:top_level_membership")
    if manifest.get("status") != "RH-389_fixed_publication_manifest":
        failures.append("manifest:status")

    local_entries = manifest.get("publication_artifacts")
    external_entries = manifest.get("external_git_inputs")
    local_count = _verify_map(ROOT, local_entries, "local", failures)
    external_count = _verify_map(WORKSPACE, external_entries, "external_git", failures)
    if type(manifest.get("publication_file_count")) is not int or manifest.get("publication_file_count") != local_count:
        failures.append("manifest:publication_file_count")
    if type(manifest.get("release_stage_file_count")) is not int or manifest.get("release_stage_file_count") != len(LOCAL_MEMBERS) + 2:
        failures.append("manifest:release_stage_file_count")
    if type(manifest.get("external_git_input_count")) is not int or manifest.get("external_git_input_count") != external_count:
        failures.append("manifest:external_git_input_count")
    if local_count != len(LOCAL_MEMBERS) or type(local_entries) is not dict or set(local_entries) != set(LOCAL_MEMBERS):
        failures.append("manifest:publication_membership")
    if external_count != 95:
        failures.append("manifest:external_git_membership")
    if type(manifest.get("remote_logical_input_count")) is not int or manifest.get("remote_logical_input_count") != 3:
        failures.append("manifest:remote_logical_input_count")
    if not exact_equal(manifest.get("source_commits"), SOURCE_COMMITS):
        failures.append("manifest:source_commits")
    if (
        type(manifest.get("logical_source_digest")) is not str
        or manifest.get("logical_source_digest") != source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    ):
        failures.append("manifest:logical_source_digest")
    if not exact_equal(manifest.get("remote_source_lock_sha256"), REMOTE_DIGESTS):
        failures.append("manifest:remote_source_lock_sha256")

    result_rebuild = schema_rebuild = result_match = False
    release_pass = digest_pass = logical_pass = certificate_pass = remote_pass = False
    try:
        result = loads_strict((ROOT / "results" / "result.json").read_text(encoding="utf-8"))
        schema = loads_strict((ROOT / "results" / "result.schema.json").read_text(encoding="utf-8"))
        result_rebuild = exact_equal(result, build_result.build_payload())
        schema_rebuild = exact_equal(schema, build_schema.build_schema())
        result_files = validated_result_git_source_map(result)
        result_match = exact_equal(result_files, external_entries)
        git_locks = result["source_locks"]["git"]
        release_pass = git_locks.get("release_identity_pass") is True
        digest_pass = git_locks.get("digest_contract_pass") is True
        source_contract = result["source_locks"]
        logical_pass = (
            source_contract.get("logical_source_digest") == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
            and source_contract.get("logical_digest_pass") is True
            and source_contract.get("pass") is True
        )
        certificate = result.get("certificate")
        certificate_pass = (
            type(certificate) is dict
            and payload_sha256(certificate) == build_result.CERTIFICATE_FIXTURE_SHA256
        )
        remote = validated_remote_locks(result)
        remote_pass = exact_equal(remote.get("canonical_digests"), REMOTE_DIGESTS)
    except (KeyError, OSError, RuntimeError, TypeError, ValueError) as exc:
        failures.append(f"result:invalid:{type(exc).__name__}")

    offline_rows: list[dict[str, object]] = []
    offline_pass = False
    try:
        offline_rows = list(offline_remote_replay())
        offline_pass = len(offline_rows) == 3 and all(
            row.get("status") == "NETWORK_DISABLED"
            and row.get("network_opt_in") is False
            and type(row.get("requests_made")) is int
            and row.get("requests_made") == 0
            for row in offline_rows
        )
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        failures.append(f"remote:offline_replay:{type(exc).__name__}")
    if not exact_equal(manifest.get("offline_remote_replay"), offline_rows):
        failures.append("manifest:offline_remote_replay")

    payload_excluded = external_payload_exclusion()
    semantic_match = (
        type(local_entries) is dict
        and local_entries.get("main.pdf") == local_entries.get("active-c11-terminal-log-all-clock-capacity.pdf")
    )
    current = {
        "result_rebuild_match": result_rebuild,
        "schema_rebuild_match": schema_rebuild,
        "result_source_lock_match": result_match,
        "release_blob_identity_pass": release_pass,
        "source_digest_contract_pass": digest_pass,
        "logical_source_digest_pass": logical_pass,
        "exact_certificate_digest_pass": certificate_pass,
        "remote_lock_exact_pass": remote_pass,
        "offline_remote_zero_requests": offline_pass,
        "remote_payload_excluded": payload_excluded,
        "semantic_pdf_match": semantic_match,
    }
    for key, value in current.items():
        if value is not True or manifest.get(key) is not True:
            failures.append(f"manifest:{key}")

    rebuild_match = False
    try:
        rebuild_match = exact_equal(manifest, build_payload())
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        failures.append(f"manifest:rebuild_error:{type(exc).__name__}")
    else:
        if not rebuild_match:
            failures.append("manifest:rebuild_mismatch")

    return {
        "status": "RH-389_archive_verified" if not failures else "RH-389_archive_failed",
        "publication_file_count": local_count,
        "release_stage_file_count": len(LOCAL_MEMBERS) + 2 if not failures else 0,
        "external_git_input_count": external_count,
        "remote_logical_input_count": 3 if remote_pass else 0,
        "failure_count": len(failures),
        "failures": failures,
        "manifest_rebuild_match": rebuild_match,
        **current,
    }


def serialized_report(payload: dict[str, object]) -> str:
    if type(payload) is not dict:
        raise TypeError("archive report must be an exact object")
    return json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    try:
        manifest = loads_strict(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, TypeError, ValueError) as exc:
        payload = _failure_payload(f"manifest:invalid:{type(exc).__name__}")
    else:
        payload = verify_manifest(manifest)
    OUTPUT.write_text(serialized_report(payload), encoding="utf-8")
    print(json.dumps(payload, sort_keys=True))
    if payload["failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
