"""Build RH-89 dependency, result, and publication hashes."""

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
        "rh87_injection_summary": PAPERS / "RH-87-rayleigh-injection-recursion" / "results" / "summary.json",
        "rh88_predictor_summary": PAPERS / "RH-88-predictor-corrector-energy-contraction" / "results" / "summary.json",
        "rh88_predictor_audit": PAPERS / "RH-88-predictor-corrector-energy-contraction" / "results" / "predictor_corrector_audit.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "rank_one_complement_ritz_correction.pdf", ROOT / "figures" / "rank_one_complement_ritz_correction.png", ROOT / "main.pdf", ROOT / "rank-one-complement-ritz-correction.pdf"]
    dependency = {"status": "all_rh89_inputs_sources_and_publication_artifacts_hashed", "external_inputs": {name: entry(path) for name, path in external.items()}, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "ritz_correction_audit.json").read_text(encoding="utf-8"))
    result_paths = [ROOT / "results" / "ritz_correction_audit.json", ROOT / "results" / "ritz_correction_smoke.json", dependency_path]
    summary = {
        "status": "rh89_rank_one_complement_ritz_correction_archived",
        "theorem": {"rank_one_complement_ritz_theorem": True, "cross_block_maximal_coupling_direction": True, "small_corrector_tail_upper": True},
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "minimum_fraction": audit["audit_summary"]["minimum_interval_reference_dividend_fraction"], "maximum_contraction": audit["audit_summary"]["maximum_interval_corrected_contraction"]}, sort_keys=True))


if __name__ == "__main__":
    main()
