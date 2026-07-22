"""Build RH-83 dependency, result, and publication hashes."""

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
        "rh16_endpoint_rank_manuscript": PAPERS / "RH-16-endpoint-gaussian-resolution-rank" / "main.tex",
        "rh77_effective_rank_audit": PAPERS / "RH-77-postblock-effective-rank-compression" / "results" / "effective_rank_audit.json",
        "rh82_rank_clock_summary": PAPERS / "RH-82-half-log-postblock-rank-clock" / "results" / "summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "optimal_endpoint_singular_factorization.pdf",
        ROOT / "figures" / "optimal_endpoint_singular_factorization.png",
        ROOT / "main.pdf",
        ROOT / "optimal-endpoint-singular-factorization.pdf",
    ]
    dependency = {
        "status": "all_rh83_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "singular_factorization_audit.json").read_text(encoding="utf-8"))
    result_paths = [ROOT / "results" / "singular_factorization_audit.json", ROOT / "results" / "singular_factorization_smoke.json", dependency_path]
    summary = {
        "status": "rh83_optimal_endpoint_singular_factorization_archived",
        "theorem": {
            "optimal_factorization_constant": True,
            "factorization_constant_converse": True,
            "optimal_approximate_factorization": True,
            "coordinate_identity_branch_verdict": True,
        },
        "audit": {**audit["audit_summary"], "scale_count": len(audit["rows"])},
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "scale_count": len(audit["rows"]), "maximum_factor": audit["audit_summary"]["maximum_optimal_factor_constant"]}, sort_keys=True))


if __name__ == "__main__":
    main()

