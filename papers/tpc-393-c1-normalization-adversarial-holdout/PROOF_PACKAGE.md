# TPC-393 proof package

## Proved finite facts

1. The five selected affine intervals are pairwise disjoint from every
   declared prior panel and from one another.
2. The rational 13-point anchor has positive row geometry and symmetric law
   matrices for all declared laws.
3. The response-blind Cartesian panel has exactly 64 rows and 8 cells.
4. The four normalization definitions, calibration/holdout roles, forecast
   functional, and envelope caps are fixed in the canonical payload.
5. The producer emits canonical JSON with a payload hash and exact TPC-392
   parent code/certificate provenance.
6. An independent descending-shell implementation reconstructs every row and
   phase aggregate; its 25-mutation stress suite rejects altered contracts.

## Numerically certified finite facts

The fresh panel has forecast passes 2/2 for each normalization across the two
laws.  The maximum forecast errors are

```text
local_diagonal             0.01010300962072197
pooled_train_scalar        0.0097142554430971195
origin_scalar              0.011039357664235361
frozen_train_1024_scalar   0.0097142554430980077
```

The terminal normalization ordering is frozen, origin, pooled, local.  The
spectral cap fails in 32/32 rows and the Schur cap fails in 0/32 rows.  The
one-percent stability census is 4/8 at each of the three count levels; all
four all-plus cells are stable and all four alternating-index cells are not.
These statements are scoped to the finite certificate and were independently
replayed in the opposite shell order.

## Strongest obstruction

The earlier forecast anomaly is not robust under a fresh adversarial family:
the alternating-index/local-diagonal forecast error is only
`0.01010300962072197`, inside the cap.  The persistent finite signal is
origin spread for the alternating law, while the universal spectral failure
shows that the declared $0.64$ spectral envelope is not a viable pass
criterion on this panel.

## Open theorem and route status

It remains open to prove any source-valid normalization or origin-uniform
bound for a growing analytic operator.  Source-uniform arithmetic $L^2$,
prime-shell reassembly, Route-A closure, Route-B reassembly, and the
twin-prime endpoint remain open.  No fixed-power credit is assigned.

The official Session evaluator files are absent from this checkout.  Local
Route-B evidence is fail-closed artifact consistency only and cannot declare
an official Route-A or Route-B pass.

## Reusable structure and next clue

The reusable structure is a minimal adversarial holdout protocol: fresh affine
coordinates, response-blind law selection, fixed normalization definitions,
exact parent provenance, reverse-order replay, and mutation testing.  The
next clue is

```text
ROUND2_CLUE = TEST_C1_ORIGIN_UNIFORMITY_AFTER_REPLICATION
```

The next project should test the alternating-law origin signal directly on a
fresh predeclared family, while retaining all-plus as a control and keeping
the spectral obstruction visible.
