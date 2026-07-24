from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    external = {
        "rh135_audit": ROOT.parent / "RH-135-relative-metric-affine-tail-recurrence/results/relative_affine_audit.json",
        "rh135_source": ROOT.parent / "RH-135-relative-metric-affine-tail-recurrence/experiments/build_relative_affine_audit.py",
        "rh136_summary": ROOT.parent / "RH-136-metric-balanced-packet-gauge/results/summary.json",
        "rh136_source": ROOT.parent / "RH-136-metric-balanced-packet-gauge/experiments/build_metric_balanced_audit.py",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/finite_horizon_young_tail_envelope.pdf",
        "figures/finite_horizon_young_tail_envelope.png", "main.pdf", "finite-horizon-young-tail-envelope.pdf",
    )]
    dependency = {
        "status": "all_rh137_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    manifest = ROOT / "results" / "dependency_manifest.json"
    manifest.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "finite_horizon_audit.json").read_text(encoding="utf-8"))
    result_files = [ROOT / "results" / name for name in ("finite_horizon_audit.json", "finite_horizon_smoke.json", "dependency_manifest.json")]
    summary = {
        "status": "rh137_finite_horizon_young_tail_envelope_archived",
        "theorem": {
            "pointwise_optimal_young_envelope": True,
            "sharp_safety_radius": True,
            "finite_candidate_greedy_horizon_optimality": True,
            "global_gauge_optimizer": False,
        },
        "audit": audit["audit_summary"], "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_files},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
