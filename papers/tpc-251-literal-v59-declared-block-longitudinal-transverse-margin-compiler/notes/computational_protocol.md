# Computational Protocol

The release certificate uses `fractions.Fraction` throughout the real
operator replay.  A separate Gaussian-rational fixture stores each complex
scalar as a pair of canonical rational strings and detects dropped
conjugations in both `C_long` and the projected Gram subtraction.

The independent checker imports no producer module.  It uses strict duplicate
JSON-key rejection, canonical rational parsing, exact integer type identity,
an exhaustive/nonempty partition audit, full operator recomputation, and
digest rebinding tests.  Its mutation suite rejects 15 mutations, including
typed, partition, source, operator, projected-Gram, coherence, conjugation,
equality, firewall, stale-digest, and duplicate-key attacks.

Release commands from this project directory:

```text
python -B code/tpc251_margin_certificate.py --check
python -B experiments/tpc251_independent_checker.py --check
python -O -B experiments/tpc251_independent_checker.py --check
python -B experiments/tpc251_margin_stress.py --check
python -O -B experiments/tpc251_margin_stress.py --check
```

The stress script deterministically checks 160 exact-rational two-block
partitions and probe families.  Four-coordinate Hadamard bases keep every
flat direction, probe norm, coherence value, and comparison rational.  The
stress label is `FINITE_STRUCTURAL_STRESS_NOT_ASYMPTOTIC`; finite examples do
not estimate literal V59 asymptotics.

Python is invoked with `-B`, and release logic uses explicit exceptions rather
than optimization-sensitive `assert` statements.
