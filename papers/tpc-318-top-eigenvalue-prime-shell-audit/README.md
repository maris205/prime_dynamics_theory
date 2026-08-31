# TPC-318 — Finite top-eigenvalue audit of the literal prime-shell operator

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-318 takes the exact finite prime-shell matrix frozen by TPC-317 and reads
the largest eigenvalue of its Gram matrix directly.  On
`X=640,1280,2560`, `Q={24,36,54,80}`, `s={1,2}`, all 24 rows have dual-solver
finite intervals, and all 16 adjacent normalized top-eigenvalue comparisons
strictly decrease.  The finite log-base-two slopes range from about
`-0.9972` to `-0.4239`.

The same audit exposes the necessary obstruction: 10 of 24 rows have a
relative top/second-eigenvalue gap below `0.01`, with minimum about `0.001704`.
The normalized trend therefore does not establish an unnormalized growing
power saving or a canonical arithmetic eigenvector.

## Claim firewall

```text
PROVED_EXACT_FINITE = PSD spectrum facts and Weyl perturbation inequality
NUMERICALLY_CERTIFIED_FINITE = 24 top rows; 16 strict decreases;
                               dual solver/residual/gap audit
NUMERICAL_OBSERVATION = finite normalized spectral compression
OPEN = clustered eigenspace theorem; unnormalized/growing law; arithmetic
       cancellation; normalization; fixed-power credit; full Gate B;
       twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The finite intervals use a safe uniform literal-entry bound `|K|<=160`, dual
shell order, solver spread, residual, and Weyl's elementary norm conversion.
This is a numerical certificate under the declared finite model, not an exact
algebraic eigenvalue calculation or an asymptotic theorem.

The complete package is `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`,
`PROOF_PACKAGE.md`, `notes/`, `code/`, `experiments/`, `results/`, and
`paper/`.  The canonical outputs are
[results/tpc318_certificate.json](results/tpc318_certificate.json) and
[paper/paper.pdf](paper/paper.pdf).

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc318_top_eigenvalue_prime_shell_audit.py --write
python -B code/tpc318_top_eigenvalue_prime_shell_audit.py --check
python -O -B code/tpc318_top_eigenvalue_prime_shell_audit.py --check
python -B experiments/tpc318_independent_checker.py --check
python -O -B experiments/tpc318_independent_checker.py --check
python -B experiments/tpc318_spectral_stress.py
python -O -B experiments/tpc318_spectral_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc318_top_eigenvalue_checker.py --check
```
