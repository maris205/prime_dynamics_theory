"""Arb certificate for a unified all-order deterministic coefficient envelope."""

from __future__ import annotations

from dataclasses import dataclass

from flint import arb

from boundary_budget import certify_boundary_budget


@dataclass(frozen=True)
class EnvelopeCertificate:
    q_star: arb
    nu1: arb
    nu2: arb
    nu3: arb
    scaled_cube: arb
    residue_constants: tuple[arb, arb, arb]
    envelope_constant: arb


def certify_envelope(reduced_bounds: object) -> EnvelopeCertificate:
    """Certify ``|a_n| < 48 q_star^n`` from the RH-13 bounds."""

    budget = certify_boundary_budget(reduced_bounds, scaled_circle=arb(1))
    lam = reduced_bounds.lam
    q_star = (1 / ((arb(17) / 20) * lam)).upper()
    nu1 = budget.nuclear_norm.upper()
    nu2 = (budget.operator_norm * nu1).upper()
    nu3 = (budget.operator_square_norm * nu1).upper()
    scaled_cube = (reduced_bounds.beta_one_cube_bound * lam**6).upper()
    if not scaled_cube < 1:
        raise RuntimeError("the reduced trace residues do not decay after lambda scaling")
    constants = tuple(
        (1 + 2 * nu * lam ** (2 * residue)).upper()
        for residue, nu in enumerate((nu1, nu2, nu3), start=1)
    )
    envelope_constant = max(constants).upper()
    if not envelope_constant < arb(48):
        raise RuntimeError("the clean envelope constant 48 was not certified")
    if not lam**-1 < arb(3).sqrt() - 1:
        raise RuntimeError("the endpoint scalar inequality was not certified")
    return EnvelopeCertificate(
        q_star=q_star,
        nu1=nu1,
        nu2=nu2,
        nu3=nu3,
        scaled_cube=scaled_cube,
        residue_constants=constants,
        envelope_constant=envelope_constant,
    )


def clean_envelope(order: int, q_star: arb) -> arb:
    n = int(order)
    if n < 2:
        raise ValueError("the envelope starts at order two")
    return (arb(48) * arb(q_star) ** n).upper()
