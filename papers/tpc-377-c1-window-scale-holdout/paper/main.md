# A Finite Window-Scale Holdout for the $c=1$ Prime-Shell Band

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: See preserved source title block
- Source date: See preserved source title block
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-376 moved the first finite bandwidth cutoff matching a high-$Q$ failure support to a response-blind grid-index holdout at count $2048$. This paper tests the next scale question without changing that origin family or its normalization. We freeze the nested counts $N=1024,1536,2048$, three origins, and $Q=512,2048,8192$ before reading any response, giving 27 rows. The $c=1$ spectral failure profile is $(0,3,3)$ at every count: 18 of 27 rows fail the spectral cap and no row fails the Schur cap. The selected full-mode band Rayleigh retention ranges from $0.93760019185559207$ to $0.98047323365759775$. This is a finite nested-prefix scale audit. It does not establish a growing operator bound, origin or window uniformity, source-uniform arithmetic $L^2$, a power saving, or a twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

**A Finite Window-Scale Holdout for the $c=1$ Prime-Shell Band**\
Liang Wang\
School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China\
September 4, 2026

# Question and claim boundary

The preceding finite audits found a recurring high-$Q$ all-plus signature in a normalized prime-shell matrix. TPC-375 identified block-distance cutoff $c=1$ as the first member of a finite list reproducing that support, and TPC-376 reproduced the profile on three predeclared grid-index holdout origins at $N=2048$. The present question is whether the support survives when the window count is changed while the left endpoint is fixed.

The word scale is deliberately finite here. For each origin, the three intervals are nested prefixes. They are not independent samples and their separately normalized matrices are not restrictions of one claimed growing operator. Every conclusion below is scoped to the declared 27-row panel.

# Finite object and exact identities

For $I=[a,a+N-1]\cap\mathbb Z$, $p\in(Q,2Q]$, and $u,t\in I$, define $$K_p(u,t)=p\left(\frac pQ\right)^2
 \frac{66^2}{66^2+(u-t)^2}
 \left({\bf1}_{p\mid(u-t)}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.$$ The all-plus matrix and its full-window square-energy geometry are $$A(u,t)=\sum_{Q<p\le 2Q}K_p(u,t),\qquad
 G(u)=\sum_{t\in I}\sum_{Q<p\le2Q}K_p(u,t)^2,
 \qquad T(u,t)=\frac{A(u,t)}{\sqrt{G(u)G(t)}}.$$ For the fixed block length 256, put $b_N(u)=\lfloor(u-a)/256\rfloor$ and $$B_1(u,t)=T(u,t){\bf1}_{|b_N(u)-b_N(t)|\le1},
 \qquad R_1=T-B_1.$$ The geometry is a finite sum of nonnegative rational squares. Thus the exact anchor checks positivity and symmetry. The mask gives $T=B_1+R_1$ entrywise. If $Tv=\lambda v$ and $\|v\|_2=1$, then $$v^\mathsf{T}B_1v+v^\mathsf{T}R_1v
 =v^\mathsf{T}Tv=\lambda.$$ These are exact finite identities. They do not provide a bound uniform in $N$.

# Predeclared scale protocol

We retain the TPC-376 origins $$(a_1,a_2,a_3)=(1012006,1016016,1022031).$$ Before any new metric is read, we freeze $$N\in\{1024,1536,2048\},\quad
 Q\in\{512,2048,8192\},\quad
 \beta=2,\quad \text{exponent}=1,\quad \text{law}=\text{all-plus}.$$ The counts have respectively $4,6,8$ contiguous blocks of length 256. The complete Cartesian product is evaluated, with spectral and Schur caps $0.64$ and $0.83$. The extremal full mode is the largest-absolute-value eigenmode, with the minimum mode resolving an exact tie.

For each fixed origin the intervals satisfy $$[a,a+1023]\subset [a,a+1535]\subset [a,a+2047].$$ This nesting is the only cross-scale relation asserted. The response, source, and geometry values are not used to select a count or a row.

# Results

Table [1](main.tex#L113){reference-type="ref" reference="tab:profile"} gives the complete count-by-$Q$ census. Each entry is the range of the three origin-level band spectral values; the final column is the number of spectral-cap failures out of three origins.

<div id="tab:profile">

|  $N$ | blocks |       $Q=512$       |       $Q=2048$      |       $Q=8192$      | failure profile |
|:----:|:------:|:-------------------:|:-------------------:|:-------------------:|:---------------:|
| 1024 |    4   | .60985931–.60989656 | .65204036–.65207842 | .65334212–.65334761 |  $0/3,3/3,3/3$  |
| 1536 |    6   | .53577339–.53578769 | .66150303–.66153359 | .66281632–.66281968 |  $0/3,3/3,3/3$  |
| 2048 |    8   | .50281931–.50283444 | .66562826–.66563868 | .66694246–.66694503 |  $0/3,3/3,3/3$  |

: Band spectral ranges and finite failure census.

</div>

The full panel therefore has 18 spectral-cap violations and zero Schur-cap violations. The profile is identical across all three declared counts and matches the TPC-376 profile. The magnitudes are not asserted to be constant: for example, the $Q=512$ band range decreases as the count grows, whereas the two high-$Q$ ranges increase. This separates the finite support statement from any magnitude-stability theorem.

Using the selected full eigenvector at each row, the absolute band-Rayleigh retention over all 27 rows is $$0.93760019185559207
 \le \frac{|v^\mathsf{T}B_1v|}{|\lambda|}
 \le 0.98047323365759775,$$ and the largest corresponding tail fraction is $0.062399808144408715$. Residual, norm, symmetry, Schur, and Frobenius checks are part of the certificate.

# Independent audit and limitations

The producer locks the TPC-376 code and canonical certificate. A separate checker rebuilds primes up to 20000, accumulates the shell in descending order, constructs the all-plus matrix directly, and recomputes all 27 eigensystems. A mutation suite tests protocol, schema, finite-audit, and claim-firewall fields. Normal and optimized Python runs are required to have empty standard error and byte-identical summary output. The local Bridge-B is fail-closed repository evidence; the official evaluator files named by the Session are absent.

The result is not an origin-uniform statement, a window-scale-uniform statement, a cross-block causality claim, a source-validity theorem for the normalization, a growing masked-operator estimate, or a source-uniform arithmetic $L^2$ bound. It pays no fixed-power credit and makes no prime-shell reassembly or twin-prime claim.

# Conclusion and next question

Within the declared finite ladder, the $c=1$ band preserves the parent high-$Q$ support signature at every tested count and every tested origin. This is a concrete scale-stability certificate for a nested-prefix panel, while the changing spectral magnitudes and the separate normalization at each count keep the asymptotic interpretation open.

The next minimal hostile experiment is a response-blind new-origin cross-holdout at the same count ladder, recorded as `TEST_C1_SCALE_ORIGIN_CROSSHOLDOUT`.

<!-- SOURCE_BODY_END -->
