# Next arithmetic obligation: two-sided structure, not one-sided support

Date: 2026-09-09. Unnumbered parent derivation, independently audited.
No arithmetic saving or new paper trigger. This note isolates an alternative
short-array attempt while the main operator/emitter reviews complete.

## 1. What an interior smooth divisor strand really gives

TPC209, paper/main.tex:156, already proves
\[
 Y_{q,d}(m)=\sum_k F_d(k)e_q(-mdk)
          =\sum_{n\equiv md(q)}\widehat F_d(n/q).
\]
**Conditional smooth-strand lemma.** Assume the original interior cutoffs
extend to \(C_c^\infty((x/2,x))\), have support diameter at most \(C_0H\),
and satisfy, for every integer \(j\ge0\),
\[
 \sup_{x,b} H^j\|\eta_b^{(j)}\|_\infty\le C_j<\infty.
\]
These quantitative constants are additional hypotheses here, not supplied
by V59's qualitative smooth bounded-overlap partition statement at line 277.
Put \(F_d(s)=\eta_b(ds)e(vds/H)\). Then
\(\widehat F_d(\xi)=d^{-1}\widehat{\eta_b}(\xi/d-v/H)\).
Integration by parts, uniformly for \(|v|\le1\), gives for each fixed
\(A>0\),
\[
 |\widehat F_d(\xi)|
 \ll_{A,C_0,C_1,\ldots} (H/d)(1+|(H/d)\xi-v|)^{-A}.
\]
Thus the dual strand is concentrated, in the Schwartz-tail sense rather
than hard support, at \(|n|\ll qd/H\), with an adjustable tail allowance.
At \(d\le U=x^{133/400}\), the largest natural dual radius is
\[
 qU/H=x^{23/2400+o(1)}\ll q^{1/2}.
\]
For radii below 1, the omitted zero residue and the tails must still be
handled; "radius below 1" does not assert an exact zero vector.
More explicitly, for \(A>1\), \(T\ge2\), and \(\rho_d=qd/H\),
\[
 \sum_{|n|>T\max(1,\rho_d)}|\widehat F_d(n/q)|
       \ll_{A,C_0,C_1,\ldots}qT^{1-A}.
\]
This is an individual-strand tail estimate, not a paid residual bound for
the complete arithmetic expression. Signed representatives allow an interval
around zero with its zero coordinate omitted or set to zero.

The statement does not automatically cover the boundary blocks: multiplying
by the sharp interval indicator may destroy smoothness. Nor does it make the
prime component \(\Lambda/\log\), the shifted-prime component, or the entire
hybrid a smooth function. The signed \(\mu(d)\) sum and its cross terms
remain mandatory. TPC209 already records the divisor-dependent permutation.

There is a useful exact centering detail. If \(Y_m\) is the unmasked
additive transform of one strand, and \(B\) is its sum over multiples of
\(q\), then for \(1\le m<q\) the Fourier coefficient of its centered
unit-residue vector is
\[
 \alpha_m=q^{-1}\{Y_m-\bar Y^\times\},\qquad
 \bar Y^\times=\frac{qB-Y_0}{q-1}.
\]
Proof: the unit transform is \(Y_m-B\); centering the unit residues adds
\((Y_0-B)/(q-1)\) at a nonzero additive frequency. Combining terms proves
the formula. Since the complete Kloosterman matrix has row/column sum 1
and the other emitted array has total sum zero, this constant centering
term annihilates in the full bilinear form. It is not a missing main term.
This cancellation requires the complete centered second array. Arbitrary
truncation can destroy its zero total sum, requiring compensation.

After relabeling \(r\equiv md\pmod q\), the Kloosterman entry is
\(S(\overline d r,n;q)\), an allowed unit multiplier in BP. This can
make the *first* strand's effective index interval short after an explicit
tail truncation. It does not shorten the second array.

## 2. Exact obstruction to a one-short/one-complete norm route

Let \(K=(S(m,n;q))_{1\le m,n<q}\), with unnormalized Kloosterman sums.
Finite additive orthogonality gives
\[
 KK^*=q^2I-(q+1)J,\qquad K\mathbf1=\mathbf1,\quad
 K^*\mathbf1=\mathbf1,                                \tag{F1}
\]
where \(J=\mathbf1\mathbf1^*\).
Indeed,
\[
 (KK^*)_{m,m'}=
 \sum_{r,s\ne0}e_q(mr-m's)
       \sum_{n\ne0}e_q(n(\bar r-\bar s))
 =q(q1_{m=m'}-1)-1.
\]
This is F1. The row/column sums follow by summing one nonzero frequency.

For any set \(\mathcal I\subset\{1,\ldots,q-1\}\) with at least two
indices, the row-restricted matrix obeys
\[
 K_{\mathcal I}K_{\mathcal I}^*
      =q^2 I_{\mathcal I}-(q+1)J_{\mathcal I}.
\]
A nonzero mean-zero vector supported on \(\mathcal I\) has singular
value exactly \(q\). Hence
\[
 \|K_{\mathcal I}\|=q.                                \tag{F2}
\]
This remains true if the complete second array is required to be centered:
for centered first vector \(a\), \(K^*a\) is centered and has norm
\(q\|a\|\). Thus both-array centering does not reduce the \(q\) norm.

The same conclusion holds for the unit-multiplier matrix
\(S(cm,n;q)\), because row multiplication by a nonzero residue is a
permutation and F1 is unchanged. It holds for an interval of length 2,
not merely for a square-root-length interval. For a single first index
the row norm is \(\sqrt{q^2-q-1}\sim q\), so even that limit offers no
fixed-power improvement in a uniform norm estimate.
A centered singleton first vector is necessarily zero; the both-centered
counterexample above uses at least two first indices.

Consequently one short array and one unrestricted complete array cannot
support a uniform \(q^{1-\epsilon}\|\alpha\|\|\gamma\|\) bound for any
fixed \(\epsilon>0\), even with centered arrays. This is a finite interface
counterexample class, NOT an assertion that the literal arithmetic second
lane realizes an extremizer.

## 3. Precisely what remains

Under the stated derivative hypotheses, an individual interior smooth
divisor strand can carry a genuinely small dual radius. The one-sided
length fact alone does not activate the critical
two-short-array saving. A positive route still has to supply either:

- two-sided short arrays with a controlled signed reassembly/tail cost;
- a coefficient-sensitive estimate exploiting the literal second lane;
- a direct signed estimate of the diagonal-subtracted V59 scalar.

The sufficient two-sided criterion in LOCAL_EMITTER_PROOF.md remains
unproved. Its extra physical loss must stay strictly below \(19/2400\),
with Gate A separately open. The present note does not estimate the
Möbius strand sum, boundary blocks, prime components, or full scalar.

Map position: island 2, image Bridge A / Gate B. Exact finite structure and
a scoped norm obstruction only. The round-2 independent emitter audit
verified the finite identities and required the conditional derivative
qualification now implemented here. No arithmetic or publication GO.
