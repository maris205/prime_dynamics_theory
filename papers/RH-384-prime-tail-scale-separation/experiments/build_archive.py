"""Build the fixed RH-384 publication and dependency manifest."""

from __future__ import annotations

import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "dependency_manifest.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))
from experiments.build_result import SOURCE_COMMITS, SOURCE_FILES, build_source_locks  # noqa: E402
from prime_tail_scales import CERTIFICATE_FIXTURE_SHA256, payload_sha256  # noqa: E402


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
    "prime-tail-scale-separation.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "results/result.schema.json",
    "src/prime_tail_scales/__init__.py",
    "src/prime_tail_scales/core.py",
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


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(
        path.read_text(),
        object_pairs_hook=_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if type(value) is not dict:
        raise ValueError(f"JSON root is not an object: {path}")
    return value


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


@lru_cache(maxsize=1)
def _expected_source_locks() -> dict[str, object]:
    return build_source_locks()


def validated_result_source_map(result: dict[str, object]) -> dict[str, str]:
    if type(result) is not dict or type(result.get("source_locks")) is not dict:
        raise RuntimeError("result source-lock object is absent")
    source_locks = result["source_locks"]
    entries = source_locks.get("entries")
    if type(entries) is not list or len(entries) != len(SOURCE_FILES):
        raise RuntimeError("result source-lock entries are not the frozen 51 rows")
    paths: list[str] = []
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"group", "commit", "path", "sha256"}:
            raise RuntimeError("a result source-lock row has invalid membership")
        path = entry.get("path")
        sha = entry.get("sha256")
        if type(path) is not str or type(sha) is not str:
            raise RuntimeError("a result source-lock row has invalid path/hash types")
        paths.append(path)
    if len(set(paths)) != len(SOURCE_FILES) or set(paths) != set(SOURCE_FILES):
        raise RuntimeError("result source-lock paths are not the frozen unique set")
    if type(source_locks.get("count")) is not int or source_locks.get("count") != len(SOURCE_FILES):
        raise RuntimeError("result source-lock count is not the exact integer 51")
    if source_locks.get("pass") is not True or source_locks != _expected_source_locks():
        raise RuntimeError("stored source-lock object differs from fresh release locks")
    return {entry["path"]: entry["sha256"] for entry in entries}


def build_payload() -> dict[str, object]:
    publication = hash_map(ROOT, LOCAL_MEMBERS)
    external = hash_map(WORKSPACE, list(SOURCE_FILES))
    result = load_json(ROOT / "results/result.json")
    result_locks = validated_result_source_map(result)
    if result_locks != external:
        raise RuntimeError("result source locks do not match archive external inputs")
    source_locks = result["source_locks"]
    certificate = result.get("certificate")
    if source_locks.get("release_blob_identity_pass") is not True:
        raise RuntimeError("result did not certify release-blob identity")
    if source_locks.get("digest_contract_pass") is not True:
        raise RuntimeError("result did not certify the 51-source digest contract")
    if type(certificate) is not dict or payload_sha256(certificate) != CERTIFICATE_FIXTURE_SHA256:
        raise RuntimeError("result certificate differs from the frozen exact fixture")
    if publication["main.pdf"] != publication["prime-tail-scale-separation.pdf"]:
        raise RuntimeError("semantic PDF is not byte-identical to main.pdf")
    return {
        "status": "RH-384_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": publication,
        "external_input_count": len(SOURCE_FILES),
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
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
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
