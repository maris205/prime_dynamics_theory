# TPC-348 derivation package

## 1. Locked finite object

For an interval `I={o,...,o+M-1}`, let `R_I` be restriction and `E_I` zero
extension.  For each prime `p` in the declared shell, let `P_p` be the diagonal
projection

```text
(P_p f)(n) = 1_(p does not divide n) f(n).
```

Let `K_p` be the translated, zero-diagonal residue kernel used in TPC-347 and
let `e_p` be its declared sign.  The physical and unmasked comparison blocks
are

```text
A_I = sum_p e_p R_I P_p K_p P_p E_I,
T_I = R_I (sum_p e_p K_p) E_I,
D_I = A_I - T_I.
```

This paper studies `D_I` only; it does not identify `A_I` with `T_I`.

## 2. Exact projection expansion

For one prime, `P=P_p`,

```text
P K_p P - K_p = (P-I) K_p P + K_p(P-I).
```

Therefore

```text
D_I = sum_p e_p R_I ((P_p-I)K_pP_p + K_p(P_p-I)) E_I.
```

For a coordinate vector `e_t` with `t in I`, two cases give a position-aware
formula.  If `p divides t`, then `P_p e_t=0` and the right-mask term is
`-K_p e_t`.  If `p does not divide t`, then `(P_p-I)e_t=0` and only output
coordinates divisible by `p` survive in `(P_p-I)K_p e_t`.  Thus

```text
D_I e_t = - sum_(p|t) e_p R_I K_p e_t
          + sum_(p not|t) e_p R_I (P_p-I) K_p e_t.
```

The identity is exact and explains why the defect depends on the absolute
position of the interval, even when the unmasked convolution does not.

## 3. Coordinate lower-witness inequality

For every matrix `D` and every unit coordinate vector `e_t`, the definition of
the induced Euclidean operator norm gives

```text
||D||_(2->2) = sup_(||x||_2=1) ||Dx||_2 >= ||D e_t||_2.
```

Taking the maximum over the declared mask-hit set `J_I` gives the exact finite
functional inequality

```text
||D_I||_(2->2) >= W_I(D) := max_(t in J_I) ||D_I e_t||_2.
```

No leading eigenvector is used, and no sign or cancellation assumption is
needed.  The first-hit coordinate is a fixed non-adaptive control; `W_I` is a
declared coordinate envelope over all mask-hit positions.

## 4. What the numerical ratio means

The certificate reports `W_I(D)/||D_I||` and `W_I(D)/||T_I||` on the frozen
192-row grid.  These ratios measure the strength of a finite coordinate witness.
They are not lower bounds as the source count or origin grows.  In particular,
the lower bound theorem survives if every reported ratio is removed; the
ratios are only the finite audit readout.

## 5. Exact anchor

At `I={1,...,6}`, `Q=4`, exponent `1`, and all-plus signs, the shell is
`{5,7}` and `J_I={5}`.  The fifth column of `D_I` has exact squared Euclidean
norm

```text
1264004832717663389653333 / 162252681195863096059456.
```

The certificate also stores a canonical digest of the six rational entries.

## 6. Boundary

This derivation supplies a finite position-aware obstruction to silently
discarding the masks.  It does not prove source-uniform arithmetic `L2`, a
uniform bound for `D_I`, any fixed-power saving, Route-B reassembly, or the
twin-prime conjecture.
