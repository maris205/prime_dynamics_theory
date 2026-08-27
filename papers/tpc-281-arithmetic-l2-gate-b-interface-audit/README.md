# TPC-281 — A typed arithmetic `L2` interface for four-packet Gate-B reassembly

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

If a literal source operator satisfies the typed hypothesis
`||A_X||_(2->2)<=K X^(-sigma)`, then TPC-280's two-term packet budget gives the
exact output bound

`||A_X S||_2^2 <= K^2 X^(-2sigma) Q_X D`

and, with `Q_X<=(B+ell/d)X^(-kappa)` and `D<=d_+X^a`, the collapsed bound
`K^2d_+(B+ell/d)X^(a-2sigma-kappa)`.  A scalar readout is controlled by
Cauchy--Schwarz.  However, an exact orthogonal-functional pair with equal
operator norm gives full versus zero attachment for the same packets, so
geometry plus an `L2` norm does not identify the arithmetic attachment.

The typed interface is conditional; the literal source-level arithmetic `L2`
estimate remains open.  Four exact packet witnesses, four interface budgets,
and all twelve TPC-280 parent rows pass independent and hostile checks.  No
fixed-power credit, full Gate-B closure, or twin-prime conclusion is claimed.

## Claim ceiling

```text
PROVED_EXACT = typed Hilbert-space L2-to-output interface under its hypothesis
PROVED_EXACT = scalar-readout contraction and orthogonal attachment obstruction
NUMERICALLY_CERTIFIED_FINITE = 4 packet fixtures + 4 interface cases + 12 parent rows
CONDITIONAL_ONLY = literal arithmetic L2 input and source attachment
OPEN = literal source arithmetic L2, typed attachment nondegeneracy, full Gate B
REFUTED_EXACT = geometry/operator-norm data alone identify a positive attachment
FIXED_POWER_CREDIT = 0
ARITHMETIC_ADVANCE = NO
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc281_arithmetic_l2_interface_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc281_arithmetic_l2_interface_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc281_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc281_attachment_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The finite parent
transfer is exact coordinate inheritance from TPC-280 and is not an arithmetic
estimate.  The Session-named `propose.md` and Route evaluator files are absent
from this checkout; the local proof package, theorem ledger, certificate,
independent replay, stress audit, and Bridge-B checker provide the fail-closed
scoped evaluation.
