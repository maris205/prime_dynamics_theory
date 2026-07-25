#!/usr/bin/env python3
"""Deterministic finite certificate for TPC-107."""

import cmath
import json
from pathlib import Path


def close(a, b, tol=1e-10):
    return abs(a - b) <= tol


def evaluate(atom_coeffs, phases, resonances, filt):
    atom_count = len(atom_coeffs)
    freq_count = len(filt)
    profile = []
    kernels = [0j] * atom_count
    preabs = 0.0
    for r in range(freq_count):
        value = 0j
        for p in range(atom_count):
            rho = resonances[p][r]
            value += atom_coeffs[p] * phases[p][r] * rho
            kernels[p] += filt[r] * phases[p][r] * rho
            preabs += abs(atom_coeffs[p]) * abs(filt[r]) * rho
        profile.append(value)
    frequency_sum = sum(filt[r] * profile[r] for r in range(freq_count))
    atom_sum = sum(atom_coeffs[p] * kernels[p] for p in range(atom_count))
    filtered_majorant = sum(
        abs(atom_coeffs[p]) * abs(kernels[p]) for p in range(atom_count)
    )
    signed_energy = sum(abs(value) ** 2 for value in profile)

    gram_energy = 0j
    for p in range(atom_count):
        for u in range(atom_count):
            gram = sum(
                phases[p][r]
                * phases[u][r].conjugate()
                * resonances[p][r]
                * resonances[u][r]
                for r in range(freq_count)
            )
            gram_energy += atom_coeffs[p] * atom_coeffs[u].conjugate() * gram
    return {
        "frequency_sum": frequency_sum,
        "atom_sum": atom_sum,
        "filtered_majorant": filtered_majorant,
        "preabs": preabs,
        "signed_energy": signed_energy,
        "gram_energy": gram_energy,
    }


def run():
    checks = 0
    filt = [1 + 0j, 1j, -0.5 + 0.25j, 0.75 - 0.5j]
    coeffs = [1 + 0.5j, -0.75j, -0.5 + 0.25j]
    phases = [
        [1, 1j, -1, -1j],
        [1, cmath.exp(0.4j), cmath.exp(0.8j), cmath.exp(1.2j)],
        [-1j, 1, 1j, -1],
    ]
    resonances = [
        [1, 1, 0, 1],
        [1, 0, 1, 1],
        [0, 1, 1, 1],
    ]
    data = evaluate(coeffs, phases, resonances, filt)
    assert close(data["frequency_sum"], data["atom_sum"])
    assert abs(data["frequency_sum"]) <= data["filtered_majorant"] + 1e-10
    assert data["filtered_majorant"] <= data["preabs"] + 1e-10
    assert close(data["signed_energy"], data["gram_energy"].real)
    assert abs(data["gram_energy"].imag) <= 1e-10
    filt_norm = sum(abs(x) ** 2 for x in filt) ** 0.5
    assert abs(data["frequency_sum"]) <= (
        filt_norm * data["signed_energy"] ** 0.5 + 1e-10
    )
    checks += 6

    # Complete signed cancellation, while the positive carrier is nonzero.
    cancel = evaluate(
        [1 + 0j, -1 + 0j],
        [[1, 1j, -1], [1, 1j, -1]],
        [[1, 1, 1], [1, 1, 1]],
        [1, 1, 1],
    )
    assert close(cancel["frequency_sum"], 0)
    assert close(cancel["signed_energy"], 0)
    assert cancel["preabs"] > 0
    checks += 3

    # Gauge saturation for one atom.
    gauge_filter = [1 + 2j, -2 + 0.5j, 0.25 - 1j]
    gauge_phase = [
        x.conjugate() / abs(x) if x else 1 for x in gauge_filter
    ]
    gauge = evaluate(
        [1 + 0j],
        [gauge_phase],
        [[1, 1, 1]],
        gauge_filter,
    )
    assert close(abs(gauge["frequency_sum"]), gauge["preabs"])
    checks += 1

    result = {
        "schema": "tpc-107-signed-filter-certificate-v1",
        "status": "PASS",
        "checks": checks,
        "claim_boundary": {
            "finite_reconstruction_only": True,
            "actual_signed_energy_bound": False,
            "fixed_h0_L2_estimate": False,
            "prime_pair_result": False,
        },
        "generic_example": {
            "signed_sum_abs": abs(data["frequency_sum"]),
            "filtered_majorant": data["filtered_majorant"],
            "prefilter_majorant": data["preabs"],
            "signed_energy": data["signed_energy"],
        },
        "cancellation_example": {
            "signed_sum_abs": abs(cancel["frequency_sum"]),
            "prefilter_majorant": cancel["preabs"],
        },
        "gauge_saturation": {
            "signed_sum_abs": abs(gauge["frequency_sum"]),
            "prefilter_majorant": gauge["preabs"],
        },
    }
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
