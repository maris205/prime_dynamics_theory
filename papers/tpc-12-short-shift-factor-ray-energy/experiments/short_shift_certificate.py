"""Deterministic finite checks for the TPC-12 algebraic identities.

This script does not test the Guth--Maynard theorem or a fixed-shift
prime asymptotic.  It checks only exact regroupings, explicit obstruction
rays, a finite Cauchy--Schwarz transfer, and the Euclidean radial minimax
identity.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import math
from collections import defaultdict
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


def direct_and_ray_data(X: int, D: int, h: int) -> dict[str, object]:
    max_target = int(BETA * X) + abs(h) + 10
    spf = smallest_prime_factors(max_target)
    rays: dict[tuple[int, int], float] = defaultdict(float)
    products: dict[int, float] = defaultdict(float)
    pairs: list[tuple[int, int, float, float]] = []

    for n, m, w in supported_pairs(X, D):
        source = von_mangoldt(n, spf) - 1.0
        target = von_mangoldt(n * m + h, spf) - 1.0
        amplitude = source * target * w
        g = math.gcd(n, m)
        rays[(n // g, m // g)] += amplitude
        products[n * m] += source * source * w * w
        pairs.append((n, m, w, amplitude))

    frequency_errors: dict[str, float] = {}
    for t in (0.0, 0.37, 1.1):
        direct = sum(
            amp * cmath.exp(1j * t * math.log(n / m))
            for n, m, _, amp in pairs
        )
        compressed = sum(
            coeff * cmath.exp(1j * t * math.log(a / b))
            for (a, b), coeff in rays.items()
        )
        frequency_errors[f"{t:.2f}"] = abs(direct - compressed)

    source_direct = 0.0
    for n, _, w in supported_pairs(X, D):
        source = von_mangoldt(n, spf) - 1.0
        source_direct += source * source * w * w
    source_grouped = sum(products.values())

    exceptional = sorted(products, key=products.get, reverse=True)[:7]
    exceptional_mass = sum(products[r] for r in exceptional)
    cauchy_bound = math.sqrt(len(exceptional)) * math.sqrt(
        sum(value * value for value in products.values())
    )

    return {
        "frequency_errors": frequency_errors,
        "ray_count": len(rays),
        "pair_count": len(pairs),
        "source_direct": source_direct,
        "source_grouped": source_grouped,
        "source_regroup_error": abs(source_direct - source_grouped),
        "exceptional_size": len(exceptional),
        "exceptional_mass": exceptional_mass,
        "exceptional_cauchy_bound": cauchy_bound,
        "exceptional_transfer_holds": exceptional_mass <= cauchy_bound + 1e-12,
    }


def sign_coherent_check(X: int = 20_000) -> dict[str, object]:
    h0, a, b, D = 2, 24, 5, 0
    A = a * b
    spf = smallest_prime_factors(int(BETA * X) + h0 + 10)
    coefficient = 0.0
    baseline = 0.0
    term_count = 0
    all_sources_zero = True
    all_targets_zero = True

    for k in range(1, int(math.sqrt(BETA * X / A)) + 2):
        w = triangular_weight(A * k * k / X)
        if not w or a * k <= D:
            continue
        source_lambda = von_mangoldt(a * k, spf)
        target_lambda = von_mangoldt(A * k * k + h0, spf)
        all_sources_zero &= source_lambda == 0.0
        all_targets_zero &= target_lambda == 0.0
        coefficient += (source_lambda - 1.0) * (target_lambda - 1.0) * w
        baseline += w
        term_count += 1

    return {
        "a": a,
        "b": b,
        "h": h0,
        "term_count": term_count,
        "all_source_lambdas_zero": all_sources_zero,
        "all_target_lambdas_zero": all_targets_zero,
        "coefficient": coefficient,
        "baseline": baseline,
        "identity_error": abs(coefficient - baseline),
    }


def quadratic_embedding_check(X: int = 20_000) -> dict[str, object]:
    a, b, h, D = 6, 1, 1, 0
    A = a * b
    spf = smallest_prime_factors(int(BETA * X) + h + 10)
    coefficient = 0.0
    baseline = 0.0
    polynomial_sum = 0.0
    source_zero = True
    term_count = 0

    for k in range(1, int(math.sqrt(BETA * X / A)) + 2):
        w = triangular_weight(A * k * k / X)
        if not w or a * k <= D:
            continue
        source_lambda = von_mangoldt(a * k, spf)
        target_lambda = von_mangoldt(A * k * k + h, spf)
        source_zero &= source_lambda == 0.0
        coefficient += (source_lambda - 1.0) * (target_lambda - 1.0) * w
        baseline += w
        polynomial_sum += target_lambda * w
        term_count += 1

    return {
        "term_count": term_count,
        "all_source_lambdas_zero": source_zero,
        "coefficient": coefficient,
        "baseline_minus_polynomial_sum": baseline - polynomial_sum,
        "identity_error": abs(coefficient - (baseline - polynomial_sum)),
    }


def radial_minimax_check(B: float = 3.0) -> dict[str, object]:
    v = [0.0, 0.2, 1.0, -0.4, 0.7]
    gamma = sum(v) / len(v)
    residual = [value - gamma for value in v]
    distance = math.sqrt(sum(value * value for value in residual))
    witness = [B * value / distance for value in residual]
    witness_sum = sum(witness)
    witness_norm = math.sqrt(sum(value * value for value in witness))
    witness_value = sum(value * z for value, z in zip(v, witness))
    predicted = B * distance
    return {
        "gamma": gamma,
        "distance_to_constants_l2": distance,
        "predicted_minimax": predicted,
        "witness_sum": witness_sum,
        "witness_norm": witness_norm,
        "witness_functional": witness_value,
        "identity_error": abs(witness_value - predicted),
    }


def build_certificate(X: int = 360, D: int = 9, h: int = 4) -> dict[str, object]:
    regrouping = direct_and_ray_data(X, D, h)
    sign = sign_coherent_check()
    quadratic = quadratic_embedding_check()
    minimax = radial_minimax_check()

    tolerance = 1e-9
    checks = {
        "ray_compression": max(regrouping["frequency_errors"].values()) < tolerance,
        "source_diagonal_regrouping": regrouping["source_regroup_error"] < tolerance,
        "finite_exceptional_transfer": regrouping["exceptional_transfer_holds"],
        "sign_coherent_identity": (
            sign["all_source_lambdas_zero"]
            and sign["all_target_lambdas_zero"]
            and sign["identity_error"] < tolerance
        ),
        "quadratic_embedding_identity": (
            quadratic["all_source_lambdas_zero"]
            and quadratic["identity_error"] < tolerance
        ),
        "radial_minimax_l2": (
            abs(minimax["witness_sum"]) < tolerance
            and abs(minimax["witness_norm"] - 3.0) < tolerance
            and minimax["identity_error"] < tolerance
        ),
    }
    return {
        "config": {"X": X, "D": D, "h": h, "alpha": ALPHA, "beta": BETA},
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "regrouping": regrouping,
        "sign_coherent_ray": sign,
        "quadratic_embedding": quadratic,
        "radial_minimax": minimax,
    }


def canonical_payload(certificate: dict[str, object]) -> bytes:
    return json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode("utf-8")


def main() -> None:
    certificate = build_certificate()
    payload_hash = hashlib.sha256(canonical_payload(certificate)).hexdigest()
    output = {**certificate, "payload_sha256": payload_hash}
    output_path = Path(__file__).resolve().parent / "data" / "short-shift-certificate.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
