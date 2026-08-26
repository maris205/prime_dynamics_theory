# TPC-261 proof package

Use the conjugate-linear-first-slot convention
`<u,v>=sum_n conjugate(u(n))v(n)`.  The proof has three independent pieces.

## Theorem 1 — strict finite-lane endpoint compiler

Let `L` be a nonempty finite set.  Fix

```text
E0=5/3,  E*=1997/1200,  Delta*=E0-E*=1/400.
```

For each `l in L`, suppose that for every `epsilon>0` there is a constant
`C_(l,epsilon)` such that, for all sufficiently large `x`,

```text
|T_l(x)| <= C_(l,epsilon) x^(E0-delta_l+lambda_l+epsilon).
```

Set `sigma_l=delta_l-lambda_l` and `sigma=min_l sigma_l`.  If
`sigma>Delta*`, then

```text
sum_(l in L) |T_l(x)| = o(x^E*).
```

If `sigma=Delta*`, the hypotheses are only borderline at the power level; if
`sigma<Delta*`, they do not close the target endpoint.

### Proof

Write `eta=sigma-Delta*>0` and choose `epsilon=eta/2`.  Since
`E0-sigma+epsilon=E*-eta/2`, each lane is bounded by a constant times
`x^(E*-eta/2)`.  The set `L` is finite, so its sum is also
`O(x^(E*-eta/2))`, which is `o(x^E*)`.  The equality and subcritical cases
follow directly from comparing the resulting exponent with `E*`; no strict
little-oh at the target follows in the equality case without an additional
rate factor.  ∎

## Theorem 2 — log/power separation

For every fixed `M>0` and `delta>0`,

```text
x^delta/(log x)^M -> infinity.
```

Hence an upper bound `x^E0/(log x)^M` supplies no positive fixed-power saving
in the sense of Theorem 1.

### Proof

Taking logarithms gives
`log(x^delta/(log x)^M)=delta log x-M log log x`, which tends to infinity
because `log log x/log x -> 0`.  ∎

## Theorem 3 — scaled null-compatible obstruction

Let `z,w` be orthonormal vectors in a complex Hilbert space and let
`a(x)=x^(5/6)`.  For `j=0,1,2,3`, define

```text
V_j^+=a(x)w,
V_j^-=(-1)^j a(x)w.
```

Both families have the same packet norms, diagonal energies, zero projection
onto every contrast orthogonal to `w`, and zero projection onto `z`.  Their
full residual energies are respectively `16x^(5/3)` and `0`.

Therefore packet marginal data, Haar contrast data, and the TPC-259 null datum
alone cannot imply a universal positive fixed-power saving for the full
four-packet sum.  This is a structural synthetic statement, not a claim about
the literal prime shell.

### Proof

The norm and projection statements follow from `||w||=1` and orthogonality.
For the plus family the sum is `4a(x)w`; for the alternating family it is
zero.  Squaring the norms gives `16a(x)^2=16x^(5/3)` and zero.  ∎

## Corollary — minimum sufficient literal bridge

A literal common-clock mode-zero or signed cross-Gram estimate with effective
saving `sigma>1/400` after all paid losses is sufficient for the target endpoint
under the finite-lane hypotheses of Theorem 1.  No such global estimate is
proved here.

## Exact scope firewall

```text
PROVED = endpoint identity; strict finite-lane compiler; log/power separation;
         scaled synthetic obstruction
CONDITIONAL_THEOREM = none beyond the hypotheses explicitly stated in Theorem 1
NUMERICALLY_CERTIFIED = exact rational audit and mutation rejection
OPEN = literal common-clock mode-zero or signed cross-Gram estimate
REFUTED_SCOPED = automatic global fixed-power credit from current marginals/null data
NOT_CLAIMED = literal growing-shell counterexample; arithmetic L2; full Gate B;
              fixed atom; twin-prime theorem
```
