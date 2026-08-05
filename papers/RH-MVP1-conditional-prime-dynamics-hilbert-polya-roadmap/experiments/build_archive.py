"""Build RH-MVP1 dependency, result, and publication hashes."""

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
    audit_path = ROOT / "results/mvp_audit.json"
    audit = json.loads(audit_path.read_text())
    external: dict[str, dict[str, str]] = {}
    for record in audit["inventory"]:
        directory = ROOT.parent / record["directory"]
        for label, relative in (
            ("readme", "README.md"),
            ("main_tex", "main.tex"),
            ("summary", "results/summary.json"),
            ("archive", "results/archive_verification.json"),
        ):
            path = directory / relative
            if path.exists():
                external[f"RH-{record['paper']}_{label}"] = {
                    "path": str(path.relative_to(REPO)),
                    "sha256": sha(path),
                }

    local = sorted({
        *(ROOT / "src").rglob("*.py"),
        *(ROOT / "experiments").glob("*.py"),
        *(ROOT / "tests").glob("*.py"),
    })
    publications = [ROOT / relative for relative in (
        ".gitignore",
        "README.md",
        "THEOREM_LEDGER.md",
        "UPDATED_ROADMAP.md",
        "main.tex",
        "references.bib",
        "pyproject.toml",
        "requirements.txt",
        "results/atomic_index.tex",
        "figures/conditional_mvp_roadmap.pdf",
        "figures/conditional_mvp_roadmap.png",
        "main.pdf",
        "conditional-prime-dynamics-hilbert-polya-roadmap.pdf",
    )]
    dependency = {
        "status": "all_rh_mvp1_corpus_sources_and_publication_artifacts_hashed",
        "external_inputs": external,
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    dependency_path = ROOT / "results/dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")

    summary = {
        "status": "rh_mvp1_conditional_prime_dynamics_hilbert_polya_roadmap_archived",
        "theorem": {
            "spectral_divisor_closure": True,
            "conditional_mvp_implication": True,
            "status_aware_completion_frontier": True,
        },
        "audit": audit["audit_summary"],
        "series": audit["series"],
        "gates": audit["gates"],
        "claim_ladder": audit["claim_ladder"],
        "theorem_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {
            "results/mvp_audit.json": sha(audit_path),
            "results/dependency_manifest.json": sha(dependency_path),
        },
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results/summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "summary": str(output.relative_to(ROOT)),
        "external_hash_count": len(external),
        **audit["audit_summary"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
