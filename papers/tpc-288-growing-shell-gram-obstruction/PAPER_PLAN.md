# TPC-288 paper plan

## Question

Does the finite prime-shell cancellation recorded by TPC-287 survive when the
shell and source scale are enlarged, and can a small four-block scalar
attachment be promoted to a physical output-energy saving?

## Claim-driven contributions

1. Define the literal deleted-diagonal prime component matrices, their output
   vectors, and the source-output Gram matrix on the same frozen TPC-268
   operator.
2. Prove the finite operator, output, scalar-attachment, energy, and Gram-PSD
   identities exactly.
3. Build a joint scale/shell path reaching 17 prime components, plus an
   independent height/cutoff control grid at the 15-component shell.
4. Certify full rank of every output Gram matrix and full active rank of six
   aggregate physical matrices by rational-to-finite-field witnesses.
5. Certify a finite obstruction: 13 rows have scalar retention upper bound
   below 1/10 while the exact vector output-energy ratio is greater than one.

## Evidence map

| Claim | Evidence |
|---|---|
| Exact identities | `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md` |
| Growth/control grid | producer and canonical JSON |
| Gram spectrum rank | exact rational vectors plus modular rank |
| Physical active full rank | six selected modular operator witnesses |
| Scalar/energy mismatch | exact energy ratios and interval retention upper bounds |
| Reproducibility | independent checker, optimized replay, stress audit |
| Route ceiling | claim firewall and Bridge-B checker |

## Non-claims

The grid is finite and declared.  It is not a growing-shell theorem, a
uniform source theorem, an arithmetic `L2` estimate, a fixed-power saving, a
Gate-B proof, or a twin-prime theorem.  Full rank and positive Gram spectrum
do not themselves provide an upper bound with a power saving.

## Next-paper trigger

`TEST_SOURCE_NATIVE_CROSS_PRIME_GRAM_BOUNDS_BEYOND_FINITE_FULL_RANK_OBSTRUCTION`
