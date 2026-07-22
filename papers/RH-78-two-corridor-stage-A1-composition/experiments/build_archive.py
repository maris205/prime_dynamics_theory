"""Build RH-78 archive manifests."""

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
        "rh54_summary": PAPERS / "RH-54-factor-aware-intrinsic-identification" / "results" / "summary.json",
        "rh55_summary": PAPERS / "RH-55-strong-weak-riesz-cutoff-transfer" / "results" / "summary.json",
        "rh75_summary": PAPERS / "RH-75-log-square-block-contraction-law" / "results" / "summary.json",
        "rh77_summary": PAPERS / "RH-77-postblock-effective-rank-compression" / "results" / "summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "two_corridor_stage_A1_composition.pdf", ROOT / "figures" / "two_corridor_stage_A1_composition.png", ROOT / "main.pdf", ROOT / "two-corridor-stage-A1-composition.pdf"]
    dependency = {"status": "all_rh78_inputs_sources_and_publication_artifacts_hashed", "external_inputs": {name: entry(path) for name, path in external.items()}, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "stage_composition_audit.json").read_text(encoding="utf-8"))
    result_paths = [ROOT / "results" / "stage_composition_audit.json", ROOT / "results" / "stage_composition_smoke.json", dependency_path]
    summary = {
        "status": "rh78_two_corridor_stage_A1_composition_archived",
        "theorem": {"full_block_stage_A1_corridor": True, "effective_rank_stage_A1_corridor": True, "two_corridor_conditional_closure": True, "strict_mesh_identification_decay": True},
        "audit": {"scale_count": len(audit["rows"]), "all_composition_gates_green": audit["all_executed_composition_gates_green"], "maximum_conditional_hardy": max(r["conditional_hardy_upper"] for r in audit["rows"]), "maximum_rank4_future_error": max(r["rank4_future_error_upper"] for r in audit["rows"]), "initial_identification_stress": audit["rows"][0]["identification_stress_envelope_upper"], "final_identification_stress": audit["rows"][-1]["identification_stress_envelope_upper"]},
        "program_boundary": {"conditional_stage_A1_A4_composition_closed": True, "all_level_corridor_proved": False, "uniform_stage_A1_closed": False, "stage_A4_unconditional_closed": False, "renormalized_determinant_limit_closed": False, "hilbert_polya_operator": False, "riemann_hypothesis": False},
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "scale_count": len(audit["rows"])}, sort_keys=True))


if __name__ == "__main__":
    main()
