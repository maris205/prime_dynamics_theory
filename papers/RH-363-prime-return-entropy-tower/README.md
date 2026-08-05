# RH-363: Prime-return admissible entropy tower

RH-363 is an independent post-RH-362 theorem paper.  It combines the exact
modular return ranks of

```text
H(x,y) = (1-6x^2-y,x)
```

with the infinite pairwise-coprime admissible-shift theorem.  For a
nonperiodic integral point `P`, write `r_p(P)` for the return period of
`P mod p` and set, for every integer `m >= 1`,

```text
B_m(P) = {p^(m r_p(P)) : p prime}.
```

Let `X_m(P)` be the corresponding two-sided `B_m(P)`-admissible shift.  The
paper proves the following package.

- Every `X_m(P)` has only `0^infinity` as a periodic point, so all levels
  have the identical Artin--Mazur zeta function `(1-z)^-1`.
- The normalized topological entropy is nevertheless

  ```text
  E_m(P) = h_top(X_m(P))/log(2)
         = product_p (1-p^(-m r_p(P)))
         = Z_P(m)^(-1).
  ```

  The sequence is strictly increasing and tends to one.
- If `Lambda_m=-log E_m` and `M_m=sum_p p^(-m r_p)`, then the exact
  multiples-Mobius inversion

  ```text
  M_m = sum_(j>=1) mu(j) Lambda_(mj)/j
  ```

  recovers every power moment.  The moments recover the distinct atoms
  `p^(-r_p)` recursively, and unique factorization then recovers every
  labeled pair `(p,r_p)`.  Thus the common periodic-orbit zeta loses all
  return-rank data while the full entropy tower retains all of it.
- For the first `k` primes, let `X_(m,k)` be the finite approximant and let
  `W_k` be their primorial.  Its fixed-point and zeta coefficients agree
  with the infinite limit through degree `W_k-1`.  The first defect is
  exactly at `W_k`, where gcd reduction produces the same prime-wheel count
  for every point `P`, every tower level `m`, and every return-rank list.
- Writing `E_(m,k)` for the finite entropy density, both origin radii of the
  logarithmic and reduced rational zeta series are exactly
  `2^(-E_(m,k))`.  They increase to `2^(-E_m)<1`, whereas the
  coefficientwise limiting zeta has radius one.  The zeta germs converge
  uniformly on every closed disk of radius below `2^(-E_m)`, and this
  exhaustion disk is sharp because the finite positive poles converge to
  its boundary.

## Route boundary

Route A is `GO`: the entropy tower, exact recovery theorem, universal first
defect, and sharp local-uniform disk are new rigorous consequences of the
two locked source packages and form a standalone mathematical result.

Route B remains negative.  The Artin--Mazur zeta is identically `(1-z)^-1`
and contains no return ranks; recovery uses a sequence of topological
entropies, not signed prime-power traces of one canonical operator.  Sampling
the RH-362 Euler product at positive integers does not identify Riemann
zeros, produce von Mangoldt weights, or supply a completed-zeta determinant.

The four-volume RH-1--RH-361 foundation stays frozen, and the physical route
coordinate remains

```text
actual_same_clock_unnormalized_head_transport_open.
```

Gates A--E remain false/open.  No Hasse--Weil interpretation,
Hilbert--Polya operator, Riemann-zero identification, completed-divisor
equality, or proof of RH is claimed.

## Reproduction

```bash
make result
make test
make pdf
make archive
```

Finite rows reproduce exact modular ranks, finite coprime fixed-point
formulas, primorial defects, and truncated numerical instances of an
analytically proved inversion.  They are not evidence for an unproved
all-prime distribution law.
