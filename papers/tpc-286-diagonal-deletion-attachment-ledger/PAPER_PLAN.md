# TPC-286 paper plan

## Question

After TPC-285 shows that diagonal deletion destroys the attractive residue
low-rank shortcut, how much of the observed finite source sensitivity is
carried by the deleted diagonal itself?

## Claim-driven contributions

1. Define the diagonal-including shell block, the physical block, and the
   explicit diagonal correction for the literal source model.
2. Prove the exact operator and scalar-attachment identities by linearity.
3. Replay all 72 TPC-284 controls and certify separate full, diagonal, and
   physical intervals with exact rational arithmetic plus outward interval
   serialization.
4. Record the finite sign census, the 15 full/physical sign flips, the 30
   opposition rows, and the 21 strict magnitude-dominance rows.
5. Make the obstruction precise: the diagonal correction is large and
   sign-sensitive on the registered atlas, so a centered-residue argument
   must explicitly pay for it.

## Evidence map

| Claim | Evidence |
|---|---|
| Exact split | `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, theorem fields in the certificate |
| 72-row finite ledger | producer, canonical JSON, independent checker |
| Reproducibility | parent hashes, frozen-engine hash, ordinary/optimized replay |
| Hostile rejection | eight mutations in `tpc286_diagonal_sensitivity_stress.py` |
| Route ceiling | claim firewall and fail-closed Bridge-B checker |

## Non-claims

The ledger does not prove diagonal dominance for growing scales, a signed
full-shell cancellation estimate, an arithmetic $L^2$ inequality, a fixed
power gain, Gate B, or a twin-prime theorem.  The source profile and finite
schedule remain the declared modeling choices of the earlier TPC artifacts.

## Next-paper trigger

`SEEK_SIGNED_FULL_SHELL_CANCELLATION_AFTER_DIAGONAL_ATTACHMENT_LEDGER`
