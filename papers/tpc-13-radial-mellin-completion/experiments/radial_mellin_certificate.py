"""Deterministic finite checks for the TPC-13 identities.

This script verifies coordinate regroupings, explicit sector gap bounds,
Fourier-side tensor-Fejer dephasing, and the energy-only minimax witness.
It does not test a short-interval prime theorem or any fixed-shift prime
correlation.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Iterable


ALPHA = 0.5
BETA = 1.5


def triangular_weight(x: float) -> float:
    """A compactly supported continuous weight on [1/2, 3/2]."""

    return max(0.0, 1.0 - 2.0 * abs(x - 1.0))


def smallest_prime_factors(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1
    for p in range(2, int(limit**0.5) + 1):
        if spf[p] == p:
            for n in range(p * p, limit + 1, p):
                if spf[n] == n:
                    spf[n] = p
    return spf


def von_mangoldt(n: int, spf: list[int]) -> float:
    if n < 2:
        return 0.0
    p = spf[n]
    m = n
    while m % p == 0:
        m //= p
    return math.log(p) if m == 1 else 0.0


def supported_pairs(X: int, D: int) -> Iterable[tuple[int, int, float]]:
    for n in range(D + 1, int(BETA * X) + 1):
        for m in range(1, int(BETA * X / n) + 1):
            w = triangular_weight(n * m / X)
            if w:
                yield n, m, w


def dyadic_floor(value: int) -> int:
    return 1 << (value.bit_length() - 1)


def hat_fejer(value: float) -> float:
    return max(0.0, 1.0 - abs(value))


def enumerate_data(X: int, D: int, h: int) -> dict[str, object]:
    max_target = int(BETA * X) + abs(h) + 10
    spf = smallest_prime_factors(max_target)
    coefficients: dict[tuple[int, int, int], float] = {}
    products: dict[int, float] = defaultdict(float)
    direct_rows: list[tuple[int, int, float]] = []
    coordinate_ok = True
    labels: set[tuple[Fraction, int]] = set()

    for n, m, w in supported_pairs(X, D):
        source = von_mangoldt(n, spf) - 1.0
        target = von_mangoldt(n * m + h, spf) - 1.0
        amplitude = source * target * w
        g = math.gcd(n, m)
        a, b, k = n // g, m // g, g
        coordinate_ok &= math.gcd(a, b) == 1
        coordinate_ok &= (a * k, b * k) == (n, m)
        label = (Fraction(a, b), k)
        coordinate_ok &= label not in labels
        labels.add(label)
        coefficients[(a, b, k)] = amplitude
        products[n * m] += source * source * w * w
        direct_rows.append((n, m, amplitude))

    transform_errors: dict[str, float] = {}
    for t, s in ((0.0, 0.0), (0.31, -0.27), (1.07, 0.63)):
        direct = sum(
            amp
            * cmath.exp(
                1j
                * (
                    t * math.log(n / m)
                    + s * math.log(math.gcd(n, m))
                )
            )
            for n, m, amp in direct_rows
        )
        compressed = sum(
            amp
            * cmath.exp(
                1j * (t * math.log(a / b) + s * math.log(k))
            )
            for (a, b, k), amp in coefficients.items()
        )
        transform_errors[f"{t:.2f},{s:.2f}"] = abs(direct - compressed)

    direct_energy = sum(value * value for value in coefficients.values())
    grouped_energy = 0.0
    for r, source_mass in products.items():
        target = von_mangoldt(r + h, spf) - 1.0
        grouped_energy += source_mass * target * target

    return {
        "coefficients": coefficients,
        "coordinate_bijection": coordinate_ok,
        "factor_pair_count": len(direct_rows),
        "joint_label_count": len(labels),
        "transform_errors": transform_errors,
        "direct_energy": direct_energy,
        "grouped_energy": grouped_energy,
        "product_center_error": abs(direct_energy - grouped_energy),
    }


def sector_checks(
    coefficients: dict[tuple[int, int, int], float], X: int
) -> dict[str, object]:
    sectors: dict[int, list[tuple[tuple[int, int, int], float]]] = defaultdict(list)
    for index, value in coefficients.items():
        a, b, _ = index
        sectors[dyadic_floor(a * b)].append((index, value))

    max_ray_gap_violation = 0.0
    max_radial_gap_violation = 0.0
    max_parseval_error = 0.0
    max_recovery_error = 0.0
    populated = 0
    ray_pair_sectors = 0
    radial_pair_sectors = 0

    for R, rows in sectors.items():
        populated += 1
        ray_delta = 2.0 * math.asinh(1.0 / (4.0 * R))
        radial_delta = math.log(1.0 + math.sqrt(R / (BETA * X)))
        rays = sorted({(a, b) for (a, b, _), _ in rows})
        radial_values = sorted({k for (_, _, k), _ in rows})

        if len(rays) >= 2:
            ray_pair_sectors += 1
            actual = min(
                abs(math.log(a / b) - math.log(c / d))
                for i, (a, b) in enumerate(rays)
                for c, d in rays[i + 1 :]
            )
            max_ray_gap_violation = max(
                max_ray_gap_violation, ray_delta - actual
            )

        if len(radial_values) >= 2:
            radial_pair_sectors += 1
            actual = min(
                math.log(radial_values[i + 1] / radial_values[i])
                for i in range(len(radial_values) - 1)
            )
            max_radial_gap_violation = max(
                max_radial_gap_violation, radial_delta - actual
            )

        T = 1.01 / ray_delta
        S = 1.01 / radial_delta
        quadratic = 0j
        for (index_i, value_i) in rows:
            a, b, k = index_i
            lambda_i, rho_i = math.log(a / b), math.log(k)
            for (index_j, value_j) in rows:
                c, d, ell = index_j
                lambda_j, rho_j = math.log(c / d), math.log(ell)
                multiplier = hat_fejer(T * (lambda_i - lambda_j))
                multiplier *= hat_fejer(S * (rho_i - rho_j))
                quadratic += value_i * value_j * multiplier
        diagonal = sum(value * value for _, value in rows)
        max_parseval_error = max(max_parseval_error, abs(quadratic - diagonal))

        selected_index, selected_value = rows[0]
        a0, b0, k0 = selected_index
        lambda0, rho0 = math.log(a0 / b0), math.log(k0)
        recovered = 0j
        for (a, b, k), value in rows:
            multiplier = hat_fejer(T * (math.log(a / b) - lambda0))
            multiplier *= hat_fejer(S * (math.log(k) - rho0))
            recovered += value * multiplier
        max_recovery_error = max(
            max_recovery_error, abs(recovered - selected_value)
        )

    return {
        "populated_sector_count": populated,
        "ray_pair_sector_count": ray_pair_sectors,
        "radial_pair_sector_count": radial_pair_sectors,
        "max_ray_gap_violation": max_ray_gap_violation,
        "max_radial_gap_violation": max_radial_gap_violation,
        "max_normalized_parseval_error": max_parseval_error,
        "max_coefficient_recovery_error": max_recovery_error,
    }


def energy_minimax_check(B: float = 3.0) -> dict[str, float]:
    endpoint = [B, 0.0, 0.0, 0.0]
    complement = [0.0, 0.0, B, 0.0]

    def total(values: list[float]) -> float:
        return sum(value * value for value in values)

    def target(values: list[float]) -> float:
        return sum(value * value for value in values[:2])

    observed_endpoint = total(endpoint)
    observed_complement = total(complement)
    target_endpoint = target(endpoint)
    target_complement = target(complement)
    estimator = observed_endpoint / 2.0
    return {
        "observed_difference": abs(observed_endpoint - observed_complement),
        "target_separation": abs(target_endpoint - target_complement),
        "lower_bound": abs(target_endpoint - target_complement) / 2.0,
        "endpoint_estimator_error": abs(target_endpoint - estimator),
        "complement_estimator_error": abs(target_complement - estimator),
    }


def build_certificate(X: int = 360, D: int = 9, h: int = 4) -> dict[str, object]:
    data = enumerate_data(X, D, h)
    sectors = sector_checks(data["coefficients"], X)
    minimax = energy_minimax_check()
    tolerance = 1e-9
    checks = {
        "coordinate_bijection": data["coordinate_bijection"],
        "joint_transform_compression": (
            max(data["transform_errors"].values()) < tolerance
        ),
        "explicit_sector_gaps": (
            sectors["max_ray_gap_violation"] < tolerance
            and sectors["max_radial_gap_violation"] < tolerance
        ),
        "tensor_fejer_parseval": (
            sectors["max_normalized_parseval_error"] < tolerance
        ),
        "tensor_fejer_recovery": (
            sectors["max_coefficient_recovery_error"] < tolerance
        ),
        "product_center_identity": data["product_center_error"] < tolerance,
        "energy_minimax_witness": (
            minimax["observed_difference"] < tolerance
            and abs(minimax["lower_bound"] - 4.5) < tolerance
            and abs(minimax["endpoint_estimator_error"] - 4.5) < tolerance
            and abs(minimax["complement_estimator_error"] - 4.5) < tolerance
        ),
    }
    public_data = {key: value for key, value in data.items() if key != "coefficients"}
    return {
        "config": {
            "X": X,
            "D": D,
            "h": h,
            "alpha": ALPHA,
            "beta": BETA,
        },
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "coordinate_and_energy": public_data,
        "sector_dephasing": sectors,
        "energy_minimax": minimax,
    }


def canonical_payload(certificate: dict[str, object]) -> bytes:
    return json.dumps(
        certificate, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def main() -> None:
    certificate = build_certificate()
    payload_hash = hashlib.sha256(canonical_payload(certificate)).hexdigest()
    output = {**certificate, "payload_sha256": payload_hash}
    output_path = (
        Path(__file__).resolve().parent / "data" / "radial-mellin-certificate.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
