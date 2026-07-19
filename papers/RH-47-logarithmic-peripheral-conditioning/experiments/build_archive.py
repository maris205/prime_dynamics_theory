"""Build dependency and publication archives for RH-47."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
RH44 = PAPERS / "RH-44-validated-rank-two-peripheral-complement"
RH46 = PAPERS / "RH-46-small-noise-mesh-double-pole"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def external_inputs() -> dict[str, Path]:
    return {
        "rh14_boundary_layer_manuscript": RH14 / "main.tex",
        "rh14_boundary_layer_summary": RH14
        / "results"
        / "square_root_boundary_layer_summary.json",
        "rh14_boundary_layer_source": RH14
        / "src"
        / "parity_boundary"
        / "boundary_layer.py",
        "rh14_operator_source": RH14
        / "src"
        / "parity_boundary"
        / "operators.py",
        "rh42_fixed_noise_euclidean_contour": RH42
        / "results"
        / "uniform_euclidean_parity_certificate.json",
        "rh44_fixed_noise_rank_two_complement": RH44
        / "results"
        / "validated_rank_two_peripheral_complement.json",
        "rh46_small_noise_mesh_certificate": RH46
        / "results"
        / "small_noise_mesh_double_pole_certificate.json",
    }


def dependency_manifest() -> dict[str, object]:
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
        ROOT / "figures" / "logarithmic_peripheral_conditioning.pdf",
        ROOT / "figures" / "logarithmic_peripheral_conditioning.png",
        ROOT / "logarithmic-peripheral-conditioning.pdf",
    ]
    return {
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


def main() -> None:
    dependency = dependency_manifest()
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(
        json.dumps(dependency, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    certificate_path = (
        ROOT
        / "results"
        / "logarithmic_peripheral_conditioning_certificate.json"
    )
    pilot_path = (
        ROOT / "results" / "small_noise_peripheral_factor_pilot.json"
    )
    certificate = load(certificate_path)
    pilot = load(pilot_path)
    smallest = pilot["rows"][-1]
    hashed_results = [certificate_path, pilot_path, dependency_path]
    summary = {
        "status": certificate["status"],
        "scope": certificate["scope"],
        "evidence_level": certificate["evidence_level"],
        "mesoscopic_endpoint_theorem": certificate[
            "mesoscopic_endpoint_theorem"
        ],
        "peripheral_conditioning_theorem": certificate[
            "peripheral_conditioning_theorem"
        ],
        "resolvent_obstruction": certificate["resolvent_obstruction"],
        "peripheral_kernel_derivatives": certificate[
            "peripheral_kernel_derivatives"
        ],
        "continuum_anchored_bulk": certificate["continuum_anchored_bulk"],
        "intrinsic_discrete_identification_boundary": certificate[
            "intrinsic_discrete_identification_boundary"
        ],
        "floating_pilot": {
            "status": pilot["status"],
            "evidence_level": pilot["evidence_level"],
            "noise_levels": len(pilot["rows"]),
            "resolution": pilot["resolution"],
            "smallest_sigma": smallest["sigma"],
            "smallest_dimension": smallest["dimension"],
            "smallest_perron_projector_norm": smallest[
                "perron_projector_norm"
            ],
            "smallest_parity_projector_norm": smallest[
                "parity_projector_norm"
            ],
            "smallest_rank_two_frobenius": smallest[
                "weighted_rank_two_frobenius"
            ],
            "smallest_perron_resolvent_lower": smallest[
                "perron_contour_resolvent_lower"
            ],
            "smallest_parity_resolvent_lower": smallest[
                "parity_contour_resolvent_lower"
            ],
            "smallest_endpoint_perron_coefficient": smallest[
                "endpoint_perron_tail_coefficient"
            ],
            "smallest_endpoint_parity_coefficient": smallest[
                "endpoint_parity_tail_coefficient"
            ],
            "perron_log_fit": pilot["perron_log_fit"],
            "parity_log_fit": pilot["parity_log_fit"],
            "rank_two_log_fit": pilot["rank_two_log_fit"],
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path)
            for path in hashed_results
        },
        "publication_artifact_hashes": dependency[
            "publication_artifacts"
        ],
        "limitations": certificate["limitations"],
    }
    output = ROOT / "results" / "summary.json"
    output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
