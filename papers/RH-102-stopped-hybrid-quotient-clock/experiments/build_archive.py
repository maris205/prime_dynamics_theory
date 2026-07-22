"""Build RH-102 dependency, result, and publication hashes."""

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
        "rh77_model_source": PAPERS / "RH-77-postblock-effective-rank-compression" / "experiments" / "run_effective_rank_audit.py",
        "rh82_clock_source": PAPERS / "RH-82-half-log-postblock-rank-clock" / "src" / "half_log_rank" / "bounds.py",
        "rh94_source_seed": PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh" / "src" / "source_seeded_refresh" / "bounds.py",
        "rh96_quotient_source": PAPERS / "RH-96-gap-weighted-weak-mode-quotient" / "experiments" / "run_weak_mode_quotient_audit.py",
        "rh96_summary": PAPERS / "RH-96-gap-weighted-weak-mode-quotient" / "results" / "summary.json",
        "rh97_summary": PAPERS / "RH-97-nonlinear-hybrid-horizon-budget" / "results" / "summary.json",
        "rh100_roadmap": PAPERS / "RH-100-hundred-layer-route-review" / "UPDATED_ROADMAP.md",
        "rh101_summary": PAPERS / "RH-101-finite-memory-packet-gram-action" / "results" / "summary.json",
    }
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "THEOREM_LEDGER.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "stopped_hybrid_quotient_clock.pdf",
        ROOT / "figures" / "stopped_hybrid_quotient_clock.png",
        ROOT / "main.pdf",
        ROOT / "stopped-hybrid-quotient-clock.pdf",
    ]
    dependency = {
        "status": "all_rh102_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {name: entry(path) for name, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    audit = json.loads((ROOT / "results" / "stopped_hybrid_clock_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "stopped_hybrid_clock_audit.json",
        ROOT / "results" / "stopped_hybrid_clock_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh102_stopped_hybrid_quotient_clock_archived",
        "theorem": {
            "accepted_hybrid_telescoping": True,
            "stopped_endpoint_budget": True,
            "validated_gate_slack_allowance": True,
            "local_global_certificate_composition": True,
        },
        "audit": audit["audit_summary"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
