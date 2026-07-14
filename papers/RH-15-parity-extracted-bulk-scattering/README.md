# Parity-extracted bulk scattering

This directory contains the fifteenth-layer theory paper in the quadratic
prime-dynamics program:

> *Parity-Extracted Bulk Scattering at a Quadratic Band-Merging Map: Exact
> Endpoint Poles, Resonance-Cloud Necessity, and Geometric Finite-Section
> Scaling*

The analytic part identifies the deterministic target left open by RH-14.
If `E_{1,n}` is the even beta-one circle trace and
`a_n = lambda**(-n)`, then the physical flat trace is

```text
P_{2n} = 2 E_{1,n} - 2 a_n/(1+a_n) - a_n**2/(1-a_n**2).
```

The validated reduced-sector gap from RH-13 therefore gives

```text
P_{2n} = 2 - 2 lambda**(-n) + lambda**(-2*n) + O(3**(-n)).
```

After Perron/parity extraction, the exact deterministic bulk determinant has
the local factorization

```text
D_bulk,2(z) = G(z)/(1-z**2/lambda),
```

where `G` is holomorphic and nonzero for `|z| < lambda`. Thus the nearest
singularities are genuine simple poles at `z = +/-sqrt(lambda)`. A naive
locally uniform entire noisy determinant limit across those poles is
impossible.

The numerical audit shows how finite noise resolves the poles. At
`sigma=1e-4`, fourteen outer bulk resonances lie close to the quantized phases
of

```text
1 + q + ... + q**7,  q = z**2/lambda.
```

The exact geometric model has the scaled profile `(exp(s)-1)/s`. Matching of
the noisy cloud to that model is a floating-point diagnostic and a stated
conjecture, not a theorem.

## Reproduction

Run the tests and full sparse audit:

```bash
/root/math/.venv/bin/python -m pytest -q
PYTHONPATH=src OPENBLAS_NUM_THREADS=16 \
  /root/math/.venv/bin/python experiments/run_bulk_scattering_audit.py
```

The full audit reaches a `204800`-state matrix and resolves 80 leading
eigenvalues. To rebuild figures and the JSON summary from archived CSV files:

```bash
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_bulk_scattering_audit.py --reuse-results
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The exact trace reconstruction, q-product factorization, endpoint poles,
normal-family obstruction, and canonical finite-section theorem are analytic.
The large sparse spectra and their cloud fits are ordinary floating-point
computations.
