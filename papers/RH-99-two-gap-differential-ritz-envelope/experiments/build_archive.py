"""Build RH-99 dependency, result, and publication hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]; PAPERS = ROOT.parent; REPOSITORY = PAPERS.parent


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""): digest.update(chunk)
    return digest.hexdigest()


def entry(path: Path) -> dict[str, str]: return {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256_file(path)}


def main() -> None:
    external = {
        "rh77_model_source": PAPERS / "RH-77-postblock-effective-rank-compression" / "experiments" / "run_effective_rank_audit.py",
        "rh82_clock_source": PAPERS / "RH-82-half-log-postblock-rank-clock" / "src" / "half_log_rank" / "bounds.py",
        "rh94_source": PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh" / "experiments" / "run_source_seeded_horizon_audit.py",
        "rh96_source": PAPERS / "RH-96-gap-weighted-weak-mode-quotient" / "src" / "weak_mode_quotient" / "bounds.py",
        "rh98_summary": PAPERS / "RH-98-projector-lipschitz-propagation-barrier" / "results" / "summary.json",
        "rh98_roadmap": PAPERS / "RH-98-projector-lipschitz-propagation-barrier" / "UPDATED_ROADMAP.md",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "UPDATED_ROADMAP.md", ROOT / "THEOREM_LEDGER.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "two_gap_differential_ritz_envelope.pdf", ROOT / "figures" / "two_gap_differential_ritz_envelope.png", ROOT / "main.pdf", ROOT / "two-gap-differential-ritz-envelope.pdf"]
    dependency = {"status": "all_rh99_inputs_sources_and_publication_artifacts_hashed", "external_inputs": {name: entry(path) for name, path in external.items()}, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"; dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "two_gap_differential_audit.json").read_text(encoding="utf-8"))
    result_paths = [ROOT / "results" / "two_gap_differential_audit.json", ROOT / "results" / "two_gap_differential_smoke.json", dependency_path]
    summary = {
        "status": "rh99_two_gap_differential_ritz_envelope_archived",
        "theorem": {"cross_covariance_derivative": True, "spectral_projector_sylvester_bound": True, "two_gap_refresh_derivative": True},
        "audit": audit["audit_summary"], "program_boundary": audit["theorem_boundary"], "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths}, "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"; summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__": main()
