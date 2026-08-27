# TPC-275 derivation package

## 1. Packet decomposition

Let `A` be the finite literal V59 operator and `P_3` the orthogonal projection
onto the three declared four-block Haar contrasts.  Split the exact source
vector into four consecutive block vectors
`beta = beta^(0)+...+beta^(3)` and define

```text
V_j = (I-P_3) A beta^(j),
g_perp = sum_j V_j.
```

The packet Gram is the real symmetric matrix

```text
Gamma_(j,k) = <V_j,V_k>.
```

Write `D=trace(Gamma)` for the packet-diagonal energy, `G=1^T Gamma 1` for
the exact signed output energy, and `X=G-D` for the total signed cross term.

## 2. Exact signed identities

For any finite real or complex Hilbert-space vectors,

```text
G = sum_j ||V_j||^2 + 2 sum_(j<k) Gamma_(j,k).
```

For real packets, every cross term is recovered without an unproved estimate by

```text
Gamma_(j,k) = (||V_j+V_k||^2-||V_j-V_k||^2)/4.
```

With the four-point DFT

```text
Vhat_k = 1/2 sum_j i^(-j k) V_j,
```

Parseval and the mode-zero identity give

```text
sum_k ||Vhat_k||^2 = D,
G = 4 ||Vhat_0||^2.
```

For real packets, the mode energies used by the certificate are

```text
E_0 = ||V_0+V_1+V_2+V_3||^2/4,
E_2 = ||V_0-V_1+V_2-V_3||^2/4,
E_1=E_3 = (||V_0-V_2||^2+||V_3-V_1||^2)/4.
```

Thus `E_0+E_1+E_2+E_3=D` and `G=4E_0` are exact finite identities.

## 3. Envelopes and margin

The TPC-274 envelope is

```text
F = ||(I-P_3)A||_F^2 ||beta||_2^2.
```

The packet-diagonal envelope is `D`.  Since `G` is the exact signed output,
the finite audit compares `D/G` and `F/G` directly.  A conservative
packet-diagonal margin proxy is

```text
m_D^2 = |C_perp|^2/(W_perp D).
```

When the net cross term is negative, `G<D`, so `m_D^2<=m^2`; a low value of
`m_D` is therefore a limitation of the diagonal envelope, not a proof that the
actual margin is low.

## 4. Finite interpretation

The source-specific certificate reports a useful compression: on the registered
rows, `1 < D/G < 12/5`, while `F/G>50`.  This is a real signed cancellation
signal in the literal source-block decomposition.  It does not prove that the
same inequalities hold on a growing sequence, nor does it supply the missing
arithmetic `L2` estimate or the strict `1/400` endpoint payment.
