# Geometry-Adversarial\ Position Normalization: A Finite Holdout

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We test a response-independent diagonal congruence introduced in the preceding finite masked-operator audit. The new test chooses origins by a declared geometry-only adversarial rule: among 51 late origins, it maximizes the pilot spread of the unsigned mask-energy diagonal, then retains three well-separated origins. The source response is evaluated only after this selection is frozen. With the inherited three counts, three shell anchors, two kernel exponents, and four sign laws, the resulting certificate contains 216 rows. Raw and normalized output polarization are positive in all rows. On this selected panel, normalization raises the all-plus minimum from 0.63140161782616067 to 0.65046429467683675 and the mean from 0.8687258535297816 to 0.87560762679420479. These are finite, scoped observations: no growing-origin bound, arithmetic advance, source-uniform $L^2$ estimate, or twin-prime conclusion follows.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

The preceding release TPC-355 introduced a position-aware normalization for the literal divisibility-masked shell operator. Its finite panels suggested a partial repair of an all-plus floor drift, while also exhibiting a law-level exception and no uniform theorem. The present paper asks a narrower adversarial question: does the same frozen normalization retain a positive finite signal when the origin is selected using only a deliberately uneven geometry score?

The distinction between geometry and response is central. We select origins before constructing the V59 response vectors and before choosing a sign law. Consequently, the experiment can test transfer of a fixed geometric preconditioner, but it cannot establish an asymptotic statement. The Session-named official Route-A and Route-B evaluator files are not present in this checkout; the local Bridge-B checker is therefore treated as fail-closed reproducibility evidence, not as an official evaluator pass.

# Finite model

Let $I=[x,x+N-1]\cap\mathbb Z$, let $S_Q$ be the primes in $(Q,2Q]$, and let $H=66$. For $s\in\{1,2\}$ define the endpoint-masked component $$B_p(u,t)=p\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{p\mid u-t}-\frac{1}{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.
 \label{eq:component}$$ The unsigned geometry energy and the signed operator are $$G_u=\sum_{p\in S_Q}\sum_{t\in I}B_p(u,t)^2,
 \qquad A_{\varepsilon}=\sum_{p\in S_Q}\varepsilon_p B_p.
 \label{eq:geometry}$$ TPC-355 uses the finite diagonal congruence $$A_{\varepsilon}^{\#}=D_G^{-1/2}A_{\varepsilon}D_G^{-1/2},
 \qquad D_G=\operatorname{diag}(G_u).
 \label{eq:normalization}$$ It is defined only on rows for which every audited $G_u$ is positive.

The source is the inherited finite V59 model $\beta=\Lambda-b$, with $\Lambda(t)=\log p$ when $t+2$ is a prime power and zero otherwise, and with the declared finite comparison midpoint for $b$. For either $T=A_{\varepsilon}$ or $T=A_{\varepsilon}^{\#}$, the finite identity is $$\|T\beta\|_2^2=\|T\Lambda\|_2^2+\|Tb\|_2^2
 -2\langle T\Lambda,Tb\rangle.
 \label{eq:polarization}$$ We report $$\kappa(T)=\frac{2\langle T\Lambda,Tb\rangle}
 {\|T\Lambda\|_2^2+\|Tb\|_2^2}.
 \label{eq:kappa}$$

# Geometry-only adversarial selection

The candidate list is $$\mathcal C=\{38001+211j:0\leq j\leq 50\}.$$ For each $x\in\mathcal C$, we use only $N=256$ and compute $G$ for the six settings $(Q,s)\in\{24,54,80\}\times\{1,2\}$. The score is $$\operatorname{score}(x)=\max_{Q,s}\frac{\max_{u\in I}G_u}
 {\min_{u\in I}G_u}.$$ Origins are sorted by descending score (ascending origin breaks ties), and a greedy pass retains an origin only when it is at least 1536 from all already retained origins. This finite rule selects $$(x_1,x_2,x_3)=(38423,42010,45597).$$ The top four scores are $3.8870419375431311$, $3.8771763076444055$, $3.8701431023865749$, and $3.7759841567305057$; all four attain their maximum at $(Q,s)=(24,2)$. The response vectors and sign laws are not read by this selection rule.

After selection, we replay counts $N\in\{256,512,1024\}$, anchors $Q\in\{24,54,80\}$, exponents $s\in\{1,2\}$, and the four fixed laws `all_plus`, `alternating_index`, `mod4_character`, and `half_split`. Thus there are $3\cdot3\cdot2\cdot4=216$ law-level rows.

# Results

Table [1](main.tex#L137){reference-type="ref" reference="tab:summary"} gives the minimum, maximum, and mean of $\kappa$ across the 54 rows for each sign law. The raw and normalized operators are evaluated on exactly the same source and response vectors.

<div id="tab:summary">

| Law         | Operator   |           min|          max|         mean|
|:------------|:-----------|-------------:|------------:|------------:|
| all-plus    | raw        |   0.631401618|  0.990891726|  0.868725853|
| all-plus    | normalized |   0.650464295|  0.990564435|  0.875607627|
| alternating | raw        |   0.016051497|  0.618739757|  0.166767330|
| alternating | normalized |   0.025211276|  0.636154698|  0.177915732|
| mod-4       | raw        |  0.0089180989|  0.680182216|  0.293802778|
| mod-4       | normalized |   0.016499059|  0.685605122|  0.313030365|
| half-split  | raw        |   0.055137448|  0.645447176|  0.303461555|
| half-split  | normalized |   0.062237618|  0.650701231|  0.322866469|

: Finite polarization summaries on the geometry-adversarial holdout.

</div>

The all-plus minimum gain is $$0.65046429467683675-0.63140161782616067
 =0.019062676850676086,$$ and the mean gain is $0.0068817732644231855$. Both raw and normalized classifications contain 216 positive, zero negative, and zero unresolved rows. This does not mean that all sign laws or all origins are positive: it is a statement about the declared finite holdout only. In particular, the normalized all-plus minimum is below the TPC-355 higher-origin value 0.66473411648923819, so the experiment does not support a universal floor.

# Exact and independent checks

For an exact rational anchor we use the interval $[38431,38444]$, $Q=4$, and $s=1$. The shell is $(5,7]$, the geometry diagonal is positive, and the polarization identity is verified as an equality of rational numbers. The producer accumulates shell components in forward order. A separate reverse-shell checker rebuilds the V59 source, divisibility masks, geometry, four sign laws, normalized matrices, and all 216 metrics without importing the producer. Its declared tolerance is $2\times10^{-5}$.

The canonical JSON certificate also locks the TPC-355 producer and certificate. Ten in-memory mutations of schema, rows, parent provenance, selection independence, audit counts, firewall status, exact anchor, and payload hash are all rejected. The local Bridge-B checker reruns producer, independent, and stress checks in normal and optimized Python modes and compares their stdout.

# Claim firewall and conclusion

The finite selection rule and its response-blindness are exact properties of the declared program. The 216-row replay and the two all-plus gains are numerically certified finite observations. The experiment therefore gives a useful positive transfer signal for the frozen preconditioner under a geometry-adversarial selection rule.

The obstruction is equally important: no estimate controls the selected score, the diagonal, or the normalized operator as the origin and interval grow. Consequently we assign zero fixed-power credit and leave the source-uniform masked $L^2$ bound, arithmetic reassembly, full Gate B, and any twin-prime conclusion open. The next rational experiment is an origin-scale stability or operator-norm certificate fixed before any arithmetic reassembly.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc355,
  author       = {Liang Wang},
  title        = {Position-aware mask-energy normalization},
  year         = {2026},
  note         = {TPC-355 finite research release in the accompanying repository}
}

@misc{v59,
  author       = {Liang Wang},
  title        = {Literal V59 residual-radius census},
  year         = {2026},
  note         = {Finite source model and certificate in the accompanying repository}
}
```

<!-- SOURCE_BODY_END -->
