# Dark-channel Schur self-energy

This directory contains the twenty-second-layer paper in the quadratic
prime-dynamics spectral program:

> *Dark-Channel Schur Self-Energy in Critical-Branch Returns at a Quadratic
> Band-Merging Map: Exact Target-Coupling Laws, a Local No-Go Theorem, and a
> Nested-Complement Route*

For a bright/dark return matrix

```text
M = [[a,b],
     [c,d]],
```

the exact scalar Schur function is

```text
F_b(z) = z - a - bc/(z-d),
det(zI-M) = (z-d) F_b(z).
```

If `tau = rho_bulk**(2*k)` is the physical return-scale target, the unique
coupling product that places `tau` in the local spectrum is

```text
p_req = (tau-a)(tau-d).
```

The ratio `bc/p_req` is simultaneously the signed fraction of the required
self-energy supplied at the target. In all seven archived matrices,
`d < tau < a`, so attenuation requires `bc < 0`. Six matrices have the
opposite sign. The only sign-compatible point, `sigma=1e-3`, supplies just
`5.5894e-5` of the required product. Across all seven scales the magnitude
coverage is below `0.135`, and its maximum occurs with the wrong sign.

At `sigma=1e-4`,

```text
tau                         = 1.1634451595e-2
a                           = 2.2879369039e-2
d                           = -2.4035474851e-7
bc                          = 2.0772389503e-9
p_req                       = -1.3083115047e-4
bc / p_req                  = -1.5877250509e-5
|tau-d| / |tau|             = 1.0000206589
local Schur one-step radius = 0.7897058595
physical bulk radius        = 0.7570230790
```

Thus the scalar local dark profile is neither resonant nor strong enough to
close the physical gap. Perron/parity extraction and biorthogonalization do
not change this conclusion. A three-density recomputation at
`n*sigma = 10.24, 15.36, 20.48` preserves the relevant coupling signs at
`sigma=1e-3` and `1e-4`.

This is a local no-go result, not a no-go result for complement self-energy.
An exact nested Schur identity shows how an external complement `E` replaces
`a,b,c,d` by spectral-parameter-dependent entries involving
`(zI-E)^{-1}`. That larger resolvent can provide a different sign, a nearby
pole, or a direct bright--external--bright excursion. It is the next
falsifiable operator target.

Run the tests and regenerate the archived-data audit with:

```bash
/root/math/.venv/bin/pytest -q
PYTHONPATH=src /root/math/.venv/bin/python \
  experiments/run_dark_schur_audit.py
```

Rebuild the six sparse resolution checks with:

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=16 /root/math/.venv/bin/python \
  experiments/run_dark_schur_audit.py --rebuild-resolution
```

Build the manuscript with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
