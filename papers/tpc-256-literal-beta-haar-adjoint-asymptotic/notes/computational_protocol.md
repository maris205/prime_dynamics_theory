# TPC-256 computational protocol

## Purpose

The executables verify provenance, exact finite bookkeeping, schemas, and
adversarial controls.  They do not prove the large-`x` PNT input or infer an
asymptotic from finite data.

Set:

```bash
export PYTHONDONTWRITEBYTECODE=1
```

## Producer

```bash
python -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/code/tpc256_literal_beta_haar_certificate.py --check
python -O -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/code/tpc256_literal_beta_haar_certificate.py --check
```

The producer reconstructs the canonical JSON in memory and requires the
committed result to be byte-identical.  It checks:

- baseline commit and eight `git show` source hashes;
- 19 exact source-claim markers;
- rational exponent identities `-67/400`, `5/6`, `55/48`, `56/48`, and
  gap `1/48`;
- 64 integer/noninteger rank fixtures and 1,536 divisor layers;
- 90 complete combined unit rows and 8,814 mask terms;
- hard-window and child-jump cardinality rules;
- two finite beta-Haar observations, explicitly carrying proof credit
  `NONE`.

`--emit` prints the expected canonical JSON to stdout and never writes it.

## Independent checker

```bash
python -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/experiments/tpc256_independent_checker.py --check
python -O -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/experiments/tpc256_independent_checker.py --check
```

The independent implementation imports no producer code.  It separately
reconstructs source hashes, finite counts, beta samples, constants, exponents,
firewall markers, and the exact project manifest.  It rejects 112 mutations
across 14 semantic classes and parses all three Python programs to reject
language-level assertion statements.

## Stress program

```bash
python -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/experiments/tpc256_beta_haar_asymptotic_stress.py --check
python -O -B papers/tpc-256-literal-beta-haar-adjoint-asymptotic/experiments/tpc256_beta_haar_asymptotic_stress.py --check
```

The stress program executes 192 deterministic families:

```text
96 integer clocks
96 noninteger rational clocks
```

Every family checks ordered-rank normalization, 32 divisor-density layers,
combined and separately exposed unit-mask zero modes, pointwise mask bounds,
hard-window crossing counts, child-jump crossing counts, and the exact
exponent ledger.

## Optimization invariant

For all three programs:

```text
normal exit code = 0
optimized exit code = 0
normal stderr = empty
optimized stderr = empty
normal stdout = optimized stdout byte for byte
```

No Python `assert` statement is used, so optimized execution cannot erase a
validation condition.

## PDF build and QA

From the `paper/` directory run exactly:

```bash
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
bibtex paper
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
```

Release QA requires no LaTeX warnings, undefined references, overfull or
underfull boxes; all fonts embedded, subsetted, and Unicode-mapped; and every
rendered page visually inspected from a temporary directory outside the
repository.
