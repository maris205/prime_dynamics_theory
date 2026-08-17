# Theorem ledger

## Proven statements

`PROVED` — Moving-hole identity.  For every `q>=2`, every complex row
`z in C^q`, and every deleted residue `h`,

```text
V_h = V_all - q/(q-1)|z_h-mu|^2.
```

`PROVED` — Projector form and sharp spectrum.  With
`v_h=sqrt(q/(q-1))(e_h-q^-1 1)`, one has
`V_h=V_all-|<z,v_h>|^2`.  For `h!=0`, `q>2`, the defect
`P_{v_0}-P_{v_h}` has nonzero eigenvalues
`+/-sqrt(q(q-2))/(q-1)`.  It degenerates to zero for `q=2` or `h=0`.

`PROVED` — Exact `q-2` diagonal lift:

```text
R_h-R_0
 = q/(q-1)(|z_0-mu|^2-|z_h-mu|^2)
   + (q-2)/(q-1)(E_h-E_0).
```

The V59 row has outer weight `q`; omitting it is invalid.

`PROVED` — Translation compiler.  Under `n=s+m`, the deleted local residue is
`h_q=-s mod q`.  The common physical phase cancels in variances.  When two
packets use different own origins, the correct common-origin conversion is
`W_r^common=e(vd/H)W_{r-d}^own`, where `d=s_w-s_beta`.

`PROVED` — Four-packet lift.  For `a^(j)=beta+i^j w`, weights `i^j/4`
recover the polarized defect with the cross-diagonal term
`(q-2)/(q-1)(F_h-F_0)`.

`PROVED` — Deterministic block payment.  Under the paper's bounded-support,
bounded-overlap, coefficient-envelope, and Schwartz-kernel hypotheses,

```text
sum_{b,c}|M_bc| << A_beta A_w J(H^2+HQ+Q^2).
```

The proof integrates first, uses
`||1_{m=r(q)}-1/q||_1 << H/q+1`, preserves Schwartz separation, and obtains
`J`, not `J^2`.

`PROVED` — At `H=x^(21/32)`, `Q=x^(1/3)`, and
`J=x/H*x^o(1)`, the translation defect is
`x^(53/32+o(1))=x^(5/3-1/96+o(1))`; hence it pays every fixed
`1/400 < delta' < 1/96`.

## Classification

```text
CLAIM_LEVEL=PROVED_STRUCTURAL_L1
V60_ROUTE_ADVANCE=YES
V60_TRANSLATION_SUBGATE_DELTA=1_OVER_96_PROVED
V60_TRANSLATION_SUBGATE_STRICT_1_OVER_400=PAID
V60_FULL_GATE_B_STRICT_1_OVER_400=UNPAID
V60_ARITHMETIC_ADVANCE=NO
V60_FIXED_ATOM_CREDIT=0
V60_L2=NONE
TPC_207_TRIGGER=true
```

## Strongest positive result

The formerly opaque translation mismatch is removed as a fatal obstruction:
it is an exact rank-two leverage correction plus a mandatory two-residue
diagonal-energy correction, and the complete correction is deterministically
payable at the `1/96` clock after block reassembly.

## Strongest obstruction

The defect operator norm tends to one.  Finite rank alone supplies no saving,
and same-residue multi-spikes can retain quadratic-size defects before the
localized block geometry is used.

## Open theorem

Prove a power-saving theorem for the standard zero-hole, prime-only,
`q`-weighted, kernel-localized, exact-diagonal-subtracted signed remainder of
the four literal V59 packets, uniformly in block and frequency, together with
collective reassembly.

## Reusable structure

The reusable object is the leave-one-out projector calculus:

```text
moving physical row = standard zero-hole row
                    + selected leverage difference
                    + selected diagonal-energy difference.
```

It cleanly separates coordinate translation from the arithmetic BDH engine.

## ROUND2_CLUE

In additive DFT coordinates, the bare leverage difference has coefficient
`1/q^2` and factor `1-e_q((k-l)h_q)`.  After the exact `q/(q-1)` correction
prefactor its coefficient is `1/[q(q-1)]`; the outer BDH weight is separate.
The selector vanishes on `k=l`.  The next attack should test
whether this off-equal-frequency selector can be compiled jointly with the
zero-hole signed remainder without applying triangle inequalities inside the
four-packet or block sums.
