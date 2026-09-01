# TPC-324 proof package

## Proposition 1 — conditional translation covariance

Let (Isubsetmathbb Z) be finite and let (d) satisfy
(pmid d) for every (pinmathcal P_Q).  Under the coordinate relabeling
(T_df(u+d)=f(u)),

\[
 B_{p,I+d}^{(s)}=T_dB_{p,I}^{(s)}T_d^{-1}.
\]

### Proof

Put (u'=u+d) and (t'=t+d).  The difference factor is unchanged because
(u'-t'=u-t).  The deleted diagonal is unchanged because (u'=t') iff
(u=t).  Since (pmid d), both congruence indicators satisfy
(1_{u'\equiv t'\pmod p}=1_{u\equiv t\pmod p}) and
(1_{p\nmid u'}=1_{p\nmid u}), with the analogous identity for (t).
The scalar kernel is therefore identical entry by entry after relabeling.
Conjugating and summing gives the two Gram identities.  Unitary conjugation
preserves eigenvalues and trace, hence preserves (ho_e) and (pi(G)).
(square)

## Proposition 2 — finite profile protocol is well-typed

For every finite row in the certificate, (G_0) and (G_e) are positive
semidefinite (n	imes n) matrices with positive trace.  Therefore
(pi(G)) is a probability vector and the cumulative comparison is defined.

### Proof

Each (B_p^*B_p) and (C_e^*C_e) is positive semidefinite.  The literal
blocks are nonzero on every declared row, so the recorded trace checks are
positive.  Spectral decomposition then gives nonnegative eigenvalues whose
sum is the trace; normalizing produces a probability vector. (square)

## Proposition 3 — energy and shape are independent coordinates

For any (a>0), (pi(aG)=pi(G)), while
(operatorname{tr}(aG)=aoperatorname{tr}(G)).  Hence an energy ratio does not
determine a normalized spectral profile.

### Proof

Every eigenvalue of (aG) is (alambda_j(G)), and the common factor cancels
in the normalized vector.  The trace scales by (a). (square)

## Finite certified statement

The producer and independent checker certify the following scoped statement:

\[
 \text{all-plus profile majorizes direct profile on 48/48 rows,}
\]

with 24/24 on each of the two frozen holdout panels.  The three alternative
law counts (majorizing/mixed) are 34/14, 42/6, and 36/12.  These are
`NUMERICALLY_CERTIFIED_FINITE` observations, not consequences of Proposition
1 and not asymptotic statements.

## Non-claims

No line above proves a uniform-in-(X) law, a canonical arithmetic sign,
source-native (L^2) cancellation, a power saving, a fixed-power credit, or
the twin-prime conjecture.  Official Session evaluator files are absent; the
local Bridge-B checker is intentionally fail-closed.
