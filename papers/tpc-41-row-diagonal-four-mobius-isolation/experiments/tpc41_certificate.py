#!/usr/bin/env python3
"""Deterministic exact-arithmetic certificate for TPC-41.

The certificate checks finite alias-Gram, folded-energy, affine
nonproportionality, formal Dirichlet-convolution, and endpoint-exponent
identities.  It uses only the Python standard library, integers, Fractions,
and exact Gaussian-integer pairs.  It uses no floating point, random draws,
NumPy, or optimization-sensitive ``assert`` statements.

It does not verify any asymptotic analytic input, estimate a physical
four-Mobius form, breach sieve parity, prove a prime-pair asymptotic, or
prove the twin-prime conjecture.
"""

from __future__ import annotations

import ast
import hashlib
import json
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple


class CertificateError(RuntimeError):
    """Raised when an exact certificate check fails."""


CHECKS = 0


def require(condition: bool, message: str) -> None:
    """Record one optimization-safe exact check."""

    global CHECKS
    CHECKS += 1
    if not condition:
        raise CertificateError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        )
        + "\n"
    ).encode("ascii")


def canonical_digest(value: object) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def frac_text(value: Fraction | int) -> str:
    rational = Fraction(value)
    if rational.denominator == 1:
        return str(rational.numerator)
    return f"{rational.numerator}/{rational.denominator}"


def cyclic_character_sum(modulus: int, exponent: int) -> int:
    require(modulus >= 1, "cyclic modulus must be positive")
    return modulus if exponent % modulus == 0 else 0


def matvec(
    matrix: Sequence[Sequence[int]], vector: Sequence[int]
) -> List[int]:
    require(
        all(len(row) == len(vector) for row in matrix),
        "matrix-vector dimensions do not match",
    )
    return [
        sum(row[index] * vector[index] for index in range(len(vector)))
        for row in matrix
    ]


def dot(left: Sequence[int], right: Sequence[int]) -> int:
    require(len(left) == len(right), "dot-product dimensions do not match")
    return sum(a * b for a, b in zip(left, right))


def verify_alias_grams() -> Dict[str, object]:
    start = CHECKS
    minimal_cases = 0
    full_cases = 0
    for radius in range(1, 81):
        aliases = list(range(-radius, radius + 1))
        minimal_modulus = radius + 1
        minimal_gram = [
            [
                cyclic_character_sum(minimal_modulus, right - left)
                // minimal_modulus
                for right in aliases
            ]
            for left in aliases
        ]
        for left_index, left in enumerate(aliases):
            for right_index, right in enumerate(aliases):
                expected = 1 if (left - right) % minimal_modulus == 0 else 0
                require(
                    minimal_gram[left_index][right_index] == expected,
                    "minimal alias Gram entry failed",
                )

        zero_index = aliases.index(0)
        e_zero = [0] * len(aliases)
        e_zero[zero_index] = 1
        require(
            matvec(minimal_gram, e_zero) == e_zero,
            "zero alias is not the eigenvalue-one direction",
        )
        for residue in range(1, radius + 1):
            positive_index = aliases.index(residue)
            negative_index = aliases.index(residue - minimal_modulus)
            symmetric = [0] * len(aliases)
            antisymmetric = [0] * len(aliases)
            symmetric[positive_index] = 1
            symmetric[negative_index] = 1
            antisymmetric[positive_index] = 1
            antisymmetric[negative_index] = -1
            require(
                matvec(minimal_gram, symmetric)
                == [2 * value for value in symmetric],
                "folded symmetric vector is not an eigenvalue-two vector",
            )
            require(
                matvec(minimal_gram, antisymmetric)
                == [0] * len(aliases),
                "folded antisymmetric vector is not in the kernel",
            )
        minimal_cases += 1

        full_modulus = 2 * radius + 1
        for left in aliases:
            for right in aliases:
                gram_entry = (
                    cyclic_character_sum(full_modulus, right - left)
                    // full_modulus
                )
                require(
                    gram_entry == (1 if left == right else 0),
                    "full DFT alias Gram is not the identity",
                )
        full_cases += 1

    return {
        "checks": CHECKS - start,
        "radius_range": [1, 80],
        "minimal_Gram_cases": minimal_cases,
        "full_DFT_cases": full_cases,
        "minimal_spectrum": {"0": "L", "1": "1", "2": "L"},
        "full_spectrum": {"1": "2L+1"},
    }


def minimal_real_energy(radius: int, atoms: Sequence[int]) -> Tuple[int, int]:
    require(len(atoms) == 2 * radius + 1, "real atom length failed")
    aliases = list(range(-radius, radius + 1))
    values = {alias: atoms[index] for index, alias in enumerate(aliases)}
    diagonal = sum(value * value for value in atoms)
    folded = values[0] * values[0]
    modulus = radius + 1
    for residue in range(1, radius + 1):
        bucket = values[residue] + values[residue - modulus]
        folded += bucket * bucket
    return diagonal, folded


Gaussian = Tuple[int, int]


def gaussian_norm(value: Gaussian) -> int:
    return value[0] * value[0] + value[1] * value[1]


def gaussian_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def minimal_gaussian_energy(
    radius: int, atoms: Sequence[Gaussian]
) -> Tuple[int, int]:
    require(len(atoms) == 2 * radius + 1, "Gaussian atom length failed")
    aliases = list(range(-radius, radius + 1))
    values = {alias: atoms[index] for index, alias in enumerate(aliases)}
    diagonal = sum(gaussian_norm(value) for value in atoms)
    folded = gaussian_norm(values[0])
    modulus = radius + 1
    for residue in range(1, radius + 1):
        folded += gaussian_norm(
            gaussian_add(values[residue], values[residue - modulus])
        )
    return diagonal, folded


def verify_same_row_closure() -> Dict[str, object]:
    start = CHECKS
    real_vectors = 0
    gaussian_vectors = 0
    for radius in range(1, 4):
        for atoms in product(range(-2, 3), repeat=2 * radius + 1):
            diagonal, folded = minimal_real_energy(radius, atoms)
            off_alias = folded - diagonal
            require(folded >= 0, "real folded energy is negative")
            require(folded <= 2 * diagonal, "real E_same <= 2D failed")
            require(abs(off_alias) <= diagonal, "real |S_same| <= D failed")
            real_vectors += 1

    gaussian_alphabet: Tuple[Gaussian, ...] = (
        (0, 0),
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    )
    for radius in range(1, 3):
        for atoms in product(
            gaussian_alphabet, repeat=2 * radius + 1
        ):
            diagonal, folded = minimal_gaussian_energy(radius, atoms)
            off_alias = folded - diagonal
            require(folded >= 0, "Gaussian folded energy is negative")
            require(
                folded <= 2 * diagonal,
                "Gaussian E_same <= 2D failed",
            )
            require(
                abs(off_alias) <= diagonal,
                "Gaussian |S_same| <= D failed",
            )
            gaussian_vectors += 1

    sharp_positive = minimal_real_energy(1, (1, 0, 1))
    sharp_negative = minimal_real_energy(1, (-1, 0, 1))
    require(sharp_positive == (2, 4), "positive sharp case failed")
    require(sharp_negative == (2, 0), "negative sharp case failed")
    return {
        "checks": CHECKS - start,
        "real_vectors": real_vectors,
        "Gaussian_integer_vectors": gaussian_vectors,
        "sharp_positive_case": list(sharp_positive),
        "sharp_negative_case": list(sharp_negative),
    }


def verify_folded_alias_pairs() -> Dict[str, object]:
    start = CHECKS
    pair_cases = 0
    for radius in range(1, 201):
        modulus = radius + 1
        aliases = set(range(-radius, radius + 1))
        used = {0}
        require(0 in aliases, "zero alias is missing")
        for residue in range(1, radius + 1):
            pair = {residue, residue - modulus}
            require(len(pair) == 2, "folded pair is not a doubleton")
            require(pair <= aliases, "folded pair leaves alias interval")
            require(not (pair & used), "folded pairs overlap")
            require(residue - (residue - modulus) == modulus, "gap is not q")
            used.update(pair)
            allowed = {
                (residue, residue),
                (residue, residue - modulus),
                (residue - modulus, residue),
                (residue - modulus, residue - modulus),
            }
            require(len(allowed) == 4, "expanded alias pair count failed")
            pair_cases += len(allowed)
        require(used == aliases, "folded pairs do not partition aliases")
    return {
        "checks": CHECKS - start,
        "radius_range": [1, 200],
        "expanded_ordered_pair_cases": pair_cases,
    }


def verify_affine_nondegeneracy() -> Dict[str, object]:
    start = CHECKS
    models = (
        (5 * 7 * 11, 2),
        (7 * 11 * 13, 3),
        (11 * 13 * 17, 5),
        (13 * 17 * 19, 7),
    )
    determinants = 0
    for modulus, shift in models:
        require(gcd(modulus, shift) == 1, "toy shift is not coprime")
        rows = list(range(1, min(modulus, 61)))
        for left in rows:
            for right in rows:
                if left == right:
                    continue
                require(
                    abs(left - right) < modulus,
                    "toy row gap exceeds modulus",
                )
                for alias_left in range(-3, 4):
                    for alias_right in range(-3, 4):
                        determinant = (
                            left * (shift + alias_right * modulus)
                            - right * (shift + alias_left * modulus)
                        )
                        require(
                            determinant != 0,
                            "distinct admissible rows produced proportional forms",
                        )
                        if determinant % modulus == 0:
                            require(
                                (left - right) * shift % modulus == 0,
                                "determinant modular implication failed",
                            )
                        determinants += 1
    return {
        "checks": CHECKS - start,
        "toy_models": len(models),
        "determinants_checked": determinants,
    }


def prime_factorization(value: int) -> Dict[int, int]:
    require(value >= 1, "factorization input must be positive")
    remaining = value
    factors: Dict[int, int] = {}
    prime = 2
    while prime * prime <= remaining:
        while remaining % prime == 0:
            factors[prime] = factors.get(prime, 0) + 1
            remaining //= prime
        prime += 1
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def mobius(value: int) -> int:
    factors = prime_factorization(value)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def divisors(value: int) -> List[int]:
    factors = list(prime_factorization(value).items())
    result = [1]
    for prime, exponent in factors:
        powers = [1]
        for _ in range(exponent):
            powers.append(powers[-1] * prime)
        result = [base * power for base in result for power in powers]
    return sorted(result)


FormalLog = Dict[int, int]


def formal_lambda(value: int) -> FormalLog:
    factors = prime_factorization(value)
    if len(factors) != 1:
        return {}
    prime = next(iter(factors))
    return {prime: 1}


def add_formal(target: FormalLog, source: FormalLog, scale: int) -> None:
    for prime, coefficient in source.items():
        target[prime] = target.get(prime, 0) + scale * coefficient
        if target[prime] == 0:
            del target[prime]


def completed_convolution(value: int) -> FormalLog:
    total: FormalLog = {}
    for lambda_index in divisors(value):
        lambda_value = formal_lambda(lambda_index)
        if not lambda_value:
            continue
        quotient = value // lambda_index
        for mobius_index in divisors(quotient):
            add_formal(total, lambda_value, mobius(mobius_index))
    return total


def verify_formal_convolution() -> Dict[str, object]:
    start = CHECKS
    coefficient_checks = 0
    for value in range(1, 10001):
        actual = completed_convolution(value)
        expected = formal_lambda(value)
        primes = set(actual) | set(expected)
        for prime in primes:
            require(
                actual.get(prime, 0) == expected.get(prime, 0),
                "formal Lambda*mu*1 coefficient failed",
            )
            coefficient_checks += 1
        require(actual == expected, "formal convolution dictionary failed")
    return {
        "checks": CHECKS - start,
        "integer_range": [1, 10000],
        "formal_prime_log_coefficient_checks": coefficient_checks,
        "identity": "Lambda*mu*1=Lambda",
    }


def verify_endpoint_exponents() -> Dict[str, object]:
    start = CHECKS
    orbit = Fraction(133, 400)
    row = Fraction(267, 400)
    modulus = Fraction(399, 400)
    alias = Fraction(1, 400)
    target = Fraction(167, 100)
    require(3 * orbit == modulus, "triple-prime exponent failed")
    require(1 - modulus == alias, "alias length exponent failed")
    require(row + orbit == 1, "QJ=X exponent failed")
    require(row - 2 * orbit == alias, "K_B=Q/J^2 exponent failed")
    require(
        2 * row + orbit + alias == target,
        "B0*K_B endpoint exponent failed",
    )
    require(3 * row - orbit == target, "Q^3/J exponent failed")
    require(row - alias == 2 * orbit, "Q/K_B=J^2 exponent failed")
    return {
        "checks": CHECKS - start,
        "Y": frac_text(orbit),
        "Q": frac_text(row),
        "M": frac_text(modulus),
        "K": frac_text(alias),
        "target": frac_text(target),
        "identities": [
            "3*(133/400)=399/400",
            "1-399/400=1/400",
            "2*(267/400)+133/400+1/400=167/100",
            "3*(267/400)-133/400=167/100",
            "267/400-1/400=2*(133/400)",
        ],
    }


def verify_source_constraints(script_path: Path) -> Dict[str, object]:
    start = CHECKS
    source = script_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(script_path))
    assert_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    float_nodes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, float)
    ]
    division_nodes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
    ]
    imports: List[str] = []
    random_imports: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
                if alias.name == "random" or alias.name.startswith("random."):
                    random_imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.append(module)
            if module == "random" or module.startswith("random."):
                random_imports.append(module)
    allowed_roots = {
        "__future__",
        "ast",
        "fractions",
        "hashlib",
        "itertools",
        "json",
        "math",
        "pathlib",
        "typing",
    }
    external_imports = sorted(
        {
            module
            for module in imports
            if module.split(".")[0] not in allowed_roots
        }
    )
    require(not assert_nodes, "certificate source contains assert")
    require(not float_nodes, "certificate source contains a float literal")
    require(not division_nodes, "certificate source contains true division")
    require(not random_imports, "certificate source imports random")
    require(not external_imports, "certificate source imports a non-stdlib module")
    return {
        "checks": CHECKS - start,
        "stdlib_only": True,
        "assert_statements": len(assert_nodes),
        "float_literals": len(float_nodes),
        "true_division_nodes": len(division_nodes),
        "random_imports": len(random_imports),
        "external_imports": external_imports,
        "optimization_safe_explicit_checks": True,
    }


def build_report(script_path: Path) -> Dict[str, object]:
    source_key = "experiments/tpc41_certificate.py"
    report: Dict[str, object] = {
        "schema": "tpc41-row-diagonal-four-mobius-certificate-v1",
        "status": "pass",
        "arithmetic": (
            "exact integers, Fraction exponents, modular character sums, "
            "Gaussian-integer atoms, and formal prime-log vectors"
        ),
        "source_sha256": {source_key: sha256_bytes(script_path.read_bytes())},
        "source_constraints": verify_source_constraints(script_path),
        "minimal_and_full_alias_Grams": verify_alias_grams(),
        "same_row_closure": verify_same_row_closure(),
        "folded_alias_pairs": verify_folded_alias_pairs(),
        "affine_nondegeneracy": verify_affine_nondegeneracy(),
        "formal_Dirichlet_convolution": verify_formal_convolution(),
        "endpoint_exponent_ledger": verify_endpoint_exponents(),
        "claims": {
            "finite_minimal_alias_Gram_checks": True,
            "finite_spectrum_2_1_0_checks": True,
            "finite_full_DFT_identity_checks": True,
            "finite_same_row_closure_checks": True,
            "finite_sharp_closure_examples": True,
            "finite_folded_alias_pair_checks": True,
            "finite_affine_nondegeneracy_checks": True,
            "finite_formal_Lambda_mu_one_identity_checks": True,
            "endpoint_exponent_checks": True,
            "uses_floating_point": False,
            "uses_random_inputs": False,
            "proves_KMT_asymptotic_input": False,
            "proves_multiplicative_large_sieve": False,
            "proves_physical_four_Mobius_bound": False,
            "proves_parity_break": False,
            "proves_hardy_littlewood_prime_pairs": False,
            "proves_twin_primes": False,
        },
        "claim_boundaries": [
            (
                "The certificate verifies finite exact algebraic identities "
                "and endpoint rational-exponent ledgers only."
            ),
            (
                "The raw triple-prime variance theorem uses cited analytic "
                "inputs and is not certified by finite computation."
            ),
            (
                "No physical four-Mobius estimate, parity breach, prime-pair "
                "asymptotic, or twin-prime conclusion is certified."
            ),
        ],
    }
    report["check_total"] = CHECKS
    report["certificate_digest"] = canonical_digest(report)
    return report


def main() -> int:
    script_path = Path(__file__).resolve()
    output_path = script_path.with_suffix(".json")
    report = build_report(script_path)
    encoded = canonical_json_bytes(report)
    output_path.write_bytes(encoded)
    source_key = "experiments/tpc41_certificate.py"
    summary = {
        "certificate": str(output_path),
        "checks": report["check_total"],
        "digest": report["certificate_digest"],
        "json_sha256": sha256_bytes(encoded),
        "source_sha256": report["source_sha256"][source_key],
        "status": report["status"],
    }
    print(canonical_json_bytes(summary).decode("ascii").rstrip("\n"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CertificateError as error:
        print(
            canonical_json_bytes(
                {"error": str(error), "status": "fail"}
            ).decode("ascii").rstrip("\n")
        )
        raise SystemExit(1)
