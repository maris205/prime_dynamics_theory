"""Compose the RH-36 nested-grid physical-count theorem certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    block_path = ROOT / "results" / "nested_block_certificate_sigma_1e-02.json"
    atlas_path = ROOT / "results" / "physical_resolvent_atlas.json"
    coarse_path = ROOT / "results" / "coarse_count_replay.json"
    pilot_path = ROOT / "results" / "fine_spectrum_pilot_sigma_1e-02.json"
    snapshot_path = ROOT / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
    block = load(block_path)
    atlas = load(atlas_path)
    coarse = load(coarse_path)
    pilot = load(pilot_path)

    snapshot_hash = sha256_file(snapshot_path)
    object_identity = bool(
        snapshot_hash == block["snapshot_sha256"]
        and snapshot_hash == coarse["snapshot_sha256"]
    )
    block_gate = block["continuation_gate"]
    detail_gate = bool(
        block_gate["detail_spectrum_outside_counting_circle"]
        and float(block_gate["detail_norm_upper"])
        < float(block_gate["contour_origin_distance_lower"])
    )
    atlas_gate = bool(
        atlas["status"] == "full_physical_resolvent_continuation_atlas"
        and atlas["exact_rational_partition_verified"]
        and atlas["unresolved_leaf_count"] == 0
        and atlas["all_continuation_products_below_one"]
        and float(atlas["maximum_continuation_product_upper"]) < 1.0
    )
    coarse_gate = bool(
        coarse["coarse_physical_inside_count_certified"]
        and int(coarse["coarse_physical_inside_count"]) == 1
        and coarse["pair_defect_hash_match"]
        and coarse["transfer_ledger_hash_match"]
    )
    theorem = bool(object_identity and detail_gate and atlas_gate and coarse_gate)
    payload = {
        "status": (
            "rigorous_nested_grid_physical_count_one"
            if theorem
            else "nested_grid_physical_count_incomplete"
        ),
        "scope": (
            "exact stored binary64 Perron/parity-extracted physical two-step "
            "matrices at sigma=1e-2 on the 2048 and 4096 midpoint grids"
        ),
        "evidence_level": "rigorous_computer_assisted_stored_model_theorem",
        "sigma": float(block["sigma"]),
        "coarse_dimension": int(block["coarse_dimension"]),
        "fine_dimension": int(block["fine_dimension"]),
        "snapshot_sha256": snapshot_hash,
        "stored_object_identity_verified": object_identity,
        "exact_dyadic_coordinate_decomposition": True,
        "exact_schur_determinant_identity": True,
        "coarse_physical_inside_count_certified": coarse_gate,
        "coarse_physical_inside_count": 1 if coarse_gate else None,
        "detail_inside_count_certified_zero": detail_gate,
        "detail_inside_count": 0 if detail_gate else None,
        "full_boundary_continuation_certified": atlas_gate,
        "fine_physical_inside_count_certified": theorem,
        "fine_physical_inside_count": 1 if theorem else None,
        "block_norm_uppers": {
            name: float(values["block_two_norm_upper"])
            for name, values in block["block_certificates"].items()
        },
        "detail_resolvent_upper": float(
            block_gate["detail_resolvent_upper"]
        ),
        "self_energy_upper": float(block_gate["self_energy_upper"]),
        "effective_perturbation_upper": float(
            block_gate["effective_perturbation_upper"]
        ),
        "theorem_admissible_coarse_resolvent_upper": float(
            atlas["theorem_admissible_coarse_resolvent_upper"]
        ),
        "atlas_center_count": int(atlas["center_count"]),
        "atlas_leaf_count": int(atlas["closed_leaf_count"]),
        "maximum_transported_coarse_resolvent_upper": float(
            atlas["maximum_transported_inverse_upper"]
        ),
        "maximum_continuation_product_upper": float(
            atlas["maximum_continuation_product_upper"]
        ),
        "coarse_count_replay": {
            "leaf_count": int(coarse["leaf_count"]),
            "pair_defect_hash_match": bool(coarse["pair_defect_hash_match"]),
            "transfer_ledger_hash_match": bool(
                coarse["transfer_ledger_hash_match"]
            ),
            "maximum_feshbach_rouche_product_upper": float(
                coarse["maximum_feshbach_rouche_product_upper"]
            ),
        },
        "floating_localization": {
            "evidence_level": "floating_not_validated",
            "coarse_inside_real": float(pilot["coarse_inside"][0]["real"]),
            "coarse_inside_imag": float(pilot["coarse_inside"][0]["imag"]),
            "fine_inside_real": float(pilot["fine_inside"][0]["real"]),
            "fine_inside_imag": float(pilot["fine_inside"][0]["imag"]),
            "coarse_to_fine_displacement": float(
                pilot["inside_eigenvalue_displacement"]
            ),
        },
        "certificate_files": {
            "nested_block_certificate": {
                "path": str(block_path.relative_to(ROOT)),
                "sha256": sha256_file(block_path),
            },
            "physical_resolvent_atlas": {
                "path": str(atlas_path.relative_to(ROOT)),
                "sha256": sha256_file(atlas_path),
            },
            "coarse_count_replay": {
                "path": str(coarse_path.relative_to(ROOT)),
                "sha256": sha256_file(coarse_path),
            },
            "floating_spectrum_pilot": {
                "path": str(pilot_path.relative_to(ROOT)),
                "sha256": sha256_file(pilot_path),
            },
        },
        "limitations": [
            "The theorem compares two exact finite stored binary64 matrices at one fixed noise scale.",
            "It does not enclose either matrix relative to the continuum Gaussian operator.",
            "It does not prove convergence for arbitrarily increasing dimensions.",
            "It does not prove a zero-noise limit or identify any zeta zero.",
            "It makes no Hilbert-Polya or Riemann-hypothesis claim.",
        ],
    }
    output = ROOT / "results" / "nested_grid_physical_count_certificate.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not theorem:
        raise RuntimeError("the nested-grid physical count theorem did not close")


if __name__ == "__main__":
    main()
