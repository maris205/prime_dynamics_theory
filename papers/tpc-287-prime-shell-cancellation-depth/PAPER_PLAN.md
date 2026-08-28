# TPC-287 paper plan

## Question

After TPC-286 separates the diagonal correction from the physical
deleted-diagonal operator, does the literal physical attachment exhibit
genuine multi-prime signed cancellation, or were the earlier sign changes
only two-term effects from a very small prime shell?

## Claim-driven contributions

1. Prove the exact finite shell-additivity identity: the physical shell
   output and every linear attachment are sums of their prime-indexed
   components.
2. Define an interval-certified cancellation-retention envelope from the
   shell attachment and the sum of component absolute masses.
3. Introduce a declared shell-cardinality ladder with exactly 1, 2, 3, 4, 5,
   6, and 7 primes, evaluated on the six frozen source baselines and both
   kernel exponents.
4. Certify the component signs, mixed-sign rows, retention thresholds, and
   leave-one-prime-out sign sensitivity with an independent replay and hostile
   mutation audit.
5. Close a map gap: the original TPC-284 control atlas has only one- or
   two-prime shells, while the expanded ladder reaches genuine multi-prime
   cancellation; neither finite observation is an asymptotic arithmetic
   $L^2$ theorem.

## Evidence map

| Claim | Evidence |
|---|---|
| Exact shell additivity | `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, theorem fields in the certificate |
| 1--7 prime shell ladder | producer, canonical JSON, independent checker |
| 336 component intervals | exact rational physical replay with outward interval endpoints |
| Cancellation depth census | 84 row records and aggregate finite audit |
| Reproducibility | TPC-286 parent lock and frozen TPC-268 engine lock, ordinary/optimized replay |
| Hostile rejection | mutations to theorem, ladder, components, ratios, flags, provenance, and rows |
| Route ceiling | claim firewall and fail-closed Bridge-B checker |

## Non-claims

The ladder is a declared finite shell experiment.  It does not prove a
growing-shell cancellation theorem, an average over all primes, a uniform
retention bound, a literal arithmetic $L^2$ estimate, fixed-power credit, Gate
B, or a twin-prime theorem.  The source profile, six baselines, and shell
anchors are modeling choices inherited or explicitly declared for map
exploration.

## Next-paper trigger

`TEST_CANCELLATION_STABILITY_UNDER_GROWING_SHELL_AND_SOURCE_CONTROLS`
