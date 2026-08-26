# TPC-260: Null-Compatible Four-Packet Residual Reassembly

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

Status:

```text
PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION
```

TPC-259 suppresses one source-frozen rank-one channel on the common literal V59
clock, but leaves `w_perp`.  TPC-260 asks whether packet marginals and the
existing four-block Haar information can determine that residual.  The answer
is a finite structural no-go with a sharp positive replacement:

```text
D=sum_j d_j, d_max=max_j d_j,
max(2*d_max-D,0) <= |<w,sum_j V_j>| <= D.
```

The whole interval is attained by phase choices while the null projection stays
zero.  In the equal-norm case, plus and alternating families have the same
packet diagonal `(1,1,1,1)`, zero projection on all three Haar contrasts, and
zero TPC-259 null coefficient, but full residual energies `16` and `0`.

The four-packet DFT makes the missing information explicit:

```text
sum_k ||Vhat_k||^2=sum_j||V_j||^2,
sum_j V_j=2 Vhat_0,
||sum_j V_j||^2=4||Vhat_0||^2.
```

Thus the next literal theorem must estimate mode zero or the signed cross-Gram
sum.  This paper does not claim a growing prime-shell counterexample, arithmetic
`L2`, fixed-atom credit, full Gate B, strict `1/400`, or a twin-prime result.

## Project structure and reproduction

```text
README.md
PAPER_PLAN.md
DERIVATION_PACKAGE.md
PROOF_PACKAGE.md
paper/main.tex
paper/references.bib
paper/paper.pdf
code/
experiments/
results/tpc260_certificate.json
notes/
```

From the repository root:

```bash
python -B papers/tpc-260-four-packet-residual-reassembly/code/tpc260_four_packet_residual_certificate.py --check
python -O -B papers/tpc-260-four-packet-residual-reassembly/code/tpc260_four_packet_residual_certificate.py --check
python -B papers/tpc-260-four-packet-residual-reassembly/experiments/tpc260_independent_checker.py --check
python -O -B papers/tpc-260-four-packet-residual-reassembly/experiments/tpc260_independent_checker.py --check
python -B papers/tpc-260-four-packet-residual-reassembly/experiments/tpc260_residual_stress.py --check
```

The certificate uses exact rational and Gaussian-rational arithmetic.  The
finite audit is reproducibility evidence for the algebra only; all arithmetic
claims about the literal growing shell remain open.

## Claim firewall

```text
TPC260_ROUTE_ADVANCE = YES_SCOPED_MODE_AUDIT
TPC260_HAAR_COMPLEMENT = PROVED_EXACT_FINITE
TPC260_POLYGON_COMPLETION = PROVED_EXACT_FINITE
TPC260_DFT_MODE_LEDGER = PROVED_EXACT
TPC260_NULL_CHANNEL_COMPATIBILITY = PROVED_EXACT_SYNTHETIC
TPC260_FULL_RESIDUAL_IDENTIFIABILITY = REFUTED_SCOPED
TPC260_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC260_ARITHMETIC_ADVANCE = NO
TPC260_FIXED_ATOM_CREDIT = 0
TPC260_L2 = NONE
TPC260_FULL_GATE_B = OPEN
TPC260_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC260_TWIN_PRIME_RESULT = NONE
```

## Batch handoff fields

```text
STRONGEST_POSITIVE_RESULT = SHARP_NULL_COMPATIBLE_POLYGON_COMPLETION_AND_MODE_ZERO_DFT_LEDGER
STRONGEST_OBSTRUCTION = IDENTICAL_PACKET_MARGINALS_AND_ZERO_HAAR_NULL_PROJECTIONS_ALLOW_RESIDUAL_ENERGIES_ZERO_AND_SIXTEEN
OPEN_THEOREM = COMMON_CLOCK_LITERAL_V59_MODE_ZERO_OR_SIGNED_CROSS_GRAM_ESTIMATE
REUSABLE_STRUCTURE = FOUR_BLOCK HAAR COMPLEMENT -> NULL COMPATIBLE COMPLETION -> DFT MODE LEDGER -> RESIDUAL FIREWALL
ROUND2_CLUE = PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE_FOR_THE_COMMON_V59_FOUR_PACKET_OUTPUT
```

TPC-222 treated generic packet Gram diagonal/trace non-identifiability.  The
new ingredient here is the TPC-258 null direction embedded in the concrete
four-block Haar complement, together with the sharp completion interval and
mode-zero diagnosis.
