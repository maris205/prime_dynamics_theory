#!/usr/bin/env python3
"""Deterministic finite audit for TPC-126.

This checks only exact/algebraic interfaces.  It does not test the
growing H3 estimate.
"""

from __future__ import annotations

import argparse
import cmath
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "tpc126_literal_packet_audit.json"
TOL = 1.0e-10


def close(x: complex, y: complex, tol: float = TOL) -> bool:
    return abs(x - y) <= tol


def phase(t: float) -> complex:
    return cmath.exp(2j * cmath.pi * t)


def ttstar(values: list[complex], alpha: float) -> tuple[complex, complex, float]:
    direct_sum = sum(a * phase(-alpha * z) for z, a in enumerate(values))
    # Avoid a platform-dependent sqrt-then-square ULP in abs(z) ** 2.
    direct = (direct_sum * direct_sum.conjugate()).real
    lag = 0j
    symmetry_defect = 0.0
    n = len(values)
    correlations: dict[int, complex] = {}
    for r in range(-(n - 1), n):
        corr = sum(
            values[z + r] * values[z].conjugate()
            for z in range(n)
            if 0 <= z + r < n
        )
        correlations[r] = corr
        lag += phase(-alpha * r) * corr
    for r, corr in correlations.items():
        symmetry_defect = max(
            symmetry_defect, abs(correlations[-r] - corr.conjugate())
        )
    return complex(direct), lag, symmetry_defect


def abel(signs: list[complex], weights: list[complex]) -> tuple[complex, complex, float]:
    prefixes: list[complex] = []
    running = 0j
    for sigma in signs:
        running += sigma
        prefixes.append(running)
    direct = sum(s * w for s, w in zip(signs, weights))
    rhs = prefixes[-1] * weights[-1]
    rhs += sum(
        prefixes[k] * (weights[k] - weights[k + 1])
        for k in range(len(weights) - 1)
    )
    bv = abs(weights[-1]) + sum(
        abs(weights[k] - weights[k + 1]) for k in range(len(weights) - 1)
    )
    bound = max(abs(p) for p in prefixes) * bv
    return direct, rhs, bound


def family_audit() -> dict[str, float | bool]:
    blocks = [
        {"gamma": 1.0 + 0.2j, "t": 2.0 - 0.4j, "mass": 4.0},
        {"gamma": -0.5 + 0.3j, "t": 0.7 + 0.8j, "mass": 2.0},
        {"gamma": 0.3 - 0.1j, "t": -0.2 + 0.1j, "mass": 1.0},
    ]
    absolute_mass = sum(abs(b["gamma"]) * b["mass"] for b in blocks)
    total = sum(b["gamma"] * b["t"] for b in blocks)
    q = [abs(b["gamma"]) * b["mass"] / absolute_mass for b in blocks]
    l1 = sum(qi * abs(b["t"]) / b["mass"] for qi, b in zip(q, blocks))
    l2 = sum(
        qi * abs(b["t"]) ** 2 / b["mass"] ** 2 for qi, b in zip(q, blocks)
    ) ** 0.5
    ratio = abs(total) / absolute_mass
    return {
        "direct_ratio": ratio,
        "weighted_l1": l1,
        "weighted_l2": l2,
        "triangle_pass": ratio <= l1 + TOL,
        "cauchy_pass": l1 <= l2 + TOL,
    }


def build_certificate() -> dict[str, object]:
    record = {
        "h0": 2,
        "d": 1,
        "s": 3,
        "u": 1,
        "a": 1,
        "native_key": "ell=1|k=2|d=1",
        "normalization": "nu_X",
        "content": 1,
        "polarization": "left",
        "mask": "literal",
    }
    determinant = record["s"] * record["u"] - record["a"] * record["d"]
    sample_metadata_fields = {
        "native_key", "normalization", "content", "polarization", "mask", "h0"
    }
    sample_metadata_presence_pass = sample_metadata_fields.issubset(record)

    values = [1 + 2j, -2 + 0.5j, 0.25 - 1j, 3 - 0.75j, -0.5 + 0.2j]
    direct, lag, symmetry_defect = ttstar(values, alpha=2 / 11)

    signs = [1, -1, -1, 1, 1]
    weights = [2 + 0.3j, 1.2 - 0.2j, 0.5 + 0.4j, -0.1 + 0.2j, 0.3]
    abel_direct, abel_rhs, abel_bound = abel(signs, weights)

    family = family_audit()
    phase_alpha = 3 / 13
    magnitudes = [0.5, 1.5, 2.0, 0.75]
    saturated = [
        magnitude * phase(phase_alpha * z + 1 / 17)
        for z, magnitude in enumerate(magnitudes)
    ]
    saturated_sum = abs(
        sum(a * phase(-phase_alpha * z) for z, a in enumerate(saturated))
    )
    saturation_pass = close(saturated_sum, sum(magnitudes))

    finite_regression_pass = all(
        [
            determinant == record["h0"],
            sample_metadata_presence_pass,
            close(direct, lag),
            symmetry_defect <= TOL,
            close(abel_direct, abel_rhs),
            abs(abel_direct) <= abel_bound + TOL,
            bool(family["triangle_pass"]),
            bool(family["cauchy_pass"]),
            saturation_pass,
        ]
    )

    return {
        "paper": "TPC-126",
        "scope": "finite literal-interface regression only",
        "determinant": {
            "computed": determinant,
            "declared_h0": record["h0"],
            "pass": determinant == record["h0"],
        },
        "metadata": {
            "scope": "declared sample-key presence only; not complete archive metadata",
            "sample_required": sorted(sample_metadata_fields),
            "sample_presence_pass": sample_metadata_presence_pass,
            "complete_literal_metadata_checked": False,
        },
        "ttstar": {
            "direct_real": direct.real,
            "lag_real": lag.real,
            "lag_imaginary_defect": abs(lag.imag),
            "hermitian_defect": symmetry_defect,
            "pass": close(direct, lag) and symmetry_defect <= TOL,
        },
        "abel": {
            "identity_defect": abs(abel_direct - abel_rhs),
            "direct_absolute": abs(abel_direct),
            "bv_bound": abel_bound,
            "pass": close(abel_direct, abel_rhs)
            and abs(abel_direct) <= abel_bound + TOL,
        },
        "family": family,
        "phase_saturation": {
            "observed": saturated_sum,
            "absolute_mass": sum(magnitudes),
            "pass": saturation_pass,
        },
        "verdict": {
            "FINITE_REGRESSION_PASS": finite_regression_pass,
            "GO_INTERFACE": False,
            "GO_H3": False,
            "reason": (
                "The finite identities pass, but the complete actual "
                "archive extraction is not supplied here.  No theorem for "
                "the complete growing family or outer-loss exponent is supplied."
            ),
        },
        "status": "PASS" if finite_regression_pass else "FAIL",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    certificate = build_certificate()
    rendered = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.write:
        CERTIFICATE.write_text(rendered, encoding="utf-8")
    if args.check:
        if not CERTIFICATE.exists():
            raise SystemExit("certificate missing; run with --write")
        if CERTIFICATE.read_text(encoding="utf-8") != rendered:
            raise SystemExit("certificate mismatch; regenerate with --write")
    print(rendered, end="")
    if certificate["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
