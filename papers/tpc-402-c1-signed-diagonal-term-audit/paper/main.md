# TPC-402: The Signed Diagonal-Deletion Coefficient in a Finite C1 Panel

> This Markdown file is a mechanical TeX-to-GFM conversion of the preserved source manuscript. The TeX and PDF originals remain authoritative; this file does not upgrade the mathematical scope.

- **Source TeX:** [`paper/main.tex`](main.tex)
- **Source PDF:** [`paper/main.pdf`](main.pdf)
- **Author:** Liang Wang; School of Mathematics and Statistics, Huazhong University; of Science and Technology (HUST), Wuhan, China
- **Source date:** September 5, 2026
- **Repository source commit:** `9a2bab8588f5a81316ac3c6b6435e691e84ae8b7`

## Abstract

We continue the exact finite decomposition from TPC-401 and retain the endpoint sign as a named modeling choice. For \(N<Q<p\) and an off-diagonal pair, the signed component coefficient has the exact form \(M_\sigma(u,v)=T_{uv}[-A_\sigma+b_\sigma(u)+b_\sigma(v)]\). An exact rational audit checks the all-plus and alternating-index laws on 240 sampled off-diagonal rows, or 209280 prime-level comparisons, across six TPC-400 origins and the 872-prime shell. The \(N=13,Q=8,p=11\) anchor remains a boundary counterexample. No arithmetic sign identification or asymptotic estimate follows.

# Setup and boundary

Use \(I_o=\{o,\ldots,o+N-1\}\), \(T_{uv}=H^2/(H^2+(u-v)^2)\), and \(a_p=p(p/Q)^2/(p-1)\). The six origins are \[7600001,\ 7603209,\ 7606417,\ 7609625,\ 7612833,\ 7616041.\] The laws \(\sigma_p=1\) and \(\sigma_p=(-1)^{\operatorname{index}(p)}\) are synthetic finite probes. All claims here are finite.

# Signed coefficient identity

Define \[A_\sigma=\sum_p\sigma_pa_p,\qquad
b_\sigma(u)=\sum_{p\mid u}\sigma_pa_p.\] For \(u\ne v\) in a production window, \(|u-v|<p\) and no prime in the shell divides both \(u\) and \(v\). Thus \[\sum_p\sigma_pa_p\mathbf1_{p\nmid u}\mathbf1_{p\nmid v}
=A_\sigma-b_\sigma(u)-b_\sigma(v),\] and the literal centered component gives \[\boxed{M_\sigma(u,v)=T_{uv}[-A_\sigma+b_\sigma(u)+b_\sigma(v)]}.\] The diagonal is still zero because the original operator deletes it.

# Exact audit

The producer uses \(N=1024,Q=8192,H=66\), exact ‘Fraction‘ arithmetic, two laws, five positions per origin, and every one of the 872 shell primes. It checks 240 sampled off-diagonal rows and 209280 prime-level equalities. The independent checker reverses the shell order, checks the typed census, and repeats a reverse-shell coefficient check; a three-mutation stress checker rejects altered contracts. All exact equalities pass.

# Anchor obstruction and route ledger

At \(N=13,Q=8,p=11\), the active pair \(u=7600001,v=7600012\) has difference \(-11\). The divisibility term is one, so the production identity does not apply. The finite result is therefore bounded by its hypotheses.

| item                                    | status                  |
| :-------------------------------------- | :---------------------- |
| signed coefficient identity             | `PROVED_EXACT_FINITE`   |
| finite audit                            | `NUMERICAL_OBSERVATION` |
| source sign identification              | `OPEN`                  |
| arithmetic advance / fixed-power credit | `NO` / 0                |
| Route-B / twin-prime result             | `OPEN` / `NONE`         |

The next clue is `TEST_C1_SIGNED_DIAGONAL_TERM_GROWING_OBSTRUCTION`.

# Reproduction

The project contains the required README, code, experiments, results, notes, proof package, and `paper/paper.pdf`. The three checks are listed in the README.

## Conversion boundary

The source manuscript contains no bibliography or references section. The conversion preserves the source abstract and all numbered and unnumbered manuscript sections; proof-package assumptions and the README claim firewall remain the semantic audit sources.

For source locations and prerequisite checks, see [`CONVERSION_RECORD.md`](../CONVERSION_RECORD.md).
