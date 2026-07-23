"""Build RH-107 dependency, result, and publication hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry(path: Path) -> dict[str, str]:
    return {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256_file(path)}


def main() -> None:
    external = {
        "rh94_audit": PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh" / "results" / "source_seeded_horizon_audit.json",
        "rh96_audit": PAPERS / "RH-96-gap-weighted-weak-mode-quotient" / "results" / "weak_mode_quotient_audit.json",
        "rh102_audit": PAPERS / "RH-102-stopped-hybrid-quotient-clock" / "results" / "stopped_hybrid_clock_audit.json",
        "rh106_summary": PAPERS / "RH-106-uniform-gap-aware-quotient-law" / "results" / "summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "THEOREM_LEDGER.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "source_seeded_quotient_support.pdf",
        ROOT / "figures" / "source_seeded_quotient_support.png",
        ROOT / "main.pdf",
        ROOT / "source-seeded-quotient-support-law.pdf",
    ]
    dependency = {
        "status": "all_rh107_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    audit = json.loads((ROOT / "results" / "source_seeded_support_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "source_seeded_support_audit.json",
        ROOT / "results" / "source_seeded_support_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh107_source_seeded_quotient_support_law_archived",
        "theorem": {
            "adaptive_support_equivalence": True,
            "coarse_support_price_reduction": True,
            "support_reduced_stopped_endpoint": True,
            "finite_extrapolation_barrier": True,
        },
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
