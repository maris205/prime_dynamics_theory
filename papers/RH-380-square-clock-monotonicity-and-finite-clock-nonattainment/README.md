# RH-380: Square-clock monotonicity and finite-clock nonattainment

RH-380 closes the finite-clock attainment question left open by RH-379,
without enlarging the factor class. The clock `q` is fixed before
`N -> infinity`; admissible factors are universally distance-two-safe
phasewise lag-two tables with `c11(r)=0` at every phase. This is not an
unrestricted-memory theorem.

For

```text
q_y = 4 product_(i<=y) p_i^2,
A_y = product_(i<=y) (p_i^2-1),
D_y = product_(i<=y) (p_i^2-2),
```

write `R_l^(y)` for the positive-run counts in the odd squarefree-support
word and define

```text
mathcal_E_y = sum_(l even) R_l^(y),
L_y         = sum_(l even) l R_l^(y),
M_y         = sum_(l odd) (l-1) R_l^(y).
```

The all-order per-run deletion argument proves

```text
mathcal_E_(y+1) = (p_(y+1)^2-2) mathcal_E_y + M_y.
```

Together with the locked RH-374 odd-run recurrence and the exact RH-379
square-clock formula, this gives

```text
G(q_(y+1))-G(q_y)
  = 2(L_y-2 mathcal_E_y)/(pi^2 A_y(s-1))
    + M_y(4/pi^2-H_(y+1))/(A_y(s-1)),
s = p_(y+1)^2.
```

Because

```text
L_y-2 mathcal_E_y
  = 2 R_4^(y) + 4 R_6^(y) + 6 R_8^(y) >= 6,
```

the square-clock values `G(q_y)` are strictly increasing, with the explicit
increment lower bound `12/(pi^2 A_y(s-1))`.

The paper also proves a deliberately special saturation theorem. If
`q_y | Q` and `Q` has exactly the same prime support as `q_y`, then exact
`delta/theta` weights scale by `1/R`, where `Q=R q_y`, and mod-4/mod-9
zero-weight phases split the fine addition-by-two cycles into `R` identical
finite path copies. Hence

```text
G(Q) = G(q_y).
```

This is separator-specific. It is not a general cyclic-cover or
general-multiple theorem. The locked negative control is

```text
G(36)  = 9/(2*pi^2) - kappa2/7,
G(180) = 73/(16*pi^2) - 25*kappa2/161,
```

and their strict inequality follows from the locked
`pi^2*kappa2<4` enclosure. The multiplier `5` adds prime support.

For arbitrary fixed `q`, choose `y>=1` containing all odd prime divisors of
`q` and put `Q=lcm(q,q_y)`. Clock lifting and special saturation give

```text
G(q) <= G(Q) = G(q_y) < B_infinity,
B_infinity-G(q)
  >= 12/(pi^2 A_y(p_(y+1)^2-1)) > 0.
```

Arbitrary 2-adic exponents and arbitrary exponents on the supported odd
primes are allowed; they only enlarge `Q/q_y`. Thus no fixed finite clock
attains the RH-379 all-clock supremum.

## Exact artifact

The standard-library artifact uses exact pairs
`{"inv_pi2": u, "kappa2": v}` for `u/pi^2+v*kappa2`. It:

- checks direct and Euler-product run rows for `y=1,2,3`;
- samples the deletion ledger while the manuscript supplies the all-order
  proof;
- locks the exact recurrence and increment anchors;
- checks nine same-support refinements by every-residue density scaling,
  cause-specific separators/run replication, and an independent generic
  three-state cyclic max-plus dynamic program;
- fails closed on nonintegral Euler-product counts and ambiguous
  `pi^2*kappa2` comparisons;
- verifies 24 immutable source inputs against live SHA-256 values and the
  exact blobs at their declared release commits.

The mutable `AGENTS.md` and `RH_HANDOFF.md` are intentionally absent from
source locks.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

Finite rows reproduce exact identities and boundary controls. They are not
finite-order fits offered as an all-order proof.

## Boundaries

RH-380 does not claim monotonicity of the RH-379 correction `Delta_y`, a
growing clock `q(N)`, adaptive-capacity convergence, a theorem for nonzero
phasewise `c11`, a general cover theorem, an intrinsic operator, a
prime-power trace formula, a zero model, a Hilbert--Polya construction, or
the Riemann hypothesis. Gates A--E remain false/open.

The immediate within-class reopen trigger is an analytic first-order
asymptotic for `B_infinity-G(q_y)` normalized by
`T_y=sum_(p>p_y)(p^2-1)^-1`, requiring the successor to control the `M_y`
term at second order. RH-380 does not prove that rate theorem. The first
blocker to enlarging the class remains phase-weighted shift-two cancellation
for nonzero `c11(r)`.
