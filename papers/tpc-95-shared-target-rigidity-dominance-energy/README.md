# TPC-95: Shared-target rigidity and dominance energy

Paper title:

> *Shared-Target Rigidity and Dominance Energy in Fixed-Shift
> Determinant Fibers: Sharp Phase Envelopes, Compressed Census
> Identities, and a Loss-One Coherence Barrier*

## Main results

- Proves the sharp modulus-only determinant-energy certificate
  \[
  D\ge D_{\rm dom}
  :=\sum_n(2r_{\max,n}-R_n)_+^2.
  \]
  With the determinant fibers and native moduli fixed, this is the
  exact minimum over all free phase assignments.
- Determines the complete free-phase interval of equal-determinant
  coherence:
  \[
  [D_{\rm dom}-E_{\rm trip},
    \sum_nR_n^2-E_{\rm trip}].
  \]
- Gives a dominant-fiber sufficient condition with an explicit
  exponent transfer. This implication still requires a genuine raw
  mass lower bound and a quantified dominant share.
- Proves canonical-parent composite uniqueness: one normalized
  determinant and the two ordered complete targets identify the
  native row--orbit key.
- Proves that two distinct equal-determinant canonical parents share
  at most one complete target, including left--right cross-sharing.
- Gives an exact compressed target-correlation formula and an exact
  degree identity using the target groups `(nu, side, target)`.
- Proves that every target group is divisor-bounded, so the complete
  shared-target graph has subpower degree.
- Deduces the unconditional upper bound
  \[
  |C_{\rm tar}|
  \le X^{-1+o(1)}Q^3J^2.
  \]
  Therefore, conditional on any future determinant-energy lower bound
  with a fixed loss `lambda_D < 1`, shared-target coherence is
  `|C_tar| = o(D)` and cannot carry the main term.

## Exact boundary

The paper contains `L0` finite geometry and an `L1` crosswalk to the
literal fixed-`h0` carrier. It proves no lower bound for raw mass,
post-bin mass, dominance energy, or the actual determinant energy. It
also proves no zero-mode estimate and no new `L2` growing arithmetic
theorem.

The conclusion `|C_tar| = o(D)` is made only under a future lower bound
for `D` with fixed `lambda_D < 1`. Without that hypothesis, the paper
asserts only the absolute loss-one upper bound for `C_tar`.

The canonical-parent premise is mandatory: computational expansion
children are inverse-aggregated before composite uniqueness, group
degree, or coherence is computed. Numerical equality of two
coefficients on different targets is not a full physical duplicate.

All results preserve one prescribed nonzero `h0`, exact native keys,
actual targets and support, and the original global normalization. No
result is specialized to `h0 = 2`.

## Files

- `main.tex` and `sections/*.tex`: paper source.
- `references.bib`: bibliography.
- `experiments/tpc95_certificate.py`: exact finite regression of the
  composite-key, one-collision, compressed-correlation, degree, and
  dominance-energy identities.
- `shared-target-rigidity-dominance-energy.pdf`: compiled paper.

## Compile

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Regression

```bash
python experiments/tpc95_certificate.py
```
