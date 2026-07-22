"""Build RH-65 dependency and publication hashes."""

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
        "rh64_summary": PAPERS
        / "RH-64-weighted-terminal-residuals"
        / "results"
        / "summary.json",
        "rh64_manuscript": PAPERS
        / "RH-64-weighted-terminal-residuals"
        / "main.tex",
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
        ROOT / "figures" / "physical_family_metric_conditioning.pdf",
        ROOT / "figures" / "physical_family_metric_conditioning.png",
        ROOT / "main.pdf",
        ROOT / "physical-family-metric-conditioning.pdf",
    ]
    dependency = {
        "status": "all_rh65_inputs_sources_and_publication_artifacts_hashed",
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
    pilot = json.loads(
        (ROOT / "results" / "family_conditioning_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    arb = json.loads(
        (ROOT / "results" / "arb_two_step_audit.json").read_text(
            encoding="utf-8"
        )
    )
    result_paths = [
        ROOT / "results" / "family_conditioning_pilot.json",
        ROOT / "results" / "family_conditioning_smoke.json",
        ROOT / "results" / "arb_two_step_audit.json",
        dependency_path,
    ]
    summary = {
        "status": "rh65_physical_family_metric_conditioning_audit",
        "theorem": {
            "exact_contraction_ledger": True,
            "matched_scale_uniform_conditioning": True,
            "unmatched_jordan_obstruction": True,
            "power_law_cost_ledger": True,
            "growing_chain_superpolynomial_barrier": True,
        },
        "program_boundary": {
            "production_family_uniformity": False,
            "block_cross_column_fusion": False,
            "stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "hilbert_polya_operator": False,
        },
        "pilot": {
            "precision_decimal_digits": pilot[
                "precision_decimal_digits"
            ],
            "case_count": len(pilot["cases"]),
            "cases": [
                {
                    "dimension": case["dimension"],
                    "coupling_power": case["coupling_power"],
                    "predicted_condition_exponent": case[
                        "predicted_condition_exponent"
                    ],
                    "fitted_condition_exponent": case[
                        "fitted_condition_exponent"
                    ],
                    "predicted_metric_gap_exponent": case[
                        "predicted_metric_gap_exponent"
                    ],
                    "fitted_metric_gap_exponent": case[
                        "fitted_metric_gap_exponent"
                    ],
                    "endpoint": case["endpoint"],
                }
                for case in pilot["cases"]
            ],
        },
        "arb": {
            key: value
            for key, value in arb.items()
            if key.endswith("certified")
            or key.startswith("fixed_coupling_")
            or key.startswith("matched_condition_")
            or key.startswith("matched_metric_")
            or key in ("precision_bits", "production_interval_audit_executed")
        },
        "route_consequence": pilot["route_consequence"],
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
