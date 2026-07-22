"""Build RH-69 dependency and publication hashes."""

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
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def main() -> None:
    external = {
        "rh60_phase_pilot": PAPERS
        / "RH-60-finite-horizon-phase-aware-tails"
        / "results"
        / "phase_tail_pilot.json",
        "rh61_horizon_audit": PAPERS
        / "RH-61-directional-horizon-scaling-barrier"
        / "results"
        / "horizon_scaling_audit.json",
        "rh67_covariance_pilot": PAPERS
        / "RH-67-physical-covariance-block-envelopes"
        / "results"
        / "covariance_envelope_pilot.json",
        "rh68_depth_pilot": PAPERS
        / "RH-68-phase-coherence-block-depth-barrier"
        / "results"
        / "depth_barrier_pilot.json",
    }
    local_paths = sorted(
        {
            *(ROOT / "src").rglob("*.py"),
            *(ROOT / "experiments").glob("*.py"),
            *(ROOT / "tests").glob("*.py"),
        }
    )
    publication_paths = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "figures" / "adaptive_certificate_portfolio.pdf",
        ROOT / "figures" / "adaptive_certificate_portfolio.png",
        ROOT / "main.pdf",
        ROOT / "adaptive-certificate-portfolio.pdf",
    ]
    dependency = {
        "status": "all_rh69_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: entry(path) for name, path in external.items()
        },
        "local_sources": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in local_paths
        },
        "publication_artifacts": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in publication_paths
        },
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    portfolio = json.loads(
        (ROOT / "results" / "certificate_portfolio.json").read_text(
            encoding="utf-8"
        )
    )
    arb = json.loads(
        (ROOT / "results" / "arb_portfolio_audit.json").read_text(
            encoding="utf-8"
        )
    )
    result_paths = [
        ROOT / "results" / "certificate_portfolio.json",
        ROOT / "results" / "certificate_portfolio_smoke.json",
        ROOT / "results" / "arb_portfolio_audit.json",
        dependency_path,
    ]
    summary = {
        "status": "rh69_adaptive_upper_lower_certificate_portfolio_audit",
        "theorem": {
            "safe_pareto_pruning": True,
            "three_way_triage_soundness": True,
            "adaptive_finite_prefix_tail_composition": True,
            "conditional_polylogarithmic_ledger": True,
        },
        "program_boundary": {
            "production_interval_upper_portfolio": False,
            "physical_covariance_theorem": False,
            "asymptotic_phase_compression": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
        },
        "portfolio": {
            "phase_horizon_rows": portfolio["phase_horizon_portfolio"],
            "covariance_rows": portfolio["covariance_portfolio"],
            "depth_triage": portfolio["depth_triage"],
        },
        "arb": {
            key: value
            for key, value in arb.items()
            if key.endswith("certified")
            or key in ("precision_bits", "production_interval_audit_executed")
        },
        "route_consequence": portfolio["route_consequence"],
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in result_paths
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "dependency_manifest": str(
                    dependency_path.relative_to(ROOT)
                ),
                "summary": str(summary_path.relative_to(ROOT)),
                "result_count": len(result_paths),
                "publication_count": len(publication_paths),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
