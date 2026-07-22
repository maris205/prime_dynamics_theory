"""Build RH-88 dependency, result, and publication hashes."""

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
        "rh86_memory_summary": PAPERS / "RH-86-trace-normalized-late-memory-packets" / "results" / "summary.json",
        "rh87_injection_summary": PAPERS / "RH-87-rayleigh-injection-recursion" / "results" / "summary.json",
        "rh87_injection_audit": PAPERS / "RH-87-rayleigh-injection-recursion" / "results" / "injection_audit.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "predictor_corrector_energy_contraction.pdf", ROOT / "figures" / "predictor_corrector_energy_contraction.png", ROOT / "main.pdf", ROOT / "predictor-corrector-energy-contraction.pdf"]
    dependency = {"status": "all_rh88_inputs_sources_and_publication_artifacts_hashed", "external_inputs": {name: entry(path) for name, path in external.items()}, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "predictor_corrector_audit.json").read_text(encoding="utf-8"))
    result_paths = [ROOT / "results" / "predictor_corrector_audit.json", ROOT / "results" / "predictor_corrector_smoke.json", dependency_path]
    summary = {
        "status": "rh88_predictor_corrector_energy_contraction_archived",
        "theorem": {"residual_rayleigh_factorization": True, "predictor_corrector_contraction_identity": True, "global_norm_sufficient_condition_boundary": True},
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "channels": audit["audit_summary"]["channel_count"], "maximum_contraction": audit["audit_summary"]["maximum_actual_memory_contraction"]}, sort_keys=True))


if __name__ == "__main__":
    main()
