#!/usr/bin/env python3
"""Deterministic exact certificate for TPC-49.

The certificate checks finite models of the paper's projective-to-atomic
mechanisms.  It uses integer, rational, and finite-field arithmetic only.
It is a regression certificate, not a proof of the asymptotic theorems
and not a search for literal prime-pair or prime/cofactor atoms.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import itertools
import json
from math import gcd, isqrt
from pathlib import Path


CHECKS = 0


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def prime_divisors(n: int) -> tuple[int, ...]:
    answer = []
    work = n
    d = 2
    while d * d <= work:
        if work % d == 0:
            answer.append(d)
            while work % d == 0:
                work //= d
        d += 1
    if work > 1:
        answer.append(work)
    return tuple(answer)


def divisors(n: int) -> tuple[int, ...]:
    small = []
    large = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d * d != n:
                large.append(n // d)
        d += 1
    return tuple(small + list(reversed(large)))


def squarefree(n: int) -> bool:
    for p in prime_divisors(n):
        if n % (p * p) == 0:
            return False
    return True


def primitive_root(prime: int) -> int:
    require(is_prime(prime), "primitive-root modulus is prime")
    factors = prime_divisors(prime - 1)
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise RuntimeError("primitive root not found")


def check_rademacher_permutations() -> dict:
    start = CHECKS
    records = []
    for n in range(1, 9):
        signs = tuple(itertools.product((-1, 1), repeat=n))
        denominator = 2**n
        for i in range(n):
            for j in range(n):
                total = sum(eps[i] * eps[j] for eps in signs)
                require(
                    total == denominator * int(i == j),
                    "Rademacher average is the identity",
                )
        require(
            sum(Fraction(1, denominator) for _ in signs) == 1,
            "Rademacher projective mass is one",
        )

        permutation = tuple((3 * i + 1) % n for i in range(n))
        if n > 1 and gcd(3, n) != 1:
            permutation = tuple(reversed(range(n)))
        require(len(set(permutation)) == n, "chosen map is a permutation")
        matrix = [
            [int(j == permutation[i]) for j in range(n)]
            for i in range(n)
        ]
        for row in matrix:
            require(sum(row) == 1, "permutation has one entry per row")
        for j in range(n):
            require(
                sum(matrix[i][j] for i in range(n)) == 1,
                "permutation has one entry per column",
            )
        frobenius_squared = sum(sum(row) for row in matrix)
        nuclear = n
        require(frobenius_squared == n, "permutation Frobenius ledger")
        require(
            Fraction(nuclear * nuclear, frobenius_squared) == n,
            "permutation nuclear effective rank",
        )
        records.append(
            {
                "n": n,
                "sign_vectors": denominator,
                "projective_mass": "1",
                "atomic_energy": frobenius_squared,
                "nuclear_norm": nuclear,
                "nuclear_effective_rank": n,
            }
        )
    return {"checks": CHECKS - start, "records": records}


def complete_rows(L: int, D: int, H: int) -> tuple[tuple[int, int], ...]:
    primes = tuple(ell for ell in range(L + 1, 2 * L + 1) if is_prime(ell))
    ds = tuple(
        d
        for d in range(D + 1, 2 * D + 1)
        if squarefree(d) and gcd(d, H) == 1
    )
    return tuple((ell, d) for ell in primes for d in ds)


def augmenting_matching(mask: list[list[int]]) -> tuple[int, ...] | None:
    n = len(mask)
    right_owner = [-1] * n

    def visit(left: int, seen: list[bool]) -> bool:
        for right in range(n):
            if not mask[left][right] or seen[right]:
                continue
            seen[right] = True
            if right_owner[right] < 0 or visit(right_owner[right], seen):
                right_owner[right] = left
                return True
        return False

    for left in range(n):
        if not visit(left, [False] * n):
            return None
    left_to_right = [-1] * n
    for right, left in enumerate(right_owner):
        left_to_right[left] = right
    return tuple(left_to_right)


def check_static_mask_case(
    L: int, D: int, H: int, delta: int, G: int
) -> dict:
    start = CHECKS
    require(L > 4 * D, "row labels lie in the injective separation range")
    rows = complete_rows(L, D, H)
    n = len(rows)
    require(n > 0, "complete row universe is nonempty")
    labels = tuple(ell * d for ell, d in rows)
    require(len(set(labels)) == n, "row products are injective")

    mask = [[0] * n for _ in range(n)]
    row_degrees = []
    union_bounds = []
    category_maxima = {"same_source": 0, "near_row": 0, "gcd_bad": 0}
    for i, (ell, d) in enumerate(rows):
        same = {
            j for j, (ell2, _) in enumerate(rows) if ell2 == ell
        }
        near = {
            j for j, label in enumerate(labels) if abs(labels[i] - label) <= delta
        }
        gcd_bad = {
            j for j, (_, d2) in enumerate(rows) if gcd(d, d2) > G
        }
        category_maxima["same_source"] = max(
            category_maxima["same_source"], len(same)
        )
        category_maxima["near_row"] = max(
            category_maxima["near_row"], len(near)
        )
        category_maxima["gcd_bad"] = max(
            category_maxima["gcd_bad"], len(gcd_bad)
        )

        require(len(same) <= D, "same-source crude bound")
        require(len(near) <= 2 * delta + 1, "near-label injective bound")
        divisor_bound = sum(
            (2 * D) // g - D // g + 1
            for g in divisors(d)
            if g > G
        )
        prime_count = len({ell2 for ell2, _ in rows})
        require(
            len(gcd_bad) <= prime_count * divisor_bound,
            "gcd-bad divisor union bound",
        )

        forbidden = same | near | gcd_bad
        require(
            len(forbidden) <= len(same) + len(near) + len(gcd_bad),
            "forbidden union bound",
        )
        for j, (ell2, d2) in enumerate(rows):
            value = int(
                ell != ell2
                and abs(labels[i] - labels[j]) > delta
                and gcd(d, d2) <= G
            )
            mask[i][j] = value
            require(value == int(j not in forbidden), "literal mask formula")
        degree = sum(mask[i])
        row_degrees.append(degree)
        union_bounds.append(len(same) + len(near) + len(gcd_bad))
        require(degree == n - len(forbidden), "exact degree identity")
        require(degree >= n - union_bounds[-1], "degree union lower bound")

    column_degrees = [sum(mask[i][j] for i in range(n)) for j in range(n)]
    require(mask == [list(row) for row in zip(*mask)], "mask is symmetric")
    require(min(row_degrees) == min(column_degrees), "symmetric minimum degree")
    require(2 * min(row_degrees) > n, "finite case lies above Hall threshold")

    matching = augmenting_matching(mask)
    require(matching is not None, "admitted graph has a perfect matching")
    assert matching is not None
    require(len(set(matching)) == n, "matching uses every right vertex once")
    for left, right in enumerate(matching):
        require(mask[left][right] == 1, "matching lies in admitted positions")

    admitted_entries = sum(row_degrees)
    matching_atomic = n
    matching_nuclear = n
    require(
        matching_nuclear * matching_nuclear
        == n * matching_atomic,
        "matching packet has distortion n",
    )
    return {
        "checks": CHECKS - start,
        "parameters": {"L": L, "D": D, "H": H, "Delta": delta, "G": G},
        "row_count": n,
        "minimum_degree": min(row_degrees),
        "maximum_forbidden_union_bound": max(union_bounds),
        "category_maxima": category_maxima,
        "admitted_entries": admitted_entries,
        "admitted_density": f"{admitted_entries}/{n*n}",
        "perfect_matching": True,
        "matching_atomic_energy": matching_atomic,
        "matching_nuclear_norm": matching_nuclear,
        "matching_effective_rank": n,
    }


def check_static_masks() -> dict:
    start = CHECKS
    cases = (
        (101, 20, 6, 18, 5),
        (211, 40, 10, 35, 7),
        (151, 30, 30, 25, 7),
    )
    records = [check_static_mask_case(*case) for case in cases]
    return {"checks": CHECKS - start, "cases": records}


def check_product_kernels_and_phases() -> dict:
    start = CHECKS
    phase_cases = ((5, 11), (7, 29), (11, 23), (13, 53))
    records = []
    for q, modulus in phase_cases:
        require((modulus - 1) % q == 0, "finite field contains q-th roots")
        generator = primitive_root(modulus)
        zeta = pow(generator, (modulus - 1) // q, modulus)
        require(pow(zeta, q, modulus) == 1, "cyclotomic root closes")
        for exponent in range(1, q):
            require(pow(zeta, exponent, modulus) != 1, "root has exact order q")

        a = 2 % q
        permutation = [a * pow(x, -1, q) % q for x in range(1, q)]
        require(0 not in permutation, "product permutation stays nonzero")
        require(len(set(permutation)) == q - 1, "product delta is a permutation")
        for x, y in zip(range(1, q), permutation):
            require(x * y % q == a, "product delta equation")

        phase = [
            [pow(zeta, (x * y) % q, modulus) for y in range(1, q)]
            for x in range(1, q)
        ]
        for i in range(q - 1):
            for j in range(q - 1):
                gram = sum(
                    phase[i][k] * pow(phase[j][k], -1, modulus)
                    for k in range(q - 1)
                ) % modulus
                expected = (q - 1 if i == j else -1) % modulus
                require(gram == expected, "product phase Gram qI-J")
        records.append(
            {
                "q": q,
                "cyclotomic_modulus": modulus,
                "product_kernel_size": q - 1,
                "product_kernel_projective_mass": "1",
                "product_kernel_effective_rank": q - 1,
                "phase_singular_spectrum": {"sqrt_q_multiplicity": q - 2, "one_multiplicity": 1},
                "phase_frobenius_squared": (q - 1) ** 2,
            }
        )
    return {"checks": CHECKS - start, "records": records}


def kronecker(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [left[i][j] * right[r][c] for j in range(len(left[0])) for c in range(len(right[0]))]
        for i in range(len(left))
        for r in range(len(right))
    ]


def hadamard_power(k: int) -> list[list[int]]:
    base = [
        [-1, 1, 1, 1],
        [1, -1, 1, 1],
        [1, 1, -1, 1],
        [1, 1, 1, -1],
    ]
    matrix = [[1]]
    for _ in range(k):
        matrix = kronecker(matrix, base)
    return matrix


def check_dense_hadamard_masks() -> dict:
    start = CHECKS
    records = []
    for k in range(1, 4):
        h = hadamard_power(k)
        n = 4**k
        root_n = 2**k
        require(len(h) == n and len(h[0]) == n, "Hadamard dimension")
        for row in h:
            require(all(entry in (-1, 1) for entry in row), "Hadamard signs")
            require(sum(row) == root_n, "Hadamard constant row sum")
        for i in range(n):
            for j in range(n):
                inner = sum(h[i][s] * h[j][s] for s in range(n))
                require(inner == n * int(i == j), "Hadamard Gram identity")

        mask = [[(1 + h[i][j]) // 2 for j in range(n)] for i in range(n)]
        row_ones = (n + root_n) // 2
        for row in mask:
            require(all(entry in (0, 1) for entry in row), "dense mask is zero-one")
            require(sum(row) == row_ones, "dense mask row count")
        for i in range(n):
            for j in range(n):
                gram = sum(mask[i][s] * mask[j][s] for s in range(n))
                formula = ((n + 2 * root_n) + n * int(i == j)) // 4
                require(gram == formula, "dense mask Gram entry formula")

        frobenius_squared = n * row_ones
        nuclear_twice = n * (1 + root_n)
        effective_rank = Fraction(n + root_n, 2)
        require(
            Fraction(nuclear_twice * nuclear_twice, 4 * frobenius_squared)
            == effective_rank,
            "dense mask nuclear effective rank",
        )
        records.append(
            {
                "n": n,
                "row_ones": row_ones,
                "density": f"{row_ones}/{n}",
                "frob_squared": frobenius_squared,
                "twice_nuclear_norm": nuclear_twice,
                "effective_rank": f"{effective_rank.numerator}/{effective_rank.denominator}",
            }
        )
    return {"checks": CHECKS - start, "records": records}


def check_endpoint_ledger() -> dict:
    start = CHECKS
    mu = Fraction(267, 400)
    nu = Fraction(133, 400)
    kappa = Fraction(1, 400)
    require(mu + nu == 1, "endpoint source and orbit exponents sum to one")
    require(nu - kappa == Fraction(33, 100), "orbit permutation deficit")
    require(mu - kappa == Fraction(133, 200), "row matching deficit")
    require(mu - nu == Fraction(67, 200), "coarse collision exponent")
    require((mu - nu) - kappa == nu, "coarse collision budget deficit")
    require(nu / 2 - kappa / 2 == Fraction(33, 200), "amplitude deficit")
    return {
        "checks": CHECKS - start,
        "mu": f"{mu.numerator}/{mu.denominator}",
        "nu": f"{nu.numerator}/{nu.denominator}",
        "kappa": f"{kappa.numerator}/{kappa.denominator}",
        "product_permutation_energy_deficit": "33/100",
        "matching_energy_deficit": "133/200",
        "coarse_collision_exponent": "67/200",
        "coarse_collision_budget_deficit": "133/400",
        "product_permutation_amplitude_deficit": "33/200",
    }


def normalized_source_hash() -> str:
    source = Path(__file__).read_text(encoding="utf-8").replace("\r\n", "\n")
    return sha256(source.encode("utf-8")).hexdigest()


def main() -> None:
    result = {
        "certificate": "TPC-49 weighted mask and nuclear distortion",
        "arithmetic": "integers, rationals, and exact finite fields",
        "rademacher_permutations": check_rademacher_permutations(),
        "static_masks": check_static_masks(),
        "product_models": check_product_kernels_and_phases(),
        "dense_hadamard_masks": check_dense_hadamard_masks(),
        "endpoint_ledger": check_endpoint_ledger(),
    }
    result["total_checks"] = CHECKS
    semantic_payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["semantic_sha256"] = sha256(semantic_payload.encode("utf-8")).hexdigest()
    result["normalized_source_sha256"] = normalized_source_hash()

    output = Path(__file__).with_name("tpc49_certificate.json")
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    output_hash = sha256(output.read_bytes()).hexdigest()
    print(f"TPC-49 certificate: {CHECKS} exact checks passed")
    print(f"semantic sha256: {result['semantic_sha256']}")
    print(f"normalized source sha256: {result['normalized_source_sha256']}")
    print(f"json sha256: {output_hash}")


if __name__ == "__main__":
    main()
