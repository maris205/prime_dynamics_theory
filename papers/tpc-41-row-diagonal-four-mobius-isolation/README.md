# TPC-41: Row-Diagonal Closure and Triple-Prime Decorrelation

This directory contains the manuscript

> **Row-Diagonal Closure at the Moving Mobius Gate: Folded Alias
> Energies, Exact Four-Correlation Isolation, and Triple-Prime
> Progression Decorrelation**.

TPC-39's folded terminal square appears to contain a long-gap
two-Mobius alias problem and a cross-row four-Mobius problem. TPC-41
proves that only the second is a genuine physical arithmetic gate.

## Main results

For a normalized alias Gram `H` and atomic diagonal `D`, the complete
same-row sector satisfies

```text
E_same <= lambda_max(H) D,
|E_same - D| <= ||H-I||_op D.
```

Consequently:

- The minimal `q=L+1` Fourier bank has spectrum `2,1,0`, so
  `E_same <= 2D` and the absolute value of the complete signed same-row
  unequal-alias sector is at most `D`.
- The full `2L+1` point DFT has `H=I` and deletes every unequal-alias
  product exactly, including cross-row products.
- TPC-39 already bounded `D` at the endpoint, so the apparent long-gap
  two-Mobius alias gate is closed without Mobius cancellation.
- The only unbounded sector inside the chosen minimal folded terminal
  energy is the explicit cross-row form

```text
F_L = sum_(gamma,j,a) sum_(alpha != beta)
      c^L_(alpha,gamma,j) conjugate(c^L_(beta,gamma,j))
      u_(alpha,j,a) conjugate(u_(beta,j,a)),
```

  plus its right-hand analogue. Its summands contain four actual Mobius
  factors, physical masks, and source weights.
- Every retained pair of affine target forms is nonproportional.
- Each fixed-alias terminal column admits an exact Hilbert-valued
  one-Mobius compression; scalar compression does not control its output
  norm.

There is also a positive scalar arithmetic theorem. Let

```text
Y = X^(133/400),
M = q1 q2 q3 ~ X^(399/400),
K = X/M ~ X^(1/400),
```

where each `qi` lies in one of three disjoint admissible prime intervals.
For every fixed `0 < theta < 1/200`, all but a zero-density subfamily of
these moduli satisfy the raw, uncentered estimate

```text
sum_(a mod M)^* |sum_(n<=X, n=a mod M) mu(n)|^2
    << X K / (log X)^theta.
```

The proof combines the centered almost-all-moduli theorem of
Klurman--Mangerel--Teravainen with a maximal multiplicative large sieve
that disposes of the one subtracted character over the sparse
triple-prime family. A bounded-variation transfer includes the smooth
terminal weight `-mu(n) log(n) Phi_0(n/X)`.

Classical Barban--Davenport--Halberstam theory already gives scalar
logarithmic savings for almost all moduli in this range. The point of the
KMT route here is the sharper stretched-exponential exceptional-density
ledger for the admissible triple-prime family, not a claim that scalar
logarithmic cancellation was previously unknown.

This is a real logarithmic saving from the coefficient-blind scalar
scale `XK`. It is still a factor `K/(log X)^theta` above the scalar
diagonal and does not estimate the physical cross-row form.

## Exact certificate

Run from this directory:

```text
python experiments/tpc41_certificate.py
python -O experiments/tpc41_certificate.py
```

The two commands produce byte-identical canonical JSON. The frozen run
passes `4,358,451` exact checks using integer, rational, modular-character,
Gaussian-integer, and formal prime-logarithm arithmetic.

Certificate digest:

```text
e10174e2448d5323afb586d5855112e596ea7e134cd5899f216ef3a916748fc4
```

## Build

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Claim boundary

TPC-41 does **not** prove an individual-shift Chowla estimate, a
diagonal-scale progression variance, the physical Hilbert-valued
four-Mobius bound, a breach of sieve parity, a Hardy--Littlewood
prime-pair asymptotic, or infinitely many twin primes.
