# TPC-311 computational protocol

1. Lock TPC-310's code/result and TPC-309's code/result by normalized SHA-256.
2. Parse the 162 TPC-309 envelope rows without regenerating labels, shells, or
   physical matrices.
3. Form one profile-pooled interval for each fixed
   `(transition, exponent, tau, radius)` cell.
4. Form six declared equal-stratum blocks: native calibration, native
   confirmation, native full, and the corresponding all-radius controls.
5. Form the exponent, transition, leave-one-transition, and leave-one-ladder
   native sensitivity blocks.
6. Classify with strict thresholds `0.9` and `1.1`; preserve unresolved cells.
7. Write canonical JSON; `--check` must reproduce it byte for byte.
8. Run the independent parser/replay and exact rational stress suite in normal
   and optimized Python modes.

The parent values are padded float-replay enclosures.  The producer uses high
precision for finite endpoint aggregation, while the independent checker uses
ordinary double precision with documented replay slack.  Neither is a
directed-rounding certificate.
