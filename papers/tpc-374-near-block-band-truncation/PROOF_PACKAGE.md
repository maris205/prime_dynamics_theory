# TPC-374 proof and certificate package

## Exact finite claims

1. The panel, shell anchors, laws, beta values, block partition, and cutoff
   `3` are declared independently of the numerical results.
2. The common full-window geometry is a finite sum of nonnegative rational
   squares and is positive on every declared row.
3. The fixed band mask and its complement form an exact partition, so
   `T=B3+(T-B3)` entrywise.
4. The full, band, and tail matrices are finite symmetric matrices.  The
   extremal-mode rule is deterministic and includes an explicit tie break.
5. For a selected unit eigenvector, the two band/tail Rayleigh terms sum to
   the full eigenvalue by linearity.

These are the proof-bearing identities.  They do not imply uniformity in
the window size or a causal explanation of the parent excess.

## Numerical certificate

`results/tpc374_certificate.json` contains all 18 rows, full and band
spectral/Schur/Frobenius metrics, tail metrics, selected-mode fields,
parent and band failure keys, exact-anchor digests, provenance locks, and the
claim firewall.  The independent checker uses its own prime sieve and
reverse shell order, recomputes the eigensystems, and checks the stored
fields within explicit tolerances.  The adversarial suite mutates protocol,
provenance, row census, band definition, metrics, mode fields, audit counts,
anchor, firewall, and clue fields.

Local Bridge-B runs producer, independent replay, and stress checks in both
normal and optimized Python modes.  It requires empty standard error and
byte-identical normal/optimized output.  The official Route-A/Route-B
evaluator files are not present in this checkout; no official pass is
asserted.

## Numerical status

The `B3` band retains all six beta=2 full spectral failures.  Its beta=2
spectral failure census is `6/9`, its beta=2 Schur failure census is `0/9`,
and its baseline beta=0 census is `9/9` for both caps.  The six parent
failure rows have near-block absolute-Rayleigh retention at least
`0.99157117644491055`.

The result remains finite-scoped.  `ARITHMETIC_ADVANCE=NO`,
`FIXED_POWER_CREDIT=0`, `FULL_GATE_B=OPEN`, and the twin-prime result is
`NONE`.
