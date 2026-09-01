# TPC-324 derivation package

## 1. Literal blocks

For a finite interval (I), a prime (p), and (sin{1,2}), set

\[
 B_{p,I}^{(s)}(u,t)=
 p\,\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 1_{u\ne t}1_{p\nmid u}1_{p\nmid t}
 \left(1_{u\equiv t\pmod p}-\frac1{p-1}\right).
\]

The active shell is (mathcal P_Q={p:Q<p\le 2Q, p	ext{ prime}}),
with (H=66).  All source coordinates are retained; only the deleted
diagonal and the two divisibility masks are removed.

## 2. Direct and coherent Gram objects

Define

\[
 G_0(I,Q,s)=\sum_{p\in\mathcal P_Q}B_{p,I}^{(s)\,*}B_{p,I}^{(s)},
 \qquad
 C_e(I,Q,s)=\sum_{p\in\mathcal P_Q}e_pB_{p,I}^{(s)},
\]

and (G_e=C_e^*C_e), where (e_pin{+1,-1}).  The energy coordinate
and shape coordinate are

\[
 \rho_e=\frac{\operatorname{tr}G_e}{\operatorname{tr}G_0},
 \qquad
 \pi(G)=\frac{(\lambda_1(G),\ldots,\lambda_n(G))}{\operatorname{tr}G},
\]

where eigenvalues are sorted in descending order.  The signed profile
majorizes the direct profile when every interior prefix of
(pi(G_e)-pi(G_0)) is nonnegative and at least one is positive.

## 3. Translation covariance

Let (d) be divisible by every (pinmathcal P_Q), and let
(T_d:ell^2(I)	oell^2(I+d)) be the coordinate relabeling
((T_df)(u+d)=f(u)).  Since

\[
 (u+d)-(t+d)=u-t,qquad
 u+d\equiv u\pmod p,qquad t+d\equiv t\pmod p,
\]

every factor in the literal block is preserved.  Consequently

\[
 B_{p,I+d}^{(s)}=T_d B_{p,I}^{(s)}T_d^{-1},
 \quad G_0(I+d)=T_dG_0(I)T_d^{-1},
 \quad G_e(I+d)=T_dG_e(I)T_d^{-1}.
\]

Thus the energy ratio and normalized profile are exactly invariant under
this conditional translation.  The selected holdout offsets are not common
multiples of the complete active shell, so this identity is a control lemma,
not an explanation of the observed holdout replication.

## 4. Numerical enclosure convention

Three finite paths are retained: forward `@`, forward NumPy eigensolver,
and reverse `einsum` with NumPy eigensolver.  Each scalar interval expands
the observed path extrema by (10^{-12}).  The profile class tolerance is
(10^{-10}).  The independent checker recomputes matrices from the literal
formula rather than importing the producer; long floating profile digests
are format-checked but not treated as cross-LAPACK exact equalities.

## 5. Scope

The derivation proves an exact finite covariance identity and defines the
profile comparison.  The 48-row holdout result is a numerical certificate
for the frozen panels only.  It supplies no source-native Möbius/von Mangoldt
representation, no growing estimate, and no twin-prime conclusion.
