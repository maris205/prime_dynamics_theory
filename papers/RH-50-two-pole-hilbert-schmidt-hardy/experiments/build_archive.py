"""Build dependency and publication archives for RH-50."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH47 = PAPERS / "RH-47-logarithmic-peripheral-conditioning"
RH48 = PAPERS / "RH-48-intrinsic-riesz-identification"
RH49 = PAPERS / "RH-49-directional-reduced-resolvent"


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
        "rh14_boundary_layer_manuscript": RH14 / "main.tex",
        "rh14_folded_gaussian_source": RH14
        / "src"
        / "parity_boundary"
        / "operators.py",
        "rh47_logarithmic_conditioning_manuscript": RH47 / "main.tex",
        "rh48_intrinsic_identification_manuscript": RH48 / "main.tex",
        "rh49_quarter_power_manuscript": RH49 / "main.tex",
        "rh49_directional_certificate": RH49
        / "results"
        / "directional_reduced_resolvent_certificate.json",
        "rh49_stable_rank_pilot": RH49
        / "results"
        / "coupling_stable_rank_pilot.json",
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
        ROOT / "figures" / "two_pole_hardy_energy.pdf",
        ROOT / "figures" / "two_pole_hardy_energy.png",
        ROOT / "main.pdf",
        ROOT / "two-pole-hilbert-schmidt-hardy-energies.pdf",
    ]
    dependency = {
        "status": (
            "all_consumed_inputs_sources_and_publication_artifacts_hashed"
        ),
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

    certificate_path = ROOT / "results" / "two_pole_hardy_certificate.json"
    result_paths = [
        certificate_path,
        ROOT / "results" / "two_pole_hardy_pilot.json",
        ROOT / "results" / "two_pole_hardy_pilot_smoke.json",
        dependency_path,
    ]
    certificate = load(certificate_path)
    audit = certificate["floating_five_scale_audit"]
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_level": certificate["evidence_level"],
        "two_pole_decomposition": certificate["two_pole_decomposition"],
        "hardy_energy_theorem": certificate["hardy_energy_theorem"],
        "stein_certificate": certificate["stein_certificate"],
        "sharp_spike_derivative": certificate["sharp_spike_derivative"],
        "outgoing_hilbert_schmidt_scale": certificate[
            "outgoing_hilbert_schmidt_scale"
        ],
        "fine_side_residue_suppression": certificate[
            "fine_side_residue_suppression"
        ],
        "global_contraction_no_go": certificate[
            "global_contraction_no_go"
        ],
        "conditional_hilbert_schmidt_closure": certificate[
            "conditional_hilbert_schmidt_closure"
        ],
        "floating_five_scale_audit": {
            "noise_levels": audit["noise_levels"],
            "largest_dimension": audit["largest_dimension"],
            "maximum_power": audit["maximum_power"],
            "probe_count": audit["probe_count"],
            "hardy_radius": audit["hardy_radius"],
            "fits": audit["fits"],
            "residue_fits": audit["residue_fits"],
            "finest_row": audit["rows"][-1],
            "hardy_tail_validated": audit["hardy_tail_validated"],
            "hutchinson_values_are_validated_uppers": audit[
                "hutchinson_values_are_validated_uppers"
            ],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in result_paths
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
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
                "dependency_manifest": str(
                    dependency_path.relative_to(ROOT)
                ),
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
