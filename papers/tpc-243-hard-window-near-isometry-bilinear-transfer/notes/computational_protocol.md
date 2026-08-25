# Computational protocol

All theorem-facing fixture calculations use `fractions.Fraction` and Gaussian
pairs of exact fractions. Quarter frequencies are evaluated through exact
fourth roots of unity. No floating-point comparison is used.

## Producer and certificate

The producer exposes a required mutually exclusive `--write`/`--check` group.
It writes one-line sorted-key compact ASCII JSON with one trailing newline and
a SHA-256 digest of the payload excluding the digest field. Check mode never
writes.

## Independent checker

The independent checker does not import the producer. It separately implements
Gaussian arithmetic, the hard-window Gram, coefficient and sequence inner
products, strict JSON parsing, source hashing, and the expected complete
nested schema. Equality is type-sensitive, so `True` cannot replace integer
`1`. Fraction records must be reduced and have positive denominators.

Both checkers reject duplicate JSON keys and nonfinite JSON constants. Semantic
mutations recompute the payload digest before validation. Hostile rebound tests
replace the source lock, promote arithmetic status, promote strict `1/400`,
promote a twin-prime result, inject an extra nested key, and reverse the signed
orientation; every variant must fail after digest renewal.

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc243_hard_window_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc243_hard_window_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O code/tpc243_hard_window_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc243_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O experiments/tpc243_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc243_hard_window_stress.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O experiments/tpc243_hard_window_stress.py --check
```

Normal and optimized stdout must be byte-identical for each checker pair, and
all stderr streams must be empty. Validation uses no `assert`, so optimization
cannot bypass a gate.

## Finite scopes

- Main fixture: four quarter frequencies on `M=-3`, `N=17`.
- Stress intervals: a fixed finite list including degenerate and aligned
  windows.
- Stress coefficients: a finite Gaussian-rational alphabet in four
  coordinates.

Every finite result is labeled `NUMERICAL_FINITE_ILLUSTRATION_ONLY`.

## PDF build and machine-readable mathematics

The manuscript uses pdfLaTeX with Latin Modern fonts.  Four displayed formulas
that require extensible math glyphs also carry PDF `ActualText` spans through
`accsupp`; the visible formulas are unchanged, while text extraction receives a
plain-ASCII semantic rendering instead of font-internal control codes.

Build from `paper/` and retain the final `main.log` in the external release-QA
scratch directory:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdftotext -layout main.pdf extracted.txt
pdftotext -bbox-layout main.pdf bbox.xhtml
```

Release QA requires zero non-page-control C0 bytes in `extracted.txt`, strict XML
parsing of `bbox.xhtml`, no LaTeX warnings or over/underfull boxes, all fonts
embedded, and visual inspection of every rendered page.  The build log and page
renders are QA evidence, not theorem evidence and not committed build products.
