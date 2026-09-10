# Exact full-range Kloosterman emitter and the short-array obligation

Date: 2026-09-09. Parent integration of the Franklin derivation.
Status: original derivation and integrated E1--E6 passed independent scoped
audit; precision corrections are implemented. Exact interface, no arithmetic saving.
Source object, fixed \(h_0=2\), \(I_x,Q,H,U,z\), masks, signs and kernel
are those in DERIVATION_PACKAGE.md.

## E1. Literal packet and finite Fourier emission

Fix an original ordered block pair \((b,c)\), and write
\(a^{(j)}(t)=\eta_b(t)\beta(t)+i^j\eta_c(t)w(t)\), \(j=0,1,2,3\).
For each \(q\in\mathcal Q\) and real \(v\), set
\[
 F^{(j)}_r=\sum_{t\in I_x,\ t\equiv r(q)}a^{(j)}(t)e(vt/H),
 \quad
 F^{(j),0}_r=F^{(j)}_r-\frac1{q-1}\sum_{s\ne0}F^{(j)}_s
 \quad(r\ne0).
\]
Extend \(F^{(j),0}\) by zero at residue 0. Its total sum is zero.
For \(1\le m,n<q\), define
\[
 \alpha^{(j)}_m=\frac1q\sum_{r\ne0}F^{(j),0}_r e_q(-mr),
 \qquad
 \gamma^{(j)}_n=\frac1q\sum_{r\ne0}\overline{F^{(j),0}_r}
                                      e_q(-n\overline r).
\]
With the unnormalized \(S(m,n;q)=\sum_{r\ne0}e_q(mr+n\overline r)\),
\[
 \mathcal B_j=\sum_{m,n=1}^{q-1}
                 \alpha^{(j)}_m\gamma^{(j)}_nS(m,n;q)
             =\sum_{r\ne0}|F^{(j),0}_r|^2.             \tag{E1}
\]
Proof: the two omitted zero frequencies vanish. Fourier inversion returns
\(F^{(j),0}_r\) and \(\overline{F^{(j),0}_r}\), respectively, when
\(S\) is opened. Every unit \(r\) occurs once.

The physical packet coefficients, including \(\mu(d)\), the prime-power
term, the shifted \(\Lambda\), and the literal hybrid, all remain inside
\(F^{(j)}\). In the divisor component \(t=dk\), one has \(d\le U<q\),
so \(k\equiv r\overline d\pmod q\); the block length in \(k\) is \(O(H/d)\).
This algebra does not turn the prime component into a smooth coefficient.

## E2. Exact signed diagonal subtraction

Let
\[
 d_j(q)=\frac{q-2}{q-1}
       \sum_{t\in I_x,\ q\nmid t}|a^{(j)}(t)|^2 .
\]
Then the original block-pair contribution is
\[
 C_{bc}=\sum_{q\in\mathcal Q}q\int\psi_+(v)
              \frac14\sum_{j=0}^3i^j[\mathcal B_j-d_j(q)]\,dv. \tag{E2}
\]
This follows from V59 (4.2)--(4.4), with \(q\) still outside.
The product \(e(vt/H)e(-vu/H)\) integrates to \(K_H(u-t)\).
The diagonal is subtracted before taking absolute values. Summing all
original ordered \((b,c)\) pairs gives \(\mathfrak C_x\) exactly.

The four separate positive packets are not the consumed scalar.
Self-terms cancel only after the signed polarization. Nor may block
separation decay of the integrated mixed expression be assigned to each
positive packet before that cancellation.

## E3. Exact full-length saturation

Parseval gives
\[
 \|\alpha^{(j)}\|_2^2=\|\gamma^{(j)}\|_2^2
      =q^{-1}\|F^{(j),0}\|_2^2,\qquad
 \mathcal B_j=q\|\alpha^{(j)}\|_2\|\gamma^{(j)}\|_2.     \tag{E3}
\]
Thus every nonzero unsubtracted packet saturates its full-array norm scale.
The emitted array range is \(q-1\), not \(q^{1/2}\). This is a limitation
of this full-range representation and does not prohibit cancellation
in E2.

A centered test vector \(F=e_1-e_2\) has
\(\alpha_m=q^{-1}(e_q(-m)-e_q(-2m))\ne0\) for all \(1\le m<q\).
This shows that centering alone supplies no support compression; it is an
interface example, not a statement that the physical lane equals this vector.

### E3a. Residual-sensitive value-level compression obstruction

For one nonzero unsubtracted packet put
\(P=\|\alpha\|_2\|\gamma\|_2\), so \(\mathcal B=qP\).
Suppose \(qP=\sum_\nu\lambda_\nu\mathcal B_q(A_\nu,B_\nu)+R\), with
every rectangle satisfying the critical BP hypotheses below, and let
\(T=\sum_\nu|\lambda_\nu|\|A_\nu\|_2\|B_\nu\|_2\).
Triangle and BP imply, for each fixed \(\epsilon>0\),
\[
 |qP-R|\le C_\epsilon q^{31/32+\epsilon}T,\qquad
 T\ge C_\epsilon^{-1}q^{1/32-\epsilon}P
                \left(1-\frac{|R|}{qP}\right)_+ .
\]
Thus a fixed \(|R|\le\theta qP\), \(0\le\theta<1\), rules out
\(T\ll q^{1/32-\kappa}P\) for any fixed \(\kappa>0\), by choosing
\(\epsilon<\kappa\). It does not rule out every logarithmic improvement,
and gives no exact epsilon-free \(q^{1/32}\) lower bound.
This applies only to the unsubtracted packet. It is not an obstruction
theorem for the already signed, diagonal-subtracted physical remainder.

## E4. Source theorem and the naive splitting cost

[Blomer--Pascadi, Theorem 1.1](https://arxiv.org/html/2607.24311v1#Thmtheorem1)
accepts complex arrays on integer intervals of length at most \(N\le c\)
and a unit multiplier \(a\bmod c\), with \((m,n,c)=1\). At
\(N\asymp\sqrt c\) its bound is
\(c^{31/32+o(1)}\|\alpha\|_2\|\gamma\|_2\).
In E1, \(c=q\), \(a=1\), and both indices are nonzero modulo the prime,
so the gcd condition is met. Smoothness is not required by this theorem.

For \(L=\lfloor\sqrt q\rfloor\), split \(1,\ldots,q-1\) into
\(k_q=\lceil(q-1)/L\rceil\) intervals of length at most \(L\).
There are \(k_q^2\) ordered rectangles. Triangle and Cauchy--Schwarz give
\[
 \sum_{A,B}\|\alpha_A\|_2\|\gamma_B\|_2
 \le k_q\|\alpha\|_2\|\gamma\|_2 .
\]
Hence this method yields
\(q^{47/32+o(1)}\|\alpha\|_2\|\gamma\|_2\), worse than E3's exact
full-length scale by \(q^{15/32+o(1)}\). Relative to a hypothetical
single critical-array attachment, the worst-case extra norm reassembly is
\(q^{1/2}=x^{1/6+o(1)}\), far larger than the permitted \(19/2400\)
physical exponent margin. This is an upper-bound-method cost, not a
universal lower bound for every conceivable decomposition.

## E5. A sufficient new obligation, not a theorem

Define the signed integrated local remainder without outer \(q\):
\[
 E_{bcq}=\int\psi_+(v)\frac14\sum_j i^j[\mathcal B_j-d_j(q)]\,dv.
\]
One sufficient positive theorem would be a decomposition
\[
 E_{bcq}=\sum_\nu\lambda_\nu\mathcal B_q(A_\nu,B_\nu)+R_{bcq},
\]
with all array intervals of length at most \(L\), correct gcd conditions,
and, for \(\omega_{bc}=(1+|b-c|)^{-A}\), fixed \(A>2\),
\[
 \sum_\nu|\lambda_\nu|\|A_\nu\|_2\|B_\nu\|_2
       \ll\omega_{bc}(H/q)x^{\ell+o(1)},\qquad
 |R_{bcq}|\ll\omega_{bc}Hq^{-1/32}x^{\ell+o(1)}.         \tag{E4}
\]
These estimates must concern the already signed and integrated object.
Constants and \(o(1)\) must be uniform over all original block pairs and
the full prime shell for the fixed inherited profile and fixed admissible
\(K\), with no unpaid exceptional set. They do not follow from E1 or
from Schwartz decay alone.

The source theorem, outer \(q\), dyadic prime sum, and summable ordered
block weights would then give
\[
 |\mathfrak C_x|\ll xQ^2x^{-1/96+\ell+o(1)}.
\]
Thus \(\ell<19/2400\) suffices for the strict requirement \(\delta>1/400\).
This is a stated sufficient proof obligation, not an established estimate,
not a necessary representation, and not a definition of a new gate being closed.

## E6. Existing Poisson compiler is not a free second step

TPC209, paper/main.tex:156--175, already proves the exact fixed-divisor
Poisson reindexing \(Y_{q,D}=U_DB_{q,D}\). Its Sections 4--6 preserve the
relative divisor permutations and cross terms, then recover the original
nonprincipal-character interface by a Gauss transform.
Even if an individual smooth divisor strand has controlled short effective
dual support, this does not make all physical profiles common, remove the
prime component, or control the other array. Merely repeating that reindexing
would not pay the compression estimates (E4) in Section E5.

The new content of E1 is an explicit full-range Kloosterman realization.
Its norm saturation explains why algebraic emission alone is insufficient.
Current mathematical level: exact structural interface plus scoped
representation/norm obstruction; arithmetic fixed-power credit remains zero.
