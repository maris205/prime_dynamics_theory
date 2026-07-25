# TPC-93: Literal Low-Window Affine Export

This paper completes TPC-92 Deliverable 1A at the representation
level. It exports the full TPC-86 multiplier-weighted low-frequency
window of the literal TPC-32 determinant coefficient into the native
TPC-33 affine variables.

## Main exact results

1. **Row-native low window.** The coherent sum over every
   \(0<d_{q_X}(r,0)\le R_X\), with the actual zero-arc multiplier, is
   written as one kernel evaluated at the exact normalized
   determinant of every physical atom.

2. **Decorated affine-column theorem.** The TPC-33 pointwise
   reflection and actual-mask projector remain exact after adding the
   small-content determinant character. An explicit source-to-child
   construction gives one child for each projector divisor
   \(v\mid(d,e)\), and the displayed inverse reconstructs the original
   row, opened ultra divisor, polarization, and interval component.
   The weighted child multiplicity reassembles the exact row-gcd mask;
   it is not treated as an assumed “lossless ledger.”

3. **Exact-content expansion.** For exact content \(c\) and projector
   variable \(\kappa\), the native divisibility condition is
   \(c\kappa\mid \sigma U(t)\), and the phase remains
   \(e_{cq_X}(-r\varepsilon_\theta(M(t)-n))\), where
   \(\varepsilon_\theta=+1\) on the left polarization and \(-1\) on
   the right.

4. **Content-factor extraction.** With
   \[
   B=\frac{c\kappa}{(c\kappa,\sigma)},
   \]
   the divisibility condition gives \(t=\tau+Bz\) and
   \(U(\tau+Bz)=B V(z)\). The unreduced pair has determinant
   \(Bh_0\), but after exact extraction the pair
   \[
   D(\tau+Bz),\qquad V(z)
   \]
   has determinant exactly \(h_0\). On the nonzero Mobius support the
   extraction contributes
   \[
   \mu(B)\mathbf 1_{(B,V)=1}.
   \]
   These factors cannot be dropped.

5. **Complete sector partition.** Every resolved term belongs to
   exactly one of:

   - short fibers;
   - long resonant fibers with
     \[
     N\left\|\frac{r\ell v\sigma B}{cq_X}\right\|\le1;
     \]
   - long generic fibers.

   No resonant, bounded-fiber, content, frequency, or polarization
   sector is deleted.

## Proof-level status

- The finite Fourier, projector, progression, determinant, Mobius,
  and partition statements are **L0**.
- Their exact attachment to the literal fixed-\(h_0\) coefficient is
  **L1**.
- No new **L2** cancellation estimate is proved.

In particular, the paper does not prove a zero-mode upper bound,
determinant-energy lower bound, parity breakthrough, prime-pair lower
bound, or the twin-prime conjecture. Nothing is specialized to
\(h_0=2\).

## Build

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The final archived PDF name is:

`literal-low-window-affine-export.pdf`

## Finite regression certificate

The standard-library script
`experiments/verify_literal_export.py` checks the literal finite
identities on deterministic small instances:

- both source polarizations and source↔child reconstruction;
- projector multiplicity and Möbius-sign reassembly;
- determinant orientation and phase-compatible content inversion;
- progression resolution, the \(Bh_0\to h_0\) reduction, the required
  \(\mu(B)\mathbf 1_{(B,V)=1}\) factor, and the resolved phase.

Run:

```bash
python experiments/verify_literal_export.py
```

The checked instances are a regression certificate for the algebraic
implementation only. They are not numerical evidence for an L2
cancellation estimate.
