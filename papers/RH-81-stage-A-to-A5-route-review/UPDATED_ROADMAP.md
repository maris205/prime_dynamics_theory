# Revised RH roadmap after the RH-72--RH-81 block

Date: July 2026

This roadmap supersedes the RH-71 checkpoint while preserving its claim
discipline. Green means closed only in the exact stated scope. Five validated
noise scales are not silently promoted to an all-level theorem.

## Executive verdict

The block made more progress than the previous roadmap expected:

1. the complete finite-scale folded-Gaussian, rank-two deflation, transfer,
   and Hardy chain is now green;
2. the remaining Stage-A issue has been compressed to one all-level theorem,
   with two alternative sufficient formulations;
3. conditional Stage A now propagates through intrinsic square trace norm and
   shrinking-disk Fredholm determinants;
4. two tempting fixed-disk shortcuts have been closed negatively;
5. the viable A5 object is an exact moving-cloud relative determinant.

The preferred route is

    all-level postblock effective-rank decay
        -> unconditional Stage A1/A4
        -> actual moving-cloud Riesz factor
        -> cloud coefficient bridge + complement trace-class limit
        -> relative fixed-disk determinant.

The RH-75 all-level full-block law remains a genuine fallback for the first
arrow.

## Stage ledger

| Gate | Status | Current meaning |
|---|---|---|
| A1 finite-scale assembly/deflation/Hardy chain | green | RH-72--RH-74 close all ten channels at five scales |
| A1 all-level full-block law | amber | RH-75 gives exact sufficient constants, verified only at anchors |
| A1 all-level postblock rank law | amber, preferred | RH-77 gives exceptional finite-scale compression; analytic decay remains open |
| A1 single-arc phase route | red | RH-76 broad-arc and moment barriers reject this explanation |
| A4 conditional identification | green | RH-78 closes composition under either all-level corridor |
| A4 unconditional identification | amber | inherits the sole Stage-A all-level wall |
| A4 conditional trace-norm squares | green | RH-79 transfers intrinsic operator control to two-step trace norm |
| A4 conditional shrinking-disk determinant | green | RH-79 closes disks `R=O(sigma)` |
| A5 generic absolute fixed-disk continuity | red as a method | `exp(O(R/sigma))` is nonuniform |
| A5 fixed scalar pole cancellation | red in canonical model | RH-80 proves exterior exponential growth |
| A5 moving-cloud factorization algebra | green | exact reducing factorization and relative determinant bounds |
| A5 actual cloud/complement theorem | amber | projection, coefficient bridge, and complement limit remain open |
| B canonical scattering completion | not started | wait for a relative A5 object |
| C self-adjoint realization and counting | not started | no operator or `T log T` law |
| D arithmetic zeta identity | not started | no prime-power trace formula or zero identification |

## Immediate priority: RH-82

Prove an all-level postblock singular-value decay theorem. A useful target is

    s_{r+1}(O_k A_k^{M_k} S_k)
        <= C polylog(k) exp(-c r)

or any bound implying a rank `r_k=polylog(k)` future approximation with zero
power of `sigma_k`. The proof should exploit smoothing after one production
block, rank-two peripheral removal, and the low-dimensional source/observation
geometry. It should not attempt to compress the raw phase measure, which RH-76
showed is broad.

Preferred proof order:

1. derive approximation-number bounds for the folded Gaussian block after
   parity/Perron deflation;
2. propagate them through the normalized source and observation maps;
3. control repeated blocks without paying a raw ambient-dimension factor;
4. compare the resulting rank law with the RH-78 zero-power budget;
5. validate constants against the RH-77 five-scale certificate.

If this route fails because postblock rank necessarily carries a forbidden
power of `sigma`, return to the RH-75 full-block contraction law and seek an
inductive or analytic block estimate.

## Parallel A5 preparation

A5 work can proceed without claiming Stage A is closed:

1. define an actual moving contour enclosing the finite noisy cloud;
2. construct and validate its Riesz projection;
3. prove coefficient convergence of the resulting finite cloud polynomial to
   the deterministic double-pole factor;
4. estimate the two-step trace norm on the complementary block;
5. test whether complement convergence is uniform on fixed disks.

The fixed factor `(1-w/lambda)^2` is not a substitute for this construction.

## Continue, fallback, and stopping conditions

Continue the Stage-A route if either all-level corridor has zero or admissible
Hardy sigma power. Prefer the effective-rank corridor while it preserves the
strong RH-77 compression.

Fallback to RH-75 if a rigorous rank lower bound defeats the effective-rank
route but does not defeat block contraction.

Reassess Stage A only if rigorous lower bounds defeat both corridors under
every admissible mesh schedule. Reassess A5 if every natural moving-cloud
extraction leaves a complement whose relative determinant is non-normal on
the required fixed domain.

Failure of one finite engineering target, one contour choice, or one cloud
selection is not a stopping condition.

## Claim boundary

No canonical scattering function, self-adjoint Hilbert--Polya operator,
intrinsic `T log T` counting law, prime-power trace identity, zeta-zero
identification, or Riemann-hypothesis result has been obtained. Those later
stages remain downstream research goals, not interpretations of the present
certificates.

