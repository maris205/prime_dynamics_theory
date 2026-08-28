# Proof Package

## Claim

For every finite integer index set $I$, every finite set $\mathcal S$ of odd
primes, every real $H>0$, every integer exponent $s\geq1$, every source vector
$\beta$, and every scalar functional $C(w,\cdot)$ linear in its output
argument, define

$$
g_q(u)=\sum_{t\in I}qK_H(u-t)D_q(u,t)\beta(t),
\qquad
g_{\mathcal S}(u)=\sum_{q\in\mathcal S}g_q(u),
$$

where $D_q$ is the physical deleted-diagonal centered residue block and
$K_H$ is any fixed scalar kernel.  Then

$$
g_{\mathcal S}=\sum_{q\in\mathcal S}g_q,
\qquad
C(w,g_{\mathcal S})=\sum_{q\in\mathcal S}C(w,g_q).
$$

If intervals $J_q$ and $J_{\mathcal S}$ enclose the component attachments
$c_q=C(w,g_q)$ and shell attachment $c_{\mathcal S}=C(w,g_{\mathcal S})$,
respectively, and every $J_q$ is separated from zero, then the retention
envelope defined in the derivation package satisfies

$$
r^-\leq \frac{|c_{\mathcal S}|}{\sum_{q\in\mathcal S}|c_q|}\leq r^+.
$$

## Status

PROVABLE AS STATED

## Assumptions

- $I$ and $\mathcal S$ are finite.
- The same $I$, $\beta$, mask, kernel, and source weights are used for all
  prime components.
- $C(w,\cdot)$ is linear in the output argument.
- For the ratio statement, every component interval is separated from zero,
  so the lower unsigned mass is strictly positive.
- $J_q$ and $J_{\mathcal S}$ are valid interval enclosures of the exact
  scalar quantities.

## Notation

- $D_q$ is the centered residue block with its diagonal removed.
- $c_q=C(w,g_q)$ and $c_{\mathcal S}=C(w,g_{\mathcal S})$.
- $\operatorname{dist}(0,[a,b])$ is $-b$ when $b<0$, $a$ when $a>0$, and
  zero otherwise.
- $m^-=\sum_q\operatorname{dist}(0,J_q)$ and
  $m^+=\sum_q\max(|\ell_q|,|u_q|)$.
- $r^- = \operatorname{dist}(0,J_{\mathcal S})/m^+$ and
  $r^+ = \max(|\ell_{\mathcal S}|,|u_{\mathcal S}|)/m^-.$

## Proof Strategy

First regroup the finite operator sum by its prime index.  Apply linearity to
the scalar attachment.  Then bound the numerator and denominator of the
absolute retention ratio separately using the interval enclosures.

## Dependency Map

1. Shell additivity depends only on finiteness of $\mathcal S$ and the
   definition of $g_q$.
2. Attachment additivity depends on linearity of $C$ in its output argument.
3. The lower mass bound depends on component sign separation.
4. The retention inequalities depend on the enclosure property and the two
   mass bounds; they do not require independence of the interval endpoints.

## Proof

### Step 1: finite operator regrouping

By definition,

$$
g_{\mathcal S}(u)=\sum_{q\in\mathcal S}\sum_{t\in I}
qK_H(u-t)D_q(u,t)\beta(t).
$$

Both index sets are finite.  Regrouping the terms by $q$ gives

$$
g_{\mathcal S}(u)=\sum_{q\in\mathcal S}
\left(\sum_{t\in I}qK_H(u-t)D_q(u,t)\beta(t)\right)
=\sum_{q\in\mathcal S}g_q(u).
$$

This equality holds pointwise for every $u\in I$.

### Step 2: attachment additivity

Applying the linear functional $C(w,\cdot)$ to the equality in Step 1 gives

$$
c_{\mathcal S}=C(w,g_{\mathcal S})
=C\left(w,\sum_{q\in\mathcal S}g_q\right)
=\sum_{q\in\mathcal S}C(w,g_q)
=\sum_{q\in\mathcal S}c_q.
$$

No norm estimate or limiting operation is used.

### Step 3: lower and upper unsigned masses

Choose any admissible realization of the interval-valued source weights.  Since
$c_q\in J_q$ and each $J_q$ is sign-separated,

$$
|c_q|\geq \operatorname{dist}(0,J_q),
\qquad
|c_q|\leq \max(|\ell_q|,|u_q|).
$$

Summing these inequalities gives

$$
m^-\leq\sum_{q\in\mathcal S}|c_q|\leq m^+.
$$

The assumption of sign separation makes every term in $m^-$ positive, so
$m^->0$.

### Step 4: shell numerator bounds

Because $c_{\mathcal S}\in J_{\mathcal S}$,

$$
\operatorname{dist}(0,J_{\mathcal S})\leq |c_{\mathcal S}|
\leq\max(|\ell_{\mathcal S}|,|u_{\mathcal S}|).
$$

Dividing the lower numerator bound by the upper mass bound and the upper
numerator bound by the positive lower mass bound yields

$$
\frac{\operatorname{dist}(0,J_{\mathcal S})}{m^+}
\leq
\frac{|c_{\mathcal S}|}{\sum_q|c_q|}
\leq
\frac{\max(|\ell_{\mathcal S}|,|u_{\mathcal S}|)}{m^-}.
$$

These are exactly $r^-$ and $r^+$.  Therefore the retention envelope claim
follows. $\square$

## Finite certificate status

The 84-row and 336-component counts, signs, threshold counts, and leave-one-
prime-out events are `NUMERICALLY_CERTIFIED_FINITE` claims.  They are not
consequences of the universal algebraic theorem and are bound to the declared
source baselines, shell anchors, and frozen engine.

## Corrections or Missing Assumptions

None for the exact additivity theorem.  The ratio statement is deliberately
conditional on component sign separation and valid interval enclosures.  A
growing-shell theorem would require new uniform hypotheses.

## Open Risks

- The shell ladder is a finite modeling choice and does not define a natural
  asymptotic sampling measure.
- Interval endpoints share source-weight uncertainty; the envelope is safe but
  may be wider than the exact ratio.
- Multi-prime finite cancellation does not establish arithmetic cancellation
  at growing scale or a fixed power saving.
