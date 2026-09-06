# TPC-418 — finite-family shell-parity envelope

This package proves a finite synthetic theorem for any declared finite family
of disjoint ordered complete prime shells. The corrected parity variable is

```text
epsilon_j = (-1)^(sum before block j)       # start sign
sigma_j   = epsilon_j * (-1)^(n_j+1)         # signed-block sign
```

The envelope groups `b_j` by `sigma_j`, not by `epsilon_j`. A mixed-parity
fixture records that the old grouping can fail. The fixed four-shell replay
retains the TPC417 shell family and all 75483 primes; a small complete-shell
fixture and the regression fixture provide independent audit coverage.

All theorem quantities are exact `Fraction` values serialized as canonical
rational strings. The release is finite and synthetic only. It asserts no
growing uniform theorem, physical `h0`, arithmetic sign or `L2` result,
fixed-power credit, Route-B closure, or twin-prime result.

Commands:

```bash
python -B papers/tpc-418-c1-shell-parity-envelope/code/tpc418_c1_shell_parity_envelope.py --write
python -B papers/tpc-418-c1-shell-parity-envelope/code/tpc418_c1_shell_parity_envelope.py --check
python -B papers/tpc-418-c1-shell-parity-envelope/experiments/tpc418_independent_checker.py --check
python -B papers/tpc-418-c1-shell-parity-envelope/experiments/tpc418_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py --check
```

Each command is also run with `python -O -B`. The Bridge-B checker verifies
the exclusive package, certificate digest, independent replay, mutation
tests, and compiled PDFs when they are available.
