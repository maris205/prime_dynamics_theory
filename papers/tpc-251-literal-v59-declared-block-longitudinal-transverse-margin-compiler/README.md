# TPC-251: Declared-Block Longitudinal--Transverse Margin Compiler

TPC-251 projects the literal TPC-247 probes onto the flat direction of each
declared coordinate block.  For an exhaustive partition into nonempty blocks,
the literal weight is `lambda_cb=1`, so

```text
g_c=sum_b v_cb=P_c A_x beta,
C_x=C_long+Q_trans,
|Q_trans|<=R_trans<=R_coh.
```

The direction `u_c=|J_c|^(-1/2) 1_(J_c)` is canonical only relative to the
declared block.  It is neither V59-canonical nor the TPC-219 longitudinal
object.  The external error `E` is an independently certified conditional
input and is not supplied automatically by TPC-243.

## Reproduce

Run from this project directory:

```bash
python -B code/tpc251_margin_certificate.py --check
python -B experiments/tpc251_independent_checker.py --check
python -O -B experiments/tpc251_independent_checker.py --check
python -B experiments/tpc251_margin_stress.py --check
python -O -B experiments/tpc251_margin_stress.py --check
```

The released JSON contains one full rational `8 x 8` operator replay, one
Gaussian-rational conjugation fixture, one equality obstruction, and two edge
cases.  The independent checker imports no producer code and rejects 15
typed, semantic, stale-digest, duplicate-key, and digest-rebound mutations.
The stress script checks 160 deterministic exact-rational declared
partitions/probe families.  These finite fixtures are not asymptotic evidence.

## Claim boundary

Maximum supported claim:

```text
PROVED_STRUCTURAL_L1_LITERAL_V59_DECLARED_BLOCK_LONGITUDINAL_TRANSVERSE_MARGIN_COMPILER
```

The actual V59 projected-coherence asymptotic, a payable longitudinal
dominance estimate, full Gate B, and its strict `1/400` endpoint remain open.
There is no arithmetic advance, fixed-atom credit, L2 statement, Route A
claim, or twin-prime conclusion.
