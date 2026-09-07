# TPC-404: A Local-Normalization Boundary for the C1 CRT Proxy

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 5, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-403 produced a large raw adjacent coefficient in a finite CRT-origin proxy for the signed C1 decomposition. This paper audits the next necessary question: whether that coefficient remains large after local diagonal normalization. For the same alternating synthetic profile we prove exact finite formulas for the two local diagonal energies and the adjacent coefficient. The resulting normalized square is $(T_1P_-)^2/(G(o)G(o+1))$. An exact rational certificate covers four selected shell-prime configurations. The corresponding float64 square-root observations are approximately $0.01363$ and decrease mildly across the configurations. Thus the raw obstruction is absorbed by local geometry in this finite audit. No normalized growing theorem, arithmetic sign law, arithmetic $L^2$ estimate, or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Question and finite model

Write $T_d=H^2/(H^2+d^2)$ and let the window be $I_o=\{o,\ldots,o+N-1\}$. We retain the TPC-403 CRT proxy: even-index selected primes divide $o$, while odd-index primes first divide the exterior point $o+N$. Only selected primes are included in the operator and its local energy. Let $a_p=p^3/[Q^2(p-1)]$ and put $$P_-=\sum_{i\ \mathrm{odd}}a_{p_i},\qquad
 V_+=\sum_{i\ \mathrm{even}}a_{p_i}^{2},\qquad
 V_-=\sum_{i\ \mathrm{odd}}a_{p_i}^{2}.$$ Here $V_-$ is a sum of squares, not $P_-^2$. Define the row energy $$G(u)=\sum_p a_p^2\mathbf{1}_{p\nmid u}
       \sum_{v\in I_o\setminus\{u\}}\mathbf{1}_{p\nmid v}T_{u-v}^2.$$ Also write $$S_0=\sum_{d=1}^{N-1}T_d^2,\qquad
 S_1=\sum_{d=1}^{N-2}T_d^2+T_1^2.$$ All statements in this paper concern the declared finite profile.

# Exact local identities

At $o$, positive rows are deleted at their divisible diagonal and negative rows contribute their full translated off-diagonal energy. Therefore $$G(o)=V_-S_0.$$ At $o+1$, all selected primes are units. A negative row contributes $S_1$; each positive row loses the $d=1$ term corresponding to $o$, and contributes $S_1-T_1^2$. Hence $$G(o+1)=V_-S_1+V_+(S_1-T_1^2).$$ The signed diagonal-deletion identity from TPC-402/403 gives $$M(o,o+1)=T_1P_-.$$ Consequently the squared locally normalized entry is exactly $$\boxed{\frac{M(o,o+1)^2}{G(o)G(o+1)}
 =\frac{(T_1P_-)^2}{G(o)G(o+1)}}. \tag{1}$$

# Certificate and observations

The audit uses $Q=8192$, $N=1024$, $H=66$, and the first eight primes in the shell $Q<p\leq2Q$, with $m=1,2,3,4$ alternating configurations. Every quantity in (1), including $S_0,S_1$, is computed as an exact rational and stored as a canonical fraction string. The independent checker reconstructs an actual CRT origin and the literal masked row energies without importing the producer, and the mutation checker rejects five altered contract fields.

|  $m$|  $\sqrt{\text{normalized square}}$ (float64 observation)|
|----:|--------------------------------------------------------:|
|    1|                                        0.013630716999888|
|    2|                                        0.013610790517299|
|    3|                                        0.013594253931078|
|    4|                                        0.013570927022735|

The decimal column is not used as a proof of an asymptotic statement. It records the finite scale of the exact rational certificate.

# Interpretation and route boundary

TPC-403’s raw coefficient ratio could be very large because the signed scalar $A_\sigma$ is small while the local coefficient sees $P_-$. Formula (1) shows the relevant normalized quantity simultaneously sees the row energy at both endpoints. In the four tested finite configurations this normalization is of stable small size, not a growing obstruction. This is a useful negative result: the CRT coefficient attack cannot be promoted by itself to the needed normalized operator lower bound. In particular, a small adjacent entry is not an upper bound on the full normalized operator norm.

The arithmetic signs of the source remain unidentified. No arithmetic $L^2$ estimate, fixed-power saving, Route-B reassembly, or twin-prime implication is paid by this paper. The next scoped question is a local-normalization scale ladder. Its identifier is `TEST_C1_LOCAL_NORMALIZATION_SCALE_` `LADDER`.

|                                         |                         |
|:----------------------------------------|:------------------------|
| local identities                        | `PROVED_EXACT_FINITE`   |
| finite decimal values                   | `NUMERICAL_OBSERVATION` |
| normalized growing theorem              | `OPEN`                  |
| arithmetic advance / fixed-power credit | `NO` / 0                |
| Route-B / twin-prime result             | `OPEN` / `NONE`         |

# Reproduction

The project contains the required README, code, experiments, results, notes, proof package, route evaluation, and `paper/paper.pdf`. The README lists the producer, independent replay, and adversarial stress commands.

<!-- SOURCE_BODY_END -->
