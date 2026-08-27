# TPC-275 proof package

## Theorem 1: signed packet Gram reassembly

For finite vectors `V_0,...,V_3` and
`Gamma_(j,k)=<V_j,V_k>`,

```text
||sum_j V_j||^2 = trace(Gamma) + 2 sum_(j<k) Gamma_(j,k).
```

### Proof

Expand the squared norm and use symmetry of the real Gram matrix (or the
Hermitian conjugate pairing in the complex case).  The diagonal terms give the
trace and each off-diagonal pair occurs twice in the real case.  ∎

## Theorem 2: four-point DFT ledger

For `Vhat_k=1/2 sum_j i^(-jk)V_j`,

```text
sum_k ||Vhat_k||^2 = sum_j ||V_j||^2,
||sum_j V_j||^2 = 4 ||Vhat_0||^2.
```

### Proof

The normalized four-point DFT matrix is unitary, so Parseval gives the first
identity.  Inversion at frequency zero gives
`sum_j V_j=2 Vhat_0`, which gives the second identity.  ∎

## Theorem 3: real two-probe polarization

For real finite vectors `x,y`,

```text
<x,y> = (||x+y||^2-||x-y||^2)/4.
```

### Proof

Expand both squares; the diagonal terms cancel and the two cross terms remain.
∎

## Theorem 4: registered source-specific audit

For the six TPC-269 growing-cutoff scales and `s=1,2`, the exact source-block
packets satisfy, on all 12 rows,

- the net cross term `G-D` is strictly negative;
- `1 < D/G < 12/5`;
- the TPC-274 Frobenius envelope obeys `F/G>50`;
- the packet-diagonal conservative proxy has `m_D^2<1/16`.

The packet Gram, all six pairwise polarization probes, and all four DFT mode
energies are reconstructed with exact rational arithmetic.  Parent outward
intervals are used only for the scalar and norm quantities containing the
comparison weights.

These are finite numerical certificates.  They do not imply an asymptotic
signed cross-Gram bound.

## Claim ceiling

```text
PROVED_EXACT_FINITE = signed Gram, DFT, and polarization identities
NUMERICALLY_CERTIFIED_FINITE = 12-row literal packet cancellation and gain audit
INSUFFICIENT_SCOPED = packet-diagonal envelope for a quarter-sector margin
OPEN_ASYMPTOTIC = source-level signed cross-Gram reassembly
FIXED_POWER_CREDIT = 0
ARITHMETIC_L2 = NONE
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
