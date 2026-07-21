# TPC-48: Critical Orbit Tiling and an All-Band Actual-Coefficient Large-Sieve Reduction

This paper advances the TPC-47 single-band analysis to an exact tiling
of the entire orbit-frequency quotient. It proves both a positive
all-band reduction and the sharp boundary of what orbit Parseval alone
can deliver.

## Main results

- The quotient circle is partitioned into \(L\) orthogonal
  residue-comb bands, each with exact finite-window trace \(N/L\).
- Every determinant modulation has an exact input-output channel
  decomposition. At \(L\asymp J\) and \(m\asymp M\), each resonance
  branch has half-width
  \[
  (LH_0m)^{-1}=X^{-1+o(1)}.
  \]
- The channel-lift norm squared is exactly the maximal pointwise tube
  multiplicity. After channel labels are erased, arbitrary independent
  orbit inputs still have synthesis norm squared exactly \(K\). Thus
  all-band Parseval alone is not an atomic large sieve.
- Actual projective layers have one common smooth orbit profile. This
  yields the Hilbert-valued factor
  \[
  D_J(t;K)=\min\{K,1+(Jt)^{-1}\},
  \qquad t=\|\alpha\|_{\mathbb T}>0,
  \]
  under an explicit no-wrap condition. The factor is sharp up to
  constants for dense common-profile slope blocks.
  At \(t=0\), the definition is \(D_J(0;K)=K\).
- Exact signed reassembly reduces the full actual frozen residual
  family to a projective \(m\)-square envelope. At fixed \(m\), distinct
  cofactors give an exact \(r\)-square decomposition, while the prime
  sum inside each residual coordinate remains coherent.

At the inherited endpoint
\[
M=X^{267/400+o(1)},\qquad J=X^{133/400+o(1)},
\]
the dense-box coarse-edge collision factor is
\(X^{67/200+o(1)}\). It exceeds the inherited allowance
\(X^{1/400+o(1)}\) by the exact exponent \(133/400\). This is a sharp
model frontier, not a lower bound for the actual slope support.
Relative to any fixed projective representation with a bounded
envelope, the intermediate annulus has only logarithmic integrated
resonance cost.

## Claim boundary

Only the intercept \(h=h_0\) is the inherited physical residual
synthesis. Other shifts belong to a frozen algebraic extension. The
paper does **not** prove an atomic-normalized fixed-shift estimate,
control of the projective envelope, internal prime cancellation,
residual grouping by \(X^{o(1)}\), alias unfolding, a parity-barrier
breach, or the twin-prime conjecture.

## Exact certificate

Run from this directory:

```powershell
python experiments/tpc48_certificate.py
```

The committed record contains 68,662 exact deterministic checks.

- Semantic digest:
  `da179eb730da85c38af54f73ebf2151aece5562db62bc5fb24e2bad81d77456e`
- Normalized source SHA-256:
  `ead2a9584cd3680ce0c1f770dcec3058b3436ce5dfdecc1a0fcb3858cf067f64`
- JSON SHA-256:
  `7e4ed4d83c5e00e441f3d8ee7aa1a6d9b00a37f975af2e673a743c0c83c72882`

The finite cyclic model is a regression certificate and exact analogue;
it is not a proof of the continuous asymptotic theorem.

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Next gate

The remaining object is a projective \(m,r\)-square of coherent prime
sums. A next step must either prove coefficient-specific cancellation,
compare the projective envelope with the atomic diagonal, control the
literal residual grouping, or give a sharp actual-coefficient
counterexample showing that one of those comparisons is impossible.
