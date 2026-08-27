# TPC-274 — Projected output Frobenius envelope

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

On the locked literal V59 operator and TPC-269 growing-cutoff registry, the
projection-aware cancellation-free envelope
`G_F=||(I-P_3)A||_F^2||beta||_2^2` is proved valid, but its certified gap from
the actual output residual exceeds 50 on all 12 registered rows; the induced
conservative margin proxy satisfies `m_F^2<1/64` on all 12 rows.

## What advances

- gives a reusable projected-operator inequality rather than a raw total-norm
  bound;
- constructs `A_perp` and its Frobenius energy exactly over rational arithmetic;
- independently replays matrix multiplication, projection, envelope, and
  interval transfers from the released TPC-268 engine;
- quantifies why a cancellation-free output proof cannot certify the required
  margin on this finite interface;
- leaves signed output reassembly as the next explicit theorem target.

The statement is method-relative and finite.  `G_F/G_perp>50` is a gap between
an envelope and the observed finite output, not an asymptotic lower bound for
any sequence.  Likewise `m_F^2<1/64` says the envelope is too weak; it does not
prove that the actual margin is below `1/8`.

## Claim ceiling

```text
PROVED_EXACT_FINITE = G_perp <= ||A_perp||_F^2 ||beta||_2^2
NUMERICALLY_CERTIFIED = 12-row envelope gap and conservative-margin audit
INSUFFICIENT_SCOPED = cancellation-free projected output route
OPEN = source-level output estimate and signed four-packet reassembly
FIXED_POWER_CREDIT = 0
ARITHMETIC_ADVANCE = NO
L2 = NONE
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc274_projected_output_envelope_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc274_projected_output_envelope_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc274_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc274_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc274_envelope_stress.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc274_envelope_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
`propose.md` and evaluator files are absent in this checkout; the local
proof/checker fallback is recorded in `notes/route_evaluation.md`.
