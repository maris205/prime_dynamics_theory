# TPC-370 derivation package

## 1. Literal finite object

Let `I=[a,a+N-1]` and let `S_Q={p prime: Q<p<=2Q}`. With exponent one,

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

Every term of `G_beta` is a rational square. Positive geometry makes the
finite congruence well-defined; no claim about a limiting operator follows.

## 2. Frozen count-2048 protocol

The candidate grid is `1010001+401j`, `0<=j<41`; indices `(0,20,40)` are
fixed before signed replay, giving origins
`(1010001,1018021,1026041)`. TPC-370 fixes the single count `N=2048`,
shell anchors `Q=512,2048,8192`, exponent one, four sign laws
`all_plus`, `alternating_index`, `mod4_character`, and `half_split`, and beta
values `0,2`. No response, source vector, law score, or geometry ranking is
used in this selection. The Cartesian product contains 36 law rows per beta,
72 rows total.

The exact proof anchor is inherited unchanged from TPC-369:
`[1010346,1010359)` at `Q=4`, exponent one, shell `{5,7}`. TPC-370 does not
rerun an anchor search or use the inherited anchor to select a main-panel
parameter.

## 3. Finite envelopes

For every finite real symmetric matrix `T`,

\[
\|T\|_2\leq\max_u\sum_t|T(u,t)|,
\qquad
\|T\|_2\leq\|T\|_F.
\]

The certificate records true eigenvalue endpoints and keeps Schur and
Frobenius values as separate finite envelopes.

## 4. Count-2048 phase statement

The complete 72-row replay gives the following finite census:

* beta=0: 9 spectral-cap and 9 Schur-cap violations;
* beta=2: 6 spectral-cap and 0 Schur-cap violations;
* beta=2 failures occur at each of the three origins, at `Q=2048` and
  `Q=8192`, under `all_plus`;
* beta=2 has no spectral failure at `Q=512`.

After dropping the count coordinate, the six count-2048 failure keys agree
with the six TPC-369 parent keys. The beta=2 maximum is
`0.71099989528234753`, compared with the parent value
`0.67410489800609708`; the finite difference is
`0.036894997276250452`. This change blocks any claim that the finite maximum
has already stabilized.

## 5. Scope boundary

The phase statement is a numerical observation certified by two finite
implementations. It is not an all-origin, all-window, or asymptotic theorem,
and it supplies no arithmetic `L2`, prime-shell reassembly, fixed-power
saving, Route-A/Route-B gate closure, or twin-prime conclusion.
