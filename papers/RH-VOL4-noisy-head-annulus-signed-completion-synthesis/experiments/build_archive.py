"""Build local and source-provenance manifests for Volume IV."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    audit_path = ROOT / "results/volume_audit.json"
    audit = json.loads(audit_path.read_text())
    local_relatives = (
        ".gitignore",
        "Makefile",
        "README.md",
        "CROSSWALK.md",
        "THEOREM_LEDGER.md",
        "UPDATED_ROADMAP.md",
        "main.tex",
        "experiments/build_volume_audit.py",
        "experiments/build_archive.py",
        "experiments/verify_archive.py",
        "tests/test_volume.py",
        "pyproject.toml",
        "requirements.txt",
        "main.pdf",
        "noisy-head-annulus-signed-completion-synthesis.pdf",
        "results/volume_audit.json",
        "results/atomic_index.tex",
    )
    local = [ROOT / relative for relative in local_relatives]
    missing = [str(path.relative_to(ROOT)) for path in local if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing required publication files: {missing}")
    dependency = {
        "status": "rh_volume_iv_sources_and_publication_artifacts_hashed",
        "external_inputs": audit["source_file_hashes"],
        "local_sources": {
            str(path.relative_to(ROOT)): sha(path)
            for path in local
            if path.suffix in {".py", ".tex", ".md", ".toml", ".txt"}
            or path.name in {".gitignore", "Makefile"}
        },
        "publication_artifacts": {
            str(path.relative_to(ROOT)): sha(path)
            for path in local
            if path.suffix == ".pdf" or path.name == "volume_audit.json"
        },
    }
    dependency_path = ROOT / "results/dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")

    summary = {
        "status": "rh_volume_iv_noisy_head_annulus_signed_completion_archived",
        "series": audit["series"],
        "inventory": {
            "numbered_paper_count": audit["numbered_paper_count"],
            "consecutive_numbering": audit["consecutive_numbering"],
            "legacy_alias_group_count": len(audit["legacy_alias_groups"]),
            "review_anchor_count": len(audit["review_anchor_numbers"]),
            "source_file_hash_count": audit["source_file_hash_count"],
        },
        "route_coordinate": audit["route_coordinate"],
        "first_missing_leaf": audit["first_missing_leaf"],
        "same_clock_bridge_proved": audit["same_clock_bridge_proved"],
        "physical_obstruction_proved": audit["physical_obstruction_proved"],
        "rh_362_activated": audit["rh_362_activated"],
        "gates": audit["gates"],
        "forbidden_claims": audit["forbidden_claims"],
        "result_hashes": {
            "results/volume_audit.json": sha(audit_path),
            "results/dependency_manifest.json": sha(dependency_path),
        },
    }
    (ROOT / "results/summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        "external_input_count": len(dependency["external_inputs"]),
        "local_source_count": len(dependency["local_sources"]),
        "publication_artifact_count": len(dependency["publication_artifacts"]),
        "status": summary["status"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
