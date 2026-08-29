# TPC-301 proof package

## Finite theorem

Assume M_k is positive definite and define
\[
 {\cal F}_{k,\tau}(b)=
 \{c:\|V_kc-b\|_2\leq\tau\|b\|_2\},\qquad
 B_{k,\tau}(b)=\min_{c\in{\cal F}_{k,\tau}(b)}c^TM_kc .
\]

### Proposition 1 (tolerance monotonicity)

If 0 < tau_1 <= tau_2, then
F_{k,tau_1}(b) is contained in F_{k,tau_2}(b).  Taking the minimum of the
same positive quadratic form over nested sets gives
B_{k,tau_1}(b) >= B_{k,tau_2}(b).

### Proposition 2 (relative homogeneity)

For alpha != 0, c is in F_{k,tau}(b) if and only if alpha c is in
F_{k,tau}(alpha b), because
\[
 \|V_k(\alpha c)-\alpha b\|_2
 =|\alpha|\|V_kc-b\|_2
 \leq\tau|\alpha|\|b\|_2.
\]
The objective scales by alpha^2; applying the equivalence in both directions
proves B_{k,tau}(alpha b)=alpha^2 B_{k,tau}(b).

### Proposition 3 (first feasible prefix)

The least-squares residual is the distance from b to range(V_k).  Prefix
inclusion gives range(V_k) contained in range(V_l) for k <= l, so r_k(b)
is nonincreasing.  The set of indices satisfying r_k(b) <= tau therefore
has a first element, and increasing tau can only move that first element to
the left.

### Proposition 4 (normalization)

At a common prefix k, N_k is a positive scalar independent of the target
class.  It cancels from the quotient of the two normalized budgets, which
proves (4).  The statement does not assert invariance when the two targets
are assigned different prefixes.

## Numerical status

The proof package does not promote finite floating-point values to exact
theorems.  It labels the 324 frontier values, 54 common-prefix gap triples,
and all aggregate floors as NUMERICALLY_CERTIFIED_FINITE because a separate
source-first checker reconstructs them from the frozen parent engine and
checks the published intervals.  No asymptotic conclusion is attached.
