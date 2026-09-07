# Three-Origin Triangulation of a Finite Prime–Shell Spectral Ladder

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST)
- Source date: September 1, 2026
- Source repository commit: `b13909fddbffed372f43022d2cfaa2d7bdb1110e`
- Converter: `source-markdown-audit-v2`

## Abstract

Finite spectral experiments can be tied to one residue environment even when their summary looks stable. We therefore add a third, disjoint source origin to the frozen TPC–325/TPC–326 four-rung ladder and record a three-origin envelope range. The literal deleted-diagonal centered prime-shell blocks, height, shell anchors, exponents, and four sign laws are unchanged. At the new origin $20001$, all-plus normalized profile majorization holds on all $32$ rows, and both the profile and energy censuses agree with the two earlier origins. The maximum pooled TV and energy ranges are $0.0007970083$ and $0.0045518412$, below the predeclared controls $0.001$ and $0.005$. Reverse/einsum reconstruction, residue perturbation stress, exact rational anchoring, and normal/optimized replay are included. The result is finite triangulation evidence only: it does not prove a source-uniform limit, arithmetic $L^2$ cancellation, power saving, or twin-prime conclusion.

<!-- SOURCE_BODY_BEGIN -->

# Question and frozen object

TPC–325 and TPC–326 used the same finite prime-shell operator at origins $12001$ and $16001$. The next minimal adversarial question is whether their finite readout survives a third residue environment and whether the agreement can be summarized without choosing one panel as the reference. We use $$I_N=[20001,20000+N/2]\cap\mathbb Z,
 \qquad N\in\{320,640,1280,2560\}.$$ For $p\in(Q,2Q]$, define $$B_{p,N}^{(s)}(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
\left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
{\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.$$ The direct and signed Grams are $$G_0(N)=\sum_p B_p^*B_p,\qquad
 G_e(N)=\left(\sum_p e_pB_p\right)^*
                 \left(\sum_p e_pB_p\right).$$ The sign menu is all-plus, index-alternating, the mod-$4$ character, and a half split. The shell anchors are $Q\in\{24,36,54,80\}$ and $s\in\{1,2\}$.

For a positive-trace Gram $G$, let $$\pi(G)=\left(\frac{\lambda_1(G)}{\operatorname{tr}G},\ldots,
 \frac{\lambda_d(G)}{\operatorname{tr}G}\right),
 \qquad \lambda_1\geq\cdots\geq\lambda_d.$$ Finite Gram positivity and trace normalization give the basic spectral typing used here; see `\cite{horn2013matrix}`. No asymptotic statement is hidden in this definition.

# Triangulation protocol

The four new intervals are $$[20001,20160]\subset[20001,20320]\subset[20001,20640]
\subset[20001,21280].$$ They are disjoint from the earlier ladders and from the older source panels. The only intervention relative to the locked parents is the origin. The three-origin diagnostic at scale $N$ is $$\operatorname{range}_T(N)=\max_{o\in\{12001,16001,20001\}}T_o(N)
                         -\min_oT_o(N),$$ where $T_o$ is the all-plus TV lower envelope over the eight $(Q,s)$ rows. The energy range $\operatorname{range}_E(N)$ is defined analogously using the all-plus energy upper envelope. We require the maximum ranges to be strictly below $0.001$ and $0.005$, respectively, and require them to be nonzero as a non-vacuity control.

# Finite results

<div id="tab:new">

|   $N$|  $|I_N|$|  TV lower envelope|  energy upper envelope|
|-----:|--------:|------------------:|----------------------:|
|   320|      160|       0.2852340552|            8.901456172|
|   640|      320|       0.2108709647|            6.864102783|
|  1280|      640|       0.1900525186|            6.249238483|
|  2560|     1280|       0.1700854483|            5.998451633|

: New-origin all-plus ladder.

</div>

All $32$ new rows have positive lower endpoints in the interior prefix test, and all-plus profile majorization holds on $32/32$. The four-law profile census, listed as ‘(signed majorizes, mixed)’, is $$\begin{array}{c|rr}
\text{law}&\text{signed majorizes}&\text{mixed}\\\hline
\text{all-plus}&32&0\\
\text{alternating index}&21&11\\
\text{mod-4 character}&26&6\\
\text{half split}&23&9
\end{array}$$ with zero direct-majorization and unresolved entries. These counts agree with both earlier certificates. The energy-side counts also agree: all-plus is below one on $4/32$ rows and above one on $28/32$; the other laws retain their parent counts.

<div id="tab:range">

|   $N$|  $\operatorname{range}_T(N)$|  $\operatorname{range}_E(N)$|
|-----:|----------------------------:|----------------------------:|
|   320|                 0.0007970083|                 0.0045518412|
|   640|                 0.0003338713|                 0.0044707079|
|  1280|                 0.0001938660|                 0.0013977240|
|  2560|                 0.0000914121|                 0.0006212834|

: Three-origin pooled envelope ranges.

</div>

The maximum ranges are below the frozen controls, while every displayed range is positive. Thus the result is a finite three-point triangulation, not a copied equality. At the exact rational anchor $[20001,20016]$ with $Q=4$ and $s=1$, the shell is $\{5,7\}$. The direct and alternating signed energy digests are respectively $$\texttt{97225bdbd0cb628956b3701748cec3b2eca7b4d559c0d0b42044300f7c26889b},$$ $$\texttt{f38ac7229026dcd2ada592c5b245871d3ef1856e4bac21c86010e89766a9f9f7}.$$ The certificate retains the exact rational numerator/denominator identities; the independent checker recomputes them without importing the producer.

# Interpretation and limitations

The strongest justified statement is $$\texttt{NUMERICALLY\_CERTIFIED\_FINITE\_THREE\_ORIGIN\_SCALE\_TRIANGULATION}.$$ The third origin does not falsify the earlier finite profile readout, and the pooled ranges quantify its finite source sensitivity. It does not establish uniformity over source origins or over a growing scale ladder. In particular, the operator has no source-native Möbius or von Mangoldt signed estimate, so $$\texttt{ARITHMETIC\_ADVANCE=NO},\qquad
\texttt{FIXED\_POWER\_CREDIT=0},\qquad
\texttt{FULL\_GATE\_B=OPEN}.$$ The Session-named Route-A and Route-B evaluators are absent from this checkout; the local Bridge-B checker is therefore a fail-closed fallback, not an official evaluator pass. No twin-prime conclusion is asserted.

# Reproducibility

The project contains the locked parent artifacts, canonical full-row certificate, independent reverse/einsum checker, residue stress suite, proof and theorem ledgers, and this manuscript. From the repository root run:

    python -B papers/tpc-327-three-origin-scale-triangulation/code/
      tpc327_three_origin_scale_triangulation.py --check
    python -B papers/tpc-327-three-origin-scale-triangulation/experiments/
      tpc327_independent_checker.py --check
    python -B papers/tpc-327-three-origin-scale-triangulation/experiments/
      tpc327_three_origin_stress.py --check

Normal and optimized runs, PDF hygiene, and stdout equality are enforced by the local Bridge-B checker.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{horn2013matrix,
  author    = {Roger A. Horn and Charles R. Johnson},
  title     = {Matrix Analysis},
  edition   = {2},
  publisher = {Cambridge University Press},
  year      = {2013}
}
```

<!-- SOURCE_BODY_END -->
