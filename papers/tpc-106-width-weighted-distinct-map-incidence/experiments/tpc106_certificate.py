#!/usr/bin/env python3
"""Deterministic finite certificate for TPC-106.

This checks exact rational Gram/energy identities and the sharp
fixed-h0 alignment family.  It is not an asymptotic cancellation
experiment.
"""

from fractions import Fraction
import json
from pathlib import Path


def centered_inner(f, g, q):
    size = q - 1
    mf = sum(f.values(), Fraction(0))
    mg = sum(g.values(), Fraction(0))
    collision = sum(
        f.get(y, Fraction(0)) * g.get(y, Fraction(0))
        for y in range(1, q)
    )
    return collision - mf * mg / size


def energy(family, q):
    total = {y: Fraction(0) for y in range(1, q)}
    for f in family:
        for y, value in f.items():
            total[y] += value
    return centered_inner(total, total, q)


def direct_cross(family, q):
    answer = Fraction(0)
    for i, f in enumerate(family):
        for j, g in enumerate(family):
            if i != j:
                answer += centered_inner(f, g, q)
    return answer


def alignment_case(q, h0, j0, y0, m_values, weight):
    maps = []
    outputs = []
    for m in m_values:
        denominator = (m * j0 + h0) % q
        assert denominator
        A = y0 * pow(denominator, -1, q) % q
        slope = A * m % q
        intercept = A * h0 % q
        maps.append((slope, intercept))
        outputs.append((slope * j0 + intercept) % q)
    assert len(set(maps)) == len(maps)
    assert outputs == [y0] * len(outputs)
    family = [{y0: Fraction(weight)} for _ in maps]
    return maps, family


def run():
    cases = []
    total_checks = 0
    for q in (7, 11, 13):
        h0, j0, y0 = 2, 1, 3
        forbidden = (-h0 * pow(j0, -1, q)) % q
        m_values = [m for m in range(1, q) if m != forbidden][:4]
        maps, family = alignment_case(
            q, h0, j0, y0, m_values, weight=2
        )
        k = len(family)
        cross = direct_cross(family, q)
        internal = sum(
            (centered_inner(f, f, q) for f in family), Fraction(0)
        )
        total_energy = energy(family, q)
        predicted_cross = (
            Fraction(k * (k - 1) * 4 * (q - 2), q - 1)
        )
        predicted_internal = Fraction(k * 4 * (q - 2), q - 1)
        assert cross == predicted_cross
        assert internal == predicted_internal
        assert total_energy - internal == cross
        assert cross / internal == k - 1
        total_checks += 4

        # A non-aligned exact identity check.
        generic = [
            {1: Fraction(1), 2: Fraction(2)},
            {2: Fraction(3), 4: Fraction(1)},
            {3: Fraction(2), 5: Fraction(2)},
        ]
        cross_generic = direct_cross(generic, q)
        internal_generic = sum(
            (centered_inner(f, f, q) for f in generic), Fraction(0)
        )
        assert energy(generic, q) - internal_generic == cross_generic
        assert abs(cross_generic) <= (
            len(generic) - 1
        ) * internal_generic
        total_checks += 2
        cases.append(
            {
                "q": q,
                "map_count": k,
                "distinct_maps": len(set(maps)),
                "sharp_cross": str(cross),
                "sharp_internal_energy": str(internal),
                "sharp_coherence": str(cross / internal),
                "generic_cross": str(cross_generic),
            }
        )

    result = {
        "schema": "tpc-106-distinct-map-certificate-v1",
        "status": "PASS",
        "claim_boundary": {
            "finite_identity_only": True,
            "actual_growing_profile_bound": False,
            "fixed_h0_L2_estimate": False,
            "prime_pair_result": False,
        },
        "checks": total_checks,
        "cases": cases,
    }
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
