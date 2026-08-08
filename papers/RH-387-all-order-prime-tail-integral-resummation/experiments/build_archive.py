"""Build the fixed RH-387 publication and dependency manifest."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "dependency_manifest.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from experiments import build_result, build_schema  # noqa: E402
from integral_resummation.core import (  # noqa: E402
    exact_equal,
    loads_strict,
    payload_sha256,
)


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
    "experiments/build_archive.py",
    "experiments/build_result.py",
    "experiments/build_schema.py",
    "experiments/verify_archive.py",
    "experiments/verify_remote_source.py",
    "main.log",
    "main.pdf",
    "main.tex",
    "all-order-prime-tail-integral-resummation.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/external_source_lock.json",
    "results/result.json",
    "results/result.schema.json",
    "src/integral_resummation/__init__.py",
    "src/integral_resummation/core.py",
    "tests/test_archive.py",
    "tests/test_core.py",
    "tests/test_remote_source.py",
    "tests/test_results.py",
)

PUBLICATION_PDFS = {
    "main.pdf",
    "all-order-prime-tail-integral-resummation.pdf",
}
REMOTE_PAYLOAD_HASHES = set(build_result.REMOTE_PAYLOAD_HASHES)
SOURCE_COMMITS = {"rh386_release": build_result.RH386_RELEASE}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _check_members(members: tuple[str, ...] | list[str]) -> None:
    if len(members) != len(set(members)):
        raise ValueError("manifest member list contains duplicates")
    for relative in members:
        if type(relative) is not str:
            raise TypeError("manifest member is not text")
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"manifest member escapes its base: {relative}")


def hash_map(base: Path, members: tuple[str, ...] | list[str]) -> dict[str, str]:
    _check_members(members)
    output: dict[str, str] = {}
    for relative in members:
        path = base / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        output[relative] = digest(path)
    return output


def validated_result_git_source_map(result: dict[str, object]) -> dict[str, str]:
    locks = result.get("source_locks")
    if type(locks) is not dict or type(locks.get("git")) is not dict:
        raise RuntimeError("result Git source locks are absent")
    git_locks = locks["git"]
    entries = git_locks.get("entries")
    if type(entries) is not list or len(entries) != 68 or git_locks.get("count") != 68:
        raise RuntimeError("result Git source-lock count is not 68")
    output: dict[str, str] = {}
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise RuntimeError("invalid result Git source-lock row")
        path, source_sha = entry["path"], entry["sha256"]
        if type(path) is not str or type(source_sha) is not str or path in output:
            raise RuntimeError("invalid or duplicate result Git source-lock path")
        output[path] = source_sha
    if not exact_equal(git_locks, build_result.build_git_source_locks()):
        raise RuntimeError("stored Git locks differ from fresh release-blob locks")
    return output


def validated_remote_lock(result: dict[str, object]) -> dict[str, object]:
    source_locks = result.get("source_locks")
    if type(source_locks) is not dict or type(source_locks.get("remote")) is not dict:
        raise RuntimeError("result remote lock is absent")
    remote = source_locks["remote"]
    objects = remote.get("objects")
    if type(objects) is not list or len(objects) != 1:
        raise RuntimeError("result remote lock count is not one")
    lock = objects[0]
    file_lock = loads_strict((ROOT / "results" / "external_source_lock.json").read_text())
    fresh = build_result.build_remote_source_lock()
    if type(fresh) is not dict or type(fresh.get("objects")) is not list:
        raise RuntimeError("fresh remote lock is malformed")
    if not exact_equal(lock, fresh["objects"][0]) or not exact_equal(file_lock, lock):
        raise RuntimeError("remote lock object changed")
    if remote.get("network_fetch_performed") is not False:
        raise RuntimeError("offline result falsely claims a network fetch")
    return lock


def external_payload_exclusion() -> bool:
    if "results/external_source_lock.json" not in LOCAL_MEMBERS:
        return False
    if "experiments/verify_remote_source.py" not in LOCAL_MEMBERS:
        return False
    if {relative for relative in LOCAL_MEMBERS if relative.endswith(".pdf")} != PUBLICATION_PDFS:
        return False
    for path in ROOT.rglob("*"):
        if path.is_file() and digest(path) in REMOTE_PAYLOAD_HASHES:
            return False
    return True


def build_payload() -> dict[str, object]:
    publication = hash_map(ROOT, LOCAL_MEMBERS)
    result = loads_strict((ROOT / "results" / "result.json").read_text())
    schema = loads_strict((ROOT / "results" / "result.schema.json").read_text())
    fresh_result = build_result.build_payload()
    fresh_schema = build_schema.build_schema()
    if not exact_equal(result, fresh_result):
        raise RuntimeError("stored result differs from fresh result")
    if not exact_equal(schema, fresh_schema):
        raise RuntimeError("stored schema differs from fresh schema")

    result_git = validated_result_git_source_map(result)
    external_git = hash_map(WORKSPACE, list(result_git))
    if external_git != result_git:
        raise RuntimeError("result Git locks do not match live external inputs")
    lock = validated_remote_lock(result)

    source_locks = result.get("source_locks")
    if type(source_locks) is not dict:
        raise RuntimeError("result source lock aggregate is absent")
    logical_digest = source_locks.get("logical_source_digest")
    logical_pass = (
        type(logical_digest) is str
        and logical_digest == build_result.EXPECTED_LOGICAL_SOURCE_DIGEST
        and source_locks.get("logical_digest_pass") is True
        and source_locks.get("pass") is True
    )
    if not logical_pass:
        raise RuntimeError("logical source digest is not sealed")

    certificate = result.get("certificate")
    if type(certificate) is not dict or payload_sha256(certificate) != build_result.CERTIFICATE_FIXTURE_SHA256:
        raise RuntimeError("result certificate differs from sealed fixture")
    semantic_match = publication["main.pdf"] == publication[
        "all-order-prime-tail-integral-resummation.pdf"
    ]
    if not semantic_match:
        raise RuntimeError("semantic PDF is not byte-identical to main.pdf")
    payload_excluded = external_payload_exclusion()
    if not payload_excluded:
        raise RuntimeError("an external non-redistributed source payload is present")

    remote_lock_sha = payload_sha256(lock)
    return {
        "status": "RH-387_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": publication,
        "external_git_input_count": len(external_git),
        "external_git_inputs": external_git,
        "remote_logical_input_count": 1,
        "remote_source_lock_sha256": remote_lock_sha,
        "logical_source_digest": logical_digest,
        "source_commits": SOURCE_COMMITS,
        "result_rebuild_match": True,
        "schema_rebuild_match": True,
        "result_source_lock_match": True,
        "release_blob_identity_pass": True,
        "source_digest_contract_pass": True,
        "logical_source_digest_pass": logical_pass,
        "exact_certificate_digest_pass": True,
        "remote_lock_exact_pass": True,
        "remote_payload_excluded": payload_excluded,
        "semantic_pdf_match": semantic_match,
    }


def serialized_payload(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    payload = build_payload()
    OUTPUT.write_text(serialized_payload(payload))
    boolean_keys = (
        "result_rebuild_match", "schema_rebuild_match", "result_source_lock_match",
        "release_blob_identity_pass", "source_digest_contract_pass",
        "logical_source_digest_pass", "exact_certificate_digest_pass",
        "remote_lock_exact_pass", "remote_payload_excluded", "semantic_pdf_match",
    )
    print(json.dumps({
        "status": payload["status"],
        "publication_file_count": payload["publication_file_count"],
        "external_git_input_count": payload["external_git_input_count"],
        "remote_logical_input_count": payload["remote_logical_input_count"],
        "all_pass": all(payload[key] is True for key in boolean_keys),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
