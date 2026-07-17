"""Compose the RH-37 iterated dyadic physical-count theorem certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    metadata_path = ROOT / "results" / "second_dyadic_snapshot_sigma_1e-02.json"
    block_path = (
        ROOT / "results" / "second_dyadic_block_certificate_sigma_1e-02.json"
    )
    atlas_path = ROOT / "results" / "propagated_resolvent_atlas.json"
    replay_path = ROOT / "results" / "inherited_A4096_count_replay.json"
    pilot_path = ROOT / "results" / "second_dyadic_spectrum_pilot_sigma_1e-02.json"
    inherited_block_path = (
        RH36 / "results" / "nested_block_certificate_sigma_1e-02.json"
    )
    inherited_theorem_path = (
        RH36 / "results" / "nested_grid_physical_count_certificate.json"
    )
    metadata = load(metadata_path)
    block = load(block_path)
    atlas = load(atlas_path)
    replay = load(replay_path)
    pilot = load(pilot_path)
    inherited_block = load(inherited_block_path)
    inherited_theorem = load(inherited_theorem_path)

    part_identity = all(
        sha256_file(ROOT / relative) == metadata["snapshot_part_sha256"][name]
        for name, relative in metadata["snapshot_parts"].items()
    )
    block_identity = bool(
        block["snapshot_metadata_sha256"] == sha256_file(metadata_path)
        and block["snapshot_part_sha256"] == metadata["snapshot_part_sha256"]
        and block["inherited_snapshot_sha256"]
        == metadata["inherited_snapshot_sha256"]
    )
    object_identity = bool(
        part_identity
        and block_identity
        and replay["coarse_object_array_hash_match"]
        and replay["snapshot_hash_match"]
    )
    inherited_count_gate = bool(
        replay["rh37_coarse_physical_inside_count_certified"]
        and int(replay["rh37_coarse_physical_inside_count"]) == 1
        and inherited_theorem["status"] == "rigorous_nested_grid_physical_count_one"
    )
    second_gate = block["continuation_gate"]
    detail_gate = bool(
        second_gate["detail_spectrum_outside_counting_circle"]
        and float(second_gate["detail_norm_upper"])
        < float(second_gate["contour_origin_distance_lower"])
    )
    atlas_gate = bool(
        atlas["status"] == "full_iterated_propagated_resolvent_atlas"
        and atlas["exact_rational_partition_verified"]
        and int(atlas["unresolved_leaf_count"]) == 0
        and atlas["all_first_gates_closed"]
        and atlas["all_second_gates_closed"]
        and float(atlas["maximum_first_effective_product_upper"]) < 1.0
        and float(atlas["maximum_second_continuation_product_upper"]) < 1.0
        and atlas["inherited_first_block_certificate_sha256"]
        == sha256_file(inherited_block_path)
        and atlas["second_block_certificate_sha256"] == sha256_file(block_path)
    )
    theorem = bool(object_identity and inherited_count_gate and detail_gate and atlas_gate)
    payload = {
        "status": (
            "rigorous_iterated_dyadic_physical_count_one"
            if theorem
            else "iterated_dyadic_physical_count_incomplete"
        ),
        "scope": (
            "exact stored binary64 Perron/parity-extracted physical two-step "
            "matrices at sigma=1e-2 on the 2048, 4096, and 8192 midpoint grids"
        ),
        "evidence_level": "rigorous_computer_assisted_stored_model_theorem",
        "sigma": float(block["sigma"]),
        "base_dimension": 2048,
        "coarse_dimension": int(block["coarse_dimension"]),
        "fine_dimension": int(block["fine_dimension"]),
        "stored_object_identity_verified": object_identity,
        "split_snapshot_parts_verified": part_identity,
        "exact_dyadic_coordinate_decomposition": True,
        "exact_schur_determinant_identity_at_both_levels": True,
        "inherited_A2048_inside_count": int(
            inherited_theorem["coarse_physical_inside_count"]
        ),
        "inherited_A4096_inside_count_certified": inherited_count_gate,
        "inherited_A4096_inside_count": 1 if inherited_count_gate else None,
        "second_detail_inside_count_certified_zero": detail_gate,
        "second_detail_inside_count": 0 if detail_gate else None,
        "full_propagated_boundary_atlas_certified": atlas_gate,
        "A8192_inside_count_certified": theorem,
        "A8192_inside_count": 1 if theorem else None,
        "certified_count_chain": (
            {"A2048": 1, "A4096": 1, "A8192": 1} if theorem else None
        ),
        "first_refinement": {
            "source": str(inherited_block_path),
            "source_sha256": sha256_file(inherited_block_path),
            "block_norm_uppers": {
                name: float(values["block_two_norm_upper"])
                for name, values in inherited_block["block_certificates"].items()
            },
            "detail_resolvent_upper": float(
                inherited_block["continuation_gate"]["detail_resolvent_upper"]
            ),
            "effective_perturbation_upper": float(
                inherited_block["continuation_gate"][
                    "effective_perturbation_upper"
                ]
            ),
        },
        "second_refinement": {
            "block_norm_uppers": {
                name: float(values["block_two_norm_upper"])
                for name, values in block["block_certificates"].items()
            },
            "detail_resolvent_upper": float(second_gate["detail_resolvent_upper"]),
            "self_energy_upper": float(second_gate["self_energy_upper"]),
            "effective_perturbation_upper": float(
                second_gate["effective_perturbation_upper"]
            ),
            "admissible_A4096_resolvent_upper": float(
                second_gate["admissible_coarse_resolvent_upper"]
            ),
        },
        "propagated_atlas": {
            "total_center_count": int(atlas["center_count"]),
            "inherited_center_count": int(atlas["inherited_center_count"]),
            "additional_center_count": int(atlas["additional_center_count"]),
            "leaf_count": int(atlas["closed_leaf_count"]),
            "maximum_transported_A2048_resolvent_upper": float(
                atlas["maximum_transported_coarse_resolvent_upper"]
            ),
            "maximum_first_effective_product_upper": float(
                atlas["maximum_first_effective_product_upper"]
            ),
            "maximum_propagated_A4096_resolvent_upper": float(
                atlas["maximum_propagated_fine_resolvent_upper"]
            ),
            "maximum_second_continuation_product_upper": float(
                atlas["maximum_second_continuation_product_upper"]
            ),
        },
        "floating_localization": {
            "evidence_level": "floating_not_validated",
            "A4096_inside_real": float(pilot["coarse_inside"][0]["real"]),
            "A4096_inside_imag": float(pilot["coarse_inside"][0]["imag"]),
            "A8192_inside_real": float(pilot["fine_inside"][0]["real"]),
            "A8192_inside_imag": float(pilot["fine_inside"][0]["imag"]),
            "A4096_to_A8192_displacement": float(
                pilot["inside_eigenvalue_displacement"]
            ),
        },
        "certificate_files": {
            "snapshot_metadata": {
                "path": str(metadata_path.relative_to(ROOT)),
                "sha256": sha256_file(metadata_path),
            },
            "second_block_certificate": {
                "path": str(block_path.relative_to(ROOT)),
                "sha256": sha256_file(block_path),
            },
            "propagated_resolvent_atlas": {
                "path": str(atlas_path.relative_to(ROOT)),
                "sha256": sha256_file(atlas_path),
            },
            "inherited_count_replay": {
                "path": str(replay_path.relative_to(ROOT)),
                "sha256": sha256_file(replay_path),
            },
            "floating_spectrum_pilot": {
                "path": str(pilot_path.relative_to(ROOT)),
                "sha256": sha256_file(pilot_path),
            },
            "inherited_RH36_theorem": {
                "path": str(inherited_theorem_path),
                "sha256": sha256_file(inherited_theorem_path),
            },
        },
        "limitations": [
            "The theorem concerns three exact finite stored binary64 matrices at one fixed Gaussian width.",
            "It does not enclose any discretization relative to a continuum transfer operator.",
            "It proves one further dyadic step, not induction over all grid dimensions.",
            "The observed quarter/half block scaling is diagnostic and is not promoted to an asymptotic theorem.",
            "It does not prove a zero-noise limit or identify any zeta zero.",
            "It makes no Hilbert-Polya or Riemann-hypothesis claim.",
        ],
    }
    output = ROOT / "results" / "iterated_dyadic_physical_count_certificate.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not theorem:
        raise RuntimeError("the iterated dyadic physical count theorem did not close")


if __name__ == "__main__":
    main()
