# TPC-276 computational protocol

1. Read the canonical TPC-275 JSON and verify its file and payload SHA-256.
2. For each of its 12 exact rows, parse `D/G` and the diagonal-margin interval
   as `Fraction` values.
3. Multiply the positive interval by `D/G` to obtain the signed-margin
   interval; never use floating-point arithmetic for classifications.
4. Check the exact recovery identity, quarter/eighth threshold counts, parent
   references, canonical JSON, and theorem ledger.
5. Run a separate implementation and a hostile mutation audit; run both normal
   and optimized Python modes in the bridge checker.
