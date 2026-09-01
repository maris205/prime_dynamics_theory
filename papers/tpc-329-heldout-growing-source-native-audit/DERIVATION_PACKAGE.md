# TPC-329 derivation package

## 1. Target and status

The target is a finite held-out audit of the source-native residual in the
literal centered prime-shell operator.  The algebraic layer is
`PROVED_EXACT_FINITE`.  The source-vector formula is
`PROVED_EXACT_FINITE_DECLARED_MODEL`, inherited from the hash-locked V59
finite comparison layer.  The actual/permuted rows, the scale pairing, and the
placement census are `NUMERICALLY_CERTIFIED_FINITE`; none is an asymptotic
theorem.

## 2. Invariant object

Let

```text
I_(o,N) = {o,...,o+N/2-1},
```

and let `e_t` be the source-coordinate basis vector.  For `p in (Q,2Q]`,

```text
B_p(u,t) = 1_(u != t) 1_(p does not divide u) 1_(p does not divide t)
            p H^(2s)/(H^2+(u-t)^2)^s
            (1_(p divides u-t)-1/(p-1)).
```

For a fixed sign law `e`, set `C_e=sum_p e_p B_p`.  For a finite source vector
`v`, define

```text
E_e(v) = ||C_e v||_2^2,
D_e(v) = sum_t v_t^2 ||C_e e_t||_2^2,
O_e(v) = E_e(v)-D_e(v),
R_e(v) = E_e(v)/D_e(v).
```

The new control is the coordinate permutation

```text
(P_pi v)_i = v_(pi(i)),
pi(i) = (5*i+17) mod M,
M = N/2.
```

For `M=2048` or `4096`, `5` is invertible modulo `M`; hence `pi` is a
bijection and `||P_pi v||_2=||v||_2` exactly.

## 3. Assumptions and modeling choices

* Origins are `28001` and `36001`; scales are `4096` and `8192`.
* `H=66`, `Q={24,36,54,80}`, and kernel exponents are `{1,2}`.
* The source is

  ```text
  beta_o^(2)(t)=Lambda(t+2)-b^(2)(t),
  b^(2)(t)=2 C_2 1_(2 does not divide t)
            product_(p|t,p>2)(p-1)/(p-2).
  ```

* The finite Euler product is cut off at `50000` and paired with the declared
  positive tail multiplier; logarithms use 100-digit Decimal centers and a
  rational `1e-70` guard.
* Matrix products and metrics are float64; the ratio separation guard is
  `5e-8`.  The exact local anchor uses rational arithmetic.
* The affine permutation is fixed by protocol before the certificate is read;
  it is not selected after inspecting row signs.

## 4. Notation map

| symbol | implementation object | role |
|---|---|---|
| `I_(o,N)` | `range(origin, origin+scale//2)` | source domain |
| `B_p` | `coherent_matrices` block | literal physical block |
| `C_e` | signed matrix for one law | coherent reassembly |
| `beta` | midpoint of the enclosed source interval | arithmetic residual |
| `P_pi beta` | `residual[placement_permutation(M)]` | norm-preserving placement null |
| `E,D,O,R` | `ratio_record` fields | energy, diagonal, cross term, ratio |

## 5. Strategy map

```text
locked V59 source
        |
        +--> actual beta --> C_e --> (E,D,O,R)
        |
        +--> P_pi beta  --> C_e --> (E,D,O,R)_placement
                                      |
                         compare signs and ratios
```

The source vector and its permuted copy have the same coordinate multiset and
the same Euclidean norm.  They do not generally have the same image under
`C_e`, because the matrix is not invariant under arbitrary coordinate
permutations.  Therefore a changed ratio is evidence of finite position
sensitivity of this diagnostic, not evidence of a changed source norm.

## 6. Main derivation

The finite product expands as

```text
C_e v = sum_t v_t C_e e_t.
```

Bilinearity gives

```text
E_e(v) = sum_(t,t') v_t v_t'
                 <C_e e_t,C_e e_t'>.
```

The terms with `t=t'` are exactly `D_e(v)`, while the remaining terms are

```text
O_e(v) = sum_(t != t') v_t v_t'
                 <C_e e_t,C_e e_t'>.
```

Consequently `E_e(v)=D_e(v)+O_e(v)` for every finite vector, without a limit or
an arithmetic estimate.  If `D_e(v)>0`, then `R_e(v)<1` is equivalent to
`O_e(v)<0`, and `R_e(v)>1` is equivalent to `O_e(v)>0`.

For the placement control, write `P=P_pi`.  Since `P` is a permutation matrix,

```text
P^T P = I,       ||P v||_2^2 = ||v||_2^2.
```

But

```text
E_e(Pv)=v^T P^T C_e^T C_e P v,
```

which equals `E_e(v)` for every `v` only if the Gram operator commutes with
`P` on the relevant vector (a property not assumed here).  Likewise the
coordinate diagonal changes because its weights are attached to source
coordinates.  This is the precise algebraic reason the null can test
placement sensitivity while holding the source multiset fixed.

## 7. Finite result map

The actual all-plus census is `31` negative and `1` positive.  The permuted
all-plus census is `0` negative and `32` positive, with `31` classifications
changed.  Across the four laws, the permuted census is

```text
all_plus           0 negative, 32 positive
alternating_index 30 negative,  2 positive
mod4_character    32 negative,  0 positive
half_split        28 negative,  4 positive.
```

The two scales are paired in `64` law-level comparisons.  All-plus signs are
persistent in `15/16` origin/shell/exponent pairs; the energy growth factor is
between `1.9663131482417533` and `2.14326466572482`.

## 8. Boundaries and open risks

The placement experiment does not identify the finite V59 model with the true
twin-prime asymptotic.  One permutation is a controlled finite null, not a
distributional theorem.  No source-uniform quantifier, canonical sign law,
operator-norm estimate, power saving, strict `1/400` payment, Route-B Gate B,
or twin-prime conclusion follows.  The next useful theorem would either
control the position-sensitive cross term uniformly or characterize the
permutation-invariant component that can be bounded from source norms alone.
