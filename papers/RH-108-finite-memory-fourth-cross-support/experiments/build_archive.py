"""Build RH-108 dependency, result, and publication hashes."""

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
        "rh95_summary": PAPERS / "RH-95-reduced-projected-cross-moment-factorization" / "results" / "summary.json",
        "rh96_audit": PAPERS / "RH-96-gap-weighted-weak-mode-quotient" / "results" / "weak_mode_quotient_audit.json",
        "rh101_summary": PAPERS / "RH-101-finite-memory-packet-gram-action" / "results" / "summary.json",
        "rh107_summary": PAPERS / "RH-107-source-seeded-quotient-support-law" / "results" / "summary.json",
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
        ROOT / "figures" / "finite_memory_fourth_cross_support.pdf",
        ROOT / "figures" / "finite_memory_fourth_cross_support.png",
        ROOT / "main.pdf",
        ROOT / "finite-memory-fourth-cross-support.pdf",
    ]
    dependency = {
        "status": "all_rh108_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    audit = json.loads((ROOT / "results" / "fourth_cross_support_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "fourth_cross_support_audit.json",
        ROOT / "results" / "fourth_cross_support_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh108_finite_memory_fourth_cross_support_archived",
        "theorem": {
            "finite_memory_weyl_support_certificate": True,
            "threshold_support_margin": True,
            "reduced_first_two_moment_realization": True,
            "radius_only_sharpness": True,
            "exact_normalized_memory_nondegeneracy_barrier": True,
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
