# TPC-276 derivation package

## 1. Three energies

Let (V_0,ldots,V_3) be the four actual source-block residual packets from
TPC-275.  Write

```text
D = sum_j ||V_j||_2^2,
G = ||sum_j V_j||_2^2,
r = D/G,
m_D^2 = |C_perp|^2/(W_perp D),
m^2 = |C_perp|^2/(W_perp G).
```

On a positive row, (G=D/r), hence

```text
m^2 = r m_D^2.
```

This is the exact bridge from the TPC-275 packet audit to the actual residual
margin.  It does not require a square-root approximation.

## 2. Conditional signed-gain compiler

Assume, for all sufficiently large (x),

```text
|C_perp(x)| <= A x^(E0-sigma+epsilon),
m_D(x) >= c x^(-eta_D-epsilon),
D(x)/G(x) >= b x^gamma,
```

with (A,b,c>0), (gammage0), and (E0=5/3).  The exact bridge gives

```text
 m(x) >= c sqrt(b) x^(-(eta_D-gamma/2)-epsilon).
```

Using (R=|C_perp|/m),

Define the effective nonnegative margin loss

```text
eta_eff=max(0,eta_D-gamma/2).
```

Then both the scalar lane and the radius lane are bounded at endpoint exponent

```text
E0-sigma+eta_eff+2 epsilon.
```

Since (E0-E*=1/400), the strict endpoint condition is

```text
sigma - eta_eff > 1/400.
```

In the non-overcompensated regime (gamma/2\leqeta_D), this reduces to
`sigma-eta_D+gamma/2>1/400`.

The gain contributes half its exponent because it enters the margin through a
square root.

## 3. Finite audit logic

The parent TPC-275 rows contain exact rational (r=D/G) and an interval for
the diagonal proxy (m_D^2).  Multiplication by positive (r) produces an
exact rational interval for the signed margin (m^2).  We retain the parent
interval as a provenance reference and make no decimal-to-power inference.

The registered data show that every row has (r>1), while three rows lie above
the quarter-margin threshold after signed recovery and five rows exceed the
eighth-margin threshold.  This is a finite threshold result, not a uniform
statement in (x).

## 4. No finite power promotion

For any finite set of positive rows, a positive table of gains can be recorded,
but it does not imply (D/G\ge b x^\gamma) on a growing sequence.  Therefore
the finite gain contributes zero fixed-power credit until a source-level,
uniform lower bound is proved.
