"""Exact finite certificate for a prime-target local-information defect.

The two nonnegative point masses in this file have the same complete residue
pushforward modulo Q = 5 * 7 * 11, and therefore the same finite CRT,
character, and centered target-rough-kernel data.  Their targets nevertheless
have different prime indicators and opposite Liouville parity.

Every calculation uses standard-library integers or ``fractions.Fraction``.
There is no floating-point arithmetic and no probabilistic computation.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Dict, Mapping, Sequence, Tuple


PRIMES: Tuple[int, ...] = (5, 7, 11)
Q = math.prod(PRIMES)
SHIFT = 2
SQUARE_TARGET = (Q + 1) ** 2
PRIME_TARGET = SQUARE_TARGET + Q
LUCAS_WITNESS = 3


def factor_integer(n: int) -> Dict[int, int]:
    """Return the exact prime factorization of a positive integer."""

    if n <= 0:
        raise ValueError("factorization is defined here only for positive integers")
    remaining = n
    factors: Dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def is_prime(n: int) -> bool:
    """Deterministic trial-division primality test."""

    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def liouville(n: int) -> int:
    """Return lambda(n) = (-1)^Omega(n) by exact factorization."""

    omega = sum(factor_integer(n).values())
    return -1 if omega % 2 else 1


def fraction_text(value: Fraction) -> str:
    """Render a rational number without introducing a decimal approximation."""

    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def kappa(h: int, primes: Sequence[int] = PRIMES) -> Fraction:
    """Exact survivor density among unit pairs for the active window primes."""

    value = Fraction(1)
    for p in primes:
        if h % p != 0:
            value *= Fraction(p - 2, p - 1)
    return value


def target(m: int, n: int, h: int = SHIFT) -> int:
    return m * n + h


def residue_cell(m: int, n: int, modulus: int = Q) -> Tuple[int, int]:
    return (m % modulus, n % modulus)


def local_signature(m: int, n: int, h: int, p: int) -> Tuple[int, int, int]:
    """Return the complete local residues of m, n, and mn+h modulo p."""

    return (m % p, n % p, target(m, n, h) % p)


def centered_kernel(
    m: int,
    n: int,
    h: int = SHIFT,
    primes: Sequence[int] = PRIMES,
) -> Fraction:
    """Evaluate the normalized centered target-rough indicator exactly."""

    modulus = math.prod(primes)
    if math.gcd(m * n, modulus) != 1:
        raise ValueError("kernel arguments must be units at every window prime")
    survives = math.gcd(target(m, n, h), modulus) == 1
    return (Fraction(1, 1) / kappa(h, primes) if survives else Fraction(0)) - 1


def lucas_certificate(n: int, witness: int) -> Dict[str, object]:
    """Build a full Lucas certificate using the factorization of n-1."""

    factors = factor_integer(n - 1)
    checks: Dict[str, Dict[str, int]] = {}
    for q in sorted(factors):
        exponent = (n - 1) // q
        residue = pow(witness, exponent, n)
        checks[str(q)] = {
            "exponent": exponent,
            "residue": residue,
            "gcd_residue_minus_one_with_n": math.gcd(residue - 1, n),
        }
    return {
        "n": n,
        "n_minus_1_factorization": {
            str(q): exponent for q, exponent in sorted(factors.items())
        },
        "witness": witness,
        "fermat_residue": pow(witness, n - 1, n),
        "prime_divisor_checks": checks,
    }


def validate_lucas_certificate(certificate: Mapping[str, object]) -> None:
    """Verify the hypotheses of the full-factorization Lucas criterion."""

    n = int(certificate["n"])
    witness = int(certificate["witness"])
    factors = {
        int(q): int(exponent)
        for q, exponent in certificate["n_minus_1_factorization"].items()
    }
    if math.prod(q**exponent for q, exponent in factors.items()) != n - 1:
        raise AssertionError("the displayed factorization does not equal n-1")
    if any(not is_prime(q) for q in factors):
        raise AssertionError("a divisor in the n-1 factorization is not prime")
    fermat_residue = pow(witness, n - 1, n)
    if certificate["fermat_residue"] != fermat_residue:
        raise AssertionError("the recorded Fermat residue is incorrect")
    if fermat_residue != 1:
        raise AssertionError("the Fermat congruence in the Lucas certificate failed")
    checks = certificate["prime_divisor_checks"]
    for q in factors:
        exponent = (n - 1) // q
        residue = pow(witness, exponent, n)
        gcd_value = math.gcd(residue - 1, n)
        recorded = checks[str(q)]
        if recorded != {
            "exponent": exponent,
            "residue": residue,
            "gcd_residue_minus_one_with_n": gcd_value,
        }:
            raise AssertionError(f"the recorded Lucas check for q={q} is incorrect")
        if gcd_value != 1:
            raise AssertionError(f"the Lucas coprimality condition failed for q={q}")


def atom_record(label: str, target_value: int) -> Dict[str, object]:
    m = 1
    n = target_value - SHIFT
    return {
        "label": label,
        "weight": 1,
        "m": m,
        "n": n,
        "target": target_value,
        "factorization": {
            str(p): exponent
            for p, exponent in sorted(factor_integer(target_value).items())
        },
        "is_prime": is_prime(target_value),
        "liouville": liouville(target_value),
        "pair_residue_mod_Q": list(residue_cell(m, n)),
        "target_residue_mod_Q": target_value % Q,
        "local_signatures": {
            str(p): list(local_signature(m, n, SHIFT, p)) for p in PRIMES
        },
        "window_survivor": math.gcd(target_value, Q) == 1,
        "centered_kernel": fraction_text(centered_kernel(m, n)),
    }


def build_certificate() -> Dict[str, object]:
    square = atom_record("square_target", SQUARE_TARGET)
    prime = atom_record("prime_target", PRIME_TARGET)
    kap = kappa(SHIFT)
    kernel_value = centered_kernel(square["m"], square["n"])

    return {
        "schema": "tpc6-exact-prime-target-defect-v1",
        "modulus": Q,
        "primes": list(PRIMES),
        "shift": SHIFT,
        "normalization": {
            "kappa": fraction_text(kap),
            "survivor_centered_kernel": fraction_text(kernel_value),
        },
        "atoms": {
            "square_target": square,
            "prime_target": prime,
        },
        "common_local_data": {
            "pair_residue_mod_Q": square["pair_residue_mod_Q"],
            "target_residue_mod_Q": square["target_residue_mod_Q"],
            "local_signatures": square["local_signatures"],
            "target_difference": PRIME_TARGET - SQUARE_TARGET,
            "second_coordinate_difference": prime["n"] - square["n"],
            "same_residue_pushforward": True,
            "all_residue_class_observables_equal": True,
        },
        "lucas_primality_certificate": lucas_certificate(
            PRIME_TARGET, LUCAS_WITNESS
        ),
        "defect_linear_algebra": {
            "signed_null_vector": {
                "square_target": 1,
                "prime_target": -1,
            },
            "local_pushforward_pairing": 0,
            "prime_functional": {
                "square_target": int(square["is_prime"]),
                "prime_target": int(prime["is_prime"]),
                "null_vector_pairing": int(square["is_prime"])
                - int(prime["is_prime"]),
                "minimax_absolute_error_lower_bound": "1/2",
            },
            "liouville_functional": {
                "square_target": square["liouville"],
                "prime_target": prime["liouville"],
                "null_vector_pairing": square["liouville"] - prime["liouville"],
                "minimax_absolute_error_lower_bound": "1",
            },
        },
    }


def validate_certificate(certificate: Mapping[str, object]) -> None:
    """Recompute every substantive claim in the reference certificate."""

    if certificate["schema"] != "tpc6-exact-prime-target-defect-v1":
        raise AssertionError("the certificate schema is incorrect")
    if certificate["modulus"] != Q or certificate["primes"] != list(PRIMES):
        raise AssertionError("the CRT window is not the reference window")
    if certificate["shift"] != SHIFT:
        raise AssertionError("the target shift is not the reference shift")

    atoms = certificate["atoms"]
    square = atoms["square_target"]
    prime = atoms["prime_target"]
    rebuilt_square = atom_record("square_target", SQUARE_TARGET)
    rebuilt_prime = atom_record("prime_target", PRIME_TARGET)
    if square != rebuilt_square or prime != rebuilt_prime:
        raise AssertionError("an atom record does not match exact recomputation")

    if square["pair_residue_mod_Q"] != prime["pair_residue_mod_Q"]:
        raise AssertionError("the two point masses have different residue pushforwards")
    if square["local_signatures"] != prime["local_signatures"]:
        raise AssertionError("the two point masses have different local signatures")
    if square["centered_kernel"] != prime["centered_kernel"]:
        raise AssertionError("the centered local kernels differ")
    if certificate["normalization"] != {
        "kappa": fraction_text(kappa(SHIFT)),
        "survivor_centered_kernel": fraction_text(centered_kernel(1, SQUARE_TARGET - SHIFT)),
    }:
        raise AssertionError("the kernel normalization is incorrect")

    common = certificate["common_local_data"]
    if common["pair_residue_mod_Q"] != square["pair_residue_mod_Q"]:
        raise AssertionError("the common residue cell is incorrect")
    if common["target_residue_mod_Q"] != 1:
        raise AssertionError("the common target residue is not 1")
    if common["local_signatures"] != square["local_signatures"]:
        raise AssertionError("the common local signature is incorrect")
    if common["target_difference"] != Q or common["second_coordinate_difference"] != Q:
        raise AssertionError("the two lifts should differ by exactly one modulus")
    if not common["same_residue_pushforward"] or not common[
        "all_residue_class_observables_equal"
    ]:
        raise AssertionError("a residue-pushforward consequence flag is false")

    lucas = certificate["lucas_primality_certificate"]
    if lucas["n"] != PRIME_TARGET:
        raise AssertionError("the Lucas certificate is attached to the wrong target")
    validate_lucas_certificate(lucas)

    defect = certificate["defect_linear_algebra"]
    if defect["signed_null_vector"] != {
        "square_target": 1,
        "prime_target": -1,
    }:
        raise AssertionError("the signed null vector is incorrect")
    if defect["local_pushforward_pairing"] != 0:
        raise AssertionError("the signed witness is not in the local nullspace")
    if defect["prime_functional"] != {
        "square_target": 0,
        "prime_target": 1,
        "null_vector_pairing": -1,
        "minimax_absolute_error_lower_bound": "1/2",
    }:
        raise AssertionError("the prime-functional defect is incorrect")
    if defect["liouville_functional"] != {
        "square_target": 1,
        "prime_target": -1,
        "null_vector_pairing": 2,
        "minimax_absolute_error_lower_bound": "1",
    }:
        raise AssertionError("the Liouville-functional defect is incorrect")


def render_certificate(certificate: Mapping[str, object]) -> bytes:
    """Return the canonical UTF-8 JSON representation."""

    return (json.dumps(certificate, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_certificate(path: Path) -> None:
    certificate = build_certificate()
    validate_certificate(certificate)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(render_certificate(certificate))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = build_certificate()
    validate_certificate(certificate)
    rendered = render_certificate(certificate)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(rendered)
    else:
        print(rendered.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
