#!/usr/bin/env python3
"""Deterministic finite regression for the literal TPC-93 export.

This is an executable consistency certificate, not evidence for an
asymptotic cancellation theorem.  It checks the exact finite identities
used in the paper:

* both TPC-33 polarizations and the source <-> projector-child inverse;
* row-gcd projector multiplicity and moving Mobius-sign reassembly;
* physical determinant orientation and phase-compatible exact content;
* progression resolution, Bh -> h determinant reduction, extracted
  Mobius factor, and the resolved phase.

Only the Python standard library is required.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from itertools import product


H0 = 1
QMOD = 1009
TWOPI = 2.0 * math.pi


def divisors(n: int) -> list[int]:
    out: list[int] = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            if d * d != n:
                out.append(n // d)
        d += 1
    return sorted(out)


def mobius(n: int) -> int:
    if n <= 0:
        raise ValueError("mobius expects a positive integer")
    value = 1
    p = 2
    residual = n
    while p * p <= residual:
        if residual % p == 0:
            residual //= p
            value = -value
            if residual % p == 0:
                return 0
            while residual % p == 0:
                residual //= p
        p += 1
    if residual > 1:
        value = -value
    return value


def is_squarefree(n: int) -> bool:
    return mobius(n) != 0


def lambda_cutoff(v: int, cutoff: int) -> int:
    return sum(mobius(v // g) for g in divisors(v) if g <= cutoff)


def echar(modulus: int, numerator: int) -> complex:
    return cmath.exp(1j * TWOPI * (numerator % modulus) / modulus)


def assert_close(left: complex, right: complex, label: str) -> None:
    if abs(left - right) > 2.0e-10:
        raise AssertionError(f"{label}: {left!r} != {right!r}")


@dataclass(frozen=True)
class Row:
    ell: int
    d: int

    @property
    def m(self) -> int:
        return self.ell * self.d


@dataclass(frozen=True)
class Source:
    side: str
    moving: Row
    opposite: Row
    j: int
    u: int
    sigma: int


@dataclass(frozen=True)
class Child:
    side: str
    moving_ell: int
    opposite: Row
    j: int
    sigma: int
    v: int
    d0: int
    u0: int
    t: int
    component: str

    @property
    def a(self) -> int:
        return self.moving_ell * self.j * self.v

    def D(self, t: int | None = None) -> int:
        parameter = self.t if t is None else t
        return self.d0 + self.sigma * parameter

    def U(self, t: int | None = None) -> int:
        parameter = self.t if t is None else t
        return self.u0 + self.a * parameter

    @property
    def moving_m(self) -> int:
        return self.moving_ell * self.v * self.D()

    @property
    def epsilon(self) -> int:
        return 1 if self.side == "L" else -1


def physical_component(moving_m: int, opposite_m: int, gap_cut: int = 2) -> str:
    gap = moving_m - opposite_m
    if abs(gap) <= gap_cut:
        raise ValueError("source lies in the deleted near-diagonal interval")
    return "below" if gap < -gap_cut else "above"


def source_to_children(source: Source) -> list[Child]:
    moving_d = source.moving.d
    common = math.gcd(moving_d, source.opposite.d)
    component = physical_component(source.moving.m, source.opposite.m)
    children: list[Child] = []
    for v in divisors(common):
        a = source.moving.ell * source.j * v
        if math.gcd(a, source.sigma) != 1:
            raise AssertionError("target primitivity did not make the slope invertible")
        if source.sigma == 1:
            d0 = 0
        else:
            d0 = (-H0 * pow(a, -1, source.sigma)) % source.sigma
        quotient_d = source.moving.d // v
        if (quotient_d - d0) % source.sigma != 0:
            raise AssertionError("source does not land in its canonical residue")
        t = (quotient_d - d0) // source.sigma
        u0_numerator = a * d0 + H0
        if u0_numerator % source.sigma != 0:
            raise AssertionError("nonintegral affine origin")
        child = Child(
            side=source.side,
            moving_ell=source.moving.ell,
            opposite=source.opposite,
            j=source.j,
            sigma=source.sigma,
            v=v,
            d0=d0,
            u0=u0_numerator // source.sigma,
            t=t,
            component=component,
        )
        children.append(child)
    return children


def child_to_source(child: Child) -> Source:
    moving = Row(child.moving_ell, child.v * child.D())
    return Source(
        side=child.side,
        moving=moving,
        opposite=child.opposite,
        j=child.j,
        u=child.U(),
        sigma=child.sigma,
    )


def generate_rows() -> list[Row]:
    rows: list[Row] = []
    for ell, d in product((2, 3, 5, 7, 11), range(2, 31)):
        if is_squarefree(d) and math.gcd(ell, d) == 1:
            rows.append(Row(ell, d))
    return rows


def opened_sources(alpha: Row, gamma: Row, j: int) -> list[Source]:
    sources: list[Source] = []
    for side, moving, opposite in (("L", alpha, gamma), ("R", gamma, alpha)):
        target = moving.m * j + H0
        for u in divisors(target):
            sigma = target // u
            if (
                1 < u < target
                and sigma > 1
                and is_squarefree(u)
                and math.gcd(u * sigma, moving.m * j) == 1
            ):
                try:
                    physical_component(moving.m, opposite.m)
                except ValueError:
                    continue
                sources.append(Source(side, moving, opposite, j, u, sigma))
    return sources


def check_source_child_reassembly() -> tuple[int, int, int, int]:
    rows = generate_rows()
    source_count = 0
    child_count = 0
    projector_checks = 0
    decorated_checks = 0
    side_counts = {"L": 0, "R": 0}

    for alpha in rows[:24]:
        for gamma in rows[24:48]:
            if alpha.ell == gamma.ell or alpha.m == gamma.m:
                continue
            for j in range(1, 5):
                for source in opened_sources(alpha, gamma, j):
                    children = source_to_children(source)
                    expected = len(divisors(math.gcd(
                        source.moving.d, source.opposite.d
                    )))
                    if len(children) != expected:
                        raise AssertionError("wrong divisor-child multiplicity")
                    if len({(c.v, c.component) for c in children}) != expected:
                        raise AssertionError("duplicate projector child")
                    for child in children:
                        if child_to_source(child) != source:
                            raise AssertionError("child-to-source inverse failed")
                        if child.component != physical_component(
                            child.moving_m, child.opposite.m
                        ):
                            raise AssertionError("interval component was not preserved")
                        if child.sigma * child.U() - child.a * child.D() != H0:
                            raise AssertionError("native determinant failed")
                    for cutoff in (1, 2, 3, 5, 8, 13):
                        projector = sum(
                            lambda_cutoff(child.v, cutoff) for child in children
                        )
                        expected_projector = int(
                            math.gcd(
                                source.moving.d, source.opposite.d
                            ) <= cutoff
                        )
                        if projector != expected_projector:
                            raise AssertionError("row-gcd projector failed")
                        source_sign = (
                            -mobius(source.moving.d)
                            * mobius(source.u)
                            * expected_projector
                        )
                        child_sign = 0
                        for child in children:
                            local_mask = int(
                                math.gcd(
                                    child.v, child.D() * child.U()
                                ) == 1
                            )
                            child_sign += (
                                -mobius(child.v)
                                * lambda_cutoff(child.v, cutoff)
                                * mobius(child.D())
                                * mobius(child.U())
                                * local_mask
                            )
                        if child_sign != source_sign:
                            raise AssertionError("moving-sign reassembly failed")
                        target_moving = source.moving.m * source.j + H0
                        target_opposite = source.opposite.m * source.j + H0
                        content = math.gcd(target_moving, target_opposite)
                        ordered_difference = (
                            (1 if source.side == "L" else -1)
                            * (source.moving.m - source.opposite.m)
                        )
                        if ordered_difference % content:
                            raise AssertionError(
                                "normalized ordered determinant is nonintegral"
                            )
                        source_decorated = source_sign * echar(
                            QMOD, -3 * ordered_difference // content
                        )
                        child_decorated = 0.0 + 0.0j
                        for child in children:
                            local_mask = int(
                                math.gcd(
                                    child.v, child.D() * child.U()
                                ) == 1
                            )
                            coefficient = (
                                -mobius(child.v)
                                * lambda_cutoff(child.v, cutoff)
                                * mobius(child.D())
                                * mobius(child.U())
                                * local_mask
                            )
                            child_difference = child.epsilon * (
                                child.moving_m - child.opposite.m
                            )
                            child_decorated += coefficient * echar(
                                QMOD, -3 * child_difference // content
                            )
                        assert_close(
                            source_decorated,
                            child_decorated,
                            "decorated source-child reassembly",
                        )
                        projector_checks += 1
                        decorated_checks += 1
                    source_count += 1
                    child_count += len(children)
                    side_counts[source.side] += 1
                    if source_count >= 500:
                        break
                if source_count >= 500:
                    break
            if source_count >= 500:
                break
        if source_count >= 500:
            break

    if source_count < 200 or not all(side_counts.values()):
        raise AssertionError(
            f"insufficient two-polarization sample: {source_count}, {side_counts}"
        )
    return source_count, child_count, projector_checks, decorated_checks


def check_phase_and_content() -> int:
    rows = generate_rows()
    checks = 0
    for alpha in rows[:18]:
        for gamma in rows[18:36]:
            if alpha.ell == gamma.ell or alpha.m == gamma.m:
                continue
            for j in range(1, 5):
                target_alpha = alpha.m * j + H0
                target_gamma = gamma.m * j + H0
                content = math.gcd(target_alpha, target_gamma)
                difference = alpha.m - gamma.m
                if difference % content:
                    raise AssertionError("content does not divide the row difference")
                cutoff = min(7, content)
                for side, moving_m, opposite_m, epsilon in (
                    ("L", alpha.m, gamma.m, 1),
                    ("R", gamma.m, alpha.m, -1),
                ):
                    oriented = epsilon * (moving_m - opposite_m)
                    if oriented != difference:
                        raise AssertionError(f"{side} determinant orientation failed")
                    for r in (-7, -3, -1, 1, 2, 5):
                        physical_phase = echar(
                            QMOD, -r * difference // content
                        )
                        oriented_phase = echar(
                            QMOD, -r * oriented // content
                        )
                        assert_close(
                            physical_phase, oriented_phase, "polarization phase"
                        )

                        lhs = (
                            physical_phase if content <= cutoff else 0.0 + 0.0j
                        )
                        rhs = 0.0 + 0.0j
                        for c in range(1, cutoff + 1):
                            if content % c:
                                continue
                            for kappa in divisors(content // c):
                                b = c * kappa
                                if (
                                    target_alpha % b == 0
                                    and target_gamma % b == 0
                                ):
                                    rhs += mobius(kappa) * echar(
                                        c * QMOD, -r * oriented
                                    )
                        assert_close(lhs, rhs, "phase-compatible content inversion")
                        checks += 1
    if checks < 1000:
        raise AssertionError(f"insufficient phase/content sample: {checks}")
    return checks


def check_progression_determinant_mobius() -> tuple[int, int]:
    rows = generate_rows()
    progression_checks = 0
    mobius_checks = 0

    for alpha in rows[:20]:
        for gamma in rows[20:40]:
            if alpha.ell == gamma.ell or alpha.m == gamma.m:
                continue
            for j in range(1, 5):
                for source in opened_sources(alpha, gamma, j):
                    for child in source_to_children(source):
                        opposite_target = child.opposite.m * child.j + H0
                        common_target = math.gcd(
                            child.sigma * child.U(), opposite_target
                        )
                        for b in divisors(common_target):
                            g = math.gcd(b, child.sigma)
                            B = b // g
                            if math.gcd(child.a, B) != 1:
                                raise AssertionError(
                                    "active progression has nonprimitive slope"
                                )
                            tau = (
                                0
                                if B == 1
                                else (-child.u0 * pow(child.a, -1, B)) % B
                            )
                            if (child.t - tau) % B:
                                raise AssertionError("source missed resolved progression")
                            z = (child.t - tau) // B
                            Dtau = child.D(tau)
                            Utau = child.U(tau)
                            if Utau % B:
                                raise AssertionError("forced content factor absent")
                            Vtau = Utau // B
                            Dstar = Dtau + child.sigma * B * z
                            Ustar = Utau + child.a * B * z
                            Vstar = Vtau + child.a * z
                            if Dstar != child.D() or Ustar != child.U():
                                raise AssertionError("progression reconstruction failed")
                            if Ustar != B * Vstar:
                                raise AssertionError("content extraction failed")
                            unreduced_det = (
                                child.sigma * B * Utau
                                - child.a * B * Dtau
                            )
                            reduced_det = (
                                child.sigma * B * Vtau
                                - child.a * Dtau
                            )
                            if unreduced_det != B * H0:
                                raise AssertionError("unreduced Bh determinant failed")
                            if reduced_det != H0:
                                raise AssertionError("reduced h determinant failed")
                            if mobius(B) == 0:
                                raise AssertionError(
                                    "active squarefree U contains nonsquarefree B"
                                )
                            extracted = (
                                mobius(B)
                                * mobius(Vstar)
                                * int(math.gcd(B, Vstar) == 1)
                            )
                            if mobius(Ustar) != extracted:
                                raise AssertionError("Mobius extraction failed")
                            mobius_checks += 1

                            moving_at_tau = (
                                child.moving_ell * child.v * Dtau
                            )
                            omega = (
                                child.moving_ell
                                * child.v
                                * child.sigma
                                * B
                            )
                            for c in divisors(b):
                                kappa = b // c
                                if mobius(kappa) == 0:
                                    continue
                                for r in (-4, -1, 1, 3):
                                    direct = echar(
                                        c * QMOD,
                                        -r
                                        * child.epsilon
                                        * (
                                            child.moving_m
                                            - child.opposite.m
                                        ),
                                    )
                                    resolved = echar(
                                        c * QMOD,
                                        -r
                                        * child.epsilon
                                        * (
                                            moving_at_tau
                                            - child.opposite.m
                                        ),
                                    ) * echar(
                                        c * QMOD,
                                        -r * child.epsilon * omega * z,
                                    )
                                    assert_close(
                                        direct, resolved, "resolved affine phase"
                                    )
                                    progression_checks += 1
                    if mobius_checks >= 2500:
                        break
                if mobius_checks >= 2500:
                    break
            if mobius_checks >= 2500:
                break
        if mobius_checks >= 2500:
            break

    if progression_checks < 2000 or mobius_checks < 500:
        raise AssertionError(
            "insufficient progression sample: "
            f"{progression_checks}, {mobius_checks}"
        )
    return progression_checks, mobius_checks


def main() -> None:
    sources, children, projector_checks, decorated_checks = (
        check_source_child_reassembly()
    )
    phase_checks = check_phase_and_content()
    progression_checks, mobius_checks = (
        check_progression_determinant_mobius()
    )
    print("TPC-93 literal export regression: PASS")
    print(f"  source atoms (both polarizations): {sources}")
    print(f"  projector children round-tripped: {children}")
    print(f"  projector/sign reassemblies:       {projector_checks}")
    print(f"  decorated literal reassemblies:    {decorated_checks}")
    print(f"  orientation/content phase checks:  {phase_checks}")
    print(f"  resolved progression phases:       {progression_checks}")
    print(f"  determinant/Mobius extractions:    {mobius_checks}")
    print("  status: finite L0/L1 consistency only; no L2 claim")


if __name__ == "__main__":
    main()
