# TPC-284 paper plan

## Question

What survives when the information-model zeroing obstruction from TPC-283 is
replaced by a small, explicit family of schedule controls acting on the
literal source interface?

## Claim-driven contributions

1. Define six named controls around each registered baseline row: clock height
   `H-2/H+2`, comparison cutoff `z-1/z+1`, and prime-shell endpoint
   `Q-1/Q+1`.
2. Give a deterministic 72-row enumeration and an outward-interval protocol
   for the actual scalar attachment and normalized squared attachment.
3. Certify that all 72 finite intervals are sign-separated, with a census of
   60 negative and 12 positive rows.
4. Isolate the eight sign flips against the TPC-283 baseline and the weakest
   controlled margin as a finite obstruction to sign-stability heuristics.
5. State the exact boundary of the result: no exhaustive admissible-source
   theorem, growing-schedule theorem, arithmetic `L2` bound, or Gate-B credit.

## Success criterion

The paper is a genuine stage if the source-locked replay and an independent
replay agree on all 72 rows, hostile mutations are rejected, and the result
changes the next mathematical question.  It succeeds here by converting an
unrestricted geometric warning into a concrete finite control atlas and by
exhibiting sign instability under named controls.

## Non-claims

The six controls are not asserted to span the physical source class.  A finite
sign census is not a uniform lower bound, and a sign flip is not a twin-prime
counterexample.  Fixed-power credit remains zero.
