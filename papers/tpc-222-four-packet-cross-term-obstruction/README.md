# TPC-222: Four-Packet Polarization and the PSD Cross-Term Obstruction

作者：Liang Wang（Huazhong University of Science and Technology）

状态：`PROVED_STRUCTURAL_L1 / FOUR_PACKET_CROSS_TERM_OBSTRUCTION`

TPC-221 证明了 collision graph 的 absolute Schur envelope，但其 literal saturation
说明绝对值控制不能完成 q-collapse。TPC-222 转向 TPC-218 的 four-packet interface，
精确证明 four-point polarization identity，并把 signed reassembly 写成 PSD Gram 的
cross-term problem。

对 packet vectors `V_0,...,V_3`，用 inner product
`<x,y>=sum_i conjugate(x_i)y_i` 定义 `G_(j,l)=<V_j,V_l>`。则

```text
<x,y> = 1/4 sum_(r=0)^3 i^(-r) ||x+i^r y||_2^2,
||sum_j c_j V_j||_2^2 = c^* G c,
0 <= c^*G c <= tr(G)||c||_2^2.
```

最后一个 trace envelope 可以被 rank-one packet 完全饱和，而且不能决定 signed
cross-term。精确 adversarial pair 取
`V_j^+=(1,0)` 与 `V_j^-=(-1)^j(1,0)`。两者都有同样的 diagonal 和 trace
（均为 1 和 4），但对于 `c=(1,1,1,1)`，signed energies 分别是 `16` 与 `0`。

## Claim firewall

```text
TPC222_ROUTE_ADVANCE = YES
TPC222_PSD_PACKET_GRAM = PROVED_EXACT
TPC222_FOUR_POINT_POLARIZATION = PROVED_EXACT
TPC222_TRACE_RAYLEIGH_ENVELOPE = PROVED_EXACT
TPC222_SIGNED_CROSS_TERM_IDENTIFIABILITY = REFUTED_SCOPED
TPC222_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC222_ARITHMETIC_ADVANCE = NO
TPC222_FIXED_ATOM_CREDIT = 0
TPC222_L2 = NONE
TPC222_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC222_FULL_GATE_B = OPEN
TPC222_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC222_STATUS = PROVED_STRUCTURAL_L1
TPC222_ROUND2_CLUE = CONTROL_POLARIZED_LITERAL_PACKET_ENERGIES_WITH_SIGNED_CROSS_CORRELATION
```

## Layout

```text
paper/paper.pdf
paper/main.tex
code/four_packet_psd.py
experiments/run_certificate.py
experiments/independent_checker.py
experiments/trace_cross_term_adversary.py
results/certificate.json
notes/theorem_ledger.md
notes/source_lock.md
notes/route_evaluation.md
```
