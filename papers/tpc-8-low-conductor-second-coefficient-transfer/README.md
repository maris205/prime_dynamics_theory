# TPC-8: low-conductor second-coefficient transfer

This directory contains the manuscript

> *Periodic Second Coefficients through a Prime Target: A
> Bombieri--Vinogradov Transfer, Arithmetic Involutions, and the
> Combined-Modulus Boundary*.

## Main result

Let `x = M*N`, let `h != 0` be fixed, let `q >= 3` be odd with
`gcd(q,h) = 1`, and let `beta` be a `q`-periodic function with
`||beta||_infinity <= 1`, supported on the units modulo `q`. In the range

```text
q <= (log x)^C,
2*M*q <= sqrt(x)/(log x)^B,
```

the manuscript proves an `l1`-in-rows asymptotic for

```text
sum_n beta(n) Lambda(m*n+h) W(n/N).
```

The row main term is

```text
(m*N/phi(m)) * integral(W) * (P_(q,h) beta)(m),
```

where

```text
(P_(q,h) beta)(a)
  = (1/phi(q)) * sum_{b in G_q, gcd(a*b+h,q)=1} beta(b).
```

After row normalization, this is a self-adjoint finite Markov operator. It
annihilates character modes with a local conductor exponent at least two.
Every surviving exact squarefree conductor `r` is exchanged with its
conjugate and damped by

```text
product_{p|r} 1/(p-2),
```

with the explicit arithmetic-involution phase. This is the same local
multiplier as in TPC-5, now appearing in the main term after passage through
the genuine prime target `Lambda(m*n+h)`.

The proof is a direct application of the classical maximal
Bombieri--Vinogradov theorem. It is not a new level-of-distribution theorem.
The actual modulus is `m*q`, and splitting the periodic coefficient costs
the period `q`.

## Strict boundary

The theorem does **not** permit `beta = Lambda - 1`. TPC-7 proves that
polylogarithmic periodic spaces capture a vanishing proportion of the
`L2` energy of that coefficient. Consequently, TPC-8 proves no twin-prime
lower bound, no fixed-shift prime-pair asymptotic, and no breach of the sieve
parity barrier.

## Build

From this directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Reproducibility package

The `experiments/` directory separates exact and floating computations.

Exact certificate and tests:

```bash
python experiments/exact_transfer_certificate.py \
  --output experiments/data/exact-certificate.json
python experiments/test_exact_transfer_certificate.py
python experiments/test_lambda_transfer_diagnostics.py
```

The exact canonical payload SHA-256 is:

```text
030F20B495E68234CD3176795C1F3652D2F8792DE88C1BE49BC6A04F15FBCCFF
```

The exact JSON file SHA-256 is:

```text
2EEE645F124CCDA3A50F4FB349550AC7195321EA5FC4410853142CD655E1E37E
```

An optional NumPy diagnostic is documented in
`experiments/README.md`. Its floating output is not an exact certificate and
does not instantiate the non-explicit logarithmic cutoff in
Bombieri--Vinogradov.

## Directory layout

- `periodic-second-coefficients-prime-target.pdf`: final 16-page manuscript.
- `main.tex`: manuscript driver and abstract.
- `sections/`: modular manuscript sections.
- `references.bib`: bibliography.
- `experiments/exact_transfer_certificate.py`: integer/rational certificate.
- `experiments/lambda_transfer_diagnostics.py`: optional finite Mangoldt
  diagnostic.
- `experiments/data/exact-certificate.json`: deterministic exact artifact.
