from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPERS = ROOT.parent


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    external = {
        "rh8_temporal_summary": PAPERS / "RH-8-time-ordered-cycle-curvature" / "results/temporal_orientation_summary.json",
        "rh45_archive": PAPERS / "RH-45-bulk-two-step-trace-norm-determinant" / "results/archive_verification.json",
        "rh80_archive": PAPERS / "RH-80-moving-cloud-relative-determinant" / "results/archive_verification.json",
        "rh160_archive": PAPERS / "RH-160-conditional-all-level-reset-dichotomy" / "results/archive_verification.json",
        "rh_mvp1_archive": PAPERS / "RH-MVP1-conditional-prime-dynamics-hilbert-polya-roadmap" / "results/archive_verification.json",
    }
    local = sorted({
        *(ROOT / "src").rglob("*.py"),
        *(ROOT / "experiments").glob("*.py"),
        *(ROOT / "tests").glob("*.py"),
    })
    publications = [ROOT / relative for relative in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md",
        "main.tex", "references.bib", "pyproject.toml", "requirements.txt",
        "figures/typed_moving_cloud_assembly.pdf",
        "figures/typed_moving_cloud_assembly.png",
        "main.pdf", "packet-riesz-relative-determinant-assembly.pdf",
    )]
    dependency = {
        "status": "all_rh161_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)}
            for key, path in external.items()
        },
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    dependency_path = ROOT / "results/dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")

    audit_path = ROOT / "results/typed_assembly_audit.json"
    audit = json.loads(audit_path.read_text())
    summary = {
        "status": "rh161_packet_riesz_relative_determinant_assembly_archived",
        "theorem": {
            "packet_to_riesz_homotopy": True,
            "stable_packet_graph_bound": True,
            "complement_determinant_transfer": True,
            "trace_class_and_regularized_branches": True,
            "directed_marked_word_stability": True,
            "conditional_typed_assembly": True,
            "minimal_frontier_with_witnesses": True,
        },
        "audit": audit["audit_summary"],
        "current_statuses": audit["current_statuses"],
        "minimal_completion_bundles": audit["minimal_completion_bundles"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {
            "results/typed_assembly_audit.json": sha(audit_path),
            "results/dependency_manifest.json": sha(dependency_path),
        },
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results/summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
