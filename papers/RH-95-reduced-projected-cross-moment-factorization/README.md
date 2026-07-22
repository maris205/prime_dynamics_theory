# RH-95: reduced projected-cross moment factorization

This directory contains the ninety-fifth RH-layer paper:

> *Reduced Projected-Cross Moment Factorization: Exact Small-Matrix Closure and a Weak-Mode Conditioning Barrier*

## Main result

For an orthonormal packet V and a positive Gramian G, let

    A = V* G V,
    K = (I - V V*) G V.

Then

    K* K = V* G^2 V - A^2,

and, with `N = K* G K`,

    N = V* G^3 V - (V* G^2 V) A - A (V* G^2 V) + A^3.

An `r x r` spectral factorization of `K* K` reconstructs the selected left
cross directions, while `A`, `K* K`, and `N` determine the full `(r+k)` Ritz
compression. Thus an ambient cross SVD is unnecessary in exact arithmetic.

The 384-bit endpoint audit reveals the numerical boundary. Across 120 updates:

- QR-stabilized reduced reconstruction matches the ambient-SVD tail within
  `5.29e-7` relatively and preserves all ten RH-94 endpoint gates;
- five updates have `s_4(K)/s_1(K) < 1e-8`, reaching `2.77e-11`;
- raw inverse-singular-value reconstruction loses orthogonality in eight
  updates;
- the binary64 moment-only compression fails the `1e-3` relative criterion in
  fifty updates.

The exact reduction is therefore valid, but a moment-only binary64
implementation is not. The next layer must quotient or control weak cross
modes rather than invert them blindly.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_reduced_cross_factorization_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_reduced_cross_factorization_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf reduced-projected-cross-moment-factorization.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
