# RH-109: exterior-power fourth-cross support

This directory contains the one-hundred-and-ninth RH-layer paper:

> *Exterior-Power Fourth-Cross Support: Finite-Memory Volume Certificates
> and a Sharp Scalar-Volume Barrier*

## Main result

For a recent projected cross with singular values `shat_j` and a certified
operator tail `delta`, define `ell_j=max(shat_j-delta,0)` and
`u=shat_1+delta`.  The full fourth-mode ratio obeys

```text
s4(K)/s1(K) >= (ell_1 ell_2 ell_3 ell_4) / u^4.
```

This is the normalized spectral four-volume certificate.  If only the
reduced symmetric moment `e4` is used at packet rank `r`, then

```text
s4(K)/s1(K) >= sqrt(e4(ell_1^2,...,ell_r^2) / binom(r,4)) / u^4.
```

The binomial factor is essential: for `r>4`, `e4(K*K)` is the trace of the
fourth exterior Gramian, not its largest eigenvalue.  At rank four both
quantities reduce to `det(K*K)`.

## Five-scale result

At depth five and `eta=1/512`:

- the spectral exterior certificate covers all `78/78` fine updates at
  `tau=1e-8`;
- it covers `72/78` at `tau=1e-6` and `55/78` at `tau=1e-4`;
- the trace-`e4` certificate covers `78/78`, `65/78`, and `42/78`;
- the minimum fine spectral lower bound is `5.1091096e-8`;
- the minimum fine trace lower bound is `1.3191664e-8`;
- the minimum observed volume-loss factor
  `(s2/s1)(s3/s1)` is `5.2335553e-5`.

Thus exterior volume gives a complete fine certificate at `1e-8`, but it
does not reproduce the stronger direct Weyl certificate at the two larger
thresholds.

## Exact boundary

Writing `q=s4/s1` and `nu=(s1 s2 s3 s4)/s1^4`, one always has the sharp
interval

```text
nu <= q <= nu^(1/3).
```

Two trace-one source-seeded memory families have the same `nu`, memory
clock, packet block, and complement block while attaining the two endpoints.
Hence a scalar volume alone cannot decide support in the band
`tau^3 < nu < tau`.  A continuation needs physical wedge information plus
control of the relative second/third-mode capacity, or a direct fourth-mode
transversality law.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_exterior_support_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_exterior_support_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf exterior-power-fourth-cross-support.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
