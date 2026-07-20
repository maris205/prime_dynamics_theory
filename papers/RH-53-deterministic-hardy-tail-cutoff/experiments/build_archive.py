"""Build dependency and publication archives for RH-53."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
RH51 = PAPERS / "RH-51-cyclic-rank-growing-horizon-stein"
RH52 = PAPERS / "RH-52-intrinsic-peripheral-residue-transfer"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def repository_entry(path: Path):
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def external_inputs():
    return {
        "rh39_cutoff_manuscript": RH39 / "main.tex",
        "rh39_cutoff_bounds": RH39 / "src" / "cutoff_bridge" / "bounds.py",
        "rh50_hardy_manuscript": RH50 / "main.tex",
        "rh50_hardy_pilot": RH50 / "results" / "two_pole_hardy_pilot.json",
        "rh51_stein_manuscript": RH51 / "main.tex",
        "rh51_stein_pilot": RH51 / "results" / "structured_stein_pilot.json",
        "rh52_factor_manuscript": RH52 / "main.tex",
        "roadmap": PAPERS / "RH-ROADMAP-after-RH50.md",
    }


def main() -> None:
    local_sources = sorted(
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
        ROOT / "figures" / "deterministic_hardy_tail_cutoff.pdf",
        ROOT / "figures" / "deterministic_hardy_tail_cutoff.png",
        ROOT / "main.pdf",
        ROOT / "deterministic-block-tail-hardy-cutoff.pdf",
    ]
    dependency = {
        "status": "all_consumed_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: repository_entry(path)
            for name, path in external_inputs().items()
        },
        "local_sources": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in local_sources
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

    certificate_path = ROOT / "results" / "hardy_tail_cutoff_certificate.json"
    result_paths = [
        certificate_path,
        ROOT / "results" / "deterministic_tail_pilot.json",
        ROOT / "results" / "deterministic_tail_pilot_smoke.json",
        ROOT / "results" / "arb_tail_audit.json",
        ROOT / "results" / "arb_production_cutoff_ledger.json",
        dependency_path,
    ]
    certificate = load(certificate_path)
    audit = certificate["floating_five_scale_audit"]
    production = certificate["rh50_production_cutoff_ledger"]
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_level": certificate["evidence_level"],
        "deterministic_main_sum": certificate["deterministic_main_sum"],
        "infinite_tail_theorem": certificate["infinite_tail_theorem"],
        "perturbation_transfer": certificate["perturbation_transfer"],
        "cutoff_result": certificate["cutoff_result"],
        "program_conclusion": certificate["program_conclusion"],
        "floating_five_scale_audit": {
            "noise_levels": audit["noise_levels"],
            "largest_dimension": audit["largest_dimension"],
            "maximum_relative_energy_excess": audit[
                "maximum_relative_energy_excess"
            ],
            "maximum_selected_tail_energy_squared_upper": audit[
                "maximum_selected_tail_energy_squared_upper"
            ],
            "all_column_deterministic": audit["all_column_deterministic"],
            "hutchinson_probes_used": audit["hutchinson_probes_used"],
            "finest_row": audit["rows"][-1],
            "interval_validated": audit["interval_validated"],
        },
        "production_cutoff_audit": {
            "largest_dimension": production["largest_dimension"],
            "maximum_fixed_eight_two_norm_upper": production[
                "maximum_fixed_eight_two_norm_upper"
            ],
            "all_stored_multiples_above_adaptive_requirement": production[
                "all_stored_multiples_above_adaptive_requirement"
            ],
        },
        "arb_audit": {
            "status": certificate["arb_audit"]["status"],
            "dimension": certificate["arb_audit"]["dimension"],
            "certified_block_contraction": certificate["arb_audit"][
                "certified_block_contraction"
            ],
            "production_matrix_interval_executed": certificate["arb_audit"][
                "production_matrix_interval_executed"
            ],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in result_paths
        },
        "publication_artifact_hashes": dependency["publication_artifacts"],
        "limitations": certificate["limitations"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "dependency_manifest": str(dependency_path.relative_to(ROOT)),
                "summary": str(summary_path.relative_to(ROOT)),
                "result_count": len(result_paths),
                "publication_count": len(publication_paths),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
