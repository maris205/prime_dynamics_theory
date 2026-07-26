#!/usr/bin/env python3
"""Exact finite certificate for TPC-115 localization constants."""

from fractions import Fraction as F
import json
from pathlib import Path


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0))
             for col in bt] for row in a]


def diagonal(values):
    n = len(values)
    return [[values[i] if i == j else F(0) for j in range(n)]
            for i in range(n)]


def quadratic(vector, matrix):
    col = [[x] for x in vector]
    return matmul(transpose(col), matmul(matrix, col))[0][0]


def identity(n):
    return diagonal([F(1) for _ in range(n)])


def fraction_text(x):
    return f"{x.numerator}/{x.denominator}"


def sylvester_hadamard(n):
    assert n >= 1 and n & (n - 1) == 0
    h = [[F(1)]]
    while len(h) < n:
        h = [row + row for row in h] + [
            row + [-x for x in row] for row in h
        ]
    return h


def main():
    # Full profile space with weights 1/6, 2/6, 3/6.
    weights = [F(1, 6), F(2, 6), F(3, 6)]
    omega = diagonal(weights)
    omega_dagger = diagonal([F(1, p) for p in weights])
    full_costs = [
        quadratic([F(1) if i == h else F(0) for i in range(3)],
                  omega_dagger)
        for h in range(3)
    ]
    assert full_costs == [F(6), F(3), F(2)]

    # Constant profile.
    ones = [[F(1)] for _ in range(3)]
    constant_gram = matmul(transpose(ones), matmul(omega, ones))
    assert constant_gram == [[F(1)]]
    constant_cost = F(1) / constant_gram[0][0]
    assert constant_cost == F(1)

    # Walsh characters: B^* (I/N) B = I_d and row norm squared d.
    n = 8
    hadamard = sylvester_hadamard(n)
    character_costs = {}
    character_checks = 0
    for d in [1, 2, 4, 8]:
        bmat = [row[:d] for row in hadamard]
        gram = [[x / n for x in row]
                for row in matmul(transpose(bmat), bmat)]
        assert gram == identity(d)
        for h0 in range(n):
            cost = quadratic(bmat[h0], identity(d))
            assert cost == F(d)
            character_checks += 1
        character_costs[str(d)] = fraction_text(F(d))

    # Rank-one observation A=(1 1).
    amat = [[F(1), F(1)]]
    gram_rank_one = matmul(transpose(amat), amat)
    assert gram_rank_one == [[F(1), F(1)], [F(1), F(1)]]
    gram_dagger = [[F(1, 4), F(1, 4)],
                   [F(1, 4), F(1, 4)]]
    assert matmul(matmul(gram_rank_one, gram_dagger), gram_rank_one) \
        == gram_rank_one
    visible_target = [F(1), F(1)]
    visible_cost = quadratic(visible_target, gram_dagger)
    assert visible_cost == F(1)
    kernel_vector = [F(1), F(-1)]
    invisible_target = [F(1), F(0)]
    assert matmul(amat, [[x] for x in kernel_vector]) == [[F(0)]]
    assert sum((a * b for a, b in zip(invisible_target, kernel_vector)),
               F(0)) == F(1)

    result = {
        "schema": "tpc-115-localization-certificate-v1",
        "status": "PASS",
        "checks": {
            "unrestricted_weighted_costs": 3,
            "constant_profile_cost": 1,
            "character_orthogonality_and_costs": character_checks,
            "rank_one_pseudoinverse_identities": 2,
            "kernel_obstruction_witnesses": 2,
        },
        "exact_costs": {
            "unrestricted": [fraction_text(x) for x in full_costs],
            "constant": fraction_text(constant_cost),
            "walsh_character_subspaces": character_costs,
            "visible_rank_one_target": fraction_text(visible_cost),
            "invisible_coordinate_target": "infinite",
        },
        "claim_boundary": {
            "finite_exact_certificate": True,
            "actual_low_dimensional_shift_profile": False,
            "actual_christoffel_bound": False,
            "new_L2_fixed_shift_estimate": False,
            "parity_breakthrough": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
