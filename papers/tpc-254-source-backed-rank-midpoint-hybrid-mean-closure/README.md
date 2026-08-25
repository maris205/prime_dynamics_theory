# TPC-254: Source-Backed Rank-Midpoint Hybrid-Mean Closure and the Adjoint-Lane Source Gap

Status:

```text
PROVED_SOURCE_BACKED_L1_RANK_MIDPOINT_HYBRID_MEAN_CLOSURE_WITH_ADJOINT_LANE_SOURCE_GAP
```

Fix a finite admissible `K` and put

```text
Z_x=(log x)^K,
w(u)=Lambda(u+2)-b_x^(Z_x)(u).
```

On the ordered physical interval

```text
I_x=(x/2,x] intersect Z={n_1<...<n_N},
ell=floor(N/2), r=N-ell,
z_mid=sqrt(ell*r/N)(1_L/ell-1_R/r),
```

the frozen hybrid maximal Type-I theorem supplies, for every fixed `M>0`,

```text
max(|W_L|,|W_R|) <<_(M,K) x/(log x)^M,
|W_L/ell-W_R/r| <<_(M,K) (log x)^(-M),
|<z_mid,w>| <<_(M,K) x^(1/2)(log x)^(-M).
```

The key extraction is literal and one-sided: after freezing
`gamma_0=1/4`, the maximal Type-I sum is a sum of nonnegative rows, so its
unit-weight `m=1` row controls each consecutive rank child. The children are
defined by rank for every real `x`; no integer-only `floor(3x/4)` shortcut is
used for nonintegral clocks.

The second lane remains open. The only supported transfer is

```text
|conjugate(<z_mid,w>)<z_mid,A_x beta>|
 <<_(M,K) x^(1/2)(log x)^(-M)||A_x^*z_mid||_2||beta||_2.
```

No locked source estimates `<A_x^*z_mid,beta>`. A real zero-diagonal
derangement construction permits arbitrary signed scale, and at `N=2` the
Cauchy constant one is exact. These controls are synthetic, not literal V59
counterexamples.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/code/tpc254_midpoint_hybrid_mean_certificate.py --check
python -O -B papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/code/tpc254_midpoint_hybrid_mean_certificate.py --check
python -B papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/experiments/tpc254_independent_checker.py --check
python -O -B papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/experiments/tpc254_independent_checker.py --check
python -B papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/experiments/tpc254_midpoint_hybrid_mean_stress.py --check
python -O -B papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/experiments/tpc254_midpoint_hybrid_mean_stress.py --check
```

The canonical certificate uses exact rational and Gaussian-rational data.
The independent checker imports no producer and rejects 82 adversarial
mutations, including nested bool-as-int fields. The stress suite checks 192
deterministic exact families: 96 integer and 96 noninteger clocks, balanced
odd/even rank, and both signs of the derangement scale. These finite checks
reproduce algebra and source-contract typing only; they are not evidence for
the asymptotic maximal Type-I theorem.

## Build

From `paper/`:

```bash
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
bibtex paper
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
pdflatex -jobname=paper -interaction=nonstopmode -halt-on-error main.tex
```

## Claim boundary

`ARITHMETIC_ADVANCE=YES_SCOPED_LITERAL_W_LANE`, but `FIXED_ATOM_CREDIT=0`,
`L2=NONE`, `FULL_GATE_B=OPEN`, the global strict `1/400` budget is unpaid,
and no twin-prime result follows. Arbitrary fixed logarithmic saving is not a
fixed power saving, and neither contrast has a claimed sign or nonzero value.

Maximum supported claim:

```text
SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER_CONTROL_OF_THE_LITERAL_V59_RANK_MIDPOINT_W_CONTRAST_WITH_ONLY_EXACT_ADJOINT_CAUCHY_TRANSFER
```
