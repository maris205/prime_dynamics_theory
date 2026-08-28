# TPC-288 derivation package

## 1. Literal component operator

Let `I` be the even-length interval used by the frozen TPC-268 source engine,
let `S` be a finite set of odd primes, and put

```text
K_H^(s)(d) = H^(2s)/(H^2+d^2)^s.
```

For `u,t in I`, define

```text
A_q(u,t) = q K_H^(s)(u-t)
            [1_(u != t) 1_(q does not divide u) 1_(q does not divide t)]
            [1_(u = t mod q) - 1/(q-1)].
```

All entries are rational.  The bracket is the centered nonzero-residue
factor, and the first indicator is the physical deleted diagonal.

## 2. Finite shell regrouping

Set `A_S=sum_(q in S) A_q` and let `beta` be the literal frozen source vector.
Then, coordinate by coordinate,

```text
g_q = A_q beta,
g_S = A_S beta = sum_(q in S) g_q.
```

The TPC-268 four-block attachment `L_w` is linear in its output argument, so

```text
C_q = L_w(g_q),
C_S = L_w(g_S) = sum_(q in S) C_q.
```

No interchange of an infinite sum or asymptotic limit is used.

## 3. Output Gram and energy

For the finite list of shell primes define

```text
G_(q,r) = <g_q,g_r>_I.
```

For every real coefficient vector `a`,

```text
a^T G a = || sum_q a_q g_q ||_2^2 >= 0.
```

Thus `G` is positive semidefinite.  With `1` the all-ones vector,

```text
E_diag = trace(G) = sum_q ||g_q||_2^2,
E_shell = 1^T G 1 = ||g_S||_2^2,
R_E = E_shell/E_diag.
```

The scalar cancellation ratio and the energy ratio are different quotients:

```text
R_C = |sum_q C_q| / sum_q |C_q|,
R_E = ||sum_q g_q||_2^2 / sum_q ||g_q||_2^2.
```

Linearity supplies the numerator identity for `R_C`, but does not identify the
scalar functional with the Euclidean norm.

## 4. Active physical matrix and modular witness

The rows and columns indexed by

```text
I_active = {u in I : q does not divide u for every q in S}
```

contain the nonzero physical block.  If the reduction of the restricted
aggregate matrix `A_S|I_active` has full rank over `F_p`, and every rational
denominator is invertible modulo `p`, its rational determinant is nonzero.
This is the standard one-way modular witness used by the certificate.

The same argument applies to `G`: modular full rank implies rational full
rank; the exact PSD identity then implies that the real Gram matrix is
positive definite and has strictly positive finite spectrum.

## 5. Interval obstruction logic

Each scalar attachment is enclosed by an outward interval `J_q`, and the shell
attachment by `J_S`.  Define

```text
m_minus = sum_q lower(|J_q|),
m_plus  = sum_q upper(|J_q|),
R_C^-   = lower(|J_S|)/m_plus,
R_C^+   = upper(|J_S|)/m_minus.
```

When `m_minus>0`, the exact scalar ratio satisfies
`R_C <= R_C^+`.  Therefore `R_C^+<1/10` is a certified finite cancellation
event.  Separately, all output energies are exact rational sums, so
`R_E>1` is an exact finite energy-amplification event.  Their intersection is
the paper's scalar-to-energy obstruction; it is not an asymptotic
counterexample to every possible arithmetic estimate.
