"""Build local and corpus provenance manifests for RH-MVP2."""

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


def main() -> None:
    inventory_path = ROOT / "results/corpus_inventory.json"
    inventory = json.loads(inventory_path.read_text())
    external = dict(inventory["source_file_hashes"])

    relatives = (
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
            "experiments/build_four_volume_archive.py",
            "experiments/verify_four_volume_archive.py",
            "tests/test_synthesis.py",
            "tests/test_four_volume_archive.py",
            "pyproject.toml",
            "requirements.txt",
            "main.pdf",
            "corpus-frontier-synthesis.pdf",
            "results/corpus_inventory.json",
            "results/four_volume_archive_manifest.json",
            "results/four_volume_archive_verification.json",
    )
    local_paths = [ROOT / relative for relative in relatives]
    missing = [str(path.relative_to(ROOT)) for path in local_paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing required publication files: {missing}")
    dependency = {
        "status": "rh_mvp2_corpus_sources_and_publication_artifacts_hashed",
        "external_inputs": external,
        "local_sources": {
            str(path.relative_to(ROOT)): sha(path)
            for path in local_paths
            if path.suffix in {".py", ".tex", ".md", ".toml", ".txt"}
            or path.name in {".gitignore", "Makefile"}
        },
        "publication_artifacts": {
            str(path.relative_to(ROOT)): sha(path)
            for path in local_paths
            if path.suffix == ".pdf"
            or path.name in {
                "corpus_inventory.json",
                "four_volume_archive_manifest.json",
                "four_volume_archive_verification.json",
            }
        },
    }
    dependency_path = ROOT / "results/dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")

    summary = {
        "status": "rh_mvp2_corpus_frontier_synthesis_archived",
        "inventory": {
            "numbered_paper_count": inventory["numbered_paper_count"],
            "consecutive_numbering": inventory["consecutive_numbering"],
            "legacy_alias_group_count": len(inventory["legacy_alias_groups"]),
            "source_file_hash_count": inventory["source_file_hash_count"],
        },
        "route_coordinate": inventory["route_coordinate"],
        "first_missing_leaf": inventory["first_missing_leaf"],
        "gates": inventory["gates"],
        "forbidden_claims": inventory["forbidden_claims"],
        "result_hashes": {
            "results/corpus_inventory.json": sha(inventory_path),
            "results/dependency_manifest.json": sha(dependency_path),
        },
    }
    (ROOT / "results/summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": summary["status"],
        "external_input_count": len(external),
        "local_source_count": len(dependency["local_sources"]),
        "publication_artifact_count": len(dependency["publication_artifacts"]),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
