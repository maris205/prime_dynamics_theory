#!/usr/bin/env python3
"""Read-only finite diagnostics, NOT an arithmetic/asymptotic certificate.

Run with python -B, or python -O -B. No files are written.
The Gaussian diagnostic kernel is fixed, Hermitian and non-even, but is not
substituted for the source's compactly supported smooth Fourier profile.
"""

import json
import math
from fractions import Fraction

import numpy as np


def require(condition, message):
    if not bool(condition):
        raise RuntimeError(message)


def primes(limit):
    flags = [True] * (limit + 1)
    if limit >= 0:
        flags[0] = False
    if limit >= 1:
        flags[1] = False
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p : limit + 1 : p] = [False] * (
                (limit - p * p) // p + 1
            )
    return [p for p, flag in enumerate(flags) if flag]


def projection_checks():
    count = 0
    for q in (3, 5, 7, 11, 13, 17):
        aq = Fraction(q, q - 1)
        for r in range(q):
            for s in range(q):
                full = Fraction(q * (r == s) - 1)
                unit = aq * ((q - 1) * (r == s) - 1) * (r != 0) * (s != 0)
                correction = Fraction(
                    (q * (r == 0) - 1) * (q * (s == 0) - 1), q - 1
                )
                require(full - unit == correction, "exact projection identity")
                count += 1
    return count


def emission_checks():
    rng = np.random.default_rng(9072026)
    max_error = 0.0
    packets = 0
    for q in (3, 5, 7, 11, 17):
        idx = np.arange(1, q)
        inv = np.array([pow(int(r), -1, q) for r in idx])
        phase = np.exp(2j * np.pi * idx[:, None] * idx[None, :] / q)
        inverse_phase = np.exp(2j * np.pi * idx[:, None] * inv[None, :] / q)
        kloosterman = phase @ inverse_phase.T
        for unused in range(4):
            f = rng.normal(size=q - 1) + 1j * rng.normal(size=q - 1)
            g = rng.normal(size=q - 1) + 1j * rng.normal(size=q - 1)
            cross = 0j
            expected_cross = np.dot(f - f.mean(), np.conj(g - g.mean()))
            for j in range(4):
                centered = f + 1j**j * g
                centered -= centered.mean()
                alpha = np.conj(phase) @ centered / q
                gamma = np.conj(inverse_phase) @ np.conj(centered) / q
                value = alpha @ kloosterman @ gamma
                energy = float(np.vdot(centered, centered).real)
                saturation = q * np.linalg.norm(alpha) * np.linalg.norm(gamma)
                error = max(abs(value - energy), abs(saturation - energy))
                require(error <= 1e-10 * (1 + energy), "emission/saturation")
                require(abs(alpha.sum()) <= 1e-11 * (1 + energy), "alpha centering")
                require(abs(gamma.sum()) <= 1e-11 * (1 + energy), "gamma centering")
                max_error = max(max_error, float(error))
                cross += 1j**j * value / 4
                packets += 1
            require(
                abs(cross - expected_cross) <= 1e-10 * (1 + abs(expected_cross)),
                "signed polarization",
            )
    return {"packets": packets, "max_abs_error": max_error}


def operator_checks():
    results = []
    for x in (512, 1000):
        qscale = x ** (1 / 3)
        height = x ** (21 / 32)
        shell = [
            p for p in primes(math.floor(2 * qscale) + 1)
            if p**3 > x and p**3 <= 8 * x
        ]
        idx = np.arange(x // 2 + 1, x + 1)
        diff = idx[:, None] - idx[None, :]
        arg = diff / height
        kernel = np.exp(-np.pi * arg**2 - 2j * np.pi * 0.37 * arg)
        offdiag = ~np.eye(len(idx), dtype=bool)
        actual = np.zeros_like(kernel)
        periodic = np.zeros_like(kernel)
        correction = np.zeros_like(kernel)
        undeleted = np.zeros_like(kernel)
        diagonal = np.zeros(len(idx))
        energy_direct = np.zeros(len(idx))
        energy_formula = np.zeros(len(idx))
        for q in shell:
            aq = q / (q - 1)
            units = idx % q != 0
            unit_pair = units[:, None] & units[None, :]
            congruent = diff % q == 0
            s = aq * ((q - 1) * congruent - 1) * unit_pair
            part = kernel * s * offdiag
            r = q * (~units).astype(int) - 1
            actual += part
            undeleted += kernel * s
            periodic += kernel * (q * congruent - 1)
            correction += kernel * (r[:, None] * r[None, :]) / (q - 1)
            diagonal += aq * (q - 2) * units
            energy_direct += np.sum(abs(part) ** 2, axis=1)
            sall = np.sum(abs(kernel) ** 2 * unit_pair * offdiag, axis=1)
            same = np.sum(abs(kernel) ** 2 * congruent * offdiag, axis=1)
            energy_formula += aq**2 * units * (sall + (q - 1) * (q - 3) * same)
        errors = {
            "hermitian": float(np.max(abs(actual - actual.conj().T))),
            "diagonal_deletion": float(
                np.max(abs(actual - undeleted + np.diag(diagonal)))
            ),
            "projection_decomposition": float(
                np.max(abs(actual - periodic + correction + np.diag(diagonal)))
            ),
            "row_energy": float(np.max(abs(energy_direct - energy_formula))),
        }
        require(max(errors.values()) < 1e-8, "physical-index finite identity")
        for name, matrix in (("undeleted", undeleted), ("correction", correction)):
            require(np.linalg.eigvalsh(matrix)[0] >= -1e-8, name + " finite PSD")
        eigenvalues = np.linalg.eigvalsh(actual)
        norm = float(max(abs(eigenvalues)))
        constant_rayleigh = complex(actual.sum() / len(idx))
        require(abs(constant_rayleigh.imag) < 1e-8, "real Rayleigh quotient")
        require(abs(constant_rayleigh.real) <= norm + 1e-8, "Rayleigh norm test")
        boundary = (idx <= x / 2 + height) | (idx >= x - height)
        rng = np.random.default_rng(x)
        beta = rng.normal(size=len(idx))
        lane = rng.normal(size=len(idx))
        beta_edge = beta * boundary
        lane_edge = lane * boundary
        beta_interior = beta - beta_edge
        lane_interior = lane - lane_edge
        boundary_delta = lane @ actual @ beta - lane_interior @ actual @ beta_interior
        boundary_expansion = lane_edge @ actual @ beta + lane_interior @ actual @ beta_edge
        boundary_bound = norm * (
            np.linalg.norm(lane_edge) * np.linalg.norm(beta)
            + np.linalg.norm(lane_interior) * np.linalg.norm(beta_edge)
        )
        require(abs(boundary_delta - boundary_expansion) < 1e-8, "boundary expansion")
        require(abs(boundary_delta) <= boundary_bound + 1e-8, "paid boundary norm bound")
        band_radius = math.floor(len(idx) * (1 / (4 * qscale) - 1 / height))
        frequencies = np.arange(-band_radius, band_radius + 1)
        fourier = np.exp(2j * np.pi * idx[:, None] * frequencies[None, :] / len(idx)) / math.sqrt(len(idx))
        real_columns = [np.ones(len(idx)) / math.sqrt(len(idx))]
        for j in range(1, band_radius + 1):
            angle = 2 * np.pi * j * idx / len(idx)
            real_columns.extend([
                math.sqrt(2 / len(idx)) * np.cos(angle),
                math.sqrt(2 / len(idx)) * np.sin(angle),
            ])
        real_basis = np.stack(real_columns, axis=1)
        require(np.max(abs(real_basis.T @ real_basis - np.eye(len(frequencies)))) < 1e-10, "real Fourier basis")
        require(np.max(abs(real_basis @ real_basis.T - fourier @ fourier.conj().T)) < 1e-10, "same complex band projector")
        real_compression = (real_basis.T @ undeleted @ real_basis).real
        trace_gap = abs(np.trace(real_compression) - np.trace(fourier.conj().T @ undeleted @ fourier))
        require(trace_gap < 1e-8, "realification preserves positive trace")
        band_eigenvalues, band_eigenvectors = np.linalg.eigh(real_compression)
        require(band_eigenvalues[0] >= -1e-8, "real compression PSD")
        cutoff = float(min(diagonal)) / 2
        real_negative = real_basis @ band_eigenvectors[:, band_eigenvalues <= cutoff]
        if real_negative.shape[1]:
            compressed_actual = real_negative.T @ actual @ real_negative
            # Only the real symmetric part governs real-vector quadratic forms.
            require(
                np.linalg.eigvalsh(compressed_actual.real)[-1] <= -cutoff + 1e-8,
                "real negative-subspace quadratic bound",
            )
        results.append({
            "x": x,
            "N": len(idx),
            "Q": qscale,
            "H": height,
            "primes": shell,
            "errors": errors,
            "zero_row_energies": int(np.count_nonzero(energy_direct == 0)),
            "operator_norm_diagnostic": norm,
            "constant_rayleigh_diagnostic": constant_rayleigh.real,
            "boundary_expansion_abs_error": float(abs(boundary_delta - boundary_expansion)),
            "boundary_vectors_scope": "arbitrary real diagnostic vectors, not literal lanes",
            "realification_trace_abs_error": float(trace_gap),
            "real_cutoff_subspace_dimension_diagnostic": int(real_negative.shape[1]),
            "real_cutoff_threshold_diagnostic": cutoff,
        })
    return results


def one_sided_gram_checks():
    results = []
    for q in (3, 5, 7, 11, 17, 31):
        idx = np.arange(1, q)
        inv = np.array([pow(int(r), -1, q) for r in idx])
        phase = np.exp(2j * np.pi * idx[:, None] * idx[None, :] / q)
        inverse_phase = np.exp(2j * np.pi * idx[:, None] * inv[None, :] / q)
        kernel = phase @ inverse_phase.T
        expected = q**2 * np.eye(q - 1) - (q + 1) * np.ones((q - 1, q - 1))
        error = float(np.max(abs(kernel @ kernel.conj().T - expected)))
        require(error < 1e-8, "complete Kloosterman Gram")
        require(np.max(abs(kernel.sum(axis=0) - 1)) < 1e-10, "Kloosterman column sum")
        require(np.max(abs(kernel.sum(axis=1) - 1)) < 1e-10, "Kloosterman row sum")
        a = np.zeros(q - 1, dtype=complex)
        a[:2] = (1 / math.sqrt(2), -1 / math.sqrt(2))
        gamma = kernel.conj().T @ a / q
        value = np.conj(a) @ kernel @ gamma
        require(abs(gamma.sum()) < 1e-10, "centered right extremizer")
        require(abs(np.linalg.norm(gamma) - 1) < 1e-10, "unit right extremizer")
        require(abs(value - q) < 1e-9, "two-short-index/full-array norm saturation")
        results.append({"q": q, "gram_abs_error": error, "saturation_abs_error": float(abs(value - q))})
    return results


def smooth_partition_checks():
    cases = 0
    max_mass_error = 0.0
    max_boundary_labels = 0
    for a in (-1.75, 0.0, 0.25, 2.0, 7.125):
        for length in (0.4, 1.0, 3.25, 11.5):
            b = a + length
            for height in (0.25, 0.7, 1.0, 2.5, 8.0):
                labels = np.arange(math.floor(2 * a / height) - 3, math.ceil(2 * b / height) + 4)
                points = np.linspace(a, b, 101)
                arg = points[:, None] / height - labels[None, :] / 2
                values = np.zeros_like(arg)
                inside = abs(arg) < 0.5
                values[inside] = np.exp(-1 / (1 - 4 * arg[inside] ** 2))
                denom = values.sum(axis=1)
                require(np.min(denom) >= math.exp(-4 / 3) - 1e-12, "positive periodic denominator")
                weights = values / denom[:, None]
                error = float(np.max(abs(weights.sum(axis=1) - 1)))
                require(error < 1e-12, "smooth partition exact mass diagnostic")
                left = (labels - 1) * height / 2
                right = (labels + 1) * height / 2
                intersect = (left <= b) & (right >= a)
                interior = (left > a) & (right < b)
                boundary = intersect & ~interior
                require(np.count_nonzero(boundary) <= 6, "boundary labels")
                edge_weight = weights[:, boundary].sum(axis=1)
                beyond_edge = (points > a + height + 1e-10) & (points < b - height - 1e-10)
                require(np.all(edge_weight[beyond_edge] == 0), "boundary support collar")
                max_mass_error = max(max_mass_error, error)
                max_boundary_labels = max(max_boundary_labels, int(np.count_nonzero(boundary)))
                cases += 1
    require(Fraction(1, 3) + Fraction(133, 400) - Fraction(21, 32) == Fraction(23, 2400), "dual radius exponent")
    require((1 - Fraction(21, 32)) / 2 == Fraction(11, 64), "boundary saving exponent")
    require(Fraction(11, 64) > Fraction(1, 96), "boundary budget versus critical saving")
    return {"cases": cases, "sampled_points": 101 * cases, "max_mass_error": max_mass_error, "max_boundary_labels": max_boundary_labels}


def growing_rank_sufficient_inequalities():
    """One-scale rational checks, not a uniform asymptotic threshold."""
    qscale = 2000
    x = qscale**3
    size = x // 2
    shell = [q for q in primes(2 * qscale) if q > qscale]
    m1 = sum(shell)
    diagonal_lower = sum(
        (Fraction(q * (q - 2), q - 1) for q in shell), Fraction(0)
    ) - 4 * qscale
    # pi < 22/7 and log(2) > 2/3 give deliberately conservative rational bounds.
    c0_upper = Fraction(29, 7) ** 2
    log_lower = Fraction(2, 3) * (qscale.bit_length() - 1)
    tau_upper = qscale**2 / log_lower
    trace_ratio_upper = (
        2 * c0_upper * (1 + Fraction(2 * qscale, size)) * m1 / diagonal_lower
    )
    require(diagonal_lower >= tau_upper, "one-scale uniform diagonal sufficient inequality")
    require(trace_ratio_upper < 35, "one-scale spectral-cutoff sufficient inequality")
    # Isolate H=x^(21/32) with exact integer powers, without an irrational floor.
    target = x**21
    low, high = 0, 1 << ((target.bit_length() + 31) // 32)
    while high - low > 1:
        middle = (low + high) // 2
        if middle**32 <= target:
            low = middle
        else:
            high = middle
    require(low**32 <= target < high**32, "exact physical height isolation")
    require(low >= 8 * qscale, "one-scale height prerequisite")
    j_lower = math.floor(Fraction(size, 4 * qscale) - Fraction(size, low))
    j_upper = math.floor(Fraction(size, 4 * qscale) - Fraction(size, high))
    require(j_lower == j_upper, "exact Fourier-band integer isolation")
    dimension = 2 * j_lower + 1
    require(36 <= dimension < size, "one-scale band dimension prerequisite")
    return {
        "scope": "ONE_SCALE_SUFFICIENT_INEQUALITIES_ONLY_NOT_UNIFORM_THRESHOLD",
        "x": x,
        "Q": qscale,
        "N": size,
        "shell_prime_count": len(shell),
        "H_floor_exact": low,
        "J_exact": j_lower,
        "d_exact": dimension,
        "k_exact": dimension - 35,
        "C0_upper_rational": str(c0_upper),
        "log_Q_lower_rational": str(log_lower),
        "D_star_at_least_tau_upper": True,
        "trace_cutoff_ratio_strictly_below_35": True,
        "physical_matrix_materialized": False,
    }


def semiprime_checks():
    counts = {}
    for x in (1000, 10000, 100000):
        plist = primes(x)
        eligible = [p for p in plist if p**5 > x**2 and p**20 <= x**9]
        products = set()
        for p in eligible:
            for r in plist:
                if 2 * p * r <= x:
                    continue
                if p * r > x:
                    break
                require(p < r, "distinct ordered prime factors")
                require(p**400 > x**133 and r**400 > x**133, "exact U cutoff")
                require(p * r not in products, "semiprime unique counting")
                products.add(p * r)
        counts[str(x)] = len(products)
    for exponent in range(101):
        require(
            (exponent + 1) ** 2 <= math.comb(exponent + 3, 3),
            "divisor square inequality",
        )
    return {"semiprime_counts": counts, "divisor_exponent_cases": 101}


def main():
    report = {
        "scope": "FINITE_DIAGNOSTICS_ONLY_NO_ARITHMETIC_OR_ASYMPTOTIC_CREDIT",
        "files_written": [],
        "exact_projection_entries": projection_checks(),
        "emission": emission_checks(),
        "operators": operator_checks(),
        "lane_arithmetic_checks": semiprime_checks(),
        "one_sided_gram": one_sided_gram_checks(),
        "smooth_partition": smooth_partition_checks(),
        "growing_rank_sufficient_inequalities": growing_rank_sufficient_inequalities(),
    }
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
