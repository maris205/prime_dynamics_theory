#!/usr/bin/env python3
"""Exact finite certificate for TPC-114 residual/native grouping."""

from fractions import Fraction as F
from math import gcd
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


def fraction_text(x):
    return f"{x.numerator}/{x.denominator}"


def main():
    collision_checks = 0
    for d in range(1, 13):
        for dp in range(1, 13):
            for r in range(1, 13):
                for rp in range(1, 13):
                    if d * r != dp * rp:
                        continue
                    g = gcd(d, dp)
                    a, b = d // g, dp // g
                    assert gcd(a, b) == 1
                    assert r % b == 0 and rp % a == 0
                    assert r // b == rp // a
                    t = r // b
                    assert (d, dp, r, rp) == (g * a, g * b, b * t, a * t)
                    collision_checks += 1

    records = [
        {"d": 2, "r": 3, "gamma": "A", "j": 0, "weight": F(1)},
        {"d": 3, "r": 2, "gamma": "A", "j": 0, "weight": F(2)},
        {"d": 1, "r": 5, "gamma": "A", "j": 0, "weight": F(-1)},
        {"d": 5, "r": 1, "gamma": "A", "j": 0, "weight": F(3)},
        {"d": 1, "r": 7, "gamma": "A", "j": 0, "weight": F(2)},
        {"d": 2, "r": 2, "gamma": "B", "j": 1, "weight": F(1)},
        {"d": 4, "r": 1, "gamma": "B", "j": 1, "weight": F(-2)},
    ]

    def q(rec):
        return (rec["gamma"], rec["j"], rec["d"] * rec["r"])

    def pi(y):
        return y[:2]

    residuals = sorted({q(rec) for rec in records})
    natives = sorted({pi(y) for y in residuals})
    y_index = {y: i for i, y in enumerate(residuals)}
    i_index = {x: i for i, x in enumerate(natives)}

    rmat = [[F(0) for _ in records] for _ in residuals]
    for u, rec in enumerate(records):
        rmat[y_index[q(rec)]][u] = rec["weight"]

    pmat = [[F(0) for _ in residuals] for _ in natives]
    for y, residual in enumerate(residuals):
        pmat[i_index[pi(residual)]][y] = F(1)

    rr_star = matmul(rmat, transpose(rmat))
    weights = [
        sum((rec["weight"] ** 2 for rec in records if q(rec) == y), F(0))
        for y in residuals
    ]
    assert rr_star == diagonal(weights)

    pp_star = matmul(pmat, transpose(pmat))
    degrees = [
        sum((1 for y in residuals if pi(y) == native), 0)
        for native in natives
    ]
    assert pp_star == diagonal([F(k) for k in degrees])

    gres = matmul(transpose(rmat), rmat)
    gnat = matmul(matmul(transpose(rmat), matmul(transpose(pmat), pmat)),
                  rmat)
    entry_checks = 0
    exchange_checks = 0
    for u, rec_u in enumerate(records):
        for v, rec_v in enumerate(records):
            coeff = rec_u["weight"] * rec_v["weight"]
            expected_res = coeff if q(rec_u) == q(rec_v) else F(0)
            expected_nat = coeff if pi(q(rec_u)) == pi(q(rec_v)) else F(0)
            expected_exchange = (
                coeff if q(rec_u) != q(rec_v)
                and pi(q(rec_u)) == pi(q(rec_v)) else F(0)
            )
            assert gres[u][v] == expected_res
            assert gnat[u][v] == expected_nat
            assert gnat[u][v] - gres[u][v] == expected_exchange
            entry_checks += 2
            exchange_checks += 1

    # Sharp two-label native fiber.
    p_pair = [[F(1), F(1)]]
    plus = [[F(1)], [F(1)]]
    minus = [[F(1)], [F(-1)]]
    assert matmul(p_pair, plus) == [[F(2)]]
    assert matmul(p_pair, minus) == [[F(0)]]
    plus_native_energy = matmul(transpose(matmul(p_pair, plus)),
                                matmul(p_pair, plus))[0][0]
    minus_native_energy = matmul(transpose(matmul(p_pair, minus)),
                                 matmul(p_pair, minus))[0][0]
    assert plus_native_energy == F(4)
    assert minus_native_energy == F(0)

    positive_weights = [w for w in weights if w > 0]
    result = {
        "schema": "tpc-114-residual-native-grouping-v1",
        "status": "PASS",
        "checks": {
            "coprime_collision_normal_forms": collision_checks,
            "coarea_matrix_identity": 1,
            "native_degree_identity": 1,
            "gram_entry_identities": entry_checks,
            "alias_exchange_identities": exchange_checks,
            "sharp_add_cancel_identities": 4,
        },
        "fiber_data": {
            "residual_fibers": len(residuals),
            "native_fibers": len(natives),
            "weights": [fraction_text(w) for w in weights],
            "native_degrees": degrees,
            "grouping_condition_squared":
                fraction_text(max(positive_weights) / min(positive_weights)),
        },
        "sharp_pair": {
            "residual_energy": "2/1",
            "plus_native_energy": fraction_text(plus_native_energy),
            "minus_native_energy": fraction_text(minus_native_energy),
        },
        "claim_boundary": {
            "finite_exact_certificate": True,
            "actual_growing_fiber_bound": False,
            "actual_native_frame_bound": False,
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
