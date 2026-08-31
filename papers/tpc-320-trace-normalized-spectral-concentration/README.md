# TPC-320 — Scale-invariant spectral concentration

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## Status

    TPC320_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_TRACE_NORMALIZED_SPECTRAL_CONCENTRATION_AUDIT
    TPC320_ROUTE_ADVANCE = YES_SCOPED_SCALE_INVARIANT_SPECTRAL_READOUT
    TPC320_CONCENTRATION_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_ROWS_5_K
    TPC320_CONCENTRATION_DECREASES = NUMERICALLY_CERTIFIED_FINITE_80_OF_80
    TPC320_SCALE_INVARIANCE = PROVED_EXACT_FINITE
    TPC320_STABLE_RANK_GROWTH = NUMERICAL_OBSERVATION_FINITE_16_OF_16
    TPC320_PARTICIPATION_GROWTH = NUMERICAL_OBSERVATION_FINITE_16_OF_16
    TPC320_ENTROPY_CONTROL = NUMERICAL_OBSERVATION_MIXED
    TPC320_ARITHMETIC_ADVANCE = NO
    TPC320_FIXED_POWER_CREDIT = 0
    TPC320_FULL_GATE_B = OPEN
    TPC320_TWIN_PRIME_RESULT = NONE
    TPC320_STATUS = NUMERICALLY_CERTIFIED_FINITE_TRACE_NORMALIZED_SPECTRAL_CONCENTRATION_AUDIT
    TPC320_ROUND2_CLUE = AUDIT_SPECTRAL_PROFILE_STABILITY_ACROSS_SHELLS_OR_TEST_SIGNED_PROJECTOR_REASSEMBLY_BEFORE_ANY_ARITHMETIC_POWER_CLAIM

## Contribution

TPC-319 used \(F_k/N\), where \(N\) is the number of source columns.  TPC-320
removes that bookkeeping scale by studying

\[
C_k(G)=\frac{F_k(G)}{\operatorname{tr}G}.
\]

The exact algebra shows that \(C_k\), stable rank, participation rank, and
normalized entropy are unchanged by multiplying the Gram matrix by any positive
scalar.  On the same literal deleted-diagonal centered prime-shell operator,
the finite panel has 80/80 strict decreases of \(C_k\) across
\(X:640\to1280\to2560\), for \(k=1,2,4,8,16\).  Stable rank and participation
rank rise on all 16 adjacent row transitions as finite observations.

The entropy control is deliberately mixed rather than forced into the headline:
one scalar concentration law is not a substitute for a theorem about the full
spectral profile.

## Reproducible artifacts

- code/tpc320_trace_normalized_spectral_concentration.py — producer and
  canonical certificate writer/replayer.
- experiments/tpc320_independent_checker.py — independent matrix rebuild and
  full-spectrum replay.
- experiments/tpc320_concentration_stress.py — scalar-invariance, PSD,
  quotient-interval, and Weyl stress tests.
- results/tpc320_certificate.json — canonical finite certificate.
- paper/paper.pdf — compiled paper (identical to paper/main.pdf).
- notes/route_evaluation.md — scoped local Route-B assessment.
- research/tpc-big-road/bridge_b_tpc320_trace_normalized_spectral_concentration.md
  and its checker — fail-closed bridge record.

Run the core checks from the repository root:

    python -B papers/tpc-320-trace-normalized-spectral-concentration/code/tpc320_trace_normalized_spectral_concentration.py --check
    python -B papers/tpc-320-trace-normalized-spectral-concentration/experiments/tpc320_independent_checker.py --check
    python -B papers/tpc-320-trace-normalized-spectral-concentration/experiments/tpc320_concentration_stress.py --check

## Interpretation firewall

This is a finite spectral-shape audit.  It does not prove a uniform law in
\(X\), an asymptotic exponent, a signed prime-shell cancellation estimate, or
the twin-prime conjecture.  The Session-named evaluator files
propose.md, skills/route-a-evaluator.md, and skills/route-b-evaluator.md are
not present in this checkout; therefore the project records a local fail-closed
evaluation rather than an official evaluator pass.
