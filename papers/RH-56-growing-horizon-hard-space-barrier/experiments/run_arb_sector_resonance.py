"""Validate one non-Perron analytic-sector resonance inherited from RH-13."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from flint import acb, acb_mat, arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH13 = PAPERS / "RH-13-validated-reduced-sector-spectral-gap"
sys.path.insert(0, str(RH13 / "src"))

from validated_gap.certificate import (  # noqa: E402
    _finite_matrices,
    algebraic_parameter,
)


OUTPUT = ROOT / "results" / "arb_sector_resonance_certificate.json"
DIMENSION = 50
TAIL_DEGREE = 100
DISK_RADIUS_TEXT = "0.7"
CENTER_TEXT = "0.2078803"
CONTOUR_RADIUS_TEXT = "0.05"
TRUNCATION_ERROR_TEXT = "0.000523774672228"
CONTOUR_NODES = 128


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    ctx.prec = 512
    ctx.cap = TAIL_DEGREE
    disk_radius = arb(DISK_RADIUS_TEXT)
    center = arb(CENTER_TEXT)
    contour_radius = arb(CONTOUR_RADIUS_TEXT)
    truncation_error = arb(TRUNCATION_ERROR_TEXT)
    beta_one, _ = _finite_matrices(
        DIMENSION, TAIL_DEGREE, disk_radius, algebraic_parameter()
    )

    # Odd coordinate numbers are the nonzero invariant block; even input
    # columns vanish, so the remaining coordinates contribute only zeros.
    active = list(range(1, DIMENSION, 2))
    block = acb_mat(
        [[beta_one[row, column] for column in active] for row in active]
    )
    eigenvalues = block.eig(algorithm="rump", maxiter=10000)
    ordered = sorted(eigenvalues, key=lambda value: float(abs(value).upper()), reverse=True)
    lower = center - contour_radius
    upper = center + contour_radius
    inside = [
        value
        for value in eigenvalues
        if abs(value - center) < contour_radius
    ]
    if len(inside) != 1:
        raise RuntimeError("the finite active block did not isolate one eigenvalue")

    # Arb inverses at a uniform net, followed by the resolvent identity,
    # enclose the entire circular contour.
    finite = acb_mat(beta_one)
    identity = acb_mat(
        [
            [1 if row == column else 0 for column in range(DIMENSION)]
            for row in range(DIMENSION)
        ]
    )
    node_one_norm = arb(0)
    for index in range(CONTOUR_NODES):
        angle = 2 * arb.pi() * index / CONTOUR_NODES
        z = acb(
            center + contour_radius * angle.cos(),
            contour_radius * angle.sin(),
        )
        resolvent = (z * identity - finite).inv()
        for column in range(DIMENSION):
            column_sum = sum(
                abs(resolvent[row, column]) for row in range(DIMENSION)
            )
            node_one_norm = node_one_norm.max(column_sum)
    covering_radius = 2 * contour_radius * (arb.pi() / CONTOUR_NODES).sin()
    covering_product = covering_radius * node_one_norm
    if not covering_product < 1:
        raise RuntimeError("the contour net does not close by resolvent identity")
    contour_one_norm = node_one_norm / (1 - covering_product)
    perturbation_product = contour_one_norm * truncation_error
    if not perturbation_product < 1:
        raise RuntimeError("the analytic tail does not preserve the contour")

    certified_modulus_lower = lower
    one_step_rate_lower = certified_modulus_lower.sqrt()
    payload = {
        "status": "arb_validated_nonperron_analytic_sector_resonance",
        "evidence_level": (
            "512-bit Arb eigenvalue inclusion for the RH-13 finite Taylor "
            "block plus the archived analytic truncation bound"
        ),
        "precision_bits": 512,
        "dimension": DIMENSION,
        "active_dimension": len(active),
        "tail_degree": TAIL_DEGREE,
        "contour_center_ball": str(center),
        "contour_radius_ball": str(contour_radius),
        "leading_finite_eigenvalue_ball": str(ordered[0]),
        "second_finite_eigenvalue_ball": str(ordered[1]),
        "finite_eigenvalues_in_contour": len(inside),
        "contour_nodes": CONTOUR_NODES,
        "finite_full_matrix_contour_node_resolvent_one_norm_ball": str(
            node_one_norm
        ),
        "contour_covering_radius_ball": str(covering_radius),
        "contour_covering_product_ball": str(covering_product),
        "finite_full_contour_resolvent_one_norm_ball": str(contour_one_norm),
        "analytic_truncation_error_ball": str(truncation_error),
        "full_contour_perturbation_product_ball": str(perturbation_product),
        "certified_sector_resonance_modulus_lower_ball": str(
            certified_modulus_lower
        ),
        "certified_one_step_rate_lower_ball": str(one_step_rate_lower),
        "rate_lower_exceeds_r_to_eight_certified": (
            one_step_rate_lower > arb("0.85") ** 8
        ),
        "theorem_method": (
            "RH-13 gives ||T-M||_1<=epsilon. Arb isolates exactly one finite "
            "eigenvalue in |w-0.2078803|<0.05. A contour resolvent homotopy "
            "with the archived tail preserves its Riesz rank. A 128-node "
            "Arb inverse net and the resolvent identity cover the full circle."
        ),
        "sources": {
            "rh13_certificate_source": {
                "path": str(
                    (RH13 / "src" / "validated_gap" / "certificate.py").relative_to(
                        REPOSITORY
                    )
                ),
                "sha256": sha256_file(
                    RH13 / "src" / "validated_gap" / "certificate.py"
                ),
            },
            "rh13_certificate": {
                "path": str(
                    (
                        RH13
                        / "results"
                        / "validated_spectral_gap_certificate.json"
                    ).relative_to(REPOSITORY)
                ),
                "sha256": sha256_file(
                    RH13
                    / "results"
                    / "validated_spectral_gap_certificate.json"
                ),
            },
        },
        "production_noisy_bulk_eigensolver_executed": False,
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
