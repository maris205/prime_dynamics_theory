# TPC-328 derivation package

## 1. Target and status

The target is a finite, source-native test of the arithmetic residual in the
literal prime-shell operator.  The exact algebraic layer is `PROVED_EXACT_FINITE`.
The source-vector formula is `PROVED_EXACT_FINITE_DECLARED_MODEL`: it is the
finite V59 comparison model with explicit cutoff and logarithm enclosure.  The
96-row signs and ratios are `NUMERICALLY_CERTIFIED_FINITE`; they are not an
asymptotic theorem.

## 2. Invariant object

Let `I_(o,N)={o,...,o+N/2-1}` and let `e_t` denote the source coordinate
basis vector.  For `p in (Q,2Q]`, define

```text
B_p(u,t) = 1_(u != t) 1_(p does not divide u) 1_(p does not divide t)
            p H^(2s)/(H^2+(u-t)^2)^s
            (1_(p divides u-t)-1/(p-1)).
```

For a fixed sign law `e=(e_p)`, set `C_e=sum_p e_p B_p`.  For a finite real
source vector `v`, the invariant quantities are

```text
E_e(v) = ||C_e v||_2^2,
D_e(v) = sum_t v_t^2 ||C_e e_t||_2^2,
O_e(v) = E_e(v)-D_e(v).
```

The diagnostic ratio is `R_e(v)=E_e(v)/D_e(v)`, whenever `D_e(v)>0`.

## 3. Assumptions and modeling choices

* Origins are `12001,16001,20001`; scales are `320,640,1280,2560`.
* `H=66`, `Q={24,36,54,80}`, and exponents are `{1,2}`.
* The source model is

  ```text
  Lambda(m)=log p if m=p^k, and 0 otherwise,
  b^(2)(t)=2 C_2 1_(2 does not divide t)
            product_(p|t,p>2)(p-1)/(p-2).
  ```

* `C_2` is represented by the finite product through `50000` and the
  declared lower tail multiplier `1-1/(50000-1)`; logarithms use 100-digit
  Decimal centers and a `1e-70` rational guard.
* Ratios are computed in float64 after source midpoints; `5e-8` is a finite
  separation guard.  This is a numerical certificate protocol, not a claim
  that float64 proves a moving-order bound.

## 4. Notation map

| symbol | implementation object | role |
|---|---|---|
| `I_(o,N)` | `range(origin, origin+scale//2)` | source domain |
| `B_p` | `coherent_matrices` block | literal physical block |
| `C_e` | one signed matrix | coherent reassembly |
| `Lambda` | `lambda_interval` | von-Mangoldt component |
| `b^(2)` | `comparison_interval` | comparison component |
| `beta` | midpoint of `Lambda-b^(2)` interval | source-native residual |
| `E,D,O` | `ratio_record` fields | energy / diagonal / cross term |

## 5. Main derivation

Expand the finite matrix-vector product:

```text
C_e v = sum_t v_t C_e e_t.
```

Taking the Euclidean square gives

```text
E_e(v) = sum_(t,t') v_t v_t'
                 <C_e e_t, C_e e_t'>.
```

The terms with `t=t'` are exactly

```text
D_e(v) = sum_t v_t^2 ||C_e e_t||_2^2.
```

Subtracting them leaves

```text
O_e(v) = sum_(t != t') v_t v_t'
                 <C_e e_t, C_e e_t'>,
```

and therefore `E_e(v)=D_e(v)+O_e(v)` exactly for every finite vector.  Since
`D_e(v)>0` in every released row, `R_e<1` is equivalent to `O_e<0`, while
`R_e>1` is equivalent to `O_e>0`.

The source layer is inserted only after this identity is fixed.  For each
source coordinate, the producer encloses the two terms, subtracts the
intervals with reversed endpoints, and records the midpoint.  This preserves
the distinction between the exact identity and the numerical source replay.

## 6. Finite result map

The full panel has `3*4*4*2=96` rows.  With the declared guard, the census is

```text
all_plus           81 negative, 15 positive, 0 unresolved
alternating_index  73 negative, 23 positive, 0 unresolved
mod4_character     74 negative, 22 positive, 0 unresolved
half_split         61 negative, 35 positive, 0 unresolved.
```

The all-plus residual ratio range is
`[0.15702348685234854,1.4021661919173145]`.  The all-plus Lambda and comparison
controls are positive on all 96 rows, with minima `1.4345187728485156` and
`3.1071920015130248`.

## 7. Boundaries and open risks

The decomposition is coordinate-diagonal versus off-diagonal, not a proof of
arithmetic cancellation in a growing family.  The four signs are declared
finite laws, not a canonical arithmetic sign.  No source-uniform quantifier,
operator-norm estimate, power saving, strict `1/400` payment, Route-B Gate B,
or twin-prime conclusion follows.  The next useful theorem would control
`O_e(beta)` or `E_e(beta)` uniformly while preserving the literal masks and
normalization.
