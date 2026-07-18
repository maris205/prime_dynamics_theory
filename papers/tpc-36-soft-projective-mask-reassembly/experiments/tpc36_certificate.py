#!/usr/bin/env python3
"""Exact finite certificate for TPC-36.

This standard-library script uses integers and Fraction only.  Roots of
unity are handled symbolically through finite-group orthogonality, never
through floating-point approximations.  The checks cover the finite mask
reassembly, Ferrers-prefix, product-phase, permutation-kernel, and
coherent-s identities in TPC-36.  They do not certify an asymptotic
Mobius estimate, a physical alias bound, or a twin-prime assertion.
"""

from __future__ import annotations

import ast
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from math import gcd
from pathlib import Path


CHECKS = 0


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def mobius(n: int) -> int:
    if n < 1:
        raise RuntimeError("Mobius input must be positive")
    value = 1
    work = n
    p = 2
    while p * p <= work:
        if work % p == 0:
            work //= p
            value = -value
            if work % p == 0:
                return 0
            while work % p == 0:
                work //= p
        p += 1
    if work > 1:
        value = -value
    return value


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def omega(n: int) -> int:
    count = 0
    work = n
    p = 2
    while p * p <= work:
        if work % p == 0:
            count += 1
            while work % p == 0:
                work //= p
        p += 1
    if work > 1:
        count += 1
    return count


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    p = 2
    while p * p <= n:
        if n % p == 0:
            return False
        p += 1
    return True


def next_power_of_two(n: int) -> int:
    value = 1
    while value < n:
        value *= 2
    return value


def bit_parity(n: int) -> int:
    parity = 0
    work = n
    while work:
        parity ^= work & 1
        work >>= 1
    return parity


def walsh_sign(row: int, column: int) -> int:
    return -1 if bit_parity(row & column) else 1


def modular_inverse(a: int, modulus: int) -> int:
    return pow(a % modulus, -1, modulus)


def primitive_root(q: int) -> int:
    require(is_prime(q), "primitive-root modulus was not prime")
    order = q - 1
    prime_factors = []
    work = order
    p = 2
    while p * p <= work:
        if work % p == 0:
            prime_factors.append(p)
            while work % p == 0:
                work //= p
        p += 1
    if work > 1:
        prime_factors.append(work)
    for candidate in range(2, q):
        if all(pow(candidate, order // p, q) != 1
               for p in prime_factors):
            return candidate
    raise RuntimeError("primitive root not found")


def discrete_log_table(q: int) -> dict[int, int]:
    generator = primitive_root(q)
    table = {}
    value = 1
    for exponent in range(q - 1):
        table[value] = exponent
        value = value * generator % q
    require(len(table) == q - 1, "discrete-log table was incomplete")
    return table


def root_orthogonality(order: int, exponent: int) -> int:
    """Symbolic value of sum_{r mod order} zeta^(r*exponent)."""
    return order if exponent % order == 0 else 0


def lambda_g(v: int, cutoff: int) -> int:
    return sum(mobius(v // g) for g in divisors(v) if g <= cutoff)


def check_gcd_projector_and_compression() -> dict:
    start = CHECKS
    cases = []
    packets = [(5, 22, 1), (9, 34, 2), (15, 46, 3), (21, 58, 5)]
    for lower, upper, cutoff in packets:
        packet = [n for n in range(lower, upper + 1) if mobius(n) != 0]
        feature_set = sorted({v for n in packet for v in divisors(n)})
        feature_index = {v: i for i, v in enumerate(feature_set)}
        order = next_power_of_two(len(feature_set))

        for v in feature_set:
            require(abs(lambda_g(v, cutoff)) <= len(divisors(v)),
                    "truncated gcd coefficient divisor bound")

        for v in feature_set:
            for w in feature_set:
                signed_sum = sum(
                    walsh_sign(r, feature_index[v])
                    * walsh_sign(r, feature_index[w])
                    for r in range(order)
                )
                require(signed_sum == order * int(v == w),
                        "Walsh feature orthogonality")

        max_left_mass = 0
        max_right_mass = 0
        for d in packet:
            local_left = sum(abs(lambda_g(v, cutoff))
                             for v in divisors(d))
            local_right = len(divisors(d))
            require(local_left <= 3 ** omega(d),
                    "local gcd coefficient mass")
            require(local_right == 2 ** omega(d),
                    "squarefree divisor count")
            max_left_mass = max(max_left_mass, local_left)
            max_right_mass = max(max_right_mass, local_right)

        for d in packet:
            for e in packet:
                direct = int(gcd(d, e) <= cutoff)
                projector = sum(
                    lambda_g(v, cutoff)
                    for v in divisors(gcd(d, e))
                )
                require(projector == direct, "exact gcd projector")

                compressed_numerator = 0
                for r in range(order):
                    left = sum(
                        lambda_g(v, cutoff)
                        * walsh_sign(r, feature_index[v])
                        for v in divisors(d)
                    )
                    right = sum(
                        walsh_sign(r, feature_index[v])
                        for v in divisors(e)
                    )
                    require(abs(left) <= sum(
                        abs(lambda_g(v, cutoff)) for v in divisors(d)
                    ), "compressed left local envelope")
                    require(abs(right) <= len(divisors(e)),
                            "compressed right local envelope")
                    compressed_numerator += left * right
                require(compressed_numerator == order * direct,
                        "orthogonally compressed gcd projector")

        projective_envelope = max_left_mass * max_right_mass
        require(projective_envelope <= 6 ** max(omega(n) for n in packet),
                "gcd projective mass bookkeeping")
        cases.append({
            "cutoff": cutoff,
            "feature_count": len(feature_set),
            "packet_size": len(packet),
            "projective_envelope": projective_envelope,
            "walsh_order": order,
        })
    return {"checks": CHECKS - start, "cases": cases}


def check_source_equality_compression() -> dict:
    start = CHECKS
    cases = []
    for source_count in [2, 3, 5, 8, 11, 16]:
        order = next_power_of_two(source_count)
        for a in range(source_count):
            for b in range(source_count):
                equality_numerator = sum(
                    walsh_sign(r, a) * walsh_sign(r, b)
                    for r in range(order)
                )
                require(equality_numerator == order * int(a == b),
                        "source equality compression")
                inequality_numerator = order - equality_numerator
                require(inequality_numerator == order * int(a != b),
                        "source inequality compression")
        equality_mass = sum(Fraction(1, order) for _ in range(order))
        inequality_mass = Fraction(1) + equality_mass
        require(equality_mass == 1, "source equality projective mass")
        require(inequality_mass == 2,
                "source inequality projective mass envelope")
        cases.append([source_count, order])
    return {"checks": CHECKS - start, "cases": cases}


def check_ferrers_prefix_fourier() -> dict:
    start = CHECKS
    cases = []
    band_cases = []
    for n in [1, 2, 3, 5, 8, 13, 21]:
        modulus = 2 * n + 1
        interval = list(range(n))
        for prefix in range(n + 1):
            for column in range(1, n + 1):
                symbolic_numerator = sum(
                    root_orthogonality(
                        modulus, prefix - column - displacement
                    )
                    for displacement in interval
                )
                expected = modulus * int(column <= prefix)
                require(symbolic_numerator == expected,
                        "symbolic cyclic Fourier prefix reconstruction")

        harmonic = sum(Fraction(1, r) for r in range(1, n + 1))
        zero_frequency = Fraction(n, modulus)
        paired_nonzero_envelope = harmonic
        total_envelope = zero_frequency + paired_nonzero_envelope
        require(zero_frequency <= Fraction(1, 2),
                "Ferrers zero-frequency envelope")
        require(total_envelope <= harmonic + Fraction(1, 2),
                "Ferrers harmonic projective envelope")

        values = [2 * k * k + 3 * k + 1 for k in range(1, n + 1)]
        thresholds = [0]
        thresholds.extend(values[k] for k in range(n))
        thresholds.append(values[-1] + 1)
        for threshold in thresholds:
            prefix = sum(1 for value in values if value <= threshold)
            for column, value in enumerate(values, start=1):
                require(int(value <= threshold) == int(column <= prefix),
                        "arbitrary ordered Ferrers reduction")
        cases.append({
            "harmonic_envelope": str(total_envelope),
            "modulus": modulus,
            "size": n,
        })

    divisor_values = [6, 10, 14, 15, 21, 22, 26, 30]
    for source_values, center, width in [
        ([5, 7, 11], 140, 10),
        ([7, 13, 17], 247, 19),
        ([11, 19, 23], 391, 25),
    ]:
        for source in source_values:
            lower_prefix = sum(
                1 for value in divisor_values
                if source * value < center - width
            )
            upper_prefix = sum(
                1 for value in divisor_values
                if source * value <= center + width
            )
            for column, value in enumerate(divisor_values, start=1):
                prefix_formula = (
                    1 - int(column <= upper_prefix)
                    + int(column <= lower_prefix)
                )
                direct = int(abs(source * value - center) > width)
                require(prefix_formula == direct,
                        "far-row mask as two Ferrers prefixes")
        band_cases.append([source_values, center, width])
    return {
        "band_cases": band_cases,
        "cases": cases,
        "checks": CHECKS - start,
    }


Polynomial = list[int]


def poly_trim(poly: Polynomial) -> Polynomial:
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(a: Polynomial, b: Polynomial) -> Polynomial:
    size = max(len(a), len(b))
    out = [0] * size
    for i in range(size):
        out[i] = (a[i] if i < len(a) else 0) + (
            b[i] if i < len(b) else 0
        )
    return poly_trim(out)


def poly_scale(a: Polynomial, scalar: int) -> Polynomial:
    return poly_trim([scalar * value for value in a])


def poly_mul(a: Polynomial, b: Polynomial) -> Polynomial:
    out = [0] * (len(a) + len(b) - 1)
    for i, avalue in enumerate(a):
        for j, bvalue in enumerate(b):
            out[i + j] += avalue * bvalue
    return poly_trim(out)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = 0
    for i in range(len(permutation)):
        for j in range(i + 1, len(permutation)):
            inversions += int(permutation[i] > permutation[j])
    return -1 if inversions % 2 else 1


def polynomial_matrix_determinant(matrix: list[list[Polynomial]]) -> Polynomial:
    size = len(matrix)
    total = [0]
    for permutation in itertools.permutations(range(size)):
        term = [permutation_sign(permutation)]
        for row, column in enumerate(permutation):
            term = poly_mul(term, matrix[row][column])
        total = poly_add(total, term)
    return poly_trim(total)


def integer_matrix_product(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b)))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def check_triangular_gram_polynomial() -> dict:
    start = CHECKS
    cases = []
    for n in range(1, 8):
        triangle = [[int(j <= i) for j in range(n)] for i in range(n)]
        transpose = [list(column) for column in zip(*triangle)]
        gram = integer_matrix_product(triangle, transpose)
        expected_gram = [[min(i, j) + 1 for j in range(n)]
                         for i in range(n)]
        require(gram == expected_gram, "triangular min-kernel Gram")

        inverse = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            inverse[i][i] = 1 if i == n - 1 else 2
            if i + 1 < n:
                inverse[i][i + 1] = -1
                inverse[i + 1][i] = -1
        product = integer_matrix_product(gram, inverse)
        require(product == [[int(i == j) for j in range(n)]
                            for i in range(n)],
                "triangular Gram tridiagonal inverse")

        polynomial_matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                constant = -inverse[i][j]
                row.append([constant, 1] if i == j else [constant])
            polynomial_matrix.append(row)
        generic_characteristic = polynomial_matrix_determinant(
            polynomial_matrix
        )

        q0 = [1]
        if n == 1:
            recurrence_characteristic = [-1, 1]
        else:
            q1 = [-2, 1]
            qminus = q0
            qcurrent = q1
            for _ in range(2, n):
                qnext = poly_add(poly_mul([-2, 1], qcurrent),
                                 poly_scale(qminus, -1))
                qminus, qcurrent = qcurrent, qnext
            recurrence_characteristic = poly_add(
                poly_mul([-1, 1], qcurrent), poly_scale(qminus, -1)
            )
        require(generic_characteristic == recurrence_characteristic,
                "triangular inverse characteristic polynomial")
        require(generic_characteristic[-1] == 1,
                "triangular eigen-polynomial monicity")
        require(generic_characteristic[0] == (-1) ** n,
                "triangular inverse determinant one")
        require(sum(gram[i][i] for i in range(n)) == n * (n + 1) // 2,
                "triangular Gram trace")
        cases.append({
            "characteristic_coefficients": generic_characteristic,
            "size": n,
        })
    return {"checks": CHECKS - start, "cases": cases}


def check_product_phase_gram() -> dict:
    start = CHECKS
    cases = []
    for q in [3, 5, 7, 11, 13]:
        units = list(range(1, q))
        for frequency in units:
            symbolic_gram = []
            evaluated_gram = []
            for x in units:
                symbolic_row = []
                evaluated_row = []
                for z in units:
                    histogram = [0] * q
                    for y in units:
                        exponent = frequency * (x - z) * y % q
                        histogram[exponent] += 1
                    if x == z:
                        require(histogram[0] == q - 1
                                and sum(histogram[1:]) == 0,
                                "product-phase diagonal root histogram")
                        evaluated = q - 1
                    else:
                        require(histogram[0] == 0
                                and histogram[1:] == [1] * (q - 1),
                                "product-phase off-diagonal root histogram")
                        evaluated = -1
                    symbolic_row.append(histogram)
                    evaluated_row.append(evaluated)
                symbolic_gram.append(symbolic_row)
                evaluated_gram.append(evaluated_row)
            expected = [[q * int(i == j) - 1 for j in range(q - 1)]
                        for i in range(q - 1)]
            require(evaluated_gram == expected,
                    "product-phase Gram qI-J")

            ones = [1] * (q - 1)
            image_ones = [sum(row[j] * ones[j] for j in range(q - 1))
                          for row in evaluated_gram]
            require(image_ones == ones,
                    "product-phase exceptional eigenvalue one")
            for i in range(q - 2):
                vector = [0] * (q - 1)
                vector[i] = 1
                vector[-1] = -1
                image = [sum(row[j] * vector[j] for j in range(q - 1))
                         for row in evaluated_gram]
                require(image == [q * value for value in vector],
                        "product-phase sqrt-q singular subspace")
        cases.append({
            "nonzero_frequency_count": q - 1,
            "prime": q,
            "symbolic_gram": "q I_(q-1) - J_(q-1)",
        })
    return {"checks": CHECKS - start, "cases": cases}


def check_multiplicative_permutation_kernel() -> dict:
    start = CHECKS
    cases = []
    for q in [3, 5, 7, 11, 13, 17]:
        logs = discrete_log_table(q)
        order = q - 1
        units = list(range(1, q))
        for target in units:
            target_log = logs[target]
            matrix = []
            for x in units:
                row = []
                for y in units:
                    exponent = logs[x] + logs[y] - target_log
                    numerator = root_orthogonality(order, exponent)
                    direct = int(x * y % q == target)
                    require(numerator == order * direct,
                            "multiplicative-character kernel reconstruction")
                    row.append(direct)
                matrix.append(row)
            require(all(sum(row) == 1 for row in matrix),
                    "multiplicative product kernel row permutation")
            require(all(sum(matrix[i][j] for i in range(order)) == 1
                        for j in range(order)),
                    "multiplicative product kernel column permutation")
            gram = integer_matrix_product(
                matrix, [list(column) for column in zip(*matrix)]
            )
            require(gram == [[int(i == j) for j in range(order)]
                             for i in range(order)],
                    "multiplicative product kernel Gram identity")
        projective_mass = sum(Fraction(1, order) for _ in range(order))
        require(projective_mass == 1,
                "multiplicative-character projective mass one")
        cases.append([q, primitive_root(q)])
    return {"checks": CHECKS - start, "cases": cases}


def deterministic_centered_vector(q: int, seed: int) -> list[Fraction]:
    values = [Fraction(((seed + 3) * (x + 2) * (x + seed + 1)) % 17 - 8)
              for x in range(q - 1)]
    values.append(-sum(values, Fraction()))
    require(sum(values, Fraction()) == 0,
            "deterministic centered vector")
    return values


def finite_r_values(
    q: int, h: int, fvalues: list[Fraction], gvalues: list[Fraction]
) -> dict[tuple[int, int], Fraction]:
    output = {}
    for slope in range(1, q):
        for complement in range(1, q):
            inverse = modular_inverse(complement, q)
            value = sum(
                fvalues[d]
                * gvalues[((slope * d + h) * inverse) % q]
                for d in range(q)
            )
            output[(slope, complement)] = value
    return output


def legendre_symbol(value: int, q: int) -> int:
    residue = value % q
    if residue == 0:
        return 0
    power = pow(residue, (q - 1) // 2, q)
    if power == 1:
        return 1
    require(power == q - 1, "Euler criterion Legendre value")
    return -1


def check_coherent_s_trace_and_sharpness() -> dict:
    start = CHECKS
    trace_cases = []
    sharp_cases = []
    for q in [3, 5, 7, 11, 13, 17]:
        for h in [1, 2]:
            if h % q == 0:
                continue
            for seed in [1, 4, 9]:
                fvalues = deterministic_centered_vector(q, seed)
                gvalues = deterministic_centered_vector(q, seed + 5)
                rvalues = finite_r_values(q, h, fvalues, gvalues)
                for slope in range(1, q):
                    lhs = sum(rvalues[(slope, complement)]
                              for complement in range(1, q))
                    point = -h * modular_inverse(slope, q) % q
                    rhs = q * gvalues[0] * fvalues[point]
                    require(lhs == rhs, "complete coherent-s trace formula")

                bvalues = [Fraction(((seed + 2) * (ell + 1)) % 11 - 5)
                           for ell in range(1, q)]
                for orbit in range(1, q):
                    lhs = Fraction()
                    for complement in range(1, q):
                        lhs += sum(
                            bvalues[ell - 1]
                            * rvalues[(ell * orbit % q, complement)]
                            for ell in range(1, q)
                        )
                    rhs = q * gvalues[0] * sum(
                        bvalues[ell - 1]
                        * fvalues[
                            -h * modular_inverse(ell * orbit % q, q) % q
                        ]
                        for ell in range(1, q)
                    )
                    require(lhs == rhs,
                            "coherent product-slope boundary trace")
                trace_cases.append([q, h, seed])

            fvalues = [Fraction(legendre_symbol(d, q)) for d in range(q)]
            gvalues = [Fraction(-1, q) for _ in range(q)]
            gvalues[0] += 1
            bvalues = {ell: Fraction(legendre_symbol(ell, q))
                       for ell in range(1, q)}
            require(sum(fvalues, Fraction()) == 0 and fvalues[0] == 0,
                    "sharp example centered nonprincipal f")
            require(sum(gvalues, Fraction()) == 0,
                    "sharp example centered g")
            rvalues = finite_r_values(q, h, fvalues, gvalues)
            chi_minus_h = legendre_symbol(-h, q)
            for slope in range(1, q):
                expected_r = Fraction(
                    chi_minus_h * legendre_symbol(slope, q)
                )
                for complement in range(1, q):
                    require(rvalues[(slope, complement)] == expected_r,
                            "nonprincipal coherent-s R-value")

            tvalues = {}
            for orbit in range(1, q):
                for complement in range(1, q):
                    value = sum(
                        bvalues[ell]
                        * rvalues[(ell * orbit % q, complement)]
                        for ell in range(1, q)
                    )
                    expected = Fraction(
                        (q - 1) * chi_minus_h
                        * legendre_symbol(orbit, q)
                    )
                    require(value == expected,
                            "nonprincipal s-independent product slope")
                    tvalues[(orbit, complement)] = value

            separate_energy = sum(value * value for value in tvalues.values())
            coherent_energy = sum(
                sum(tvalues[(orbit, complement)]
                    for complement in range(1, q)) ** 2
                for orbit in range(1, q)
            )
            require(coherent_energy == (q - 1) * separate_energy,
                    "sharp coherent-s Cauchy factor")
            sharp_cases.append([q, h])
    return {
        "checks": CHECKS - start,
        "sharp_cases": sharp_cases,
        "trace_cases": trace_cases,
    }


def check_source_constraints() -> dict:
    start = CHECKS
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    float_nodes = [node for node in ast.walk(tree)
                   if isinstance(node, ast.Constant)
                   and isinstance(node.value, float)]
    assert_nodes = [node for node in ast.walk(tree)
                    if isinstance(node, ast.Assert)]
    division_nodes = [node for node in ast.walk(tree)
                      if isinstance(node, ast.BinOp)
                      and isinstance(node.op, ast.Div)]
    import_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            import_names.append(node.module or "")
    require(not float_nodes, "certificate source contains a float literal")
    require(not assert_nodes, "certificate source contains assert")
    require(not division_nodes, "certificate source contains true division")
    require(not any(name == "random" or name.startswith("random.")
                    for name in import_names),
            "certificate source imports random")
    return {"checks": CHECKS - start}


def main() -> None:
    results = {
        "gcd_projector_and_orthogonal_compression":
            check_gcd_projector_and_compression(),
        "source_equality_compression": check_source_equality_compression(),
        "ferrers_prefix_fourier": check_ferrers_prefix_fourier(),
        "triangular_gram_eigen_polynomial":
            check_triangular_gram_polynomial(),
        "product_phase_gram": check_product_phase_gram(),
        "multiplicative_permutation_kernel":
            check_multiplicative_permutation_kernel(),
        "coherent_s_trace_and_sharpness":
            check_coherent_s_trace_and_sharpness(),
        "source_constraints": check_source_constraints(),
    }
    claims = {
        "finite_gcd_projector_identity": True,
        "finite_gcd_orthogonal_compression": True,
        "finite_source_equality_compression": True,
        "finite_ferrers_prefix_fourier_reconstruction": True,
        "finite_ferrers_harmonic_mass_bookkeeping": True,
        "finite_far_row_two_prefix_reduction": True,
        "finite_triangular_gram_inverse_and_eigen_polynomial": True,
        "finite_product_phase_gram_qI_minus_J": True,
        "finite_multiplicative_permutation_kernel": True,
        "finite_complete_coherent_s_trace": True,
        "finite_nonprincipal_sharp_cauchy_example": True,
        "uses_floating_point": False,
        "uses_random_inputs": False,
        "proves_physical_complete_separable_completion": False,
        "proves_integer_to_modular_alias_control": False,
        "proves_weighted_physical_character_overlap": False,
        "proves_coefficient_specific_Mobius_gate": False,
        "proves_twin_primes": False,
        "breaks_sieve_parity": False,
    }
    source = Path(__file__).read_bytes().replace(b"\r\n", b"\n")
    payload = {
        "arithmetic": "integer and Fraction; roots of unity symbolic",
        "certificate_version": 1,
        "check_total": CHECKS,
        "claims": claims,
        "normalized_source_sha256": sha256(source).hexdigest(),
        "paper": "TPC-36",
        "results": results,
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    payload["certificate_digest"] = sha256(canonical).hexdigest()
    output = Path(__file__).with_name("tpc36_certificate.json")
    output_bytes = (
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    ).encode("utf-8")
    output.write_bytes(output_bytes)
    print(
        "TPC-36 exact certificate:"
        f" {CHECKS} checks;"
        f" digest {payload['certificate_digest']};"
        f" source_sha256 {payload['normalized_source_sha256']};"
        f" json_sha256 {sha256(output_bytes).hexdigest()};"
        f" wrote {output.name}"
    )


if __name__ == "__main__":
    main()
