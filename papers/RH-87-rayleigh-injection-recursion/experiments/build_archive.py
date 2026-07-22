"""Build RH-87 dependency, result, and publication hashes."""

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
        "rh77_effective_rank_audit": PAPERS / "RH-77-postblock-effective-rank-compression" / "results" / "effective_rank_audit.json",
        "rh85_snapshot_summary": PAPERS / "RH-85-midblock-snapshot-packets" / "results" / "summary.json",
        "rh86_memory_summary": PAPERS / "RH-86-trace-normalized-late-memory-packets" / "results" / "summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "rayleigh_injection_recursion.pdf", ROOT / "figures" / "rayleigh_injection_recursion.png", ROOT / "main.pdf", ROOT / "rayleigh-injection-recursion.pdf"]
    dependency = {"status": "all_rh87_inputs_sources_and_publication_artifacts_hashed", "external_inputs": {name: entry(path) for name, path in external.items()}, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "injection_audit.json").read_text(encoding="utf-8"))
    result_paths = [ROOT / "results" / "injection_audit.json", ROOT / "results" / "injection_smoke.json", dependency_path]
    summary = {
        "status": "rh87_rayleigh_injection_recursion_archived",
        "theorem": {"rank_staircase_injection_recursion": True, "scalar_convolution_corollary": True, "gap_free_current_snapshot_tail": True},
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "scale_count": audit["audit_summary"]["scale_count"], "maximum_injection_norm": audit["audit_summary"]["maximum_interval_last_injection_relative_norm"]}, sort_keys=True))


if __name__ == "__main__":
    main()
