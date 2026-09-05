# TPC-394 proof package

## Proved finite facts

1. The eight selected intervals are pairwise disjoint and disjoint from the
   recent declared TPC-393 and earlier c=1 panels.
2. The response-blind selection protocol fixes all origins, cohort roles,
   count, band, shell, laws, normalizations, and caps before readout.
3. The rational 13-point anchor at `[5000001,5000014)` with `Q=8` has positive
   row geometry and symmetric matrices for both declared laws.
4. The Cartesian panel has exactly 64 rows and 8 cells, with all origins at
   the same count.
5. The certificate is canonical JSON with a payload hash and exact TPC-393
   parent code/certificate provenance.
6. The independent checker reconstructs the rows in descending shell order,
   and the 25-case mutation suite rejects altered certificate contracts.

## Numerically certified finite facts

All four all-plus cells pass the one-percent all-origin spread rule; all four
alternating-index cells fail it.  The alternating spreads range from
`0.084824884787110394` to `0.092863374514779065`, while all-plus spreads are
at most `4.3100829568062604e-5`.  The holdout-transfer cap passes in all 8
cells.  The declared spectral cap fails in 32 of 64 rows (the all-plus rows)
and the Schur cap fails in none.

These statements are scoped to the sealed finite certificate and were
replayed with opposite summation order.

## Strongest obstruction

The alternating-index origin-spread failure is normalization-invariant across
the four declared choices on this family.  Thus TPC-393's origin signal is
not explained away by switching between local and scalar geometry
normalizations.  It remains a finite law-dependent obstruction, not a
source-uniform theorem.

## Open theorem and route status

It remains open to prove a source-valid normalization with a growing,
origin-uniform operator estimate, and to reassemble the prime shell with a
source-uniform arithmetic `L2` bound.  Route-A/Route-B closure and the twin
prime endpoint remain open.  `ARITHMETIC_ADVANCE=NO` and
`FIXED_POWER_CREDIT=0`.

The official evaluator files named by the Session are absent.  Local
Route-B/Bridge-B evidence is fail-closed artifact consistency only.

## Reusable structure and next clue

The reusable structure is a same-count origin ladder with a law control,
frozen normalization panel, calibration/holdout roles, reverse-shell replay,
and mutation testing.  The next clue is

```text
ROUND2_CLUE = TEST_C1_ORIGIN_CROSS_FAMILY_HOLDOUT
```
