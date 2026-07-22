"""Build RH-79 archive manifests."""

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
        "rh45_trace_summary": PAPERS / "RH-45-bulk-two-step-trace-norm-determinant" / "results" / "summary.json",
        "rh46_double_pole_summary": PAPERS / "RH-46-small-noise-mesh-double-pole" / "results" / "summary.json",
        "rh78_composition_audit": PAPERS / "RH-78-two-corridor-stage-A1-composition" / "results" / "stage_composition_audit.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "intrinsic_determinant_diagonal_transfer.pdf", ROOT / "figures" / "intrinsic_determinant_diagonal_transfer.png", ROOT / "main.pdf", ROOT / "intrinsic-determinant-diagonal-transfer.pdf"]
    dependency = {"status": "all_rh79_inputs_sources_and_publication_artifacts_hashed", "external_inputs": {name: entry(path) for name, path in external.items()}, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "determinant_transfer_audit.json").read_text(encoding="utf-8"))
    result_paths = [ROOT / "results" / "determinant_transfer_audit.json", ROOT / "results" / "determinant_transfer_smoke.json", dependency_path]
    summary = {
        "status": "rh79_intrinsic_determinant_diagonal_transfer_archived",
        "theorem": {"intrinsic_square_trace_transfer": True, "strict_diagonal_trace_norm_closure": True, "shrinking_disk_determinant_transfer": True, "fixed_disk_exponential_barrier": True},
        "audit": {"scale_count": len(audit["rows"]), "shrinking_disk_gates_green": audit["all_executed_shrinking_disk_gates_green"], "initial_square_error": audit["rows"][0]["square_trace_error_upper"], "final_square_error": audit["rows"][-1]["square_trace_error_upper"], "initial_shrinking_disk_error": audit["rows"][0]["shrinking_disk_determinant_error_upper"], "final_shrinking_disk_error": audit["rows"][-1]["shrinking_disk_determinant_error_upper"], "minimum_fixed_disk_error": min(r["fixed_disk_determinant_error_upper"] for r in audit["rows"]), "final_fixed_disk_error": audit["rows"][-1]["fixed_disk_determinant_error_upper"]},
        "program_boundary": {"conditional_square_and_shrinking_disk_transfer_closed": True, "fixed_disk_transfer_closed": False, "pole_renormalized_limit_closed": False, "stage_A5_closed": False, "hilbert_polya_operator": False, "riemann_hypothesis": False},
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "scale_count": len(audit["rows"])}, sort_keys=True))


if __name__ == "__main__":
    main()
