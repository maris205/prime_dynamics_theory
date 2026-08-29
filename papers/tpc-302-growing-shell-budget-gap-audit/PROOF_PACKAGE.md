# TPC-302 proof package

## Proposition 1 - Gram positivity and sign reduction

For any finite family of output vectors (g_q), (G=(\langle g_q,g_r\rangle)
is a Gram matrix and hence (c^TGc=\|\sum_qc_qg_q\|_2^2\geq0).  Replacing
(c) by (-c) leaves the quadratic form unchanged.  Consequently the
constraint (c_{q_0}=+1) selects one representative of every global-sign
class.

## Proposition 2 - finite enumeration

After multiplying a rational Gram matrix by a common positive denominator, all
quadratic values are integers.  The reflected Gray sequence flips one tail
coordinate at a time and runs through the (2^{m-1}) tail bit strings.  The
incremental update is algebraically the same quadratic value as direct
evaluation, so the reported minimum is the exact minimum on the declared
finite sign domain.

## Proposition 3 - budget monotonicity

For (0<\tau_1\leq\tau_2), the feasible ball for (\tau_1) is contained in
that for (\tau_2), so (B_{k,\tau_1}(b)\geq B_{k,\tau_2}(b)).  Since the
columns of (V_k) are nested, enlarging a prefix also enlarges the feasible
set and cannot increase the minimum.  The first feasible prefix is therefore
nonincreasing in (\tau).

## Proposition 4 - common normalization

If (N_k>0) depends on the row and prefix but not on the target class, then

\[
 \frac{B_{k,\tau}(b_w)/N_k}{B_{k,\tau}(b_+)/N_k}
 =\frac{B_{k,\tau}(b_w)}{B_{k,\tau}(b_+)}.
\]

This is a finite algebraic identity and does not transfer a target-specific
prefix comparison to a common-prefix comparison.

## Numerical scope

The 34 source-first sign labels and all reported ratios are exact rational
replays.  The frontier values are 60-digit numerical calculations enclosed
outward and independently checked for the declared finite rows.  They are
not asymptotic estimates.  The growing profile-budget theorem, arithmetic
(L^2), fixed-power credit, full Gate B, and a twin-prime theorem remain
OPEN.
