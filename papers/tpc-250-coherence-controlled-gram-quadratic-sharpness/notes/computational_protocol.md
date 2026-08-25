# Computational Protocol

All release checks use Python's exact `fractions.Fraction` arithmetic.  Gram
positive semidefiniteness is checked by every principal minor for the small
fixtures.  The independent checker contains no producer import and recomputes
the theorem semantics from the JSON primitives.

Release commands, from the project root:

```bash
python -B code/tpc250_coherence_certificate.py --check
python -B experiments/tpc250_independent_checker.py --check
python -O -B experiments/tpc250_independent_checker.py --check
python -B experiments/tpc250_coherence_stress.py --check
python -O -B experiments/tpc250_coherence_stress.py --check
```

The checker rejects a canonical-type mutation, a semantic mutation, a
firewall mutation whose digest has been rebound, and a stale-digest mutation.
Release logic contains no Python optimization-sensitive assertion statement.

The stress script deterministically checks 128 rational unit-vector weighted
families plus the `D=0` and singleton-active edge cases.  Its label is
`NUMERICAL_FINITE_ILLUSTRATION_ONLY`; it is not asymptotic evidence.
