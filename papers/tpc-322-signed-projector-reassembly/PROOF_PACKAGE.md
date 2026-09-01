# TPC-322 proof package

## Proposition 1 — direct-sum identity

For every (v),
\[
 \|A_\oplus v\|^2=\sum_p\|B_pv\|^2.
\]

**Proof.** The summands are coordinates in an orthogonal direct sum.  Expand
the Hilbert norm. \(square\)

## Proposition 2 — signed projector identity

For every sign vector (e), (E_e^*E_e=I), (P_e=E_eE_e^*) is an orthogonal
projection, and
\[
 \|P_eA_\oplus\|_{\rm HS}^2=m^{-1}\|\sum_pe_pB_p\|_F^2.
\]

**Proof.** The factors (m^{-1/2}) and (e_p^2=1) give
(E_e^*E_e=m^{-1}\sum_pI=I).  Thus (P_e) is an orthogonal projection.
For each source basis vector (u_t),
\[
P_eA_\oplus u_t=E_e(m^{-1/2}C_eu_t).
\]
The isometry (E_e) preserves norms.  Summing the squared column norms gives
the identity. \(square\)

## Proposition 3 — cross-block Gram and contraction

Let (H_{pq}=\langle B_p,B_q\rangle_F).  Then (H\succeq0),
(D=\operatorname{tr}H>0), and
\[
 \rho_e=e^THe/D,\qquad 0\leq\phi_e=\rho_e/m\leq1.
\]

**Proof.** (H) is a Gram matrix in the Frobenius inner-product space, so it
is PSD.  The expansion of (C_e) gives (\|C_e\|_F^2=e^THe).  Finally,
orthogonal projection contraction gives
\(\|P_eA_\oplus\|_{\rm HS}\leq\|A_\oplus\|_{\rm HS}\), proving the last
inequality. \(square\)

## Proposition 4 — global sign gauge

For every (e), (ho_{-e}=ho_e).  Therefore fixing the first sign to +1
does not remove any distinct ratio.

**Proof.** (C_{-e}=-C_e), and the Frobenius norm is unchanged. \(square\)

## Proposition 5 — finite signed atlas

On the 24 declared literal rows, the dual accumulation paths and exhaustive
search certify a sign with (ho_e<1) and a sign with (ho_e>1) in every
row.  The all-plus ratios are below one in 3 rows and above one in 21 rows;
the index-alternating ratios are below one in 21 rows and above one in 3 rows.

These are finite numerical statements under the declared binary64 error guard.
They do not assert a canonical sign law or a growing estimate. \(square\)

## Claim ceiling

```text
PROVED_EXACT_FINITE = projector, cross-block Gram, contraction, and gauge identities
NUMERICALLY_CERTIFIED_FINITE = 24 literal rows; dual paths; exhaustive signs
NUMERICAL_OBSERVATION = canonical-law counts and finite ratio ranges
REFUTED_FINITE_PANEL = all-plus and alternating universal laws
OPEN = growing signed reassembly, source-native arithmetic L2, fixed-power credit,
       full Gate B, and twin-prime endpoint
```
