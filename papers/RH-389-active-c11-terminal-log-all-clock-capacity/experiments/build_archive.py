"""Build the fixed RH-389 publication and dependency manifest."""

from __future__ import annotations

from functools import lru_cache
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "dependency_manifest.json"

for directory in (ROOT, ROOT / "src", ROOT / "experiments"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from experiments import build_result, build_schema, source_locks  # noqa: E402
from experiments.verify_tao_source import loads_strict  # noqa: E402
from terminal_log_capacity.core import exact_equal, payload_sha256  # noqa: E402


LOCAL_MEMBERS = (
    ".gitignore",
    "FORMAT_AUDIT.md",
    "INTEGRITY_AUDIT.md",
    "Makefile",
    "README.md",
    "REMOTE_SOURCE_AUDIT.md",
    "REPLAY_AUDIT.md",
    "REVIEW_AUDIT.md",
    "TABLE_TRACE.md",
    "THEOREM_LEDGER.md",
    "UPDATED_ROADMAP.md",
    "VISUAL_QA.md",
    "active-c11-terminal-log-all-clock-capacity.pdf",
    "experiments/build_archive.py",
    "experiments/build_result.py",
    "experiments/build_schema.py",
    "experiments/source_locks.py",
    "experiments/verify_archive.py",
    "experiments/verify_tao_source.py",
    "main.log",
    "main.pdf",
    "main.tex",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/external_source_lock.json",
    "results/maynard_external_source_lock.json",
    "results/result.json",
    "results/result.schema.json",
    "results/tao_external_source_lock.json",
    "src/terminal_log_capacity/__init__.py",
    "src/terminal_log_capacity/core.py",
    "tests/test_archive.py",
    "tests/test_core.py",
    "tests/test_results.py",
    "tests/test_source_locks.py",
    "tests/test_tao_source.py",
)

PUBLICATION_PDFS = {"main.pdf", "active-c11-terminal-log-all-clock-capacity.pdf"}
REMOTE_PAYLOAD_HASHES = set(source_locks.REMOTE_PAYLOAD_HASHES)
SOURCE_COMMITS = {
    "rh388_release": source_locks.RH388_RELEASE,
    "tpc137_release": source_locks.TPC137_RELEASE,
}
REMOTE_DIGESTS = [
    source_locks.JY_CANONICAL_SHA256,
    source_locks.MAYNARD_CANONICAL_SHA256,
    source_locks.TAO_CANONICAL_SHA256,
]
REMOTE_OFFLINE_COMMANDS = (
    (
        "johnston-yang-arxiv-2204.01980v2",
        ROOT.parent / "RH-387-all-order-prime-tail-integral-resummation" / "experiments" / "verify_remote_source.py",
    ),
    (
        "maynard-annals-2015-small-gaps",
        ROOT.parent / "RH-388-rank-one-p2-tail-resummation" / "experiments" / "verify_remote_source.py",
    ),
    (
        "tao-cambridge-2016-logarithmic-chowla",
        ROOT / "experiments" / "verify_tao_source.py",
    ),
)


def digest(path: Path) -> str:
    if not isinstance(path, Path):
        raise TypeError("digest path must be pathlib.Path")
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _check_members(members: tuple[str, ...] | list[str]) -> None:
    if type(members) not in (tuple, list):
        raise TypeError("manifest members must be a tuple or list")
    if len(members) != len(set(members)):
        raise ValueError("manifest member list contains duplicates")
    for relative in members:
        if type(relative) is not str:
            raise TypeError("manifest member is not text")
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"manifest member escapes its base: {relative}")


def hash_map(base: Path, members: tuple[str, ...] | list[str]) -> dict[str, str]:
    if not isinstance(base, Path):
        raise TypeError("manifest base must be pathlib.Path")
    _check_members(members)
    output: dict[str, str] = {}
    for relative in members:
        path = base / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        output[relative] = digest(path)
    return output


def validated_result_git_source_map(result: dict[str, object]) -> dict[str, str]:
    if type(result) is not dict:
        raise TypeError("result must be an exact object")
    locks = result.get("source_locks")
    if type(locks) is not dict or type(locks.get("git")) is not dict:
        raise RuntimeError("result Git source locks are absent")
    git_locks = locks["git"]
    entries = git_locks.get("entries")
    if (
        type(entries) is not list
        or len(entries) != 95
        or type(git_locks.get("count")) is not int
        or git_locks.get("count") != 95
    ):
        raise RuntimeError("result Git source-lock count is not 95")
    output: dict[str, str] = {}
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise RuntimeError("invalid result Git source-lock row")
        path, source_sha = entry["path"], entry["sha256"]
        if type(path) is not str or type(source_sha) is not str or path in output:
            raise RuntimeError("invalid or duplicate result Git source-lock path")
        output[path] = source_sha
    if not exact_equal(git_locks, source_locks.build_git_source_locks()):
        raise RuntimeError("stored Git locks differ from fresh release-blob locks")
    return output


def validated_remote_locks(result: dict[str, object]) -> dict[str, object]:
    if type(result) is not dict:
        raise TypeError("result must be an exact object")
    locks = result.get("source_locks")
    if type(locks) is not dict or type(locks.get("remote")) is not dict:
        raise RuntimeError("result remote locks are absent")
    remote = locks["remote"]
    fresh = source_locks.build_remote_source_locks()
    if not exact_equal(remote, fresh):
        raise RuntimeError("stored remote locks differ from fresh exact locks")
    if (
        type(remote.get("count")) is not int
        or remote.get("count") != 3
        or type(remote.get("objects")) is not list
        or len(remote["objects"]) != 3
        or remote.get("network_fetch_performed") is not False
        or not exact_equal(remote.get("canonical_digests"), REMOTE_DIGESTS)
    ):
        raise RuntimeError("remote lock contract changed")
    return remote


def external_payload_exclusion() -> bool:
    required = {
        "results/external_source_lock.json",
        "results/maynard_external_source_lock.json",
        "results/tao_external_source_lock.json",
        "experiments/source_locks.py",
        "experiments/verify_tao_source.py",
    }
    if not required.issubset(LOCAL_MEMBERS):
        return False
    if len(REMOTE_PAYLOAD_HASHES) != 5:
        return False
    if {relative for relative in LOCAL_MEMBERS if relative.endswith(".pdf")} != PUBLICATION_PDFS:
        return False
    member_hashes = {digest(ROOT / relative) for relative in LOCAL_MEMBERS}
    if not member_hashes.isdisjoint(REMOTE_PAYLOAD_HASHES):
        return False
    for path in ROOT.rglob("*"):
        if path.is_file() and digest(path) in REMOTE_PAYLOAD_HASHES:
            return False
    return True


@lru_cache(maxsize=1)
def offline_remote_replay() -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    for source_key, verifier in REMOTE_OFFLINE_COMMANDS:
        if not verifier.is_file():
            raise RuntimeError(f"offline verifier is absent: {source_key}")
        completed = subprocess.run(
            [sys.executable, "-B", str(verifier)],
            cwd=verifier.parent.parent,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if completed.returncode != 0 or completed.stderr:
            raise RuntimeError(f"offline verifier failed: {source_key}")
        payload = loads_strict(completed.stdout)
        if type(payload) is not dict:
            raise RuntimeError(f"offline verifier returned a nonobject: {source_key}")
        row = {
            "network_opt_in": payload.get("network_opt_in"),
            "requests_made": payload.get("requests_made"),
            "source_key": source_key,
            "status": payload.get("status"),
        }
        if not exact_equal(row, {
            "network_opt_in": False,
            "requests_made": 0,
            "source_key": source_key,
            "status": "NETWORK_DISABLED",
        }):
            raise RuntimeError(f"offline verifier touched the network or changed status: {source_key}")
        rows.append(row)
    return tuple(rows)


def build_payload() -> dict[str, object]:
    publication = hash_map(ROOT, LOCAL_MEMBERS)
    result = loads_strict((ROOT / "results" / "result.json").read_text(encoding="utf-8"))
    schema = loads_strict((ROOT / "results" / "result.schema.json").read_text(encoding="utf-8"))
    if not exact_equal(result, build_result.build_payload()):
        raise RuntimeError("stored result differs from fresh result")
    if not exact_equal(schema, build_schema.build_schema()):
        raise RuntimeError("stored schema differs from fresh schema")

    result_git = validated_result_git_source_map(result)
    external_git = hash_map(WORKSPACE, list(result_git))
    if not exact_equal(external_git, result_git):
        raise RuntimeError("result Git locks do not match live external inputs")
    remote = validated_remote_locks(result)

    source_contract = result.get("source_locks")
    if type(source_contract) is not dict:
        raise RuntimeError("result source aggregate is absent")
    logical_digest = source_contract.get("logical_source_digest")
    logical_pass = (
        type(logical_digest) is str
        and logical_digest == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
        and source_contract.get("logical_digest_pass") is True
        and source_contract.get("pass") is True
    )
    if not logical_pass:
        raise RuntimeError("logical source digest is not sealed")

    certificate = result.get("certificate")
    if type(certificate) is not dict or payload_sha256(certificate) != build_result.CERTIFICATE_FIXTURE_SHA256:
        raise RuntimeError("result certificate differs from sealed fixture")
    semantic_match = publication["main.pdf"] == publication["active-c11-terminal-log-all-clock-capacity.pdf"]
    if not semantic_match:
        raise RuntimeError("semantic PDF is not byte-identical to main.pdf")
    payload_excluded = external_payload_exclusion()
    if not payload_excluded:
        raise RuntimeError("an external source payload is present")
    offline_rows = list(offline_remote_replay())

    return {
        "status": "RH-389_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": publication,
        "release_stage_file_count": len(LOCAL_MEMBERS) + 2,
        "external_git_input_count": len(external_git),
        "external_git_inputs": external_git,
        "remote_logical_input_count": 3,
        "remote_source_lock_sha256": remote["canonical_digests"],
        "logical_source_digest": logical_digest,
        "source_commits": SOURCE_COMMITS,
        "offline_remote_replay": offline_rows,
        "result_rebuild_match": True,
        "schema_rebuild_match": True,
        "result_source_lock_match": True,
        "release_blob_identity_pass": True,
        "source_digest_contract_pass": True,
        "logical_source_digest_pass": logical_pass,
        "exact_certificate_digest_pass": True,
        "remote_lock_exact_pass": True,
        "offline_remote_zero_requests": len(offline_rows) == 3,
        "remote_payload_excluded": payload_excluded,
        "semantic_pdf_match": semantic_match,
    }


def serialized_payload(payload: dict[str, object]) -> str:
    if type(payload) is not dict:
        raise TypeError("manifest payload must be an exact object")
    return json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    payload = build_payload()
    OUTPUT.write_text(serialized_payload(payload), encoding="utf-8")
    boolean_keys = (
        "result_rebuild_match", "schema_rebuild_match", "result_source_lock_match",
        "release_blob_identity_pass", "source_digest_contract_pass",
        "logical_source_digest_pass", "exact_certificate_digest_pass",
        "remote_lock_exact_pass", "offline_remote_zero_requests",
        "remote_payload_excluded", "semantic_pdf_match",
    )
    print(json.dumps({
        "status": payload["status"],
        "publication_file_count": payload["publication_file_count"],
        "release_stage_file_count": payload["release_stage_file_count"],
        "external_git_input_count": payload["external_git_input_count"],
        "remote_logical_input_count": payload["remote_logical_input_count"],
        "all_pass": all(payload[key] is True for key in boolean_keys),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
