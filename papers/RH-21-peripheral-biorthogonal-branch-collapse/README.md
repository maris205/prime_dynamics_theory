# Peripheral biorthogonalization and branch-memory collapse

This directory contains the twenty-first-layer paper in the quadratic
prime-dynamics spectral program:

> *Peripheral Biorthogonalization of Critical-Branch Returns at a Quadratic
> Band-Merging Map: Gauge Invariance, Branch-Memory Collapse, and a No-Go
> Theorem for Normalization-Based Half Weights*

RH-20 left a precise ambiguity. In the symmetric rank-one branch model, both
a cubic relative phase and a positive half-weight reproduce one-branch
modulus. This paper tests whether the half-weight can be derived merely by
building Perron/parity-biorthogonal Grushin entrance and exit maps.

Let `Q = I - R L*` be the oblique spectral complement of the Perron and
parity modes. For raw trial and test maps `V0,W0`, define

```text
G  = W0* Q V0,
V  = Q V0,
W* = G^{-1} W0* Q.
```

Then `W*V=I`, `QV=V`, `W*Q=W*`, and `P=VW*` is an idempotent packet
projection inside the physical bulk complement. The construction is exact.

It also gives two no-go results.

1. A change of biorthogonal coordinates is a gauge transformation:
   `M -> S^{-1} M S`. It preserves the endpoint operator, determinant, and
   nonzero spectrum. It cannot divide the bright eigenvalue by two.
2. With real Gaussian dynamics, real peripheral projectors, and static real
   trial/test maps, the reduced bright scalar is real. A nonreal cubic phase
   must enter through a spectral-parameter boundary condition or another
   genuinely complex structure.

The coefficient dual to the unnormalized bright vector `(1,1)` is indeed
close to `(1/2,1/2)`, but this is only coordinate normalization. Together
with the bright synthesis vector it forms the projector

```text
P_b = (1/2) [[1,1],[1,1]],
```

which acts as the identity on the bright channel and therefore does not
attenuate its eigenvalue.

The second result is a conditioning barrier. If two normalized branch
histories have overlap `c`, then

```text
cond(V)       = sqrt((1+c)/(1-c)),
cond(V*V)     = (1+c)/(1-c),
norm(W*) >= 1/sqrt(1-c)
```

for every exact two-label dual `W*V=I`. At `sigma=1e-4`, the endpoint overlap
is `0.99885850`; the raw Gram condition is `1751.07`. After Perron/parity
projection the overlap becomes `0.99906159`, the Gram condition is `2130.26`,
and the canonical analysis norm is `32.72`. Peripheral extraction does not
restore lost branch memory.

The next valid object is a spectral-parameter bright/dark Schur complement.
It may attenuate the bright return through a genuine self-energy and may
become complex away from the real axis; a static coordinate normalization
cannot do either.

Run the tests and full audit with:

```bash
/root/math/.venv/bin/pytest -q
PYTHONPATH=src OPENBLAS_NUM_THREADS=16 /root/math/.venv/bin/python \
  experiments/run_biorthogonal_branch_audit.py
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
