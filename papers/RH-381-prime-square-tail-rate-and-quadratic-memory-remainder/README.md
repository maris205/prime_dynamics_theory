# RH-381: Prime-square tail rate and quadratic memory remainder

RH-381 proves the first-order square-clock gap rate inside the exact
fixed-clock-first factor class frozen by RH-379 and retained by RH-380:
universally distance-two-safe phasewise lag-two tables with `c11(r)=0` at
every phase. It does not enlarge that class.

Let

```text
a_(j+1) = 1/(p_(j+1)^2-1),
T_y     = sum_(j>=y) a_(j+1),
X_j     = (L_j-2 mathcal_E_j)/A_j,
```

and

```text
e_m        = product_(p odd) (1-m/p^2),
X_infinity = (2e_4-4e_5+6e_6-8e_7+10e_8)/e_1.
```

The RH-374 run formula gives

```text
X_infinity >= 6e_8/e_1 > 0.
```

Factorwise Euler-tail comparison, the exact RH-379 `H` product, and a
site-count bound for the RH-380 memory statistic give

```text
|X_j-X_infinity| <= 170 T_j,
0 <= 4/pi^2-H_(j+1) <= (4/pi^2) T_(j+1),
0 <= M_j/A_j <= 1.
```

The exact tail identities are

```text
sum_(j>=y) a_(j+1) T_j
  = (T_y^2 + sum_(j>=y) a_(j+1)^2)/2,

sum_(j>=y) a_(j+1) T_(j+1)
  = (T_y^2 - sum_(j>=y) a_(j+1)^2)/2.
```

Finite telescoping of the RH-380 increment, followed by the already proved
cofinal limit `G(q_j) -> B_infinity`, yields

```text
|B_infinity-G(q_y)-(2X_infinity/pi^2)T_y|
  <= (342/pi^2) T_y^2,

(B_infinity-G(q_y))/T_y -> 2X_infinity/pi^2 > 0.
```

The proof does not exchange an `N`-limit with a square-clock limit. Every
clock is fixed before `N -> infinity`. It also uses no prime number theorem:
`T_y -> 0` follows from the elementary integer-square tail

```text
T_y <= 1/2 (1/p_y + 1/(p_y+1)).
```

## Exact artifact

The standard-library artifact has two independent layers.

- Exact `Fraction` arithmetic regenerates six run/Euler/increment rows and
  four finite tail-identity rows. The canonical six-row fixture is 2574
  bytes with SHA-256
  `d55fd48071eb5b88c054f3d34329f274f792f2bbd859b4ab98e31b5b7020beb8`.
- Directed 60-digit decimal arithmetic is converted to exact rational
  endpoints. It enumerates all 9592 primes through 100000, bounds the
  omitted prime tail by `200001/20000200000`, and checks the 170/342 bounds
  at `y=1,2,3,5,10,25`. The independently rebuilt 6851-byte fixture has
  SHA-256
  `e0342f871b1f952039da2b1025fa7598771b9fa089295f07cb60b11f70cee15c`.

Comparisons fail closed. The tests mutate the constants, numeric types,
cutoff, precision, fixture digest, release commits, source membership,
paths, and source digests. The same certificate is also run under
`PYTHONOPTIMIZE=2`.

Exactly 25 immutable predecessor inputs are locked: 7 from RH-374, 8 from
RH-379, 8 from RH-380, and 2 from the RH-MVP2 archive. Every live file must
be byte-identical to its declared release blob. Mutable `AGENTS.md` and
`RH_HANDOFF.md` are deliberately excluded.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

The semantic PDF must be byte-identical to `main.pdf`. Archive verification
fails on missing members, unsafe paths, duplicate keys, hash drift,
source-lock mismatch, release rebinding, or PDF mismatch.

## Boundaries

RH-381 does not claim an exact second-order coefficient, an asymptotic in
`p_y`, a growing clock `q(N)`, adaptive-capacity convergence, a theorem for
nonzero phasewise `c11`, an intrinsic operator, determinant, prime-power
trace, zero model, Hilbert--Polya construction, or the Riemann hypothesis.
Gates A--E remain false/open.

The within-class next edge is a genuine second-order Euler-tail analysis
that retains every independent quadratic scale, including
`S_y=sum_(j>=y)a_(j+1)^2`, and proves an all-order cubic remainder. This
paper does not state that coefficient. The first class-enlargement blocker
remains phase-weighted shift-two Mobius cancellation.
