# Physical-return derivation package

Date: 2026-09-09. Status: unnumbered research; round-1 scoped audits passed;
the recorded precision corrections are implemented for round-2 delta review.
Formal endpoint remains TPC418. No publication GO and no arithmetic Gate closure.

## 1. Object lock and question

This round asks whether the literal V59 operator admits a coefficient-blind
norm route to the required scalar bound. It also records a complete-frequency
Kloosterman emitter, without claiming a short-array theorem attachment.

The map location is island 2 inside image Bridge A, repository Gate B. This
is not image Bridge B (distinguished-seed dynamics).

Use \(e(y)=\exp(2\pi i y)\), the standard complex inner product
\(\langle f,g\rangle=\sum\overline f g\), and
\[
 I=I_x=(x/2,x]\cap\mathbb Z,\quad N=|I|,\quad Q=x^{1/3},
 \quad H=x^{21/32},\quad U=x^{133/400},\quad
 \mathcal Q=\{q\text{ prime}:Q<q\le2Q\}.
\]
The legacy source clock is \(x=2X\), so
\(N=\lfloor x\rfloor-\lfloor x/2\rfloor=X+O(1)\), not exactly \(X\).
This follows from bridge_b_literal_jutila_farey_atom_compiler.md:43.
The \(X=x\) wording in some archived raw reports is superseded by this
source-locked crosswalk; their raw text is preserved without alteration.
All limits are \(x\to\infty\). The physical shift is \(h_0=2\), never \(H\),
\(q\), or a model shell height. The exact domain is the full ordered pair
\(t,u\in I\), \(t\ne u\), with both unit masks for each \(q\). No block or
prefix has been substituted for this domain.

The coefficient and Fourier definitions are V59 (1.1)--(1.6),
in research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:37:
\[
 \beta(t)=\frac{\Lambda(t)}{\log t}-\sum_{\substack{d\mid t\\d\le U}}\mu(d),
 \qquad w(u)=\Lambda(u+2)-b_x^{(z)}(u),\quad
 K_H(h)=\kappa(h/H),\quad
 \kappa(y)=\int\psi_+(v)e(-vy)\,dv .
\]
Here \(z=(\log x)^K\), with \(K>0\) fixed after the requested
Ford--Maynard input exponent and before the \(x\)-threshold. Constants may
depend on \(K\); no one fixed \(K\) is asserted to support all saving orders.

## 2. Recovered hybrid and profile source locks

The hybrid is exactly the definition in
research/tpc-big-road/fm_local_comparison_compiler.md:727:
\[
 b_x^{(z)}(u)=1_I(u)C_z W_z\,1_{(u+2,P(z))=1}
       \prod_{\substack{p\mid u\\p>z}}\frac{p-1}{p-2},
\]
\[
 P(z)=\prod_{p\le z}p,\qquad W_z=\prod_{p\le z}\frac p{p-1},\qquad
 C_z=\prod_{p>z}\left(1-\frac1{(p-1)^2}\right).
\]
The low-prime product includes \(2\), and its forbidden residue is \(-2\).
The actual sign in \(w=\Lambda(\cdot+2)-b\) is retained. The parameter order is
recorded in the same source, Section 8.3 (line 797).

The profile ancestry must be read with its Fourier convention:

- bridge_b_prime_shell_jutila_and_stable_dynamics.md:186 fixes a real
  smooth \(\psi:\mathbb R\to[0,1]\), supported on \([-1,1]\), with integral 1.
- bridge_b_corrected_fourier_factorable_emitter.md:87 uses
  \(\widehat\psi_+(\xi)=\int\psi(v)e(+\xi v)\,dv\).
- bridge_b_multiroute_ratio_core_atlas.md:122 and V59 (1.3) write a negative
  Fourier transform of \(\psi_+\).

The same kernel is therefore represented by \(\psi_+(v)=\psi(-v)\). This
reflection is an explicit derivation, not a quotation claiming that the
source printed it. It preserves the originally fixed profile; it is not a
new Gaussian or an \(x\)-dependent choice. Hence \(\psi_+\) is real,
nonnegative, smooth, supported on \([-1,1]\), and has integral 1. In
particular \(\kappa(0)=1\), \(\kappa(-y)=\overline{\kappa(y)}\), and \(\kappa\)
is Schwartz. Neither evenness of \(\psi_+\) nor reality of \(\kappa\) follows.
There is no hard cutoff \(|u-t|\le H\).

For estimates fix constants \(B_\kappa,B_\psi<\infty\), \(0<\rho,b\le1\):
\[
 |\kappa(y)|\le B_\kappa(1+|y|)^{-2},\quad
 |\kappa(y)|\ge b\quad(|y|\le\rho),\qquad
 0\le\psi_+(v)\le B_\psi(1+|v|)^{-2}.
\]
All depend only on the fixed inherited profile.

## 3. Literal operator and ordinary row-energy normalization

Put \(a_q=q/(q-1)\). For \(u,t\in I\), define
\[
 A_q(u,t)=a_q\kappa((u-t)/H)
   [(q-1)1_{q\mid u-t}-1]\,1_{q\nmid u}1_{q\nmid t}1_{u\ne t},
 \qquad A=\sum_{q\in\mathcal Q}A_q.
\]
The exact scalar is \(\mathfrak C_x=\langle w,A\beta\rangle\). The outer
physical \(q\) is already included in \(a_q[(q-1)1-1]\); adding another
\(q\), or dropping \(a_q\), would change the object. The matrix is Hermitian.

For the particular full-row-energy normalization studied here define
\[
 G(u)=\sum_{q\in\mathcal Q}\sum_{t\in I}|A_q(u,t)|^2,\quad
 D_G=\operatorname{diag}G,\quad Z=D_G^{-1/2}AD_G^{-1/2}.
\]
This \(G\) sums the squared per-prime entries, not
\(\sum_t|\sum_qA_q(u,t)|^2\), and is not a freely chosen model energy.
The exact readout is
\[
 \mathfrak C_x=\langle D_G^{1/2}w,ZD_G^{1/2}\beta\rangle .
\]
Thus both lane norms are obligatory. A small normalized norm alone has no
physical exponent credit.

## 4. Exact structural reduction

The proof package derives, on the same finite interval,
\[
 A=T_{\mathcal Q}-R-\Delta,\qquad
 0\le A+\Delta=T_{\mathcal Q}-R\le T_{\mathcal Q},\qquad R\ge0,
\]
where
\[
 T_{\mathcal Q}(u,t)=\kappa((u-t)/H)
   \sum_{q\in\mathcal Q}\sum_{a=1}^{q-1}e(a(u-t)/q),
\]
\[
 R(u,t)=\kappa((u-t)/H)
   \sum_{q\in\mathcal Q}\frac{r_q(u)r_q(t)}{q-1},
 \quad r_q(n)=q1_{q\mid n}-1,
\]
\[
 \Delta(u)=\sum_{q\in\mathcal Q}a_q(q-2)1_{q\nmid u}.
\]
In particular the unit-residue correction \(R\) and the deleted diagonal
\(\Delta\) must both survive. Positivity of the undeleted operator does not
make the diagonal-deleted operator positive.

## 5. Derived bounds and their meaning

The companion proofs and their separate round-1 operator/lane audits establish,
\[
 G_{\min}\asymp_\psi G_{\max}\asymp_\psi HQ^2/\log Q,\qquad
 \|A\|\ll_\psi H+Q^2\ll_\psi Q^2,
\]
and the constant-mode calculation gives
\[
 \|A\|\ge(3/2+o(1))Q^2/\log Q.
\]
Consequently
\[
 H^{-1}\ll_\psi\|Z\|\ll_\psi(\log Q)/H.
\]
These are bounds for the literal physical operator, not a claim that its
literal mixed arithmetic scalar is large.

The lane-norm package proves
\[
 \|w\|_2^2\sim (x/2)\log x,\qquad
 \|\beta\|_2^2\ge(\tfrac12\log(27/22)+o(1))x/\log x.
\]
Therefore a coefficient-blind norm upper bound
\(B_x\|\beta\|_2\|w\|_2\), with \(B_x\ge\|A\|\), is itself at least a
constant multiple of \(xQ^2/\log Q\). It cannot establish
\(|\mathfrak C_x|\ll xQ^2x^{-\delta+o(1)}\) for any fixed \(\delta>0\).
This is a limitation of that upper-bound method, not a lower bound for
\(|\mathfrak C_x|\), not a nonexistence theorem for twin primes, and not a
ban on coefficient-sensitive cancellation.

These are eventual full-domain statements, uniform over every physical row
and the complete prime shell for the fixed profile, with no exceptional
rows. There is no unrestricted-profile, arbitrary-origin row-energy, or
coordinate/prime-prefix theorem. A singleton coordinate restriction has
zero deleted row energy and is not in the eventual full-domain assertion.

The required Gate-B saving remains \(\delta>1/400\). The short-array
benchmark \(\delta=1/96\) would leave only \(19/2400\) for all additional
losses. The separately audited emitter report identifies a complete-range
\(q-1\) array, not a critical \(q^{1/2}\) array; its naive chopping
worst-case norm reassembly has an extra \(q^{1/2}\) factor.
The full terminal ledger is V58 Theorem 5.1: division by
\(K_*=x^{2/3+o(1)}\), physical error exponent \(79/96\), and a separate
Gate-A estimate with saving \(\eta_A>0\). The allowed final saving is
\[
 0<\eta<\min\{\eta_A,\delta-1/400,419/2400\}.
\]
No term in that ledger is paid by an interface identity alone.

## 6. Scope, provenance, and remaining work

All raw agent reports are preserved in agent-reports/. A finite-model
orientation correction is recorded separately; raw reports are not rewritten.
The operator and lane theorems passed distinct adversarial round-1 audits;
their small notation/definition corrections await a bounded delta review.
A growing-rank negative-subspace extension is being investigated separately.
The startup regression report records PASS of the inherited read-only suite;
that PASS is not theorem evidence.

No numbered paper, handoff change, gate promotion, external-model upload,
staging, commit, or push is authorized by these draft estimates alone.
The remaining positive route needs a literal coefficient-sensitive signed
estimate, including the diagonal, masks, profile, and all compression losses.
