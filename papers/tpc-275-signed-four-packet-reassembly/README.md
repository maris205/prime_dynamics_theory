# TPC-275 — Signed four-packet reassembly on the literal V59 output

**Author:** Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

For the actual four source-block packets of the locked literal V59 operator,
exact Gram/DFT/polarization replay certifies negative net packet cross-coupling
on all 12 registered rows and compresses the output envelope to
`1 < D/G < 12/5`, compared with the TPC-274 Frobenius gap `F/G>50`; the
packet-diagonal margin proxy nevertheless remains below `1/4` on every row.

## What advances

- replaces the synthetic TPC-260 completion test with the actual source-block
  vectors `V_j=(I-P_3)A beta^(j)`;
- proves exact signed Gram expansion, four-point DFT identities, and real
  two-probe polarization;
- independently reconstructs the 4-by-4 packet Gram and all DFT modes with
  rational arithmetic;
- certifies `G-D<0`, `D/G<12/5`, `F/G>50`, and `m_D^2<1/16` on 12 rows;
- leaves the source-level signed cross-Gram estimate and endpoint payment open.

The finite gain is not an asymptotic theorem.  In particular, the conservative
proxy `m_D` is not the actual margin upper bound; its smallness only limits the
packet-diagonal proof route.

## Claim ceiling

```text
PROVED_EXACT_FINITE = signed Gram + DFT + polarization identities
NUMERICALLY_CERTIFIED = literal 12-row packet replay and cancellation audit
INSUFFICIENT_SCOPED = packet-diagonal envelope for a quarter-sector margin
OPEN = source-level signed cross-Gram, arithmetic L2, full Gate B
FIXED_POWER_CREDIT = 0
TWIN_PRIME_RESULT = NONE
```

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc275_signed_four_packet_reassembly_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc275_signed_four_packet_reassembly_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc275_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc275_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc275_reassembly_stress.py
PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc275_reassembly_stress.py
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The Session-named
`propose.md` and evaluator files are absent in this checkout; the local
proof/checker fallback is recorded in `notes/route_evaluation.md`.
