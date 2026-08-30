# TPC-316 — Literal Arithmetic `L2` Envelope on the Fresh Prime-Shell Panel

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-316 turns the deleted-diagonal prime-shell formula into the literal finite
operator

```text
A_(Q,s,X): ell^2(I_X) -> ell^2(S_Q x I_X)
```

and proves the finite Frobenius interface

```text
N^(-1)||A beta||_2^2 <= (HS(A)^2/N)||beta||_2^2.
```

The Hilbert--Schmidt mass is evaluated exactly by a difference/residue-count
identity, not by floating point.  On the two disjoint panels
`I_640={321,...,640}` and `I_1280={641,...,1280}`, there are 16 exact rows
and 80 coordinate probes.  The normalized Hilbert--Schmidt upper envelope
increases from `X=640` to `X=1280` in all eight matched `(Q,s)` rows, by
factors between `1.074` and `1.316`.  On the fresh `X=1280` panel the
Frobenius upper envelope is over 517 times the strongest five-point coordinate
lower witness in every row.

This is a genuine finite literal `L2` envelope and a scoped obstruction to
using that envelope as evidence for a decaying power.  It does not estimate
the true operator norm asymptotically, pay arithmetic `L2` credit for Route B,
or prove anything about twin primes.

## What is new relative to TPC-315

* TPC-315 studied Gram vectors produced by one locked source coefficient
  vector.  TPC-316 retains the same physical formula but exposes every source
  coordinate as a column of the full source-to-output operator.
* The Hilbert--Schmidt mass is compressed exactly to counts of admissible
  residue pairs at each signed difference.  This makes the literal finite
  `L2` interface independently replayable without importing the producer.
* Five endpoint-inclusive coordinate columns per row give exact lower
  witnesses for the operator norm.  The resulting upper/lower gap is recorded
  rather than silently treating the Frobenius bound as the operator norm.
* A disjoint two-panel comparison records a finite obstruction: the normalized
  Frobenius envelope rises on all eight matched rows, while the finite gap is
  large.  The comparison is explicitly labelled finite observation only.

## Claim firewall

```text
PROVED_EXACT_FINITE = literal rational source-to-output matrix;
                       difference/residue Hilbert--Schmidt identity;
                       Frobenius L2 interface; coordinate lower witnesses
NUMERICALLY_CERTIFIED_FINITE = 16 rows, 80 probes, 8/8 two-panel rises;
                               exact rational digests and independent replay
NUMERICAL_OBSERVATION = the two-panel normalized-HS rise is a finite trend
REFUTED_SCOPED = normalized Hilbert--Schmidt envelope is not a decaying
                 proxy on these two declared panels
OPEN = true growing operator-norm estimate; arithmetic cancellation beyond
       Frobenius; canonical normalization; fixed-power credit; full Gate B
       and twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The finite matrix is the same locked TPC-268 physical engine used by the
previous releases.  The two-scale comparison therefore is not an external
physical holdout.  The Session-named `propose.md` and Route-A/Route-B
evaluator files are absent from this checkout; `notes/route_evaluation.md`,
the proof package, the independent checker, and the local Bridge-B checker
are fail-closed substitutes and no official evaluator pass is asserted.

## Reproduction

From this project directory:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc316_literal_arithmetic_l2_fresh_panel.py --write
python -B code/tpc316_literal_arithmetic_l2_fresh_panel.py --check
python -O -B code/tpc316_literal_arithmetic_l2_fresh_panel.py --check
python -B experiments/tpc316_independent_checker.py --check
python -O -B experiments/tpc316_independent_checker.py --check
python -B experiments/tpc316_l2_stress.py
python -O -B experiments/tpc316_l2_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc316_literal_arithmetic_l2_checker.py --check
```

The canonical certificate is
[results/tpc316_certificate.json](results/tpc316_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project
package.  The next route question is whether a substantially sharper,
growing operator estimate can be proved from arithmetic cancellation rather
than from the Frobenius envelope.
