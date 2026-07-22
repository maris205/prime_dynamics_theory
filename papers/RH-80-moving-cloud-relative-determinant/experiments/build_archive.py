"""Build RH-80 dependency, result, and publication hashes."""

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
        "rh15_outer_resonance_cloud": PAPERS / "RH-15-parity-extracted-bulk-scattering" / "results" / "outer_resonance_cloud.csv",
        "rh46_double_pole_summary": PAPERS / "RH-46-small-noise-mesh-double-pole" / "results" / "summary.json",
        "rh79_diagonal_transfer_summary": PAPERS / "RH-79-intrinsic-determinant-diagonal-transfer" / "results" / "summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "moving_cloud_relative_determinant.pdf",
        ROOT / "figures" / "moving_cloud_relative_determinant.png",
        ROOT / "main.pdf",
        ROOT / "moving-cloud-relative-determinant.pdf",
    ]
    dependency = {
        "status": "all_rh80_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "cloud_renormalization_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "cloud_renormalization_audit.json",
        ROOT / "results" / "cloud_renormalization_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh80_moving_cloud_relative_determinant_archived",
        "theorem": {
            "fixed_scalar_pole_cancellation_fails_across_circle": True,
            "exact_moving_cloud_factorization": True,
            "relative_trace_class_normality_criterion": True,
            "coefficient_deconvolution_identifies_residual": True,
        },
        "audit": {
            "precision_bits": audit["precision_bits"],
            "cloud_level_count": len(audit["archived_cloud_rows"]),
            "finest_cloud_gate": audit["finest_cloud_gate"],
            "degree_64_radius_08_error_upper": next(row["uniform_error_upper"] for row in audit["ideal_model"]["interior_rows"] if row["degree"] == 64 and row["radius_ratio"] == 0.8),
            "degree_64_q_105_growth_lower": next(row["fixed_cancellation_magnitude_lower"] for row in audit["ideal_model"]["exterior_rows"] if row["degree"] == 64 and row["point_ratio"] == 1.05),
        },
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "cloud_levels": len(audit["archived_cloud_rows"])}, sort_keys=True))


if __name__ == "__main__":
    main()

