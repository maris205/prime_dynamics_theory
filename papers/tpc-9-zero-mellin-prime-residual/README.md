# TPC-9: zero Mellin mode of the prime-target residual

This directory contains the manuscript

> *The Zero Mellin Mode of a Prime-Target Residual: Fixed-Shift Titchmarsh
> Closure, a Large-Factor Subtraction Formula, and the Scale-Localization
> Boundary*.

## Main result

For fixed nonzero `h`, smooth compactly supported `W`, and

```text
A_{h,>D}(X;W)
  = sum_{m,n >= 1, n > D}
      (Lambda(n)-1) Lambda(m*n+h) W(m*n/X),
```

the paper proves an explicit fixed-shift asymptotic uniformly for

```text
D <= sqrt(X)/(log X)^B.
```

The exact complete-factor identity is

```text
sum_{n|r} (Lambda(n)-1) = log(r)-tau(r).
```

It converts the full factor aggregation into a shifted prime number theorem
minus a Titchmarsh divisor sum. The complete sum is evaluated using the
established theorem of Assing--Blomer--Li; classical maximal
Bombieri--Vinogradov evaluates `n <= D`. Exact subtraction evaluates the
entire complementary tail.

If

```text
C_h(s)
  = product_{p|h} (1-p^(-s-1))
    product_{p not|h} (1+1/((p-1)p^(s+1))),
```

then the tail has leading term

```text
(1-C_h(0)) X log(X/D) integral(W).
```

When the logarithmic coefficient is nonzero, its `X log X` coefficient at
the square-root cutoff is one half of the complete-sum coefficient. For
`h=2`,

```text
C_2 = zeta(2) zeta(3) / (3 zeta(6)) = 0.647865...
```

## Strict boundary

The theorem controls only the complete multiplicative scale aggregate, or
zero Mellin mode. A ratio cutoff in `n/m` requires all Mellin frequencies.
The single layer `m=1` contains

```text
sum_n (Lambda(n)-1) Lambda(n+h) W(n/X),
```

whose fixed-shift asymptotic is the Hardy--Littlewood prime-pair problem.
Thus the paper proves no dyadic Type-II estimate, fixed prime-pair
asymptotic, twin-prime lower bound, new level of distribution, or parity
breakthrough.

## Build

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Reproducibility

See `experiments/README.md`. The exact certificate uses formal logarithm
symbols and the Python standard library. The sharp-box diagnostic code is
committed, while its generated floating JSON is intentionally ignored.

## Directory layout

- `main.tex`: manuscript driver and abstract.
- `zero-mellin-prime-residual.pdf`: compiled manuscript.
- `sections/`: modular manuscript sections.
- `references.bib`: bibliography.
- `experiments/exact_zero_mellin_certificate.py`: exact formal certificate.
- `experiments/test_exact_zero_mellin_certificate.py`: exact tests.
- `experiments/zero_mellin_diagnostic.py`: optional finite diagnostic.
- `experiments/data/exact-zero-mellin-certificate.json`: deterministic exact
  artifact.
