# Constructive smooth partition and paid boundary remainder

Date: 2026-09-09. Unnumbered parent proof, independently audited.
Object and source clock are exactly those in DERIVATION_PACKAGE.md:
\(I_x=(x/2,x]\cap\mathbb Z\), \(x=2X\), \(Q=x^{1/3}\),
\(H=x^{21/32}\), \(U=x^{133/400}\), fixed physical shift \(h_0=2\),
fixed nonnegative compact profile, literal signed \(\beta,w\), full prime
shell, unit masks, outer \(q\), and off-diagonal deletion.

This note makes an **explicit admissible choice** at V59's partition step
(bridge_b_polarized_local_bdh_scalar_compiler.md:277). It does not assert
derivative bounds for an arbitrary previously chosen partition. The scalar
is partition-independent by V59 (5.3); a theorem stated for a different
particular partition cannot silently be transferred block by block.
No arithmetic saving for the interior scalar is proved.

## S1. An explicit admissible partition

Fix the standard bump
\[
 \chi(s)=
 \begin{cases}
 \exp[-1/(1-4s^2)],&|s|<1/2,\\
 0,&|s|\ge1/2 .
 \end{cases}
\]
It is nonnegative and \(C_c^\infty(\mathbb R)\), and it is positive on
\([-1/4,1/4]\). Let
\[
 D(s)=\sum_{j\in\mathbb Z}\chi(s-j/2),\qquad
 \eta_{j,H}(t)=\frac{\chi(t/H-j/2)}{D(t/H)}.
                                                               \tag{S1}
\]
The sum defining \(D\) is locally finite. It is smooth, \(1/2\)-periodic,
and uniformly bounded below by
\(\min_{|s|\le1/4}\chi(s)>0\), since each real number is within \(1/4\)
of a half-integer. Every derivative of \(D\) is bounded on a period, and
therefore every derivative of \(1/D\) is also bounded.

It follows that \(0\le\eta_{j,H}\le1\),
\(\sum_j\eta_{j,H}(t)=1\) for all real \(t\), and
\[
 \operatorname{supp}\eta_{j,H}
   \subset [(j-1)H/2,(j+1)H/2],\qquad
 H^r\|\eta_{j,H}^{(r)}\|_\infty\le C_r\quad(r\ge0),       \tag{S2}
\]
where \(C_r\) depends only on the fixed bump, not on \(x,H,j\).
This follows by differentiating the fixed smooth translated periodic
quotient with respect to \(t/H\). At most three closed supports overlap;
at any point at most two terms are positive. Only \(O(x/H+1)\) labels
have supports intersecting \([x/2,x]\). Thus this is a smooth
bounded-overlap partition of physical block length \(H\), as allowed by
V59. Its center spacing \(H/2\) changes separation-weight constants only.

## S2. Interior versus boundary, without a sharp-cutoff fiction

Write \(a=x/2\), \(b=x\). Let \(\mathcal J_{\mathrm{int}}\) consist of labels
whose closed supports are contained in \((a,b)\); among labels whose
supports intersect \([a,b]\), put the others in
\(\mathcal J_{\partial}\). Since each support is an interval, each
boundary support contains \(a\) or \(b\). Hence
\(|\mathcal J_{\partial}|\le6\). Define on the physical integers
\[
 \theta_\partial(n)=\sum_{j\in\mathcal J_\partial}\eta_{j,H}(n),
 \qquad \theta_{\mathrm{int}}(n)=1-\theta_\partial(n).
\]
Both weights lie in \([0,1]\), and
\[
 \operatorname{supp}_{I_x}\theta_\partial
 \subset I_x\cap([a,a+H]\cup[b-H,b]),\qquad
 |\operatorname{supp}_{I_x}\theta_\partial|=O(H+1).       \tag{S3}
\]
The interior cutoffs are genuine elements of \(C_c^\infty((a,b))\) with
the uniform derivative bounds S2. No sharp truncation is applied before
the interior Fourier argument. Boundary cutoffs are not assigned such a
property after restriction to \(I_x\); they are handled by S3 and S4.

## S3. Literal pointwise envelopes used only for the boundary cost

For each fixed \(\varepsilon>0\), the elementary divisor bound is
\(\tau(n)\ll_\varepsilon n^\varepsilon\). One proof is to use
\(k+1\le2^k\le p^{\varepsilon k}\) for primes
\(p\ge2^{1/\varepsilon}\); for the finitely many smaller primes,
\(\sup_{k\ge0}(k+1)p^{-\varepsilon k}\) is finite. Multiplication over
prime powers proves the bound with a fixed constant.

The literal beta therefore obeys
\[
 |\beta(n)|\le1+\tau(n).
\]
For \(z=(\log x)^K\ge2\), fixed \(K>0\), the recovered hybrid satisfies
\[
 0\le b_x^{(z)}(n)
 \le W_z\prod_{\substack{p\mid n\\p>z}}\frac{p-1}{p-2}
 \le W_z\,2^{\omega(n)}
 \le W_z\,\tau(n).
\]
Here \(C_z\le1\), the low-prime mask is at most 1, and the product has only
\(p>2\). The classical Mertens input already locked in LANE_NORM_PROOF.md
gives \(W_z\ll_K\log\log x\). Consequently, uniformly for \(n\in I_x\),
\[
 |\beta(n)|+|w(n)|\ll_{\varepsilon,K}x^\varepsilon
\]
after decreasing the exponent used in the divisor bound and absorbing
logarithms. These are envelopes for a norm calculation, not substitutions
in the signed scalar.

Put \(\beta_\partial=\theta_\partial\beta\),
\(w_\partial=\theta_\partial w\), and similarly for the interior weight.
S3 gives
\[
 \|\beta_\partial\|_2+\|w_\partial\|_2
        \le H^{1/2}x^{o(1)},\qquad
 \|\beta\|_2+\|w_{\mathrm{int}}\|_2\le x^{1/2+o(1)}.
\]
As everywhere here, the \(o(1)\) notation means that for every fixed
positive loss the corresponding bound holds eventually, for fixed \(K\)
and fixed profile. It is not uniform over growing \(K\).

## S4. Boundary terms are paid in the original scalar

Using the literal matrix \(A\), whose entries, signs and masks are unchanged,
write
\[
 \mathfrak C_x=w^T A\beta,\qquad
 \mathfrak C_x^{\mathrm{int}}
      =w_{\mathrm{int}}^T A\beta_{\mathrm{int}}.
\]
All coefficient vectors are real; \(A\) may be complex Hermitian for a
non-even fixed profile. The complex bilinear expression still obeys the
usual Euclidean norm bound. Exact expansion, counting the double-boundary
term once, gives
\[
 \mathfrak C_x-\mathfrak C_x^{\mathrm{int}}
   =w_\partial^T A\beta+w_{\mathrm{int}}^T A\beta_\partial.
\]
The independently audited P4 bound in PROOF_PACKAGE.md gives
\(\|A\|\ll_\psi H+Q^2\ll_\psi Q^2\) at the physical scales. Thus
\[
 \boxed{
 |\mathfrak C_x-\mathfrak C_x^{\mathrm{int}}|
 \le Q^2\sqrt{xH}\,x^{o(1)}
 =xQ^2x^{-11/64+o(1)} .}                                \tag{S4}
\]
In particular, all ordered pairs with at least one boundary label can be
removed **collectively, before taking separate packet absolute values**,
at this explicit paid cost. Neither diagonal deletion nor reduced-residue
centering has been changed. This is a boundary-support estimate, not a
saving for the whole scalar.
The removal is of the weighted packet contribution with a boundary label,
not disjoint deletion of all integer pairs in a boundary collar; no
separate absolute estimate for each polarized packet is claimed.

## S5. What this repairs, and what it does not

For this explicit admissible partition, the interior derivative hypotheses
in NEXT_ARITHMETIC_OBLIGATION.md hold by construction. Its Poisson decay
and individual-strand tail bound therefore apply to these interior
cutoffs. The boundary error S4 is smaller than the prospective critical
saving \(xQ^2x^{-1/96+\ell+o(1)}\) for
\(0\le\ell<19/2400\), since \(11/64>1/96\).
For a future interior estimate outside that benchmark, with saving
\(\delta_{\mathrm{int}}\), this argument certifies the full saving only at
\(\delta=\min(\delta_{\mathrm{int}},11/64)\). Equivalently, the general
terminal ledger includes the additional margin
\(11/64-1/400=271/1600\); it is redundant for the benchmark just stated.

This does not turn the prime components or the hybrid into smooth functions,
does not identify divisor-dependent dual profiles, does not shorten the
second array, and does not control the signed divisor reassembly or the
full residual. The exact one-short/one-complete norm obstruction remains.
A positive route still owes the literal coefficient-sensitive, two-sided
interior estimate with \(\delta>1/400\), together with Gate A.

Uniformity: all sufficiently large real \(x\), all original physical
integers, complete prime shell, fixed inherited profile and fixed \(K\),
no exceptional arithmetic set. No arbitrary-origin, maximal-prefix, or
varying-profile theorem is asserted. Terminal ledger is unchanged:
\[
 0<\eta<\min\{\eta_A,\delta-1/400,419/2400\}.
\]
Map: island 2, image Bridge A / Gate B. Formal endpoint TPC418, no new
numbered writer, no novelty claim and no publication GO. Closest source:
V59's exact pair partition and the ordinary P4 norm bound derived in this
round. The constructive partition is standard smooth analysis. The
independent round-3 audit verified S1–S5 at the stated benchmark and required
the general boundary-margin clarification implemented above.
