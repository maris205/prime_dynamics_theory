# TPC-260 proof package

## Theorem 1 — null-compatible polygon completion

Let `H` be a complex Hilbert space containing orthonormal vectors `z,w`.
Given nonnegative `d_0,...,d_3`, consider packet families satisfying
`||V_j||=d_j` and `<z,sum_j V_j>=0`.  Among families of the form
`V_j=d_j exp(i theta_j)w`, the possible values of

```text
R=<w,sum_j V_j>
```

have exactly the radial range

```text
max(2 d_max-D,0) <= |R| <= D,
D=sum_j d_j, d_max=max_j d_j.                 (1)
```

In particular, when all `d_j=1`, the residual modulus fills `[0,4]` and
the residual energy fills `[0,16]`.

### Proof

For any phases, `|R|` is the length of the sum of four planar vectors with
lengths `d_j`.  The triangle inequality gives the upper endpoint `D`.  If
`d_max` is longer than the sum of the other three lengths, reversing the
shorter vectors gives the lower bound `d_max-(D-d_max)=2d_max-D`; otherwise
the four vectors can be joined head-to-tail to close a polygon, giving lower
endpoint zero.  Rotating one side continuously while keeping the other
three fixed fills every intermediate length.  A final common phase rotates
the resulting sum to any argument.  Conversely, the same triangle inequality
and long-side inequality apply to every choice of phases.  This proves (1).

Because every `V_j` is a multiple of `w` and `z` is orthogonal to `w`, the
null constraint holds identically.  The construction is therefore a complete
null-compatible family.  ∎

## Theorem 2 — four-packet DFT ledger

For arbitrary `V_0,...,V_3` in `H`, define

```text
Vhat_k=1/2 sum_j i^(-jk)V_j.
```

Then

```text
sum_k ||Vhat_k||^2=sum_j||V_j||^2,
sum_jV_j=2Vhat_0,
||sum_jV_j||^2=4||Vhat_0||^2.                (2)
```

### Proof

The matrix `(1/2 i^(-jk))_(k,j)` is unitary, so the first identity is
Parseval.  Inverting the DFT at index zero gives the second identity, and
the third follows by taking norms.  ∎

## Theorem 3 — Haar-complement realization

For any four positive block lengths, the TPC-257 vectors `z0,z1,z2` are
orthonormal and orthogonal to the normalized scaling direction `e_scale`.
The TPC-258 source-frozen `z_null` is orthogonal to `e_scale`.  Set
`z=z_null` and `w=e_scale` in the same four-block Hilbert space.  The packet
families in Theorem 1 then have zero projection on all three Haar contrasts
and zero TPC-259 null channel, while their full residual still has the range
(1).

This is a finite structural theorem.  It does not identify `w` with the
literal hybrid sequence or `sum V_j` with a prime-shell output.

## Exact obstruction

With unit packet lengths and a unit residual direction, the aligned family
`V_j^+=w` has

```text
packet norms = (1,1,1,1), contrast projections = 0,
null channel = 0, |<w,sum_jV_j^+>|=4.
```

The alternating family `V_j^-=(-1)^j w` has exactly the same displayed data
except that the full residual is zero.  Their DFT mode distributions are
different: the plus family occupies mode zero, while the alternating family
occupies mode two.

## Claim firewall

```text
TPC260_MAXIMUM_CLAIM = PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION
TPC260_ROUTE_ADVANCE = YES_SCOPED_MODE_AUDIT
TPC260_HAAR_COMPLEMENT = PROVED_EXACT_FINITE
TPC260_POLYGON_COMPLETION = PROVED_EXACT_FINITE
TPC260_DFT_MODE_LEDGER = PROVED_EXACT
TPC260_NULL_CHANNEL_COMPATIBILITY = PROVED_EXACT_SYNTHETIC
TPC260_FULL_RESIDUAL_IDENTIFIABILITY = REFUTED_SCOPED
TPC260_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC260_ARITHMETIC_ADVANCE = NO
TPC260_FIXED_ATOM_CREDIT = 0
TPC260_L2 = NONE
TPC260_FULL_GATE_B = OPEN
TPC260_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC260_TWIN_PRIME_RESULT = NONE
TPC260_STATUS = PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION
TPC260_ROUND2_CLUE = PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_FOR_THE_COMMON_V59_FOUR_PACKET_OUTPUT
```

The named Session evaluator files are absent from this checkout.  The proof,
theorem ledger, certificate, bridge checker, and `AGENTS.md` are used as the
fail-closed local evaluation authority.
