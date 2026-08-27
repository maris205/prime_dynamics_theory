# TPC-277 — Four-packet gain floor and a source-level lower-bound attack

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

For four actual packet vectors, the exact universal inequality is
`G <= 4D`, hence `D/G >= 1/4`; if the net signed cross term is nonpositive,
the sharper conditional floor is `D/G >= 1`.  An exact replay of the same
literal TPC source on eight registered/extended rows has negative net cross
term and `D/G>1` on every row, but the row at `N=192` has gain below `1.01`.

The finite scan therefore gives a real source-level diagnostic while refusing
to promote a bounded finite gain to a polynomial lower bound.

## What is new

- a sharp four-packet geometric gain floor and its equality model;
- the exact cancellation coordinate
  `kappa=(D-G)/D=1-1/r` and its inverse relation to gain;
- a matrix-free exact-rational replay of the actual prime-shell source at
  eight scales, including new `N=512,768,1024,1536,2048` rows;
- a scoped finite obstruction to the stronger one-percent gain floor;
- an explicit statement of the missing source-level theorem needed for any
  positive power credit.

## Claim ceiling

```text
PROVED_EXACT = G<=4D; E<=0 => G<=D; r=(1-kappa)^(-1)
NUMERICALLY_CERTIFIED_FINITE = exact source replay on 8 rows
REFUTED_SCOPED = r>=101/100 on this finite registry
OPEN = uniform growing signed gain; arithmetic L2; full Gate B
FIXED_POWER_CREDIT = 0
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc277_four_packet_gain_floor_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc277_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc277_gain_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The source replay uses
the frozen TPC-268 engine and the released TPC-275 result as provenance
anchors.  The Session-named `propose.md` and evaluator files are absent in
this checkout; the proof package, exact certificate, independent replay,
stress audit, and Bridge-B checker are the available fail-closed fallback.
