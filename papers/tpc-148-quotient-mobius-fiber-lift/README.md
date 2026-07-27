# TPC-148: Quotient-Mobius fiber lift

Paper title:

> *Multiplicative Quotient Lifts on Determinant-Two Fibers:
> Exact Mobius Recovery and Stable Nonpretentiousness*

## Core result

For every positive integer `c`, the paper constructs an explicit
1-bounded multiplicative function `G_c` satisfying

```text
G_c(c*m) = mu(m)
```

for every positive integer `m`.  On the determinant-two fiber

```text
D(z)=d+s*z, V(z)=u+a*z, s*u-a*d=2,
t=a*D(z)=a*d+a*s*z,
```

this gives the exact identity

```text
mu(D(z))*mu(V(z)) = G_a(t)*G_s(t+2).
```

The full Mobius squarefree information is already encoded in the
two multiplicative functions.  No Liouville conversion, prime-square
cutoff, CRT squarefree expansion, or truncation tail is required.

At prime arguments, `G_c` differs from the Liouville function only at
primes dividing `c` to exact exponent one.  The resulting
pretentious-distance loss is at most

```text
2 * sum_{p || c} 1/p.
```

For `c <= (log X)^A` with any fixed `A>0`, this is lower order than
the sourced Liouville nonpretentiousness bound (once `X` is large
enough depending on `A`), so a smaller fixed power of logarithm still
satisfies the nonpretentious branch of Tao--Teravainen.

## Claim boundary

The lift is an exact L0 identity and its nonpretentious stability is
an L1 input.  It does not prove a weighted, phase-uniform, all-prefix,
four-point, positive-L2, fixed-X-power, `1/400`, prime-pair, or
twin-prime result.

## Reproduce

```powershell
python experiments/tpc148_quotient_lift_audit.py
python experiments/tpc148_quotient_lift_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Stable archival PDF:

`tpc-148-quotient-mobius-fiber-lift.pdf`
