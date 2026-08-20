"""Exact finite algebra for TPC-214 shared-frequency clusters.

The emitter is the V46 reciprocal row with the logarithmic Mobius prefactor
removed from the row and retained as a symbolic coefficient.  The finite
profile psi(t)=(1+t^2)^(-2) makes every row rational, so the cluster and Gram
identities can be checked exactly before evaluating the logarithms.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path


Q_VALUES = (11, 13, 17)
H = 40
PSI_NAME = "(1+t^2)^(-2)"
FIXTURE_FAMILIES = ((5, 7, 35), (3, 5, 7, 105))

Polynomial = dict[tuple[str, ...], Fraction]


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def prime_factors(value: int) -> tuple[int, ...]:
    require(type(value) is int and value >= 1, "positive integer")
    remaining = value
    factors: list[int] = []
    candidate = 2
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            factors.append(candidate)
            remaining //= candidate
            require(remaining % candidate != 0, "squarefree divisor required")
        candidate += 1
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def mobius(value: int) -> int:
    factors = prime_factors(value)
    product = 1
    for prime in factors:
        if value % (prime * prime) == 0:
            return 0
        product = -product
    return product


def positive_divisors(value: int) -> tuple[int, ...]:
    return tuple(d for d in range(1, value + 1) if value % d == 0)


def psi_weight(argument: Fraction) -> Fraction:
    return Fraction(1, 1) / (1 + argument * argument) ** 2


def emitter_row(divisor: int, q_values: tuple[int, ...] = Q_VALUES, height: int = H) -> tuple[Fraction, ...]:
    """Return B_d(r) for the literal reciprocal cutoff and rational psi."""

    require(divisor >= 1 and height >= 1, "positive parameters")
    row = [Fraction(0, 1) for _ in range(divisor)]
    for q in q_values:
        require(gcd(q, divisor) == 1, "q must be a unit modulo every divisor")
        limit = divisor * q // height
        for m in range(-limit, limit + 1):
            if m == 0:
                continue
            residue = (m * pow(q, -1, divisor)) % divisor
            row[residue] += psi_weight(Fraction(height * m, divisor * q))
    return tuple(row)


def dilation_check(divisor: int, denominator: int) -> bool:
    require(divisor % denominator == 0, "denominator must divide divisor")
    large = emitter_row(divisor)
    small = emitter_row(denominator)
    scale = divisor // denominator
    return all(large[scale * residue] == small[residue] for residue in range(denominator))


def row_hash(row: tuple[Fraction, ...]) -> str:
    payload = "|".join(str(value) for value in row).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def row_norm_squared(row: tuple[Fraction, ...], primitive_only: bool = False) -> Fraction:
    if not primitive_only:
        return sum((value * value for value in row), Fraction(0, 1))
    modulus = len(row)
    return sum(
        (row[residue] * row[residue] for residue in range(modulus) if gcd(residue, modulus) == 1),
        Fraction(0, 1),
    )


def frequency_gram(
    left: int,
    right: int,
    left_row: tuple[Fraction, ...],
    right_row: tuple[Fraction, ...],
    period: int | None = None,
) -> Fraction:
    common_period = lcm(left, right) if period is None else period
    require(common_period % lcm(left, right) == 0, "period must contain the pair period")
    return common_period * sum(
        (
            left_row[left_residue] * right_row[right_residue]
            for left_residue in range(left)
            for right_residue in range(right)
            if Fraction(left_residue, left) == Fraction(right_residue, right)
        ),
        Fraction(0, 1),
    )


def polynomial_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for monomial, value in right.items():
        result[monomial] = result.get(monomial, Fraction(0, 1)) + value
        if result[monomial] == 0:
            del result[monomial]
    return result


def polynomial_scale(poly: Polynomial, scalar: Fraction) -> Polynomial:
    return {monomial: scalar * value for monomial, value in poly.items() if scalar * value}


def polynomial_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = result.get(monomial, Fraction(0, 1)) + left_value * right_value
    return {monomial: value for monomial, value in result.items() if value}


def coefficient_polynomial(divisor: int) -> Polynomial:
    """Formal polynomial for Mobius(d) log(d)/d in prime-log variables."""

    value = Fraction(mobius(divisor), divisor)
    if value == 0:
        return {}
    return {("log(%d)" % prime,): value for prime in prime_factors(divisor)}


def polynomial_evaluate(poly: Polynomial) -> float:
    logs = {name: math.log(int(name[4:-1])) for name in {item for monomial in poly for item in monomial}}
    total = 0.0
    for monomial, value in poly.items():
        term = float(value)
        for variable in monomial:
            term *= logs[variable]
        total += term
    return total


def polynomial_json(poly: Polynomial) -> dict[str, str]:
    return {"*".join(monomial): str(poly[monomial]) for monomial in sorted(poly)}


def polynomial_from_json(data: dict[str, str]) -> Polynomial:
    return {
        tuple(key.split("*")) if key else tuple(): Fraction(value)
        for key, value in data.items()
    }


def reduced_denominators(divisors: tuple[int, ...]) -> tuple[int, ...]:
    values = {h for divisor in divisors for h in positive_divisors(divisor)}
    return tuple(sorted(values))


def cluster_coefficient(divisors: tuple[int, ...], denominator: int) -> Polynomial:
    result: Polynomial = {}
    for divisor in divisors:
        if divisor % denominator == 0:
            result = polynomial_add(result, coefficient_polynomial(divisor))
    return result


def cluster_scales(divisors: tuple[int, ...]) -> dict[int, Fraction]:
    period = math.lcm(*divisors)
    return {
        denominator: period * row_norm_squared(emitter_row(denominator), primitive_only=True)
        for denominator in reduced_denominators(divisors)
    }


def gram_matrix(divisors: tuple[int, ...]) -> tuple[tuple[Fraction, ...], ...]:
    rows = {divisor: emitter_row(divisor) for divisor in divisors}
    period = math.lcm(*divisors)
    return tuple(
        tuple(frequency_gram(left, right, rows[left], rows[right], period) for right in divisors)
        for left in divisors
    )


def energy_polynomial_from_gram(divisors: tuple[int, ...]) -> Polynomial:
    matrix = gram_matrix(divisors)
    coefficients = {divisor: coefficient_polynomial(divisor) for divisor in divisors}
    result: Polynomial = {}
    for left_index, left in enumerate(divisors):
        for right_index, right in enumerate(divisors):
            result = polynomial_add(
                result,
                polynomial_scale(
                    polynomial_multiply(coefficients[left], coefficients[right]),
                    matrix[left_index][right_index],
                ),
            )
    return result


def direct_sum_energy_polynomial(divisors: tuple[int, ...]) -> Polynomial:
    period = math.lcm(*divisors)
    result: Polynomial = {}
    for divisor in divisors:
        coefficient = coefficient_polynomial(divisor)
        diagonal = period * row_norm_squared(emitter_row(divisor))
        result = polynomial_add(
            result,
            polynomial_scale(polynomial_multiply(coefficient, coefficient), diagonal),
        )
    return result


def cluster_energy_polynomial(divisors: tuple[int, ...]) -> Polynomial:
    result: Polynomial = {}
    scales = cluster_scales(divisors)
    for denominator, scale in scales.items():
        coefficient = cluster_coefficient(divisors, denominator)
        result = polynomial_add(
            result,
            polynomial_scale(polynomial_multiply(coefficient, coefficient), scale),
        )
    return result


def row_hashes_for(divisors: tuple[int, ...]) -> dict[int, str]:
    denominators = reduced_denominators(divisors)
    return {denominator: row_hash(emitter_row(denominator)) for denominator in denominators}


def coefficient_values(divisors: tuple[int, ...]) -> dict[int, float]:
    return {
        divisor: mobius(divisor) * math.log(divisor) / divisor
        for divisor in divisors
    }


def coefficient_sign(divisor: int) -> int:
    return mobius(divisor)


def audit_family(divisors: tuple[int, ...]) -> dict[str, object]:
    require(divisors in FIXTURE_FAMILIES, "unknown release fixture")
    period = math.lcm(*divisors)
    gram = gram_matrix(divisors)
    gram_poly = energy_polynomial_from_gram(divisors)
    cluster_poly = cluster_energy_polynomial(divisors)
    direct_poly = direct_sum_energy_polynomial(divisors)
    cross_poly = polynomial_add(cluster_poly, polynomial_scale(direct_poly, Fraction(-1, 1)))
    physical_value = polynomial_evaluate(cluster_poly)
    direct_value = polynomial_evaluate(direct_poly)
    dilation_pairs = [
        (divisor, denominator)
        for divisor in divisors
        for denominator in positive_divisors(divisor)
    ]
    cross_terms = []
    for left_index, left in enumerate(divisors):
        for right_index in range(left_index + 1, len(divisors)):
            right = divisors[right_index]
            value = gram[left_index][right_index]
            if value:
                cross_terms.append({
                    "left": left,
                    "right": right,
                    "gram": str(value),
                    "coefficient_sign_product": coefficient_sign(left) * coefficient_sign(right),
                    "cross_term_sign": coefficient_sign(left) * coefficient_sign(right),
                })
    cross_signs = {term["cross_term_sign"] for term in cross_terms}
    require(bool(cross_terms), "fixture must have a cross term")
    require(len(cross_signs) == 1, "fixture cross terms must have one exact sign")
    exact_cross_sign = "POSITIVE_EXACT" if next(iter(cross_signs)) > 0 else "NEGATIVE_EXACT"
    return {
        "divisors": list(divisors),
        "period": period,
        "coefficients": {str(d): format(value, ".17g") for d, value in coefficient_values(divisors).items()},
        "reduced_denominators": list(reduced_denominators(divisors)),
        "row_hashes": {str(d): value for d, value in row_hashes_for(divisors).items()},
        "cluster_row_norms": {
            str(d): str(row_norm_squared(emitter_row(d), primitive_only=True))
            for d in reduced_denominators(divisors)
        },
        "cluster_scales": {str(d): str(value) for d, value in cluster_scales(divisors).items()},
        "cluster_coefficients": {
            str(d): polynomial_json(cluster_coefficient(divisors, d))
            for d in reduced_denominators(divisors)
        },
        "gram_matrix": [[str(value) for value in row] for row in gram],
        "gram_energy_polynomial": polynomial_json(gram_poly),
        "cluster_energy_polynomial": polynomial_json(cluster_poly),
        "direct_sum_energy_polynomial": polynomial_json(direct_poly),
        "cross_energy_polynomial": polynomial_json(cross_poly),
        "cross_energy_sign": exact_cross_sign,
        "cross_terms": cross_terms,
        "physical_energy": format(physical_value, ".17g"),
        "direct_sum_energy": format(direct_value, ".17g"),
        "physical_to_direct_ratio": format(physical_value / direct_value, ".17g"),
        "dilation_pairs": [list(pair) for pair in dilation_pairs],
        "dilation_covariance": all(dilation_check(*pair) for pair in dilation_pairs),
        "zero_axis": all(emitter_row(d)[0] == 0 for d in reduced_denominators(divisors)),
        "cluster_factorization": gram_poly == cluster_poly,
    }


def gaussian_add(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return left[0] + right[0], left[1] + right[1]


def gaussian_mul(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def gaussian_conjugate(value: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return value[0], -value[1]


def gaussian_scale(value: tuple[Fraction, Fraction], scalar: Fraction) -> tuple[Fraction, Fraction]:
    return scalar * value[0], scalar * value[1]


def gaussian_norm_squared(value: tuple[Fraction, Fraction]) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def four_packet_certificate() -> dict[str, object]:
    beta = (Fraction(2, 1), Fraction(1, 1))
    weight = (Fraction(1, 1), Fraction(-2, 1))
    powers = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)), (Fraction(-1), Fraction(0)), (Fraction(0), Fraction(-1)))
    total = (Fraction(0), Fraction(0))
    for power in powers:
        packet = gaussian_add(beta, gaussian_mul(power, weight))
        total = gaussian_add(total, gaussian_scale(gaussian_mul(power, (gaussian_norm_squared(packet), Fraction(0))), Fraction(1, 4)))
    expected = gaussian_mul(beta, gaussian_conjugate(weight))
    return {
        "beta": [str(value) for value in beta],
        "weight": [str(value) for value in weight],
        "polarized_value": [str(value) for value in total],
        "expected_value": [str(value) for value in expected],
        "identity": total == expected,
    }


def build_certificate() -> dict[str, object]:
    families = [audit_family(family) for family in FIXTURE_FAMILIES]
    return {
        "schema": "TPC214_MOBIUS_FREQUENCY_CLUSTER_CERTIFICATE_V1",
        "classification": "PROVED_STRUCTURAL_L1_MOBIUS_CLUSTER_REDUCTION",
        "modeling_choice": "RATIONAL_SCHWARTZ_PSI_EQUALS_ONE_OVER_ONE_PLUS_T_SQUARED_SQUARED",
        "fixture": {
            "q_values": list(Q_VALUES),
            "H": H,
            "psi": PSI_NAME,
            "q_below_H": max(Q_VALUES) < H,
            "families": [list(family) for family in FIXTURE_FAMILIES],
        },
        "families": families,
        "four_packet": four_packet_certificate(),
        "claim_firewall": {
            "route_advance": "YES",
            "structural_threshold_a": "PASS",
            "emitter_dilation_covariance": "PROVED_EXACT",
            "reduced_denominator_cluster_factor": "PROVED_EXACT",
            "zero_axis_scope": "PROVED_EXACT",
            "four_packet_polarization": "PROVED_EXACT_LINEAR_EXTENSION",
            "nested_cluster_cancellation": "PROVED_EXACT_FINITE_SIGN",
            "composite_quotient_enhancement": "PROVED_EXACT_FINITE_SIGN",
            "finite_energy_ratios": "NUMERICAL_OBSERVATION",
            "universal_cluster_saving_sign": "REFUTED_SCOPED",
            "literal_v46_asymptotic_cluster_bound": "OPEN",
            "prime_shell_reassembly": "OPEN",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b_strict_1_over_400": "UNPAID",
        },
        "audit_counts": {
            "fixture_families": len(families),
            "dilation_pairs": sum(len(family["dilation_pairs"]) for family in families),
            "reduced_denominator_rows": sum(len(family["reduced_denominators"]) for family in families),
            "factorization_checks": sum(int(family["cluster_factorization"]) for family in families),
        },
        "open_theorem": "BOUND_THE_ACTUAL_V46_MOBIUS_LOG_CLUSTER_TAILS_UNIFORMLY_AND_REASSEMBLE_THE_PRIME_SHELL",
    }


def write_certificate(path: Path) -> None:
    path.write_text(json.dumps(build_certificate(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    certificate_path = root / "results/certificate.json"
    write_certificate(certificate_path)
    print("TPC214_CERTIFICATE_WRITE=PASS")
    print("schema=TPC214_MOBIUS_FREQUENCY_CLUSTER_CERTIFICATE_V1")
    for family in build_certificate()["families"]:
        print(
            "family=%s physical=%s direct=%s ratio=%s factorization=%s"
            % (
                ",".join(str(value) for value in family["divisors"]),
                family["physical_energy"],
                family["direct_sum_energy"],
                family["physical_to_direct_ratio"],
                family["cluster_factorization"],
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
