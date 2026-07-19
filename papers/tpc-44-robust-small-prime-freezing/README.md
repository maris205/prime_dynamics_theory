# TPC-44: Robust small-prime freezing

This directory contains the manuscript

> **Robust Small-Prime Freezing at the Four-Mobius Gate: Walsh-Face
> Compression, Exact Prime Descent, and the High-Prime Drift Barrier**.

TPC-43 proved exact annealed diagonalization for the equality packet and
identified the physical Mobius function with the all-minus corner of one
prime-sign Walsh cube. TPC-44 partially de-randomizes that corner.

## Main unconditional advance

For a cutoff `z`, split every actual squarefree equality label into its
small-prime and high-prime parts. Let `nu_z` be the number of distinct
small-prime parts occurring in the packet. Then

```text
P_high(sup_all-low-signs Z_0 > L nu_z D_0) <= 1/L.
```

The supremum is inside the probability: one high-prime environment
works simultaneously for every assignment of all signs `p <= z`.

At the inherited endpoint,

```text
z = (log X)^(501/500),
nu_z <= X^(62549/26302500 + o(1)),
K_B = X^(1/400 + o(1)).
```

The exact exponent gap is

```text
1/400 - 62549/26302500 = 12829/105210000 > 0.
```

Hence a density `1-o(1)` set of high-prime environments remains within
the endpoint budget after every small-prime sign is overwritten
arbitrarily. In particular, all signs through the mildly
superlogarithmic cutoff can be fixed to the physical Mobius value `-1`.

## Exact descents

For the centered spectrum `F = Z_0 - D_0`, define the coefficient after
freezing the first `r` active primes by

```text
C_r(m) = sum_(a | p_1...p_r) mu(a) C(am).
```

Then

```text
C_r(m) = C_(r-1)(m) - C_(r-1)(p_r m),
E_r = (1-theta_r) E_(r-1),
|F(-1)|^2 = Var(Z_0) product_r (1-theta_r).
```

A second exact transport uses nonnegative conditional face energies and
expresses `Z_0(-1)/D_0` as a product of conditional likelihood biases in
the energy-weighted measure.

## Sharp boundary

The manuscript constructs a degree-two Gram energy supported entirely
on `z`-rough kernels with vanishing relative variance, vanishing
normalized influences, and vanishing prime-toggle quadratic variation,
but with diverging all-minus amplification. Thus variance, fixed
moments, rough support, and small local defects do not determine the
physical high-prime corner.

The remaining gate is a coefficient-specific bound on cumulative
high-prime anti-correlation, naturally a bilinear/Type-II target.

## Exact certificate

Run from this directory:

```text
python experiments/tpc44_certificate.py
python -O experiments/tpc44_certificate.py
```

Both commands produce byte-identical canonical JSON. The frozen run
passes `15,677` exact checks.

Certificate digest:

```text
24b7eb3f19af7a2c8a016672020ee593578463857f1d7fe3dabedd7e59b57433
```

Certified source SHA-256:

```text
1bc866f4e7981b3beea6fd4682fc702bef7cc28b949c192a628e1582d69a5da1
```

JSON SHA-256:

```text
bc0f83c2ba177f395a4c6b22a2d5c5bf1773249134149a4fbce4326bb2e7d7ea
```

## Build

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Claim boundary

TPC-44 does **not** prove that the high-prime all-minus environment is
good, the residual amplification is subpolynomial, a fixed-shift Chowla
estimate, a parity breach, the Hardy-Littlewood prime-pair asymptotic,
or infinitely many twin primes.
