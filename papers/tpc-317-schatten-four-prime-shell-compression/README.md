# TPC-317 — Schatten-4 Compression of the Literal Prime-Shell Operator

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong
University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-317 keeps the exact deleted-diagonal centered prime-shell matrix from
TPC-316 and inserts the next positive-semidefinite trace-power envelope:

```text
N^(-1)||A beta||_2^2
  <= (sqrt(trace((A^*A)^2))/N) ||beta||_2^2
  <= (trace(A^*A)/N) ||beta||_2^2.
```

On the three panels `X=640,1280,2560`, all 24 rows are rebuilt twice (forward
and reverse shell order).  The normalized Schatten-4 envelope decreases in
all 16 adjacent-scale comparisons, while the normalized Frobenius envelope
increases in all 16.  A small one-prime panel verifies both trace powers by
exact rational arithmetic.

This is a finite spectral-compression result, not a theorem that the true
operator norm decays.  The large-panel values are numerically certified under
the declared error model; no arithmetic cancellation, fixed-power Route-B
credit, Gate-B passage, or twin-prime conclusion is claimed.

The propagated floating-point guard uses the safe uniform literal-entry bound
`|K_{p,u,t}| <= 160` (all declared shell primes satisfy `p <= 157`); it is not
the smaller heuristic bound used in an earlier draft.

## What is new relative to TPC-316

* TPC-316 stopped at the Hilbert--Schmidt/Frobenius envelope and explicitly
  left the true operator norm open.  TPC-317 proves the finite Schatten-4
  envelope from the PSD Gram spectrum.
* The certificate adds a third source scale and uses 16 adjacent-scale
  interval-separated trace-power comparisons, while retaining the same
  physical kernel and source normalization.
* Forward/reverse shell accumulation and an exact rational small-panel anchor
  separate numerical reproducibility from the mathematical trace-power
  identity.
* The opposite finite trends show why the Frobenius mass cannot be treated as
  a sharp proxy for spectral scale, but they do not supply an asymptotic power.

## Claim firewall

```text
PROVED_EXACT_FINITE = PSD Gram trace-power chain and normalized finite L2
NUMERICALLY_CERTIFIED_FINITE = 24 rows; 16 Schatten-4 decreases;
                               16 Frobenius increases; exact small anchor
REFUTED_SCOPED = Frobenius mass as a sharp spectral proxy on these panels
OPEN = true top-eigenvalue asymptotic; arithmetic cancellation; normalization;
       fixed-power credit; full Gate B; twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The Session-named `propose.md` and Route-A/Route-B evaluator files are absent
from this checkout.  `notes/route_evaluation.md`, the proof package, the
independent checker, the stress suite, and the local Bridge-B checker are
fail-closed substitutes; no official evaluator pass is asserted.

## Reproduction

From this project directory:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc317_schatten_four_prime_shell_compression.py --write
python -B code/tpc317_schatten_four_prime_shell_compression.py --check
python -O -B code/tpc317_schatten_four_prime_shell_compression.py --check
python -B experiments/tpc317_independent_checker.py --check
python -O -B experiments/tpc317_independent_checker.py --check
python -B experiments/tpc317_spectral_stress.py
python -O -B experiments/tpc317_spectral_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc317_schatten_four_checker.py --check
```

The canonical certificate is
[results/tpc317_certificate.json](results/tpc317_certificate.json), and the
compiled manuscript is [paper/paper.pdf](paper/paper.pdf).

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project
package.  The next route question is whether a genuinely certified top
eigenvalue or trace-power ladder can be obtained before attempting arithmetic
cancellation.
