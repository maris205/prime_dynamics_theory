# Source lock

## Harper crosswalk

Primary source:

Adam J. Harper, *Simple Barban--Davenport--Halberstam type asymptotics for
general sequences*, arXiv:2412.19644v1 (2024).

Harper groups residue classes by `(a,q)`.  For prime `q`, the non-unit class
`a=0 mod q` is a singleton and contributes zero variance.  Consequently the
prime-modulus row in Harper's variance is exactly the zero-hole variance
`V_0` used here.

This paper isolates and proves the exact crosswalk from that zero-hole row to
the physical translated row `V_{h_q}`, with `h_q=-s mod q`.  The targeted
source search did not find this leave-one-out identity stated as a dedicated
moving-hole theorem.  No broad novelty claim is made.

## What the source does not provide

Harper's theorem controls an unweighted all-dyadic-moduli, gcd-grouped,
positive variance for one `q`-independent sequence under explicit structural
hypotheses.  It does not directly prove the V59 object, which is:

```text
prime-only
+ outer q weight
+ kernel localization
+ exact (q-2) diagonal subtraction
+ signed four-packet polarization
+ literal block packets
+ collective block reassembly.
```

The hypotheses required by Harper have not been verified uniformly for all
literal V59 packets, block origins, and frequencies.  An all-moduli signed
asymptotic cannot be restricted to the prime subset by positivity after exact
diagonal subtraction.

## Internal source

The V59 object and its frozen scale ledger are repository-internal artifacts:

```text
TPC_HANDOFF.md, BOLD_CHANNEL_V59_SEALED_FOR_NEW_SESSION
research/tpc-big-road/ (V59 proof and checker lineage)
```

TPC-207 changes only the translation subgate.  It does not rewrite or reopen
the remaining V59 source locks.

## Source-locked claim

```text
SOURCE_LOCKED_HARPER_CROSSWALK=YES
HARPER_DIRECT_FULL_GATE_B_ATTACHMENT=NO
TRANSLATION_DEFECT_SEPARATELY_PAID=YES
ZERO_HOLE_PRIME_SIGNED_BDH_THEOREM=OPEN
```
