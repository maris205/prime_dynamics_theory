# TPC-276 proof package

## Theorem 1: exact signed-gain margin recovery

Let (W,D,G>0), let (C) be a scalar, and define

```text
m_D^2 = |C|^2/(W D),   r=D/G,   m^2=|C|^2/(W G).
```

Then `m^2=r m_D^2`.

### Proof

Substitute (G=D/r) into the definition of (m^2):

```text
|C|^2/(W G) = |C|^2/(W(D/r)) = r |C|^2/(W D).
```

All denominators are positive, so the identity is exact. ∎

## Theorem 2: signed-gain endpoint compiler

Set (E_0=5/3), (E_*=1997/1200).  Suppose, for every sufficiently large
(x),

```text
|C(x)| <= A x^(E0-sigma+epsilon),
m_D(x) >= c x^(-eta_D-epsilon),
D(x)/G(x) >= b x^gamma,
```

where (A,b,c>0), (gammage0), and (epsilon>0) can be chosen small.
Then

```text
|C(x)|+R(x)
 <= A(1+(c sqrt(b))^(-1))
    x^(E0-sigma+eta_eff+2 epsilon),
```

where `R=|C|/m` and

```text
eta_eff=max(0,eta_D-gamma/2).
```

In particular, the endpoint is strictly beaten whenever

```text
sigma - eta_eff > 1/400.
```

If (gamma/2\leqeta_D), the condition is equivalently
`sigma-eta_D+gamma/2>1/400`.

### Proof

Theorem 1 and the two lower bounds give

```text
m(x) >= c sqrt(b) x^(-(eta_D-gamma/2)-epsilon)
       >= c sqrt(b) x^(-eta_eff-epsilon).
```

Consequently

```text
R(x) <= A(c sqrt(b))^(-1)
        x^(E0-sigma+eta_eff+2 epsilon).
```

Adding the scalar term and increasing the constant proves the displayed
bound.  Since (E_0-E_*=1/400), choose (epsilon) below half the strict
excess in (sigma-eta_eff-1/400). ∎

## Theorem 3: finite signed-margin transfer

On the 12 registered TPC-275 rows, the exact positive gain (r=D/G) multiplies
the parent diagonal-margin interval.  All 12 rows have (r>1); three have
signed (m^2>1/16), and five have signed (m^2>1/64).  These are finite
certificates with exact rational endpoints.

## Theorem 4: finite power-credit firewall

A finite list of values (r(N_i)>1) does not imply a bound
(r(x)ge b x^gamma) on a growing sequence.  Thus the TPC-276 finite audit
assigns fixed-power credit zero.

### Proof

The conditional compiler requires a quantified lower bound for all sufficiently
large (x).  A finite list has no such quantifier and can be extended by any
positive function outside the listed points.  Hence the implication is not
valid without an additional source-level uniformity theorem. ∎

## Claim ceiling

```text
PROVED_CONDITIONAL = signed-gain strict endpoint compiler
PROVED_EXACT_FINITE = m^2=(D/G)m_D^2 and finite power-credit firewall
NUMERICALLY_CERTIFIED_FINITE = 12-row signed-margin transfer
OPEN = source-level signed gain, arithmetic L2, full Gate B
FIXED_POWER_CREDIT = 0
TWIN_PRIME_RESULT = NONE
```
