"""Build dependency and publication archives for RH-49."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH38 = PAPERS / "RH-38-dyadic-haar-block-decay"
RH46 = PAPERS / "RH-46-small-noise-mesh-double-pole"
RH48 = PAPERS / "RH-48-intrinsic-riesz-identification"


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
        "rh14_folded_gaussian_operator_source": RH14
        / "src"
        / "parity_boundary"
        / "operators.py",
        "rh38_haar_decay_manuscript": RH38 / "main.tex",
        "rh46_small_noise_mesh_manuscript": RH46 / "main.tex",
        "rh48_intrinsic_identification_manuscript": RH48 / "main.tex",
        "rh48_intrinsic_identification_certificate": RH48
        / "results"
        / "intrinsic_riesz_identification_certificate.json",
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
        ROOT / "figures" / "directional_reduced_resolvent.pdf",
        ROOT / "figures" / "directional_reduced_resolvent.png",
        ROOT / "residue-deflated-directional-resolvents.pdf",
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

    certificate_path = (
        ROOT / "results" / "directional_reduced_resolvent_certificate.json"
    )
    result_paths = [
        certificate_path,
        ROOT / "results" / "reduced_directional_pilot.json",
        ROOT / "results" / "reduced_directional_pilot_smoke.json",
        ROOT / "results" / "mixed_operator_gain_pilot.json",
        ROOT / "results" / "mixed_operator_gain_pilot_smoke.json",
        ROOT / "results" / "coupling_stable_rank_pilot.json",
        ROOT / "results" / "coupling_stable_rank_pilot_smoke.json",
        dependency_path,
    ]
    certificate = load(certificate_path)
    audit = certificate["floating_five_scale_audit"]
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_level": certificate["evidence_level"],
        "exact_residue_deflation": certificate["exact_residue_deflation"],
        "stable_rank_transfer": certificate["stable_rank_transfer"],
        "critical_endpoint_coupling_theorem": certificate[
            "critical_endpoint_coupling_theorem"
        ],
        "quarter_power_closure": certificate["quarter_power_closure"],
        "residual_certificate": certificate["residual_certificate"],
        "floating_five_scale_audit": {
            "noise_levels": audit["noise_levels"],
            "largest_dimension": audit["largest_dimension"],
            "quarter_power_target": audit["quarter_power_target"],
            "rh48_critical_exponent": audit["rh48_critical_exponent"],
            "fits": audit["fits"],
            "last_three_level_fits": audit["last_three_level_fits"],
            "finest_row": audit["rows"][-1],
            "operator_candidates_are_validated_uppers": audit[
                "operator_candidates_are_validated_uppers"
            ],
            "hutchinson_gains_are_validated_uppers": audit[
                "hutchinson_gains_are_validated_uppers"
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
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
