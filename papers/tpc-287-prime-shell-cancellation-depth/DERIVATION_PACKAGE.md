# TPC-287 derivation package

## Frozen physical component

For a finite integer interval $I$, an odd prime $q$, height $H>0$, and integer
$s\geq 1$, define

```text
m_q(u) = 1_{q does not divide u}
B_q(u,t) = m_q(u)m_q(t)(1_{u=t mod q}-1/(q-1))
D_q = B_q - diag(B_q).
```

The physical prime component is

```text
g_q(u) = sum_{t in I} q K_H(u-t) D_q(u,t) beta(t),
K_H(h) = H^(2s)/(H^2+h^2)^s.
```

For a finite shell $\mathcal S_Q=\{q:Q<q\leq 2Q, q$ prime$\}$,

```text
g_shell(u) = sum_{q in S_Q} g_q(u).
```

The TPC-287 computation uses the same exact rational source profile and
interval-valued comparison weights as the frozen TPC-268 engine.  The shell
lower endpoints are explicitly declared as

```text
Q = 3, 4, 9, 10, 16, 22, 27,
```

whose prime shells are respectively

```text
[5], [5,7], [11,13,17], [11,13,17,19],
[17,19,23,29,31], [23,29,31,37,41,43],
[29,31,37,41,43,47,53].
```

Thus the ladder contains exactly one row-family for each shell cardinality
from one through seven.

## Exact shell additivity

Let $C(w,\cdot)$ be any scalar functional linear in its output argument.  The
finite sums can be regrouped by their prime index:

```text
g_shell = sum_q g_q,
C(w,g_shell) = sum_q C(w,g_q).
```

This is an exact finite identity, not an estimate and not a claim that the
intervals representing the separate terms have identical endpoints to the
interval representing their sum.

## Certified cancellation envelope

For each prime component let $J_q=[\ell_q,u_q]$ enclose
$c_q=C(w,g_q)$, and let $J_S=[\ell_S,u_S]$ enclose the shell attachment
$c_S=C(w,g_{\rm shell})$.  When every $J_q$ is separated from zero, define

```text
m^- = sum_q dist(0,J_q),
m^+ = sum_q max(|ell_q|,|u_q|),
r^- = dist(0,J_S)/m^+,
r^+ = max(|ell_S|,|u_S|)/m^-.
```

For every admissible realization of the interval-valued source weights,
$r^-\leq |c_S|/(\sum_q|c_q|)\leq r^+$.  The proof uses only the enclosure
properties and the positivity of $m^-$.  The ratio is called a retention
envelope because it measures the signed shell mass retained relative to the
unsigned component mass; it is not a normalized asymptotic statistic.

## Leave-one-prime-out diagnostic

For each $q_0\in\mathcal S_Q$, define

```text
g_{\setminus q_0} = sum_{q in S_Q, q != q_0} g_q.
```

The checker records the interval and sign of $C(w,g_{\setminus q_0})$.  A
nonzero remainder with the opposite sign from $c_S$ is a sign-flip event; a
zero remainder is recorded separately.  This is a finite sensitivity
diagnostic, not a proof that any one prime is indispensable in a growing
theorem.

## Declared finite registry

Each of the seven shell anchors is paired with the six source baselines

```text
(64,15,4,4), (96,20,5,4), (128,24,5,4),
(192,32,6,5), (256,38,6,5), (384,50,7,5),
```

and exponents $s=1,2$.  This gives $7\cdot6\cdot2=84$ rows and
$12(1+2+3+4+5+6+7)=336$ prime components.  The registry is intentionally
finite and declared for route exploration; it is not silently promoted to an
admissible growing shell family.
