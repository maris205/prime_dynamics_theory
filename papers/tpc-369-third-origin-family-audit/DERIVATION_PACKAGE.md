# TPC-369 derivation package

## 1. Literal finite object

Let `I=[a,a+N-1]` and let `S_Q={p prime: Q<p<=2Q}`.  With exponent one,

\[
B_p(u,t)=p\frac{66^2}{66^2+(u-t)^2}
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.
\]

For beta in `{0,2}` and a fixed sign law `epsilon`, define

\[
A_{\beta,\epsilon}=\sum_{p\in S_Q}\epsilon_p(p/Q)^\beta B_p,
\qquad
G_\beta(u)=\sum_{p\in S_Q}\sum_{t\in I}((p/Q)^\beta B_p(u,t))^2.
\]

When `G_beta(u)>0`, the normalized finite matrix is

\[
A_{\beta,\epsilon}^{\#}(u,t)=
\frac{A_{\beta,\epsilon}(u,t)}{\sqrt{G_\beta(u)G_\beta(t)}}.
\]

Every term of `G_beta` is a rational square.  Positive geometry makes the
finite congruence well-defined; no claim about a limiting operator follows.

## 2. Finite envelopes

For every finite real symmetric matrix `T`,

\[
\|T\|_2\leq\max_u\sum_t|T(u,t)|,
\qquad
\|T\|_2\leq\|T\|_F.
\]

The certificate records the true eigenvalue endpoint computation together
with Schur and Frobenius values as distinct finite quantities.

## 3. Origin and anchor protocol

The candidate list `1010001+401j`, `0<=j<41`, and indices `(0,20,40)` are
fixed before signed replay.  The exact-anchor rule begins at
`[1010342,1010355)` and scans rightward for the first 13-point interval whose
exact geometry is positive for both betas.  The initial interval is exactly
refuted by a zero geometry row; the first valid interval is
`[1010346,1010359)`.  This repair reads unsigned exact geometry only and does
not inspect a main-panel response.

## 4. Finite phase statement

The 144-row replay has beta=2 spectral-cap violations exactly at

\[
(a,1024,2048,1,\mathrm{all\mathchar`-plus})\quad\text{and}\quad
(a,1024,8192,1,\mathrm{all\mathchar`-plus})
\]

for each `a` in `(1010001,1018021,1026041)`.  There are six such rows and no
beta=2 Schur-cap failures.  Count 512 has no beta=2 spectral failure at the
three anchors; beta=0 has 18 spectral and 18 Schur failures.

This is a finite numerical observation, not an all-origin, all-window, or
asymptotic theorem.
