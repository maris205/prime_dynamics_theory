# Cross-Scale Signed-Gain Stability and a Shell/Clock Counterexample

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `225edf5e32a3a90ca64da6f3a05ec312dff962cb`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-277 separated the universal four-packet gain floor from the source-level near-cancellation needed for a power gain. We now test whether the favorable sign of the actual packet cross term is stable under small declared changes of the prime shell and kernel clock. The source, beta weights, masks, deleted diagonal, exponent $s=2$, and rank-three Haar projection are held fixed. An exact rational audit of twelve rows gives eight negative and four positive net cross terms. In particular, at $N=192$ the natural shell $Q=6$ has $D/G\simeq1.006248$, whereas $Q=7$ has $D/G\simeq0.866928$; changing the clock from $H=29$ to $H=32$ also reverses the sign. Thus the finite statement $D/G\geq1$ is not stable on this declared interface. The result is a scoped obstruction, not an asymptotic counterexample.

<!-- SOURCE_BODY_BEGIN -->

# Question and frozen source

For the four actual source packets $V_0,\ldots,V_3$, write $$D=\sum_j\|V_j\|^2,\qquad G=\left\|\sum_jV_j\right\|^2,
 \qquad E=\sum_{j<k}\operatorname{Re}\langle V_j,V_k\rangle.$$ Then $G=D+2E$. TPC-277 found $E<0$ on a natural finite scan, which is useful but not yet a source theorem. The present question is whether that sign survives the smallest meaningful interface perturbations.

We freeze the literal prime-shell operator, exact beta source, unit masks, deleted diagonal, four consecutive source blocks, and the three four-block Haar contrasts from TPC-268–277. At each scale the comparison cutoff and exponent are unchanged. We vary only the shell endpoint $Q$ or the clock $H$, and label the natural row separately from the controls.

# Exact sign/gain relation

> **Proposition: sign equivalence** If $D>0$ and $G>0$, then $$E<0\Longleftrightarrow \frac DG>1,
>  \qquad E>0\Longleftrightarrow \frac DG<1.$$

> **Proof** Expansion gives $G-D=2E$. Division by the positive number $DG$ preserves the indicated signs.

This elementary identity is useful here because it makes a sign flip a direct failure of the signed-gain floor, rather than a change in a derived rounding statistic.

# The twelve-row audit

The producer accumulates each packet from the actual prime shell, projects the output with exact rational arithmetic, and records outward intervals on the grid $10^{15}$. A separate column-major replay verifies the exact $D,G$ digest and all interval classifications. The three natural controls are transferred from the hash-locked TPC-277 source audit.

|  $N$|  $H$|  $Q$|  $z$|  $D/G$ (display)| sign of $E$ |
|----:|----:|----:|----:|----------------:|:------------|
|  128|   24|    4|    5|      1.418569451| negative    |
|  128|   24|    5|    5|      1.873826114| negative    |
|  128|   24|    6|    5|      0.952447698| positive    |
|  192|   32|    5|    5|      1.639087079| negative    |
|  192|   32|    6|    5|      1.006248221| negative    |
|  192|   32|    7|    5|      0.866927637| positive    |
|  256|   38|    5|    6|      0.912828824| positive    |
|  256|   38|    6|    6|      1.058743787| negative    |
|  256|   38|    7|    6|      1.360349898| negative    |
|  192|   29|    6|    5|      0.977376119| positive    |
|  192|   35|    6|    5|      1.031302259| negative    |
|  384|   50|    7|    7|      1.124746633| negative    |

: Exact finite source replay at $s=2$. Displayed decimals are not used for classification.

> **Theorem: finite shell/clock instability** On the declared twelve-row grid, eight rows have $E<0$ and four have $E>0$. The following fixed-scale paths reverse the sign: $$\begin{array}{c}
> (128,Q=5)\to(128,Q=6),\quad
> (192,Q=6)\to(192,Q=7),\\
> (256,Q=5)\to(256,Q=6),\quad
> (192,H=29)\to(192,H=32).
> \end{array}$$

> **Proof** The exact rational producer and independent column-major replay return separated intervals for $G-D$ on all twelve rows. Reading the sign labels gives the stated $8/4$ census and the four displayed transitions. No floating-point comparison is used.

The first three paths vary only the prime shell endpoint. The last varies only the clock; its endpoint $(192,H=32)$ is the natural TPC registry row. This is a direct finite attack on interface stability, not a claim that the same perturbations occur infinitely often in the intended growing schedule.

# What the obstruction says about the route

The TPC-276 endpoint compiler can use a gain once a source-level lower bound is available. TPC-278 shows that a proof of such a bound cannot silently identify the natural shell/clock choice with nearby finite choices: the sign itself is not stable on the declared grid. The correct next input is a theorem for a precisely declared source schedule, preferably expressed in terms of the normalized deficit $G/D$, with all shell and clock dependence paid explicitly.

The finite flips do not refute the natural growing sequence, and the natural three controls do not prove its uniform stability. Accordingly the release assigns zero fixed-power credit and makes no arithmetic $L^2$ or twin-prime claim.

# Conclusion and route evaluation

The strongest positive result is a twelve-row exact source census with four sign flips. The strongest obstruction is that a one-step shell or clock change can turn a signed gain into a signed loss. The next minimal theorem is a coherence-to-gain criterion that states exactly what source-level deficit estimate would be sufficient.

|                               |                                               |
|:------------------------------|:----------------------------------------------|
| `ROUTE-A`                     | not applicable to this finite stability audit |
| `ROUTE-B`                     | yes, scoped shell/clock stability obstruction |
| `FIXED-POWER-CREDIT`          | 0                                             |
| `ARITHMETIC-L2 / FULL-GATE-B` | open                                          |
| `TWIN-PRIME-RESULT`           | none                                          |

# References

9 G. H. Hardy and E. M. Wright, *An Introduction to the Theory of Numbers*, 6th ed., Oxford University Press, 2008. L. Wang, “Four-Packet Gain Floors and a Source-Level Lower-Bound Attack,” TPC-277 project release, 2026.

<!-- SOURCE_BODY_END -->
