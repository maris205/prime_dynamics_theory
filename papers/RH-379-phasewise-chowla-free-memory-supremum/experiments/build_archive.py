"""Build the fixed RH-379 publication and dependency manifest."""

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
from experiments.build_result import SOURCE_COMMITS, SOURCE_FILES  # noqa: E402


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
    "experiments/verify_archive.py",
    "main.log",
    "main.pdf",
    "main.tex",
    "phasewise-chowla-free-memory-supremum.pdf",
    "pyproject.toml",
    "references.bib",
    "requirements.txt",
    "results/result.json",
    "results/result.schema.json",
    "src/phasewise_memory/__init__.py",
    "src/phasewise_memory/core.py",
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


def build_payload() -> dict[str, object]:
    """Recompute the complete archive manifest without writing it."""

    publication = hash_map(ROOT, LOCAL_MEMBERS)
    external = hash_map(WORKSPACE, SOURCE_FILES)
    result = json.loads((ROOT / "results" / "result.json").read_text())
    result_locks = result.get("source_locks", {}).get("files")
    if result_locks != external:
        raise RuntimeError("result source locks do not match archive external inputs")
    main_pdf = publication["main.pdf"]
    semantic_pdf = publication["phasewise-chowla-free-memory-supremum.pdf"]
    if main_pdf != semantic_pdf:
        raise RuntimeError("semantic PDF is not byte-identical to main.pdf")
    return {
        "status": "RH-379_fixed_publication_manifest",
        "publication_file_count": len(LOCAL_MEMBERS),
        "publication_artifacts": publication,
        "external_input_count": len(SOURCE_FILES),
        "external_inputs": external,
        "source_commits": SOURCE_COMMITS,
        "result_source_lock_match": True,
        "semantic_pdf_match": True,
    }


def serialized_payload(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main() -> None:
    payload = build_payload()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(serialized_payload(payload))
    print(
        json.dumps(
            {
                "status": payload["status"],
                "publication_file_count": payload["publication_file_count"],
                "external_input_count": payload["external_input_count"],
                "result_source_lock_match": payload["result_source_lock_match"],
                "semantic_pdf_match": payload["semantic_pdf_match"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
