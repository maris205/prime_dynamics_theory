# TPC-367 derivation package

## 1. Literal finite object

Let `I=[a,a+N-1]` and let `S_Q={p prime: Q<p<=2Q}`.  For a declared kernel
exponent `s` define

\[
B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.
\]

For integer beta and a fixed sign law `epsilon`, set

\[
A_{\beta,\epsilon}=\sum_{p\in S_Q}\epsilon_p(p/Q)^\beta B_p,
\qquad
G_{\beta}(u)=\sum_{p\in S_Q}\sum_{t\in I}((p/Q)^\beta B_p(u,t))^2.
\]

The normalized finite matrix is

\[
A_{\beta,\epsilon}^{\#}=D_{G_\beta}^{-1/2}
A_{\beta,\epsilon}D_{G_\beta}^{-1/2},
\qquad D_{G_\beta}=\operatorname{diag}(G_\beta(u)).
\]

Every term in `G_beta(u)` is a rational square.  Thus `G_beta(u)>=0`
exactly, and positivity on a declared finite row makes the congruence
well-defined.  The producer and independent checker use the equivalent
entrywise operation `A / sqrt(G(u)G(t))`.

## 2. Finite envelopes

For every real symmetric finite matrix `T`,

\[
\|T\|_2\leq\max_u\sum_t|T(u,t)|,
\qquad
\|T\|_2\leq\|T\|_F.
\]

The reported spectral value is the maximum absolute endpoint of the true
`eigvalsh` spectrum.  The Schur and Frobenius values are recorded separately;
none is substituted for an asymptotic operator estimate.

## 3. Protocol logic

The three origins are indices selected before any signed matrix is evaluated.
The candidate grid is merely a finite declaration, not a random model.  The
comparison beta=0 is literal, while beta=2 is inherited from the preceding
finite line.  All four laws are evaluated, including all-plus, so the
localized failure cannot be hidden by a law choice.

## 4. Resulting finite phase statement

The 288-row replay gives beta=2 spectral-cap violations exactly at the three
predeclared origins, count 1024, `Q=2048` and `Q=8192`, all-plus law: six
rows in total.  Count 512 has zero beta=2 spectral violations at all three
anchors, and beta=2 has zero Schur-cap violations everywhere.  The beta=0
control has 36 spectral and 36 Schur violations.

This phase localization is a finite numerical observation, not a theorem
about all intervals, all origins, or a limit in `Q` or `N`.
