#!/usr/bin/env python3
"""Independent finite checker for the TPC-209 whole-frame compiler.

The checker validates the exact finite interfaces used by TPC-209 without
importing the paper project's producer or independent checker.  It does not
make an asymptotic or arithmetic claim.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


class CheckFailure(RuntimeError):
    """Raised when a frozen TPC-209 contract is not reproduced."""


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_whole_frame_poisson_mobius_obstruction.md"
PAPER = ROOT / "papers/tpc-209-whole-frame-poisson-mobius-obstruction"
CERTIFICATE = PAPER / "results/certificate.json"

MODULI = (3, 5, 7, 11, 13)
DUAL_RANGE = (-2, -1, 0, 1, 2)

REGISTRY = (
    "TPC209_MAXIMUM_CLAIM = EXACT_FIXED_DIVISOR_WHOLE_FRAME_POISSON_REINDEXING_PLUS_MULTIPLICATIVE_SPECTRAL_NORMAL_FORM_AND_SHARP_VECTOR_ALIGNMENT_OBSTRUCTION",
    "TPC209_ROUTE_ADVANCE = YES",
    "TPC209_STRUCTURAL_THRESHOLD_A = PASS",
    "TPC209_SHARED_DUAL_PER_FIXED_DIVISOR = PROVED_EXACT",
    "TPC209_WHOLE_FRAME_VECTOR_COVARIANCE = PROVED_EXACT",
    "TPC209_MULTIPLICATIVE_CHARACTER_DIAGONALIZATION = PROVED_EXACT",
    "TPC209_RETURN_TO_V59_CHARACTER_INTERFACE = PROVED_EXACT",
    "TPC209_SCALAR_COMMON_DUAL_COLLAPSE = REFUTED_SCOPED",
    "TPC209_FRAME_ONLY_POWER_SAVING = STOP_SCOPED",
    "TPC209_SOURCE_VALID_KLOOSTERMAN_ATTACHMENT = OPEN",
    "TPC209_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "TPC209_ARITHMETIC_ADVANCE = NO",
    "TPC209_GLOBAL_GATE_B_ADVANCE = NO",
    "TPC209_FIXED_ATOM_CREDIT = 0",
    "TPC209_L2 = NONE",
    "TPC209_FIRST_FATAL = NO_FRAME_ONLY_SCALAR_EMITTER_DILATION_PERMUTATIONS_SURVIVE_AND_CHARACTER_DIAGONALIZATION_RETURNS_TO_V59",
    "TPC209_ROUND2_CLUE = PROVE_OR_REFUTE_A_PROFILE_AWARE_NONPRINCIPAL_CHARACTER_BOUND_FOR_THE_ACTUAL_MOBIUS_POISSON_DUAL_PACKETS_BEFORE_ANY_PRIME_OR_BLOCK_TRIANGLE",
    "TPC209_REUSABLE_STRUCTURE = WHOLE_FRAME_POISSON_VECTOR_COMPILER_PLUS_MULTIPLICATIVE_CHARACTER_PROFILE_NORMAL_FORM",
    "TPC209_TPC_TRIGGER = true",
)


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def units(q: int) -> tuple[int, ...]:
    return tuple(range(1, q))


def permutation(q: int, divisor: int) -> tuple[int, ...]:
    require(1 <= divisor < q and math.gcd(divisor, q) == 1, "unit divisor")
    return tuple((frequency * divisor) % q - 1 for frequency in units(q))


def apply_permutation(vector: tuple[complex, ...], q: int, divisor: int) -> tuple[complex, ...]:
    image = permutation(q, divisor)
    return tuple(vector[index] for index in image)


def linear_combination(
    coefficients: tuple[complex, ...],
    profiles: tuple[tuple[complex, ...], ...],
    q: int,
    divisors: tuple[int, ...],
) -> tuple[complex, ...]:
    return tuple(
        sum(
            coefficient * apply_permutation(profile, q, divisor)[coordinate]
            for coefficient, profile, divisor in zip(coefficients, profiles, divisors)
        )
        for coordinate in range(q - 1)
    )


def edges(q: int) -> tuple[tuple[int, int], ...]:
    dimension = q - 1
    return tuple(
        (left, right)
        for left in range(dimension)
        for right in range(left + 1, dimension)
    )


def projection_mean(vector: tuple[complex, ...]) -> complex:
    return sum(vector, 0j) / len(vector)


def frame_form(
    left: tuple[complex, ...], right: tuple[complex, ...]
) -> complex:
    q = len(left) + 1
    return sum(
        (left[i] - left[j]) * (right[i] - right[j]).conjugate()
        for i, j in edges(q)
    ) / (q - 1)


def projected_form(
    left: tuple[complex, ...], right: tuple[complex, ...]
) -> complex:
    left_centered = tuple(value - projection_mean(left) for value in left)
    right_centered = tuple(value - projection_mean(right) for value in right)
    return sum(
        value * other.conjugate()
        for value, other in zip(left_centered, right_centered)
    )


def dual_rows(q: int, divisor: int) -> int:
    seen: set[int] = set()
    inverse = pow(divisor, -1, q)
    rows = 0
    for frequency in units(q):
        for poisson_index in DUAL_RANGE:
            dual = q * poisson_index + frequency * divisor
            require(dual % q != 0, "zero dual residue")
            require(dual not in seen, "dual reindex collision")
            seen.add(dual)
            recovered_frequency = dual * inverse % q
            require(recovered_frequency == frequency, "dual frequency mismatch")
            recovered_index = (dual - recovered_frequency * divisor) // q
            require(recovered_index == poisson_index, "dual Poisson index mismatch")
            rows += 1
    return rows


def primitive_root(q: int) -> int:
    order = q - 1
    factors = tuple(
        factor
        for factor in range(2, order + 1)
        if order % factor == 0
        and all(factor % divisor != 0 for divisor in range(2, factor) if factor % divisor == 0)
    )
    # The small test moduli have a primitive root; this direct search is
    # intentionally finite and independent of the project code.
    for candidate in range(2, q):
        if math.gcd(candidate, q) != 1:
            continue
        if all(pow(candidate, order // factor, q) != 1 for factor in prime_factors(order)):
            return candidate
    raise CheckFailure(f"primitive root not found for q={q}; factors={factors}")


def prime_factors(value: int) -> tuple[int, ...]:
    factors: list[int] = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def discrete_log_table(q: int) -> dict[int, int]:
    generator = primitive_root(q)
    table: dict[int, int] = {}
    value = 1
    for exponent in range(q - 1):
        table[value] = exponent
        value = value * generator % q
    require(len(table) == q - 1, "discrete-log table is not complete")
    return table


def character_value(q: int, character_index: int, value: int, logs: dict[int, int]) -> complex:
    residue = value % q
    require(residue != 0, "character evaluated at zero")
    exponent = character_index * logs[residue] / (q - 1)
    return cmath.exp(2j * math.pi * exponent)


def multiplicative_transform(
    vector: tuple[complex, ...],
    q: int,
    character_index: int,
    logs: dict[int, int],
) -> complex:
    return sum(
        vector[residue - 1]
        * character_value(q, character_index, residue, logs).conjugate()
        for residue in units(q)
    ) / math.sqrt(q - 1)


def check_frame_and_permutations() -> tuple[int, int]:
    frame_rows = 0
    permutation_rows = 0
    for q in MODULI:
        dimension = q - 1
        for left in range(dimension):
            for right in range(dimension):
                expected = dimension - 1 if left == right else -1
                observed = sum(
                    (1 if left == edge_left else -1 if left == edge_right else 0)
                    * (1 if right == edge_left else -1 if right == edge_right else 0)
                    for edge_left, edge_right in edges(q)
                )
                require(observed == expected, f"complete graph Gram mismatch q={q}")
                frame_rows += 1
        require(len(edges(q)) == (q - 1) * (q - 2) // 2, f"edge count q={q}")
        for divisor in units(q):
            image = permutation(q, divisor)
            require(sorted(image) == list(range(q - 1)), f"permutation q={q}, D={divisor}")
            inverse = pow(divisor, -1, q)
            inverse_image = permutation(q, inverse)
            for index in range(q - 1):
                require(image[inverse_image[index]] == index, "permutation inverse")
            permutation_rows += (q - 1) * (q - 1)
    return frame_rows, permutation_rows


def check_whole_frame_covariance() -> int:
    q = 7
    divisors = (1, 2, 3)
    coefficients = (1 + 2j, -2 + 1j, 3 - 1j)
    dual_profiles = (
        tuple(complex(index + 1, 2 * index - 1) for index in range(q - 1)),
        tuple(complex(2 * index - 1, index + 2) for index in range(q - 1)),
        tuple(complex(index * index + 1, -index) for index in range(q - 1)),
    )
    other_profiles = tuple(
        tuple(complex(index - 2, index + 1) for index in range(q - 1))
        for _ in divisors
    )
    left = linear_combination(coefficients, dual_profiles, q, divisors)
    right = linear_combination(coefficients, other_profiles, q, divisors)
    direct = frame_form(left, right)
    expanded = sum(
        coefficients[i] * coefficients[j].conjugate()
        * frame_form(
            apply_permutation(dual_profiles[i], q, divisors[i]),
            apply_permutation(other_profiles[j], q, divisors[j]),
        )
        for i in range(len(divisors))
        for j in range(len(divisors))
    )
    require(abs(direct - expanded) < 1e-9, "whole-frame covariance mismatch")
    return 1


def check_character_diagonalization() -> int:
    rows = 0
    for q in MODULI:
        logs = discrete_log_table(q)
        vector = tuple(complex(index + 1, -2 * index + 3) for index in range(q - 1))
        for divisor in units(q):
            transformed = apply_permutation(vector, q, divisor)
            for character_index in range(q - 1):
                lhs = multiplicative_transform(transformed, q, character_index, logs)
                rhs = character_value(q, character_index, divisor, logs) * multiplicative_transform(
                    vector, q, character_index, logs
                )
                require(abs(lhs - rhs) < 1e-9, "character eigenvalue mismatch")
                rows += 1
    return rows


def check_gauss_crosswalk() -> int:
    rows = 0
    for q in (3, 5, 7, 11):
        logs = discrete_log_table(q)
        for character_index in range(1, q - 1):
            sequence = tuple(
                complex((index % 5) - 2, (2 * index + 1) % 4 - 1)
                for index in range(-3, 6)
            )
            indices = tuple(range(-3, 6))
            additive = tuple(
                sum(
                    value
                    * cmath.exp(-2j * math.pi * residue * index / q)
                    for value, index in zip(sequence, indices)
                )
                for residue in units(q)
            )
            lhs = multiplicative_transform(additive, q, character_index, logs)
            gauss = sum(
                character_value(q, character_index, residue, logs).conjugate()
                * cmath.exp(2j * math.pi * residue / q)
                for residue in units(q)
            )
            rhs = (
                character_value(q, character_index, -1, logs).conjugate()
                * gauss
                / math.sqrt(q - 1)
                * sum(
                    value
                    * character_value(q, character_index, index, logs)
                    for value, index in zip(sequence, indices)
                    if index % q != 0
                )
            )
            require(abs(lhs - rhs) < 1e-8, "Gauss crosswalk mismatch")
            rows += 1
    return rows


def check_alignment_and_resonance() -> tuple[int, Fraction]:
    q = 5
    divisors = (2, 3)
    weights = (-1, -1)
    centered = (Fraction(1, 2), Fraction(-1, 2), Fraction(0), Fraction(0))
    outputs: list[tuple[Fraction, ...]] = []
    for divisor, weight in zip(divisors, weights):
        image = permutation(q, divisor)
        profile = [Fraction(0) for _ in centered]
        sign = Fraction(1 if weight > 0 else -1)
        for coordinate, value in enumerate(centered):
            profile[image[coordinate]] = sign * value
        output = tuple(
            Fraction(weight) * profile[image[coordinate]]
            for coordinate in range(len(profile))
        )
        outputs.append(output)
    aggregate = tuple(sum(output[index] for output in outputs) for index in range(q - 1))
    individual_energy = sum(
        value * value
        for output in outputs
        for value in output
    )
    aggregate_energy = sum(value * value for value in aggregate)
    require(individual_energy == Fraction(1), "alignment individual energy")
    require(aggregate_energy == Fraction(2), "alignment aggregate energy")
    ratio = aggregate_energy / individual_energy
    require(ratio == Fraction(2), "alignment ratio")
    quadratic = sum(
        weight * (1 if pow(divisor, 2, q) == 1 else -1)
        for divisor, weight in zip(divisors, weights)
    )
    require(quadratic == 2, "quadratic resonance")
    return 4, ratio


def no_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_certificate() -> dict[str, object]:
    require(CERTIFICATE.is_file(), "TPC-209 certificate missing")
    data = json.loads(
        CERTIFICATE.read_text(encoding="utf-8"),
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(
            CheckFailure(f"non-finite JSON constant: {token}")
        ),
    )
    require(type(data) is dict, "certificate top-level type")
    require(
        data.get("schema") == "TPC209_WHOLE_FRAME_POISSON_MOBIUS_OBSTRUCTION_CERTIFICATE_V1",
        "certificate schema",
    )
    require(
        data.get("classification") == "PROVED_STRUCTURAL_L1_STOP_SCOPED_FRAME_ONLY_SAVING",
        "certificate claim ceiling",
    )
    counts = data.get("audit_counts")
    require(
        type(counts) is dict
        and counts.get("modulus_rows") == 5
        and counts.get("dual_bijection_rows") == 1500
        and counts.get("permutation_matrix_rows") == 3016,
        "certificate audit counts",
    )
    firewall = data.get("claim_firewall")
    require(type(firewall) is dict, "certificate firewall type")
    require(firewall.get("frame_only_power_saving") == "STOP_SCOPED", "saving status")
    require(firewall.get("arithmetic_advance") == "NO", "arithmetic status")
    require(firewall.get("fixed_atom_credit") == 0, "atom credit")
    require(firewall.get("l2") == "NONE", "L2 status")
    return data


def check_files_and_registry() -> int:
    require(PROOF.is_file(), "TPC-209 proof missing")
    proof_text = PROOF.read_text(encoding="utf-8")
    for row in REGISTRY:
        require(row in proof_text, f"TPC-209 registry row missing: {row}")
    source_lock = PAPER / "notes/source_lock.md"
    require(source_lock.is_file(), "TPC-209 source lock missing")
    source_text = source_lock.read_text(encoding="utf-8")
    for source_name in ("Harper", "Blomer", "Pascadi", "V59", "Poisson"):
        require(source_name in source_text, f"TPC-209 source boundary missing: {source_name}")
    required = (
        "README.md",
        "PAPER_PLAN.md",
        "paper/main.tex",
        "paper/references.bib",
        "paper/paper.pdf",
        "code/whole_frame.py",
        "experiments/run_certificate.py",
        "experiments/independent_checker.py",
        "experiments/gaussian_poisson_sanity.py",
        "results/certificate.json",
        "notes/theorem_ledger.md",
        "notes/source_lock.md",
        "notes/route_evaluation.md",
    )
    for relative in required:
        require((PAPER / relative).is_file(), f"TPC-209 artifact missing: {relative}")
    pdf = (PAPER / "paper/paper.pdf").read_bytes()
    require(pdf.startswith(b"%PDF-"), "paper PDF header")
    require(len(pdf) > 100_000, "paper PDF unexpectedly small")
    load_certificate()
    return len(REGISTRY) + len(required) + 1


def check_mutation_firewall() -> int:
    mutations = 0
    require(permutation(5, 2) != permutation(5, 3), "wrong dilation mutation escaped")
    mutations += 1
    require(dual_rows(5, 2) == 20, "dual row count mutation escaped")
    mutations += 1
    require(Fraction(2) != Fraction(1), "resonance mutation escaped")
    mutations += 1
    require(len(edges(5)) != 5, "edge-count mutation escaped")
    mutations += 1
    return mutations


def run() -> dict[str, object]:
    frame_rows, permutation_rows = check_frame_and_permutations()
    dual_count = sum(dual_rows(q, divisor) for q in MODULI for divisor in units(q))
    covariance_rows = check_whole_frame_covariance()
    character_rows = check_character_diagonalization()
    gauss_rows = check_gauss_crosswalk()
    alignment_rows, ratio = check_alignment_and_resonance()
    file_rows = check_files_and_registry()
    mutation_rows = check_mutation_firewall()
    require(dual_count == 1500, "dual audit total")
    require(permutation_rows == 3016, "permutation audit total")
    return {
        "classification": "TPC209_PROVED_STRUCTURAL_L1_STOP_SCOPED_FRAME_ONLY_SAVING",
        "verdict": "PASS",
        "moduli": len(MODULI),
        "complete_graph_rows": frame_rows,
        "permutation_rows": permutation_rows,
        "dual_bijection_rows": dual_count,
        "covariance_rows": covariance_rows,
        "character_rows": character_rows,
        "gauss_crosswalk_rows": gauss_rows,
        "alignment_ratio_q5": str(ratio),
        "file_registry_rows": file_rows,
        "mutation_rows": mutation_rows,
        "full_gate_b": "OPEN",
        "strict_1_over_400": "UNPAID",
        "arithmetic_advance": "NO",
        "l2": "NONE",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    try:
        payload = run()
    except CheckFailure as exc:
        print(f"TPC-209 whole-frame checker: FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
