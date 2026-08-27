# Proof Package

## Claim

For every finite integer index set $I$, every odd prime $q$, every real
height $H>0$, every integer exponent $s\geq1$, and every source vector
$\beta$, define

$$
B_q(u,t)=m_q(u)m_q(t)\left(\mathbf 1_{u\equiv t\pmod q}-\frac1{q-1}\right),
\qquad D_q=B_q-\operatorname{diag}(B_q),
$$

where $m_q(u)=\mathbf 1_{q\nmid u}$.  Let

$$
g_{\rm full}(u)=\sum_{q\in\mathcal S}\sum_{t\in I}
qK_H(u-t)B_q(u,t)\beta(t),
$$

and define $g_{\rm diag}$ using only the terms $t=u$, with
$K_H(h)=H^{2s}/(H^2+h^2)^s$.  Then

$$
g_{\rm diag}(u)=\sum_{q\in\mathcal S}qK_H(0)
\frac{q-2}{q-1}m_q(u)\beta(u),
\qquad g_{\rm phys}=g_{\rm full}-g_{\rm diag}.
$$

For every scalar functional $C$ linear in its output argument,
$C(g_{\rm phys})=C(g_{\rm full})-C(g_{\rm diag})$.

## Status

PROVABLE AS STATED

## Assumptions

- $I$ is finite, so all sums are finite.
- $\mathcal S$ is a finite set of odd primes.
- $H>0$ and $s\geq1$, so $K_H(0)$ is defined.
- The same mask, kernel, shell, and source vector are used in all three
  outputs.
- The scalar functional is linear in its output argument; the four-block
  attachment used in the certificate has this property because its source
  weights are held fixed.

## Notation

- $m_q(u)=\mathbf 1_{q\nmid u}$ is the active residue mask.
- $\operatorname{diag}(B_q)$ is the matrix with the diagonal of $B_q$ and
  zero off diagonal.
- $K_H(h)=H^{2s}/(H^2+h^2)^s$.
- $g_{\rm full}$ includes the $t=u$ terms; $g_{\rm phys}$ uses $D_q$ and
  therefore deletes them.

## Proof Strategy

Compute the diagonal entry of $B_q$ and split every finite sum into its
$t=u$ and $t\ne u$ parts.  Apply linearity first pointwise in $u$, then to
the scalar attachment.

## Dependency Map

1. The diagonal formula depends only on the definition of $B_q$ and the mask.
2. The output split depends on separating the diagonal summand from the full
   sum.
3. The attachment split depends on linearity of the declared scalar
   functional.

## Proof

### Step 1: diagonal entry

If $q\mid u$, then $m_q(u)=0$ and $B_q(u,u)=0$.  If $q\nmid u$, then
$m_q(u)=1$ and the congruence indicator in the diagonal is one.  Therefore

$$
B_q(u,u)=m_q(u)\left(1-\frac1{q-1}\right)
=m_q(u)\frac{q-2}{q-1}.
$$

### Step 2: diagonal output

The $t=u$ contribution to the diagonal-including output is

$$
\sum_{q\in\mathcal S}qK_H(0)B_q(u,u)\beta(u).
$$

Substituting Step 1 gives exactly

$$
g_{\rm diag}(u)=\sum_{q\in\mathcal S}qK_H(0)
\frac{q-2}{q-1}m_q(u)\beta(u).
$$

### Step 3: pointwise physical split

By definition, $D_q(u,t)=B_q(u,t)$ for $u\ne t$ and
$D_q(u,u)=0$.  Consequently, subtracting the $t=u$ contribution from the
full finite sum leaves precisely the sum with $D_q$:

$$
g_{\rm full}(u)-g_{\rm diag}(u)
=\sum_{q\in\mathcal S}\sum_{t\in I}qK_H(u-t)D_q(u,t)\beta(t)
=g_{\rm phys}(u).
$$

No limiting argument is used; this is a finite rearrangement.

### Step 4: scalar attachment

Let $C$ be linear in its second argument.  Applying it to the identity in
Step 3 gives

$$
C(g_{\rm phys})=C(g_{\rm full}-g_{\rm diag})
=C(g_{\rm full})-C(g_{\rm diag}).
$$

The four-block projected attachment is linear in $g$ because each block sum
and each contrast sum is linear, while the interval-valued source weights are
fixed during the evaluation.  Thus it satisfies the required hypothesis.

Therefore the exact operator and attachment decompositions follow. $\square$

## Finite certificate status

The 72-row sign, flip, opposition, and dominance statements are not part of
the universal theorem above.  They are `NUMERICALLY_CERTIFIED_FINITE` claims
supported by the canonical result, independent replay, and stress audit.  The
certificate assigns zero fixed-power credit and leaves asymptotic diagonal
dominance and signed full-shell cancellation open.

## Corrections or Missing Assumptions

None for the exact split.  A growing-scale theorem would require additional
uniform hypotheses and is deliberately not asserted.

## Open Risks

- The finite source profile is inherited from the frozen TPC-268 model.
- Interval endpoints are serialized for compatibility with earlier releases;
  the independent checker normalizes decimal spellings before comparison.
- A large finite diagonal correction does not identify the asymptotic signed
  shell behavior.
