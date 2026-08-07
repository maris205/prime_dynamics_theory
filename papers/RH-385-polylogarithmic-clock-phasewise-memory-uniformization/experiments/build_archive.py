"""Build the fixed RH-385 publication and dependency manifest."""

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

from experiments.build_result import (  # noqa: E402
    SOURCE_COMMITS,
    build_source_locks,
    _strict_load,
)
from polylog_clock import CERTIFICATE_FIXTURE_SHA256, payload_sha256  # noqa: E402


LOCAL_MEMBERS = (
    ".gitignore",
    "FORMAT_AUDIT.md",
    "INTEGRITY_AUDIT.md",
    "Makefile",
    "README.md",
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
    "main.log",
    "main.pdf",
    "main.tex",
    "polylogarithmic-clock-phasewise-memory-uniformization.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "results/result.schema.json",
    "src/polylog_clock/__init__.py",
    "src/polylog_clock/core.py",
    "tests/test_archive.py",
    "tests/test_core.py",
    "tests/test_results.py",
)


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


def validated_result_source_map(result: dict[str, object]) -> dict[str, str]:
    locks = result.get("source_locks")
    if type(locks) is not dict or type(locks.get("entries")) is not list:
        raise RuntimeError("result source-lock entries are absent")
    entries = locks["entries"]
    if type(locks.get("count")) is not int or locks["count"] != 67 or len(entries) != 67:
        raise RuntimeError("result source-lock count is not 67")
    output: dict[str, str] = {}
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise RuntimeError("invalid result source-lock row")
        path, sha = entry["path"], entry["sha256"]
        if type(path) is not str or type(sha) is not str or path in output:
            raise RuntimeError("invalid or duplicate result source-lock path")
        output[path] = sha
    if locks != build_source_locks():
        raise RuntimeError("stored source locks differ from fresh release-blob locks")
    return output


def build_payload() -> dict[str, object]:
    publication = hash_map(ROOT, LOCAL_MEMBERS)
    result = _strict_load(ROOT / "results/result.json")
    external_entries = result["source_locks"]["entries"]
    external_members = [entry["path"] for entry in external_entries]
    external = hash_map(WORKSPACE, external_members)
    result_locks = validated_result_source_map(result)
    if result_locks != external:
        raise RuntimeError("result source locks do not match archive external inputs")
    certificate = result.get("certificate")
    if type(certificate) is not dict or payload_sha256(certificate) != CERTIFICATE_FIXTURE_SHA256:
        raise RuntimeError("result certificate differs from the sealed fixture")
    if publication["main.pdf"] != publication[
        "polylogarithmic-clock-phasewise-memory-uniformization.pdf"
    ]:
        raise RuntimeError("semantic PDF is not byte-identical to main.pdf")
    return {
        "status": "RH-385_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": publication,
        "external_input_count": len(external_members),
        "external_inputs": external,
        "source_commits": SOURCE_COMMITS,
        "result_source_lock_match": True,
        "release_blob_identity_pass": True,
        "source_digest_contract_pass": True,
        "exact_certificate_digest_pass": True,
        "semantic_pdf_match": True,
    }


def serialized_payload(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> None:
    payload = build_payload()
    OUTPUT.write_text(serialized_payload(payload))
    print(json.dumps({
        "status": payload["status"],
        "publication_file_count": payload["publication_file_count"],
        "external_input_count": payload["external_input_count"],
        "all_pass": all(payload[key] is True for key in (
            "result_source_lock_match", "release_blob_identity_pass",
            "source_digest_contract_pass", "exact_certificate_digest_pass", "semantic_pdf_match",
        )),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
