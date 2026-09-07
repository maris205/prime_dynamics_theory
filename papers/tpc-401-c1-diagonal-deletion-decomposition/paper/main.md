# TPC-401: An Exact Finite Diagonal-Deletion Decomposition for the C1 Panel

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- Source date: September 5, 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We isolate an exact structural identity behind the recent C1 endpoint panels. For an integer window of length $N$ and a prime shell $Q<p\leq 2Q$, the condition $N<Q<p$ forces every off-diagonal divisibility indicator to vanish. The literal masked component consequently has the diagonal-deletion form $K_p=-a_p(D_pTD_p-D_p)$. An exact finite audit over six TPC-400 origins and the 872-prime shell verifies the entrywise reduction on 104640 sampled component rows. The small rational anchor $N=13,Q=8,p=11$ is an explicit counterexample to extending the reduction outside its hypotheses. This is a finite algebraic result; it supplies no arithmetic $L^2$ estimate, asymptotic uniformity, or twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and claim boundary

TPC-400 observed a persistent separation between same-law cohort transfer and endpoint origin stability. The present paper asks which literal terms are responsible for that finite object. We use the exact production parameters $N=1024$, $Q=8192$, and $H=66$, with origins $$7600001,\ 7603209,\ 7606417,\ 7609625,\ 7612833,\ 7616041.$$ All claims below are finite. The synthetic sign laws used by the parent panel remain modeling choices.

# Exact production-domain identity

Put $I_o=\{o,\ldots,o+N-1\}$, $T_{uv}=H^2/(H^2+(u-v)^2)$, and $D_p=\operatorname{diag}(\mathbf 1_{p\nmid u})$. The literal component is $$K_p(u,v)=p(p/Q)^2T_{uv}\left(\mathbf 1_{p\mid u-v}-\frac1{p-1}\right)
\mathbf 1_{u\ne v}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid v}.$$ If $N<Q<p$ and $u\ne v$, then $1\leq|u-v|<p$, hence $\mathbf 1_{p\mid u-v}=0$. With $a_p=p(p/Q)^2/(p-1)$, entrywise comparison gives $$\boxed{K_p=-a_p(D_pTD_p-D_p).}$$ The $D_p$ term restores the diagonal removed by $\mathbf 1_{u\ne v}$.

# Geometry formula and finite audit

Let $r_p(o)$ denote the unique multiple of $p$ in $I_o$, if it exists, and $S_o(u)=\sum_{v\in I_o,v\ne u}T_{uv}^2$. Since $p>N$, there is at most one such multiple, and the geometry is exactly $$G_o(u)=\sum_{p\nmid u}a_p^2\left(S_o(u)-
\mathbf 1_{r_p(o)\text{ exists}}T_{u,r_p(o)}^2\right).$$ The exact producer checks all six origins, five positions per origin, every off-diagonal sampled pair, and every shell prime. It records 104640 rows; all divisibility indicators are zero and every component equals the reduced formula. The independent checker uses a reverse-order sample and a contract mutation. These are exact finite checks, not a growing estimate.

# Boundary counterexample

The rational anchor uses $N=13$, $Q=8$, and $p=11$. In the interval containing $u=0$ and $v=11$, the off-diagonal difference is $-11$, so the divisibility indicator equals one. Therefore the production reduction cannot be applied to that anchor. The anchor is useful for checking other finite interpolation identities, but it does not prove this decomposition.

# Route ledger

| item                        | status                  |
|:----------------------------|:------------------------|
| production decomposition    | `PROVED_EXACT_FINITE`   |
| boundary counterexample     | `REFUTED`               |
| finite audit                | `NUMERICAL_OBSERVATION` |
| arithmetic advance          | `NO`                    |
| fixed-power credit          | $0$                     |
| Route-B / twin-prime result | `OPEN` / `NONE`         |

The next finite question is the signed diagonal-deletion term audit. A source arithmetic sign law, uniform constants, an asymptotic operator bound, and the strict $1/400$ endpoint remain absent.

# Reproduction

The project contains the exact producer, independent checker, mutation stress check, proof package, notes, and `paper/paper.pdf`. Run the three commands listed in the project README.

<!-- SOURCE_BODY_END -->
