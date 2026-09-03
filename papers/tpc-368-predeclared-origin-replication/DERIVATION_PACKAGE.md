# TPC-368 derivation package

## 1. Literal finite object

Let `I=[a,a+N-1]` and let `S_Q={p prime: Q<p<=2Q}`.  For exponent `s=1`
define

\[
B_p(u,t)=p\frac{66^{2}}{66^2+(u-t)^2}
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.
\]

For beta in `{0,2}` and a fixed sign law `epsilon`, set

\[
A_{\beta,\epsilon}=\sum_{p\in S_Q}\epsilon_p(p/Q)^\beta B_p,
\qquad
G_\beta(u)=\sum_{p\in S_Q}\sum_{t\in I}((p/Q)^\beta B_p(u,t))^2.
\]

When `G_beta(u)>0`, the finite normalized matrix is

\[
A_{\beta,\epsilon}^{\#}(u,t)=
\frac{A_{\beta,\epsilon}(u,t)}{\sqrt{G_\beta(u)G_\beta(t)}}.
\]

Each term of `G_beta` is a rational square.  Positivity on the exact anchor
and on every replay row therefore makes the finite congruence well-defined.

## 2. Finite envelopes

For every finite real symmetric matrix `T`,

\[
\|T\|_2\leq\max_u\sum_t|T(u,t)|,
\qquad
\|T\|_2\leq\|T\|_F.
\]

The certificate records the true spectral radius from `eigvalsh`, along with
the Schur and Frobenius quantities as separate finite envelopes.

## 3. Origin protocol

The candidate list `810001+353j`, `0<=j<41`, is a finite declaration.  The
indices `(0,20,40)` are selected before any signed matrix, source, or
geometry value is read.  Thus the protocol is response-blind and
predeclared, but it is not a random-sampling or uniform-origin theorem.

## 4. Finite phase statement

The 144-row replay has beta=2 spectral-cap violations exactly at

\[
(a,N,Q,s,\text{law})=(a,1024,2048,1,\text{all-plus})
\quad\text{or}\quad
(a,1024,8192,1,\text{all-plus})
\]

for each `a` in `(810001,817061,824121)`.  There are six such rows and no
beta=2 Schur-cap failures.  Count 512 has no beta=2 spectral failure at the
three anchors.  The beta=0 control has 18 spectral and 18 Schur failures.

This is a finite numerical observation and does not assert an all-origin,
all-window, or asymptotic law.
