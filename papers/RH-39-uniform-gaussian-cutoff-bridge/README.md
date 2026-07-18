# RH-39: uniform Gaussian cutoff bridge

This paper closes the hard-cutoff gate left open by RH-38 at the
exact-real folded Markov-kernel level.

For the archived support rule

\[
H_h=\lceil L\sigma/h\rceil+2,
\]

every omitted midpoint is at least `H_h h` from the folded center. Gaussian
lattice tails and the exact twice-the-tail row identity give explicit bounds

\[
\|P_h^{(L)}-P_h\|_\infty\le 2Q_h,
\qquad
\|P_h^{(L)}-P_h\|_2\le\varepsilon_h.
\]

## Main conclusion

A fixed support multiple has a tiny but positive full-kernel row defect. For
`L = 8` and `sigma = 1e-2`, the zero-mean continuum omitted mass is

```text
1.2441921148543568e-15.
```

Thus fixed eight sigma does not converge to the full Gaussian operator in
row norm. The adaptive schedule

\[
L(h)=\max\{5,2\sqrt{\log(1/h)}\}
\]

instead gives

\[
\varepsilon_h=O\!\left(h^2(\log(1/h))^{-1/4}\right),
\]

which preserves all four RH-38 Haar rates.

At dimensions `2048`, `4096`, and `8192`, 256-bit Arb evaluation gives

| dimension | analytic two-norm upper |
|---:|---:|
| 2048 | `1.2508682179e-13` |
| 4096 | `1.5270216701e-13` |
| 8192 | `1.6698632393e-13` |

The largest induced Haar cutoff upper divided by a floating stored Markov
block norm is `3.576e-9`. Eight sigma also exceeds the sufficient adaptive
schedule through dimension `floor(exp(16)) = 8,886,110`.

## Scope boundary

The theorem concerns exact-real matrices using the archived support pattern.
It does not enclose every binary64 `exp`, `logaddexp`, or row-normalization
operation used to construct the committed sparse arrays. It also does not
validate the dimension-dependent Perron/parity projectors or control the
multilevel nonnormal resolvent recursion.

## Fast verification

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python experiments/build_cutoff_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf uniform-gaussian-cutoff-bridge.pdf
PYTHONDONTWRITEBYTECODE=1 python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 python experiments/verify_archive.py
```

The floating three-grid pilot can be regenerated with

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
PYTHONDONTWRITEBYTECODE=1 python experiments/run_cutoff_pilot.py
```

The formal manuscript is `uniform-gaussian-cutoff-bridge.pdf`.
