#!/usr/bin/env python3
"""Finite deterministic audit for the TPC-121 identities."""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path


TOL = 1.0e-11


def close(a: float, b: float, tol: float = TOL) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def audit() -> dict:
    fibers = {
        "alpha": [2 + 1j, 1 - 2j, -1 + 0.5j],
        "beta": [3 - 1j],
        "gamma": [1 + 0j, -1 + 0j, 2j, -2j],
    }

    energy = 0.0
    coherent = 0.0
    fluctuation = 0.0
    determinant = 0.0
    weighted_coherent = 0.0
    for values in fibers.values():
        m = len(values)
        mean = sum(values) / m
        e_n = sum(abs(z) ** 2 for z in values)
        c_n = m * abs(mean) ** 2
        v_n = sum(abs(z - mean) ** 2 for z in values)
        d_n = abs(sum(values)) ** 2
        energy += e_n
        coherent += c_n
        fluctuation += v_n
        determinant += d_n
        weighted_coherent += m * c_n

    splitting_ok = close(energy, coherent + fluctuation)
    determinant_ok = close(determinant, weighted_coherent)

    # A certified good sector centered at angle zero, plus one bad atom.
    good = [
        2.0 * cmath.exp(1j * 0.20),
        1.5 * cmath.exp(-1j * 0.25),
        0.75 * cmath.exp(1j * 0.10),
    ]
    bad = [-0.30 + 0.05j]
    kappa = min(z.real / abs(z) for z in good)
    good_mass = sum(abs(z) for z in good)
    good_energy = sum(abs(z) ** 2 for z in good)
    participation = good_mass**2 / good_energy
    bad_mass = sum(abs(z) for z in bad)
    theta = bad_mass / good_mass
    lower = (kappa - theta) * good_mass
    actual = abs(sum(good + bad))
    sector_ok = (
        kappa > theta
        and actual + TOL >= lower
        and 1.0 <= participation <= len(good) + TOL
        and actual**2 + TOL >= (kappa - theta) ** 2
        * participation
        * good_energy
    )

    good_2 = [
        1.2 * cmath.exp(1j * 0.30),
        0.8 * cmath.exp(-1j * 0.10),
    ]
    bad_2 = [-0.05 + 0j]
    kappa_2 = min(z.real / abs(z) for z in good_2)
    theta_2 = sum(abs(z) for z in bad_2) / sum(abs(z) for z in good_2)
    rho_min = min(kappa - theta, kappa_2 - theta_2)
    family_actual = actual**2 + abs(sum(good_2 + bad_2)) ** 2
    family_mass = good_mass**2 + sum(abs(z) for z in good_2) ** 2
    family_min_margin_ok = (
        rho_min > 0
        and family_actual + TOL >= rho_min**2 * family_mass
    )

    # Sharp support/magnitude obstruction: equally spaced phases cancel.
    roots = [cmath.exp(2j * math.pi * j / 7) for j in range(7)]
    cancellation_ok = abs(sum(roots)) <= TOL

    # Exponent ledger:
    # lambda_D = max(0, lambda_E + 2 lambda_phi - gamma_R).
    exponent_cases = [
        (1.00, 0.03, 0.90, 0.16),
        (1.00, 0.00, 1.00, 0.00),
        (1.10, 0.05, 0.80, 0.40),
        (0.30, 0.00, 1.00, 0.00),
    ]
    ledger_ok = all(
        close(max(0.0, le + 2 * lp - gain), ld)
        for le, lp, gain, ld in exponent_cases
    )
    diagonal_ceiling_cases = [
        (1.00, 0.03, 0.90),
        (1.10, 0.05, 0.10),
    ]
    diagonal_ceiling_ok = all(
        (
            max(0.0, le + 2 * lp - gain) < 1.0
        )
        == (gain > le + 2 * lp - 1.0)
        for le, lp, gain in diagonal_ceiling_cases
    )
    lambda_d_cert = max(0.0, 1.00 + 2 * 0.03 - 0.90)
    eta_z = 0.09
    compatibility_ok = lambda_d_cert <= 2 * eta_z + TOL

    status = all(
        [
            splitting_ok,
            determinant_ok,
            sector_ok,
            family_min_margin_ok,
            cancellation_ok,
            ledger_ok,
            diagonal_ceiling_ok,
            compatibility_ok,
        ]
    )
    payload = {
        "schema": "tpc-121-fiber-phase-coherence-v1",
        "status": "PASS" if status else "FAIL",
        "checks": {
            "mean_fluctuation_splitting": splitting_ok,
            "determinant_weighted_coherence": determinant_ok,
            "phase_sector_lower_bound": sector_ok,
            "multiple_fiber_minimum_margin": family_min_margin_ok,
            "equal_modulus_cancellation_obstruction": cancellation_ok,
            "exponent_ledger": ledger_ok,
            "diagonal_ceiling_participation_condition": diagonal_ceiling_ok,
            "determinant_zero_compatibility": compatibility_ok,
        },
        "sample": {
            "energy": energy,
            "coherent_energy": coherent,
            "fluctuation_energy": fluctuation,
            "determinant_energy": determinant,
            "sector_actual": actual,
            "sector_lower_bound": lower,
            "good_energy": good_energy,
            "effective_participation": participation,
            "family_minimum_margin": rho_min,
            "sample_lambda_D_cert": lambda_d_cert,
        },
        "claim_boundary": {
            "actual_growing_phase_margin": False,
            "actual_growing_diagonal_lower_bound": False,
            "actual_growing_participation_gain": False,
            "fixed_h0_L2_saving": False,
        },
    }
    return payload


def main() -> None:
    payload = audit()
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
