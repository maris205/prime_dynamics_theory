"""Replay RH-MVP2 hashes and enforce the corpus claim boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(records: dict[str, str], base: Path, label: str) -> None:
    for relative, expected in records.items():
        path = base / relative
        if not path.exists() or sha(path) != expected:
            raise RuntimeError(f"{label} hash mismatch: {relative}")


def main() -> None:
    inventory = json.loads((ROOT / "results/corpus_inventory.json").read_text())
    dependency = json.loads((ROOT / "results/dependency_manifest.json").read_text())
    summary = json.loads((ROOT / "results/summary.json").read_text())
    if inventory["unique_numbers"] != list(range(1, 362)):
        raise RuntimeError("numbered corpus is not consecutive 1..361")
    if set(inventory["legacy_alias_groups"]) != {"302", "303", "304", "306"}:
        raise RuntimeError("legacy alias inventory changed")
    if inventory["route_coordinate"] != "actual_same_clock_unnormalized_head_transport_open":
        raise RuntimeError("route coordinate was promoted")
    if any(inventory["gates"].values()) or any(inventory["forbidden_claims"].values()):
        raise RuntimeError("claim firewall overrun")
    verify(dependency["local_sources"], ROOT, "local source")
    verify(dependency["publication_artifacts"], ROOT, "publication")
    for relative, expected in dependency["external_inputs"].items():
        if sha(REPO / relative) != expected:
            raise RuntimeError(f"external source hash mismatch: {relative}")
    result_hashes = summary["result_hashes"]
    if sha(ROOT / "results/corpus_inventory.json") != result_hashes["results/corpus_inventory.json"]:
        raise RuntimeError("inventory result hash mismatch")
    if sha(ROOT / "results/dependency_manifest.json") != result_hashes["results/dependency_manifest.json"]:
        raise RuntimeError("dependency result hash mismatch")

    manuscript = " ".join((ROOT / "main.tex").read_text().lower().split())
    required_phrases = (
        "provenance-preserving synthesis",
        "d_{4k}(r)",
        "gates a--e remain false/open",
        "does not construct a hilbert--polya operator",
        "rh-362 is not activated",
    )
    for phrase in required_phrases:
        if phrase not in manuscript:
            raise RuntimeError(f"missing manuscript boundary phrase: {phrase}")

    archived = {}
    for relative in (
        ".gitignore",
        "Makefile",
        "README.md",
        "CROSSWALK.md",
        "THEOREM_LEDGER.md",
        "UPDATED_ROADMAP.md",
        "main.tex",
        "experiments/build_inventory.py",
        "experiments/build_archive.py",
        "experiments/verify_archive.py",
        "tests/test_synthesis.py",
        "pyproject.toml",
        "requirements.txt",
        "main.pdf",
        "corpus-frontier-synthesis.pdf",
        "results/corpus_inventory.json",
        "results/dependency_manifest.json",
        "results/summary.json",
    ):
        path = ROOT / relative
        if path.exists():
            archived[relative] = sha(path)
    output = ROOT / "results/archive_verification.json"
    output.write_text(json.dumps({
        "status": "rh_mvp2_corpus_frontier_hashes_and_claim_boundary_verified",
        "file_count": len(archived),
        "files": archived,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "verified", "file_count": len(archived)}, sort_keys=True))


if __name__ == "__main__":
    main()
