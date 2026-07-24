# TPC-88: Two-level mass--cancellation factorization

This paper separates the TPC determinant-flatness statistic into two
exactly defined levels.

For a finitely supported complex coefficient \(a=(a_n)\), write

\[
Z=\sum_n a_n,\qquad
M=\sum_n|a_n|,\qquad
D=\sum_n|a_n|^2.
\]

For \(a\ne0\), define

\[
\mathfrak c=\frac{|Z|}{M},\qquad
S_{\mathrm{eff}}=\frac{M^2}{D},\qquad
\mathfrak F=\frac{|Z|^2}{D}.
\]

The exact factorization is

\[
\boxed{\mathfrak F=\mathfrak c^2S_{\mathrm{eff}}.}
\]

Here \(S_{\mathrm{eff}}\) measures magnitude spreading among
post-bin determinant coefficients, while \(\mathfrak c\) measures
relative phase cancellation.

## Main results

- For a nonzero coefficient, the sharp finite range is

  \[
  (2-S_{\mathrm{eff}})_+
  \le \mathfrak F
  \le S_{\mathrm{eff}}
  \le \#\operatorname{supp}a.
  \]

- \(S_{\mathrm{eff}}\) equals the actual support size exactly for
  constant-modulus coefficients.

- \(\mathfrak F=S_{\mathrm{eff}}\) exactly when all nonzero
  coefficients have one common phase.

- The lower edge at \(S_{\mathrm{eff}}=1\) is attained by one
  coefficient; for \(1<S_{\mathrm{eff}}\le2\), it is attained by two
  nonzero antiparallel coefficients. Zero-sum configurations attain
  the zero edge.

- Identical magnitude data can have maximal or zero flatness, so
  mass--energy survival alone does not prove phase cancellation.

- For the literal fixed-\(h_0\) TPC-32 coefficient, natural post-bin
  mass survival and the TPC-83 mass--energy equivalence imply

  \[
  S_{\mathrm{eff}}(A_X)=X^{o(1)}Q_X.
  \]

- At

  \[
  Q_X=X^{267/400+o(1)},\qquad
  J_X=X^{133/400+o(1)},
  \]

  the TPC-32 threshold

  \[
  \mathfrak F_X\le X^{1/400+o(1)}
  \]

  is equivalent in the natural-mass regime to

  \[
  \frac{|Z_X|}{M_X}\le\frac{X^{o(1)}}{J_X},
  \]

  and to \(|Z_X|\le X^{o(1)}Q_X^2\).

- The exact exponent ledger reproduces the TPC-82 condition
  \(2\eta_Z\ge\lambda_D\) without double counting the post-bin mass
  exponent.

- Independently, all other physical and downstream fixed-power
  losses must satisfy
  \(\Lambda_{\mathrm{phys}}<1/400\). Equality or excess is a stop
  condition, and no loss is charged in both ledgers.

## Claim status

The finite factorization and equality cases are L0. Their literal
fixed-shift crosswalk is L1. The paper proves no natural-mass lower
bound and no new L2 Möbius cancellation estimate. It does not
specialize to \(h_0=2\), breach sieve parity, or prove a prime-pair
lower bound.

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

```text
two-level-mass-cancellation-factorization.pdf
```
