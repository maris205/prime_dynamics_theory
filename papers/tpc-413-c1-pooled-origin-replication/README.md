# TPC-413: Pooled origin replication

TPC-413 repeats the pooled TPC-412 four-height profile at three distinct CRT
representatives `o_s=r+sL`, `s=1,2,3`, producing 12 exact rows.  The two full
shells retain `16458` primes, use shell-local amplitudes, and have pooled
`m_minus=m_plus=8229`; every row uses `N=4H`.

The exact certificate, fresh-sieve literal replay of every per-prime and
per-coordinate mask, and 12 mutation tests pass.  Since representatives differ
by CRT periods, the local values are exactly replicated; this is an exact
finite invariance audit, not evidence for a growing physical theorem.

Status: `PROVED_EXACT_FINITE_POOLED_ORIGIN_REPLICATION`;
`ARITHMETIC_ADVANCE=NO`; `FIXED_POWER_CREDIT=0`; `FULL_GATE_B=OPEN`.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 python -B code/tpc413_c1_pooled_origin_replication.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc413_independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc413_adversarial_certificate_stress.py --check

The next scoped question is `TEST_C1_POOLED_ORIGIN_REPLICATION`.
