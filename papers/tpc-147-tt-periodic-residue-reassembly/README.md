# TPC-147: Periodic residue reassembly

Paper title:

> *Periodic Reassembly Inside a Quantitative Multiplicative
> Correlation Corridor: Exact Quantifiers, Zero Residue-Census Loss,
> and Non-Prefix Scope*

## Core result

The paper source-locks Theorem 3.1 of Tao--Teravainen
(`arXiv:2512.01739v2`) in its general multiplicative-function form.
For one fixed admissible pair of multiplicative functions, its
exceptional set is uniform in all allowed moduli, residues and shifts.

Consequently, if an arithmetic progression of modulus `Q` carries a
bounded periodic multiplier of period `R`, and `Q*R` stays inside the
source modulus envelope, splitting the multiplier into `R` residue
classes costs no power of `R`:

```text
R classes * N/(Q*R) mass per class = N/Q.
```

Thus bounded periodic masks should be reassembled with the native
`W/N` normalization rather than charged a naive residue-count
`l1` loss.

The theorem remains a natural-average, good-scale L1 result.  It does
not contain an arbitrary physical weight, a generic additive phase,
an arbitrary interval origin, an all-prefix maximum, or a four-point
correlation.

## Machine certificate

The deterministic audit:

- records the exact local exceptional-set quantifiers;
- distinguishes Theorem 3.1 from the global Liouville affine remark;
- verifies the finite residue partition exactly;
- verifies cancellation of the period count against progression
  density;
- rejects wrong normalizations, over-height total moduli, global-set
  promotion, arbitrary weights, generic phases and all-prefix claims;
- records that no positive L2, fixed X-power, `1/400`, prime-pair or
  twin-prime result is proved.

## Reproduce

```powershell
python experiments/tpc147_periodic_reassembly_audit.py
python experiments/tpc147_periodic_reassembly_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Stable archival PDF:

`tpc-147-tt-periodic-residue-reassembly.pdf`
