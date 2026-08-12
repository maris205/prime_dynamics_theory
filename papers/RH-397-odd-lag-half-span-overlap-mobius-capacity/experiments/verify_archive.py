"""Verify RH-397 archive membership, hashes, sources, and replay gates."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
MANIFEST = ROOT / "results" / "dependency_manifest.json"
OUTPUT = ROOT / "results" / "archive_verification.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
for directory in (ROOT, ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from experiments import source_locks  # noqa: E402
from experiments.build_archive import (  # noqa: E402
    BOOLEAN_KEYS,
    LOCAL_MEMBERS,
    ALL_GIT_SOURCE_DIGEST,
    REMOTE_DIGESTS,
    REMOTE_KEYS,
    REMOTE_REDISTRIBUTION,
    SOURCE_COMMITS,
    SOURCE_GROUP_DIGESTS,
    SOURCE_GROUP_SIZES,
    build_payload,
    digest,
    offline_remote_replay,
)
from odd_lag_half_span_capacity.core import exact_equal, loads_strict  # noqa: E402


COUNT_KEYS = (
    "remote_payload_hash_count",
    "publication_payload_hash_hit_count",
    "tree_payload_hash_hit_count",
    "tree_symlink_count",
    "cache_path_count",
    "pyc_file_count",
    "sentinel_path_count",
    "sentinel_content_hit_count",
    "unlisted_regular_file_count",
    "special_path_count",
    "carriage_return_count",
    "text_eof_defect_count",
)


def _safe_relative(relative: object) -> bool:
    if type(relative) is not str or not relative or len(relative) > 4096:
        return False
    path = Path(relative)
    return not path.is_absolute() and ".." not in path.parts


def _verify_map(base: Path, entries: object, label: str, failures: list[str]) -> int:
    if type(entries) is not dict:
        failures.append(f"{label}:not_an_object")
        return 0
    for relative, expected in entries.items():
        if not _safe_relative(relative):
            failures.append(f"{label}:unsafe_path")
            continue
        if type(expected) is not str or not SHA256_RE.fullmatch(expected):
            failures.append(f"{label}:{relative}:invalid_sha256")
            continue
        try:
            path = base / relative
            if not path.is_file() or path.is_symlink():
                failures.append(f"{label}:{relative}:missing_or_nonregular")
            elif digest(path) != expected:
                failures.append(f"{label}:{relative}:hash_mismatch")
        except (OSError, ValueError):
            failures.append(f"{label}:{relative}:unreadable")
    return len(entries)


def _failure_payload(failure: str) -> dict[str, object]:
    if type(failure) is not str:
        raise TypeError("archive failure label must be text")
    return {
        "status": "RH-397_archive_failed",
        "publication_file_count": 0,
        "release_stage_file_count": 0,
        "external_git_input_count": 0,
        "remote_logical_input_count": 0,
        "logical_input_total": 0,
        **{key: 0 for key in COUNT_KEYS},
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
        "status",
        "publication_file_count",
        "publication_artifacts",
        "release_stage_file_count",
        "external_git_input_count",
        "external_git_inputs",
        "git_group_sizes",
        "git_group_digests",
        "all_git_source_digest",
        "remote_logical_input_count",
        "logical_input_total",
        "remote_source_lock_sha256",
        "remote_redistributable_in_release",
        "logical_source_digest",
        "source_commits",
        "offline_remote_replay",
        *COUNT_KEYS,
        *BOOLEAN_KEYS,
    }
    if set(manifest) != expected_keys:
        failures.append("manifest:top_level_membership")
    if manifest.get("status") != "RH-397_fixed_publication_manifest":
        failures.append("manifest:status")

    local_entries = manifest.get("publication_artifacts")
    external_entries = manifest.get("external_git_inputs")
    local_count = _verify_map(ROOT, local_entries, "local", failures)
    external_count = _verify_map(WORKSPACE, external_entries, "external_git", failures)
    if type(local_entries) is not dict or set(local_entries) != set(LOCAL_MEMBERS):
        failures.append("manifest:publication_membership")
    if type(external_entries) is not dict or external_count != 172:
        failures.append("manifest:external_git_membership")

    exact_counts = {
        "publication_file_count": len(LOCAL_MEMBERS),
        "release_stage_file_count": len(LOCAL_MEMBERS) + 2,
        "external_git_input_count": 172,
        "remote_logical_input_count": 4,
        "logical_input_total": 176,
    }
    for key, expected in exact_counts.items():
        if type(manifest.get(key)) is not int or manifest.get(key) != expected:
            failures.append(f"manifest:{key}")
    if local_count != len(LOCAL_MEMBERS):
        failures.append("manifest:publication_file_count_actual")
    if not exact_equal(manifest.get("source_commits"), SOURCE_COMMITS):
        failures.append("manifest:source_commits")
    if manifest.get("logical_source_digest") != source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST:
        failures.append("manifest:logical_source_digest")
    if not exact_equal(manifest.get("git_group_sizes"), SOURCE_GROUP_SIZES):
        failures.append("manifest:git_group_sizes")
    if not exact_equal(manifest.get("git_group_digests"), SOURCE_GROUP_DIGESTS):
        failures.append("manifest:git_group_digests")
    if manifest.get("all_git_source_digest") != ALL_GIT_SOURCE_DIGEST:
        failures.append("manifest:all_git_source_digest")
    if not exact_equal(manifest.get("remote_source_lock_sha256"), list(REMOTE_DIGESTS)):
        failures.append("manifest:remote_source_lock_sha256")
    if not exact_equal(
        manifest.get("remote_redistributable_in_release"),
        list(REMOTE_REDISTRIBUTION),
    ):
        failures.append("manifest:remote_redistributable_in_release")

    try:
        offline_rows = list(offline_remote_replay())
    except (OSError, RuntimeError, TypeError, ValueError) as exc:
        offline_rows = []
        failures.append(f"remote:offline_replay:{type(exc).__name__}")
    if [row.get("source_key") for row in offline_rows] != list(REMOTE_KEYS):
        failures.append("remote:offline_order")
    if not exact_equal(manifest.get("offline_remote_replay"), offline_rows):
        failures.append("manifest:offline_remote_replay")

    fresh: dict[str, object] | None = None
    try:
        fresh = build_payload()
    except (ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:
        failures.append(f"manifest:rebuild_error:{type(exc).__name__}")
    rebuild_match = fresh is not None and exact_equal(manifest, fresh)
    if not rebuild_match:
        failures.append("manifest:rebuild_mismatch")

    current_counts: dict[str, int] = {}
    for key in COUNT_KEYS:
        value = fresh.get(key) if fresh is not None else 0
        current_counts[key] = value if type(value) is int else 0
        if type(manifest.get(key)) is not int or manifest.get(key) != current_counts[key]:
            failures.append(f"manifest:{key}")
    current = {key: fresh is not None and fresh.get(key) is True for key in BOOLEAN_KEYS}
    for key, value in current.items():
        if value is not True or manifest.get(key) is not True:
            failures.append(f"manifest:{key}")

    return {
        "status": "RH-397_archive_verified" if not failures else "RH-397_archive_failed",
        "publication_file_count": local_count,
        "release_stage_file_count": len(LOCAL_MEMBERS) + 2 if not failures else 0,
        "external_git_input_count": external_count,
        "remote_logical_input_count": 4 if fresh is not None else 0,
        "logical_input_total": 176 if fresh is not None else 0,
        **current_counts,
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
