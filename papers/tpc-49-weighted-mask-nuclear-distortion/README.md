# TPC-49: Weighted mask survival and nuclear distortion

This paper resolves the finite-dimensional core of the
projective-to-atomic gate left by TPC-48. It gives an exact positive
criterion, proves sharp counterexamples to support-only reasoning, and
keeps the full prime/cofactor and fixed-shift boundaries explicit.

## Main results

- For a genuinely Hilbertized coefficient tensor \(T\), the optimal
  rank-one projective envelope is exactly the nuclear norm, while the
  atomic energy is the squared Frobenius norm:

  \[
  \mathcal E_{\rm pr}(T)=\|T\|_{S_1},\qquad
  \mathcal D_{\rm at}(T)=\|T\|_{S_2}^2.
  \]

  The exact intrinsic energy distortion is

  \[
  r_{\rm nuc}(T)=
  \frac{\|T\|_{S_1}^2}{\|T\|_{S_2}^2}.
  \]

- A fixed signed representation has an independent cancellation
  condition number \(c_{\mathscr R}\), with the exact ledger

  \[
  \frac{\mathcal E_{\mathscr R}(T)^2}
       {\mathcal D_{\rm at}(T)}
  =c_{\mathscr R}(T)^2r_{\rm nuc}(T).
  \]

  Adding cancelling layer pairs makes a uniform comparison over all
  exact representations impossible.

- For a weighted mask \(A=D_aKD_b\), let

  \[
  \delta_w=
  \frac{\|A\|_{S_2}^2}{\|a\|_2^2\|b\|_2^2}.
  \]

  Then

  \[
  r_{\rm nuc}(A)
  \le
  \min\left\{\operatorname{rank}A,
  \frac{\|K\|_{\pi,\infty}^2}{\delta_w}\right\}.
  \]

  A permutation mask attains the density bound exactly, so bounded
  projective cost one alone gives no dimension-free atomic estimate.

- On the complete dyadic row universe, the complete-universe extension
  of the literal TPC-36 static-mask formula has every row and column of
  admitted degree \((1-o(1))N\). A specified explicit TPC-36
  representation therefore has only \(X^{o(1)}\) energy distortion for
  this complete formula model.

- The same admitted graph contains a perfect-matching permutation
  packet with distortion

  \[
  N=X^{267/400+o(1)}.
  \]

  This packet is supported in genuine allowed mask positions but is not
  the literal physical coefficient. It proves that support and soft
  projective complexity are insufficient for arbitrary supported
  coefficients.

- Ferrers masks have

  \[
  r_{\rm nuc}(T_n)
  =\frac{2}{\pi^2}(\log n)^2+O(\log n),
  \]

  so signed Ferrers separation costs only \(X^{o(1)}\) energy on
  polynomial scales.

At the endpoint, if

\[
c_{\mathscr R}=X^{\chi+o(1)},\qquad
r_{\rm nuc}=X^{\rho+o(1)},
\]

then, if the entire endpoint allowance is assigned to this isolated
Hilbertized face, its exact face-budget target is

\[
2\chi+\rho\le\frac1{400}.
\]

This is not an if-and-only-if criterion for full TPC-48 closure: any
other coefficient-specific losses must share the same \(1/400\) exponent
budget.

For a soft bounded-projective representation, the computable sufficient
condition is \(\delta_w\ge X^{-1/400+o(1)}\).

## Claim boundary

The complete dyadic mask theorem is not automatically a theorem for an
arbitrarily pruned active joint-multiplier cell. The current inherited
interface does not provide weighted lower density, row-weight flatness,
or a frame bound for the signed residue/Mellin layers.

The paper does **not** identify the full TPC-48 Banach profile envelope
with a nuclear norm, compare its coherent prime square with the
fixed-\(h_0\) atomic diagonal, control residual grouping, unfold sparse
aliases, or localize the completed frozen field to the physical shift.
It proves no parity-barrier breach or twin-prime conclusion.

## Exact certificate

Run from this directory:

```powershell
python experiments/tpc49_certificate.py
```

The committed record contains 298,427 exact deterministic checks.

- Semantic digest:
  `20c576cf7e27e0cec91cce677395a02110b857f1db53dd161f2cc12068bac3a4`
- Normalized source SHA-256:
  `4176a42c73c01d0b68532e1dfde30974f61f162309dcd5e001a087c0fcd9e580`
- JSON SHA-256:
  `c92af6a6cf82a23a388253fd42dd9cd3c6732a37964b228cce1abfb742cb6534`

The certificate uses exact integers, rationals, and finite fields. It is
a regression certificate, not a proof of the asymptotic theorem and not
a search for literal prime-pair atoms.

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Next gate

The closest continuation is to prove weighted survival and frame
efficiency for the literal active residue/Mellin cells. The independent
arithmetic gate remains the coherent prime square inside each residual
coordinate; localization and residual grouping remain downstream.
