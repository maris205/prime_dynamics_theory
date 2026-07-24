# TPC-83: Post-Bin L1 Mass and Determinant-Energy Survival

This directory contains:

> *Post-Bin \(\ell^1\) Mass and Determinant-Energy Survival at a
> Fixed Shift: Sharp Two-Sided Exponent Transfer for the Matched
> Shell*.

## Main result

For the actual TPC-32 determinant coefficient

\[
A_X(n)=A_{C_X}(n),\qquad C_X=\lfloor J_X\rfloor,
\]

write

\[
N_{0,X}=J_XQ_X^2,\quad
S_X=\#\operatorname{supp}A_X,\quad
L_X=\|A_X\|_\infty,\quad
M_X=\|A_X\|_1,\quad
D_X=\|A_X\|_2^2.
\]

Every finite sequence satisfies

\[
\frac{M_X^2}{S_X}\le D_X\le L_XM_X.
\]

The verified matched-shell bounds

\[
S_X\ll Q_X,\qquad
L_X\ll X^{o(1)}\frac{N_{0,X}}{Q_X}
\]

therefore give the sharp exponent transfers

\[
M_X\ge X^{-\mu+o(1)}N_{0,X}
\Longrightarrow
D_X\ge X^{-2\mu+o(1)}
\frac{N_{0,X}^2}{Q_X},
\]

and

\[
D_X\ge X^{-\lambda+o(1)}
\frac{N_{0,X}^2}{Q_X}
\Longrightarrow
M_X\ge X^{-\lambda+o(1)}N_{0,X}.
\]

Consequently, subpower survival of the natural determinant energy is
equivalent to subpower survival of the actual post-bin \(\ell^1\)
mass. Natural energy also forces

\[
S_X\ge X^{-\lambda-o(1)}Q_X.
\]

The mass-to-energy exponent is sharp. The reverse mass and support
exponents are sharp in the nontrivial range
\(X^{-\lambda}Q_X\to\infty\), in particular throughout the physical
endpoint range \(\lambda<1/400\).

## Scope

- \(M_X\) is the \(\ell^1\) norm after all literal contributions in
  each determinant bin have been summed.
- A pre-bin raw absolute mass, the TPC-32 absolute majorant, or a sum
  of channelwise absolute values can upper-bound \(M_X\), but cannot
  lower-bound it.
- This paper proves an exact L0 theorem and closes an L1 equivalence
  for the actual fixed-\(h_0\) matched coefficient.
- It does not prove a lower bound for \(M_X\) or \(D_X\), so it
  supplies no unconditional L2 arithmetic input.
- It does not control the distinguished zero frequency.
- The complete physical fixed-power loss must remain strictly below
  `1/400`; stop at or above `1/400`, including equality.

## Claim boundary

The paper proves no fixed-\(2\) estimate, no fixed-shift Mobius
cancellation theorem, no parity breakthrough, no prime-pair lower
bound, and no twin-prime conclusion.

## Build

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archival filename is
`post-bin-l1-determinant-energy-equivalence.pdf`.
