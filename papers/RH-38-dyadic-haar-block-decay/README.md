# RH-38: dyadic Haar block decay

This paper proves the analytic origin of the quarter/half scaling observed in
RH-36 and RH-37.

For a `C^2` kernel sampled by midpoint Nyström matrices, exact dyadic Haar
coordinates give

\[
\|E_h\|_2=O(h^2),\qquad
\|C_h\|_2=O(h),\qquad
\|B_h\|_2=O(h),\qquad
\|D_h\|_2=O(h^2).
\]

The manuscript proves explicit constants:

\[
\|E_h\|_2\le
\frac{h^2}{32}(M_{xx}+2M_{xy}+M_{yy}),
\]

\[
\|C_h\|_2\le\frac h4M_x,qquad
\|B_h\|_2\le\frac h4M_y,qquad
\|D_h\|_2\le\frac{h^2}{16}M_{xy}.
\]

The rates survive:

- discrete row normalization of a smooth positive raw kernel;
- subtraction of a smooth finite-rank spectral projector;
- exact operator squaring.

Thus the `1/4, 1/2, 1/2, 1/4` law is a structural consequence of Haar
cancellation, not a numerical coincidence.

## Stored physical ledger

The rigorous physical block uppers from RH-36 and RH-37 become nearly
identical after division by the predicted powers of the coarse mesh:

| block | `2048 -> 4096` | `4096 -> 8192` |
|---|---:|---:|
| `E / h^2` | 834.1513371 | 833.8864287 |
| `C / h` | 23.1863048 | 23.1884515 |
| `B / h` | 28.1039701 | 28.1057350 |
| `D / h^2` | 547.4492687 | 547.5026097 |

A componentwise floating decomposition shows the same ratios independently
for the Markov matrix `P`, peripheral projector `Q`, bulk one-step matrix
`U=P-Q`, and physical matrix `A=U^2`. The maximum deviation from exact
quarter/half scaling is `2.203e-4`.

## Exact scope boundary

The analytic theorem applies directly to full smooth midpoint kernels. The
stored model additionally uses:

- an eight-sigma hard support cutoff;
- numerically resolved peripheral projectors.

Their two finite refinement levels satisfy the law, but this paper does not
prove a uniform all-grid cutoff estimate or a validated continuum spectral
projector theorem. It also does not control the multilevel nonnormal resolvent
recursion. Those are the next gates.

No zero-noise, zeta-zero, Hilbert--Pólya, or Riemann-hypothesis claim is made.

## Verification

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python experiments/build_decay_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf dyadic-haar-block-decay.pdf
PYTHONDONTWRITEBYTECODE=1 python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 python experiments/verify_archive.py
```

The formal manuscript is `dyadic-haar-block-decay.pdf`.
