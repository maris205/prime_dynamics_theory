# Computational Protocol

## Exact certificate

The producer uses `fractions.Fraction` for every real and imaginary component.
Complex scalars are encoded as pairs of canonical rational strings. The
released JSON is one-line, key-sorted, ASCII, strict JSON with a terminal
newline; `NaN`, infinities, duplicate keys, noncanonical fractions, and
noncanonical whitespace are rejected. The SHA-256 payload digest is computed
over the same compact canonical encoding.

The independent checker imports no producer code. It independently checks:

- exact integer types and exhaustive nonempty partitions;
- `g=A beta` for every source fixture;
- the projector, covariance, and transverse updates, including conjugation;
- the fixed-family projected-Gram rank-one subtraction and its scope label;
- the same-source two-coordinate coarse/singleton replay;
- all two-coordinate legal partitions for four fixed `E` values;
- the stable-source counterexample to universal instability;
- singleton projected probes, Gram, `D,L,mu,U`, both radii, and `kappa` domain;
- 28 typed, semantic, source, firewall, digest, duplicate-key, nonfinite-token,
  and canonical-byte mutations.

## Deterministic stress

The stress suite checks 192 Gaussian-rational binary-refinement families. Each
family uses a random-looking but seeded exact `8 x 8` source operator, exact
`beta,w`, a balanced `4 -> 2+2` split, and a fixed three-probe family. It
checks projector and covariance identities, the exact squared Cauchy audit
behind `R_trans` monotonicity, the fixed-probe Gram update, and singleton
collapse. No floating-point arithmetic or optimization-sensitive `assert`
statement is used.

## Release commands

Run from the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-252-declared-partition-refinement-degeneracy/code/tpc252_partition_refinement_certificate.py --check
python -O -B papers/tpc-252-declared-partition-refinement-degeneracy/code/tpc252_partition_refinement_certificate.py --check
python -B papers/tpc-252-declared-partition-refinement-degeneracy/experiments/tpc252_independent_checker.py --check
python -O -B papers/tpc-252-declared-partition-refinement-degeneracy/experiments/tpc252_independent_checker.py --check
python -B papers/tpc-252-declared-partition-refinement-degeneracy/experiments/tpc252_partition_refinement_stress.py --check
python -O -B papers/tpc-252-declared-partition-refinement-degeneracy/experiments/tpc252_partition_refinement_stress.py --check
```

Normal and optimized output must be byte-identical for each script.

Compile from the paper directory with the required explicit passes:

```bash
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
bibtex paper
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
```

Audit `paper.log` for errors, undefined references/citations, bad boxes, and
warnings; use `pdfinfo`, `pdffonts`, and `pdftotext` for page, font, and text
checks. Render every page with `pdftoppm -png -r 160` into one unique
`/tmp/tpc252-render-*` directory and retain that directory for independent
visual QA.

All finite certificate and stress results are structural reproduction only,
not literal V59 arithmetic or asymptotic evidence.
