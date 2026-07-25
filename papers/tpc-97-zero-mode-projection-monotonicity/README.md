# TPC-97: Zero-mode projection monotonicity

Paper title:

> *Zero-Mode-Safe Orthogonal Coarsening: Exact Projection
> Monotonicity, Constant-Defect Sharpness, and the Critical
> \(J^{-1}\) Interface*

## Core theorem

Let `A` be the literal coefficient on its prescribed actual support,
let `P` be an orthogonal projection on that same finite Hilbert
space, and write

```text
B = P A,
R = (I - P) A,
q = (I - P) 1.
```

The exact ledger is

```text
D(A) = D(B) + D(R),
Z(B) - Z(A) = -<R,q> = <A,(P-I)1>.
```

If `P 1 = 1`, then the zero mode is exact and

```text
rho(A)^2 = rho(B)^2 D(B)/D(A),
F(A)     = F(B)     D(B)/D(A).
```

Therefore

```text
rho(A) <= rho(B),
F(A)   <= F(B).
```

A constant-preserving orthogonal coarsening is conservative: it
cannot manufacture an artificially smaller physical flatness.
Consequently, a proved projected upper bound transfers to the
physical coefficient without requiring `||A-B||/||B|| = O(1/J)`.
This is a structural exception to, not a contradiction of, the
general TPC-89 surrogate barrier.

## Block averages

Partition averaging on the original bins is a constant-preserving
orthogonal projection. The paper proves:

- exact preservation of the physical zero mode;
- the within-block variance decomposition;
- monotonicity along nested partitions; and
- the correct weighted compressed representation.

Block multiplicities cannot be discarded. For the block-constant
physical vector `(1,-1,-1)` with block sizes `(1,2)`, the physical
sum is `-1`, while the invalid unweighted compressed vector `(1,-1)`
has apparent sum `0`.

## Missing-constant defect

For arbitrary `P`, define

```text
kappa(P) = ||(I-P)1|| / sqrt(S),
r        = ||(I-P)A|| / ||PA||.
```

Then

```text
|Z(PA)-Z(A)| <= sqrt(S) kappa(P) ||(I-P)A||
```

with optimal constant, and

```text
(rho(PA)-kappa r)_+ / sqrt(1+r^2)
    <= rho(A)
    <= (rho(PA)+kappa r) / sqrt(1+r^2).
```

The sharp structure-free critical condition is

```text
kappa(P) r = O(1/J).
```

If `kappa` is bounded below, the TPC-89 `O(1/J)` relative residual
order returns. If `kappa = 0`, no residual accuracy is needed for a
one-sided flatness certificate.

Every unsafe projection has a unique minimal rank-one constant
completion

```text
Psharp x = P x + <x,q> q / ||q||^2.
```

## Literal TPC status

At

```text
Q_X = X^(267/400 + o(1)),
J_X = X^(133/400 + o(1)),
```

a zero-mode-safe literal orthogonal surrogate satisfying

```text
rho(P_X A_X) <= X^o(1) / J_X
```

certifies

```text
F(A_X) <= X^(1/400 + o(1))
```

without a relative approximation hypothesis. This is an exact L1
certificate. The paper does not construct a growing arithmetic
projection estimate and proves no new L2 fixed-shift cancellation
theorem.

The determinant compatibility `lambda_D <= 2 eta_Z` and the strict
physical budget `Lambda_phys < 1/400` remain separate.

## Regression certificate

Run:

```bash
python experiments/check_projection_identities.py
```

The script performs exact rational exhaustive checks of block
averages and coordinate projections through dimension five, plus
seeded random complex projector and rank-one-completion checks.
The archived summary is in `experiments/certificate-output.json`.

The archived run passed:

```text
172,480 exact block cases
111,110 exact coordinate-projection cases
107,205 sharp equality cases
1,000 random safe projection cases
1,000 random defective/repair cases
```

## Build

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

```text
zero-mode-projection-monotonicity.pdf
```
