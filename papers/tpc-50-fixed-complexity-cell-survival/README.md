# TPC-50: Fixed-complexity cell survival

This paper resolves the static weighted-survival subgate for the
identified nondegenerate direct opposite-row cells left by TPC-49,
while showing exactly why the older upper-only interface could not
resolve even that subgate.

The key order of operations is canonical: split the fixed residue and
real-axis Mellin factors first, and leave the literal static mask intact.
The final TPC-47/48 projective parameter already contains a signed
Fourier/Ferrers/gcd decomposition of the mask and is not a
representation-independent physical cell.

## Main results

For a binary mask \(M\) and nonzero right weight \(b\), define

\[
\eta_M(b)
=
\max_\alpha
\frac{\sum_{\gamma:M(\alpha,\gamma)=0}|b_\gamma|^2}
     {\|b\|_2^2}.
\]

The paper proves the exact minimax identity

\[
\inf_{a\ne0}\delta_w(M;a,b)=1-\eta_M(b).
\]

Thus \(\eta_M\) is the necessary and sufficient one-sided
anti-concentration condition for survival uniformly over arbitrary
pruning of the other row.

For the literal TPC static mask, it is bounded by three explicit
concentrations:

- mass on one prime-source fibre;
- mass in one product window of width
  \(\Delta=QX^{-\kappa_0}\);
- mass on rows having gcd greater than \(G=X^{\kappa_0}\) with one
  divisor row.

After unpacking the actual fixed-complexity provenance, every identified
nondegenerate direct opposite-row pre-mask cell has the form

\[
b_{\ell,d}
=c(\log\ell)^e\psi(\ell/L)\omega(d/D)
\mathbf1_{(\ell,d)\bmod q\in\mathcal A}
\chi(\ell,d)\ell^{it_1}d^{it_2},
\qquad e\in\{0,1\},
\]

where \(q\) and the smooth shapes are fixed, the residue set is locally
admissible, and the Fourier/Mellin factors have unit modulus.
The identified direct opposite-row factor has \(e=0\); \(e=1\) is the
separately restricted source-factor variant with the physical prime
logarithm.
Fixed-modulus prime and squarefree counts give

\[
\operatorname{Flat}(b)
=\frac{N\|b\|_\infty^2}{\|b\|_2^2}
=O(1)
\]

uniformly in the real Mellin parameters. Therefore, for every nonzero
weight \(a\) on the other side, however sparse,

\[
\delta_w(M_X;a,b)
=
1-
O\!\left(
L^{-1+o(1)}
+D^{-1+o(1)}
+X^{-\kappa_0+o(1)}
\right)
=1-o(1).
\]

This physical identification is nonvacuous at the inherited endpoint:
the opened-divisor cutoff has exponent \(23/120\), exceeding the divisor
cell exponent \(10049/52500\) by exactly \(9/35000\). Hence the complete
dyadic interval lies below the hard cutoff for all sufficiently large
\(X\).

For the specified TPC-36 mask representation,

\[
\frac{
\mathcal E_{\mathscr R_{36}}(M_X;a,b)^2
}{
\|D_aM_XD_b\|_{S_2}^2
}
\le X^{o(1)}.
\]

Hence this separated static row-output face has loss exponents
\(\varpi=\theta=0\): active-cell survival consumes no polynomial part
of the isolated \(1/400\) allowance.

An additional energy-selection theorem handles boundary atoms of a
subpower-size bounded-overlap smooth frame. All energetic cells have
survival \(1-o(1)\), while the discarded cells carry only \(o(1)\) of
the aggregate cell energy. This is not a lower frame theorem for the
signed Mellin reassembly.

## Sharp upper-interface obstruction

The upper-only TPC-45/48 interface admits three polynomial-size packets
with zero survival:

- a single-source packet of size
  \(X^{10049/52500+o(1)}\);
- a near-product packet of size
  \(X^{267/400-\kappa_0+o(1)}\);
- a large-gcd packet of the same size.

Adding one admitted neighbor makes the masked tensor nonzero and gives
the exact value

\[
\delta_w=\frac1{|S|+1}.
\]

When \(\kappa_0=1/400\), the near and gcd examples have survival
\(X^{-133/200+o(1)}\), far below the isolated-face target. These are
logical countermodels to the upper-only interface, not literal TPC
coefficients: they require a moving prime, a power-shrinking window, or
a growing residue modulus.

## Claim boundary

The paper proves a theorem for the displayed canonical pre-mask weight
class on the complete prime-squarefree row universe, and identifies the
nondegenerate direct opposite-row packets whose fixed provenance lies in
that class. It does not silently replace an arbitrarily terminal-pruned
TPC-48 row support by the complete universe.
For a newly pruned packet, the three displayed concentration quantities
must be checked again.

The following gates remain open:

- lower-frame or no-cancellation control for the signed continuous
  Mellin reassembly;
- comparison of the full TPC-48 Banach profile envelope with the
  physical atomic diagonal;
- the coherent prime square at fixed source and residual coordinate;
- residual grouping under \(s=d(m)r\);
- localization of the frozen determinant family back to the physical
  shift \(h_0\);
- comparison with the native affine physical Gram face;
- the remaining slope-collision and endpoint budget.

No fixed-shift Chowla theorem, parity-barrier breach, Hardy--Littlewood
asymptotic, or twin-prime conclusion is claimed.

## Exact certificate

Run from this directory:

    python experiments/tpc50_certificate.py --check

The committed record contains 1,469,068 exact deterministic checks.

- Semantic SHA-256:
  b01a3c4ede8b20090e904d7f93cd29174f2d8bb46b294f9fc02d988e398786cf
- Normalized source SHA-256:
  8ad51dbe7dd900c993a616968111077ef9d55485e2d457239d314d31ee908915
- JSON SHA-256:
  f4f7cd5abb63a8919f7594ecee2c23d189ea07109906f069aab2112411d9393b

The certificate uses exact integers, rationals, and Gaussian unit
phases. It is a regression certificate, not a proof of the asymptotic
prime/squarefree estimates and not a search for prime pairs.

## Build

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex

## Next gate

The closest continuation is representation-frame efficiency: replace
the signed Mellin \(L^1(d|\nu|)\) envelope by a Bessel/frame comparison
with the reassembled physical Hilbert energy, or prove a sharp
condition-number obstruction. The independent arithmetic continuation
is the coherent prime square retained inside each residual coordinate.
