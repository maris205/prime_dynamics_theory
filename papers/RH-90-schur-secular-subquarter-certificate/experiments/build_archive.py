"""Build RH-90 dependency, result, and publication hashes."""

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
        "rh88_predictor_summary": PAPERS / "RH-88-predictor-corrector-energy-contraction" / "results" / "summary.json",
        "rh89_ritz_summary": PAPERS / "RH-89-rank-one-complement-ritz-correction" / "results" / "summary.json",
        "rh89_ritz_audit": PAPERS / "RH-89-rank-one-complement-ritz-correction" / "results" / "ritz_correction_audit.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "schur_secular_subquarter_certificate.pdf", ROOT / "figures" / "schur_secular_subquarter_certificate.png", ROOT / "main.pdf", ROOT / "schur-secular-subquarter-certificate.pdf"]
    dependency = {"status": "all_rh90_inputs_sources_and_publication_artifacts_hashed", "external_inputs": {name: entry(path) for name, path in external.items()}, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "schur_certificate_audit.json").read_text(encoding="utf-8"))
    result_paths = [ROOT / "results" / "schur_certificate_audit.json", ROOT / "results" / "schur_certificate_smoke.json", dependency_path]
    summary = {
        "status": "rh90_schur_secular_subquarter_certificate_archived",
        "theorem": {"schur_trial_gain_certificate": True, "target_contraction_corollary": True, "full_reference_packet_removed": True},
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "negative_count": audit["audit_summary"]["schur_negative_count"], "maximum_contraction": audit["audit_summary"]["maximum_interval_corrected_contraction"]}, sort_keys=True))


if __name__ == "__main__":
    main()
