# TPC-330 proof and scope package

## Proposition 1: exact finite Gram split

Let `I` be finite, let `C_e=sum_p e_p B_p`, and let `v` be a real vector
on `I`.  Then

```text
||C_e v||_2^2
 = sum_t v_t^2 ||C_e e_t||_2^2
   + sum_(t!=t') v_t v_t' <C_e e_t,C_e e_t'>.
```

### Proof

Write `C_e v=sum_t v_t C_e e_t` and expand the finite Euclidean square.
Partition the resulting double sum into `t=t'` and `t!=t'`.  No limit,
interchange, or arithmetic estimate is used.

## Proposition 2: five exact placement bijections

For `M in {2048,4096}`, the maps

```text
i,
(3i+11) mod M,
(5i+17) mod M,
(7i+29) mod M,
M-1-i
```

are bijections of `{0,...,M-1}`.

### Proof

The identity and reversal claims are immediate.  Since `M` is a power of
two and `3,5,7` are odd, each affine multiplier is invertible modulo `M`;
adding an offset preserves bijectivity.  The associated matrices are
permutation matrices, so `P^T P=I`, `||Pv||_2=||v||_2`, and the coordinate
multiset is unchanged.

This does not imply `C_eP=PC_e` or
`P^TC_e^TC_eP=C_e^TC_e`.

## Proposition 3: finite response-spectrum certificate

Under the frozen finite V59 source model, panel, four sign laws, five maps,
and `5e-8` ratio guard, the canonical certificate contains 640 resolved
law/control observations.  All three nontrivial affine controls classify the
all-plus off-diagonal term as positive in 32/32 rows.  Identity and reversal
classify it as negative in 31/32 rows and positive in 1/32.

### Evidence level

This proposition is `NUMERICALLY_CERTIFIED_FINITE`, not a symbolic theorem.
The producer and an independent checker separately rebuild the source,
prime-shell matrices, placements, metrics, classifications, control summaries,
law spectra, and all 10 pairwise summaries.  Normal and optimized executions,
a mutation stress suite, and a local Bridge-B wrapper are required to agree.

## Corollary: scoped placement obstruction

On the frozen panel, neither the source coordinate multiset nor its Euclidean
norm determines the all-plus sign: they are identical for all controls, but
the affine and identity/reversal classifications differ on 31 rows.  Moreover,
the TPC-329 effect is not unique to its `(5,17)` map, because both newly
predeclared affine maps reproduce the positive 32/32 census.

This corollary is scoped to the declared finite matrix, source model, and
controls.  It is not a theorem about random permutations or the true
twin-prime asymptotic.

## Exact anchor

The rational anchor on `[36001,36016]`, shell `{5,7}`, exponent `1`,
and vector `1_(t+2 prime)-1_(t odd)` verifies `E=D+O` exactly and locks the
three reduced-fraction digests in both certificate implementations.

## Missing theorem

No estimate controls the centered position response uniformly in source
origin, scale, shell, or the actual arithmetic residual.  In particular:

```text
GROWING_SOURCE_NATIVE_L2 = OPEN
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The next admissible theorem must define and control a position-aware
decomposition; adding more finite controls alone would not pay an arithmetic
gate.
