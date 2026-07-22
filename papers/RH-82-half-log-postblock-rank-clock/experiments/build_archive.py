"""Build RH-82 dependency, result, and publication hashes."""

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
        "rh16_endpoint_rank_audit": PAPERS / "RH-16-endpoint-gaussian-resolution-rank" / "results" / "endpoint_rank_audit.json",
        "rh77_effective_rank_audit": PAPERS / "RH-77-postblock-effective-rank-compression" / "results" / "effective_rank_audit.json",
        "rh78_composition_summary": PAPERS / "RH-78-two-corridor-stage-A1-composition" / "results" / "summary.json",
        "rh81_route_summary": PAPERS / "RH-81-stage-A-to-A5-route-review" / "results" / "summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "half_log_postblock_rank_clock.pdf",
        ROOT / "figures" / "half_log_postblock_rank_clock.png",
        ROOT / "main.pdf",
        ROOT / "half-log-postblock-rank-clock.pdf",
    ]
    dependency = {
        "status": "all_rh82_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "half_log_rank_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "half_log_rank_audit.json",
        ROOT / "results" / "half_log_rank_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh82_half_log_postblock_rank_clock_archived",
        "theorem": {
            "exponential_excess_rank_tail": True,
            "logarithmic_accuracy_rank": True,
            "endpoint_to_postblock_ideal_property_transfer": True,
            "factorized_stage_A_rank_criterion": True,
        },
        "audit": {
            **audit["audit_summary"],
            "physical_scale_count": len(audit["rows"]),
            "endpoint_model_scale_count": len(audit["endpoint_linear_row_model"]["rows"]),
            "maximum_endpoint_model_clock_plus_two_tail": audit["endpoint_linear_row_model"]["maximum_clock_plus_two_tail"],
        },
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "physical_scales": len(audit["rows"]), "maximum_rank": audit["audit_summary"]["maximum_clock_rank"]}, sort_keys=True))


if __name__ == "__main__":
    main()

