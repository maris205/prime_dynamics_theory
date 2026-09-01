# TPC-322 — Operator-level signed projector and prime-shell reassembly

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

For the literal deleted-diagonal prime-shell operator inherited from TPC-321,
projecting the direct-sum output onto a sign-labelled coherent subspace gives
an exact signed reassembly identity.  On 24 finite rows, exhaustive sign
search finds both a contracting sign vector and an amplifying sign vector in
every row.  The all-plus law amplifies in 21/24 rows, while the
index-alternating law contracts in 21/24 rows.

The smallest and largest unnormalised reassembly ratios are respectively
`0.59905756561947343` and `6.8711947177741193`.  These are operator-level
finite diagnostics, not an arithmetic prime-sum estimate.

## What is new

TPC-321 showed that the trace-normalised ordered spectrum is shell-sensitive,
but its PSD Gram construction did not specify how prime-labelled blocks should
be reassembled with signs.  TPC-322 makes the missing finite interface
explicit:

```text
direct sum A=(B_p)_p
        -> sign-labelled isometric diagonal E_e
        -> orthogonal projector P_e=E_e E_e^*
        -> coherent operator C_e=sum_p e_p B_p
        -> signed cross-block Gram H_{p,q}=<B_p,B_q>_F
```

The exact identity separates three facts that were previously easy to conflate:
the direct-sum energy, the coherent projected energy, and the choice of sign
law.  The finite atlas then tests four declared sign laws and all signs modulo
global gauge.

## Claim firewall

```text
TPC322_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_REASSEMBLY_ATLAS
TPC322_SIGNED_PROJECTOR_IDENTITY = PROVED_EXACT_FINITE
TPC322_OPERATOR_REASSEMBLY_ATLAS = NUMERICALLY_CERTIFIED_FINITE_24_ROWS
TPC322_MIN_SIGN_EXISTS = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
TPC322_MAX_SIGN_EXISTS = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
TPC322_ALL_PLUS_LAW = REFUTED_FINITE_PANEL
TPC322_ALTERNATING_LAW = REFUTED_FINITE_PANEL
TPC322_ARITHMETIC_ADVANCE = NO
TPC322_FIXED_POWER_CREDIT = 0
TPC322_FULL_GATE_B = OPEN
TPC322_TWIN_PRIME_RESULT = NONE
TPC322_STATUS = NUMERICALLY_CERTIFIED_FINITE_OPERATOR_LEVEL_SIGNED_PROJECTOR_REASSEMBLY_ATLAS
TPC322_ROUND2_CLUE = TEST_CANONICAL_SIGN_LAWS_AGAINST_OPERATOR_SPECTRAL_PROFILES_AND_SOURCE_NATIVE_ARITHMETIC_L2
```

The sign search is over a finite operator block Gram, not over a claimed
Möbius weight.  TPC-275 and TPC-294 studied packet/output-level signed
quantities; this paper instead retains every source column and tests the
full operator image.  No source theorem is imported to turn the finite ratios
into a growing bound.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-322-signed-projector-reassembly/code/tpc322_signed_projector_reassembly.py --write
python -B papers/tpc-322-signed-projector-reassembly/code/tpc322_signed_projector_reassembly.py --check
python -O -B papers/tpc-322-signed-projector-reassembly/code/tpc322_signed_projector_reassembly.py --check
python -B papers/tpc-322-signed-projector-reassembly/experiments/tpc322_independent_checker.py --check
python -O -B papers/tpc-322-signed-projector-reassembly/experiments/tpc322_independent_checker.py --check
python -B papers/tpc-322-signed-projector-reassembly/experiments/tpc322_reassembly_stress.py --check
python -O -B papers/tpc-322-signed-projector-reassembly/experiments/tpc322_reassembly_stress.py --check
```

The machine-readable result is
`results/tpc322_certificate.json`; the manuscript is `paper/paper.pdf`.
The local Bridge-B record and checker are in
`research/tpc-big-road/bridge_b_tpc322_signed_projector_reassembly.md` and
`research/tpc-big-road/tpc_bridge_b_tpc322_signed_projector_reassembly_checker.py`.

The Session-named `propose.md` and official Route-A/Route-B evaluator files are
absent from this checkout.  The local proof package, independent replay,
stress suite, and fail-closed bridge checker therefore document a scoped local
result and do not constitute an official evaluator pass.

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable project
package.  The next question is whether any canonical sign law remains stable
after moving from energy ratios to the signed operator's spectral profile.
