# Schatten–4 Compression of a Literal Prime–Shell Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 31 August 2026
- Source repository commit: `b9723facc6f4c261e20e0d86513230e5351dfe4d`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding TPC-316 release made the deleted-diagonal centered prime–shell formula into a literal finite source-to-output operator, but used only its Hilbert–Schmidt mass as an $L^2$ envelope. We insert the next trace power. For the positive-semidefinite Gram matrix $G=A^*A$, finite spectral calculus gives $\lambda_{\max}(G)\leq\sqrt{\operatorname{tr}(G^2)}\leq\operatorname{tr}(G)$, and hence a Schatten–4 source-level envelope strictly sharper than the Frobenius envelope. We retain exactly the same prime shells, masks, deleted diagonal, height, and source normalization. On the three panels $X=640,1280,2560$, all 24 $(X,Q,s)$ rows are rebuilt in increasing and decreasing shell order. The resulting normalized Schatten–4 envelope has 16 strict adjacent-scale decreases, whereas the normalized Frobenius envelope has 16 strict increases. A small one-prime panel verifies both trace powers by exact rational arithmetic. The large-panel values are finite numerical certificates under a declared binary64 error budget, not an asymptotic operator-norm theorem. Arithmetic cancellation, fixed-power Route-B credit, Gate-B closure, and a twin-prime conclusion remain open.

<!-- SOURCE_BODY_BEGIN -->

# Question and route position

TPC-316 exposed the full source-to-output matrix behind a physical prime-shell formula and proved a finite Frobenius interface. Its normalized Hilbert–Schmidt envelope increased on its two declared panels, but the Frobenius quantity can be much larger than the induced operator norm. The next minimal question is therefore:

> Can a trace-power envelope retain the literal arithmetic operator while removing at least part of the artificial Frobenius dimension factor?

This is a finite norm audit, not a replacement for the missing arithmetic reassembly. In particular, a finite decrease of an upper envelope cannot be identified with decay of the true operator norm. The distinction between Hilbert–Schmidt and spectral control is standard in analytic number theory `\cite{montgomeryvaughan,iwankow}`; here it is made explicit for the same locked object used in TPC-316 `\cite{tpc316}`.

# The locked literal operator

For an even integer $X$, set $$I_X=\{X/2+1,\ldots,X\},\qquad N_X=|I_X|=X/2,$$ and let $$S_Q=\{p:p\text{ is prime},\ Q<p\leq 2Q\}.$$ For $H=66$, $s\in\{1,2\}$, and $p\in S_Q$, define $$K_{p,u,t}=
 {\bf 1}_{t\ne u,\;p\nmid ut}\,p
 \frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left({\bf 1}_{u\equiv t\pmod p}-\frac1{p-1}\right).
 \label{eq:entry}$$ The source operator is $$(A_{Q,s,X}\beta)_{p,u}=\sum_{t\in I_X}K_{p,u,t}\beta_t,
 \qquad
 A_{Q,s,X}:\ell^2(I_X)\longrightarrow
 \ell^2(S_Q\times I_X).
 \label{eq:operator}$$ No source coefficient is built into $A$. The source vector is arbitrary, and the only output labels are the prime $p$ and the endpoint $u$. The four declared shell anchors have cardinalities $6,9,12,15$. Every entry is a rational number, so every finite Gram entry and every finite trace power is rational before numerical evaluation.

# The trace-power envelope

> **Theorem: finite Schatten–4 chain** Let $G=A^*A$ for any finite row of [\[eq:operator\]](main.tex#L90){reference-type="eqref" reference="eq:operator"}. Then, for every source vector $\beta$, $$\left\lVert A\beta\right\rVert_2^2
>  \leq \sqrt{\operatorname{tr}(G^2)}\,\left\lVert \beta\right\rVert_2^2
>  \leq \operatorname{tr}(G)\,\left\lVert \beta\right\rVert_2^2.
>  \label{eq:chain}$$ Consequently, $$\frac1{N_X}\left\lVert A\beta\right\rVert_2^2
>  \leq \frac{\sqrt{\operatorname{tr}(G^2)}}{N_X}\left\lVert \beta\right\rVert_2^2.
>  \label{eq:normalized}$$

> **Proof** The matrix $G$ is positive semidefinite. Let its eigenvalues be $\lambda_1,\ldots,\lambda_{N_X}\geq0$. The Rayleigh principle gives $\left\lVert A\beta\right\rVert_2^2=\beta^*G\beta\leq
> \lambda_{\max}(G)\left\lVert \beta\right\rVert_2^2$. Also $$\lambda_{\max}(G)^2\leq\sum_i\lambda_i^2=\operatorname{tr}(G^2),
>  \qquad
>  \sum_i\lambda_i^2\leq\left(\sum_i\lambda_i\right)^2=\operatorname{tr}(G)^2.$$ Taking square roots proves both inequalities. Division by $N_X>0$ proves [\[eq:normalized\]](main.tex#L113){reference-type="eqref" reference="eq:normalized"}.

The first quantity in the chain is the unknown true spectral scale. The middle quantity is the new envelope, and the last quantity is precisely the TPC-316 Frobenius envelope. The gap can be summarized by the effective trace rank $$r_{\mathrm{eff}}=\frac{\operatorname{tr}(G)^2}{\operatorname{tr}(G^2)}.$$ This is a descriptive finite statistic; it is not a rank theorem for a growing operator family.

> **Lemma: entrywise trace-square identity** Writing $r=(p,u)$ for an output row, $$\operatorname{tr}(G)=\sum_{r,t}K_{r,t}^2,qquad
>  \operatorname{tr}(G^2)=\sum_{t,v\in I_X}
>  \left(\sum_rK_{r,t}K_{r,v}\right)^2.
>  \label{eq:trace-square}$$

> **Proof** The Gram entry is $G_{t,v}=\sum_rK_{r,t}K_{r,v}$. Since the matrix is real and symmetric, $\operatorname{tr}(G^2)=\sum_{t,v}G_{t,v}G_{v,t}$, which is the second identity. The first is the diagonal identity $\operatorname{tr}(A^*A)=\sum_{r,t}K_{r,t}^2$.

# Certificate protocol

The three source panels are $$I_{640}=\{321,\ldots,640\},\quad
 I_{1280}=\{641,\ldots,1280\},\quad
 I_{2560}=\{1281,\ldots,2560\}.$$ For every $Q\in\{24,36,54,80\}$ and $s\in\{1,2\}$, the code builds the matrix in prime-shell blocks and accumulates $G=A^*A$. It repeats the accumulation in reverse prime order. This changes no mathematical object; it is a reproducibility control for floating reduction. The trace-square is then reduced in binary64 and, after conversion of the independently accumulated Gram matrix, in extended scalar precision.

The interval in the certificate combines a coarse entrywise binary64 Gram error bound, a block-accumulation and symmetrization guard, the two shell-order paths, and a fixed outward display pad. Since every declared shell has $p\leq157$ and the centered factor has modulus at most one, the guard uses the safe uniform bound $|K_{p,u,t}|\leq160$. Trend decisions are made only when the larger-scale interval is wholly below (or above) the smaller-scale interval. Thus the reported large-panel status is `NUMERICALLY_CERTIFIED_FINITE` under this explicit model, not `PROVED_EXACT`.

As an exact anchor, the independent checker directly constructs the rational matrix on $I=\{17,\ldots,32\}$ with $p=5$ and $s=1$, then evaluates both $\operatorname{tr}(G)$ and $\operatorname{tr}(G^2)$ using fractions. The producer and checker compare the numerator/denominator digests. Neither the parent producer nor any unverified source coefficient is imported by the independent checker.

# Finite results

Table [1](main.tex#L199){reference-type="ref" reference="tab:s4"} reports the normalized middle term in [\[eq:normalized\]](main.tex#L113){reference-type="eqref" reference="eq:normalized"}. The two ratios are center values; strictness is decided by the outward intervals, not by rounded table entries.

<div id="tab:s4">

|  $Q$|  $s$|  $E_{640}$|  $E_{1280}$|  $E_{2560}$|  $E_{1280}/E_{640}$|  $E_{2560}/E_{1280}$|     |
|----:|----:|----------:|-----------:|-----------:|-------------------:|--------------------:|----:|
|   24|    1|    770.465|     627.632|     473.039|            0.814615|             0.753688|     |
|   24|    2|    319.030|     241.262|     175.911|            0.756236|             0.729129|     |
|   36|    1|   1112.874|     913.931|     690.447|            0.821235|             0.755469|     |
|   36|    2|    378.376|     288.636|     211.204|            0.762828|             0.731733|     |
|   54|    1|   1234.220|    1056.292|     809.769|            0.855837|             0.766615|     |
|   54|    2|    363.229|     273.559|     199.112|            0.753132|             0.727856|     |
|   80|    1|   1135.915|    1012.495|     788.713|            0.891347|             0.778980|     |
|   80|    2|    459.858|     340.478|     246.080|            0.740399|             0.722749|     |

: Normalized Schatten–4 envelope on three source panels.

</div>

All 16 adjacent comparisons in Table [1](main.tex#L199){reference-type="ref" reference="tab:s4"} are interval-separated decreases. The effect is not an artifact of a single shell or exponent. The absolute envelope remains large, and no power of $X$ is fitted.

For contrast, the corresponding normalized Frobenius masses are shown in Table [2](main.tex#L230){reference-type="ref" reference="tab:hs"}. These are the same rows and the same source normalization used by TPC-316.

<div id="tab:hs">

|  $Q$|  $s$|  $F_{640}$|  $F_{1280}$|  $F_{2560}$|  $F_{1280}/F_{640}$|  $F_{2560}/F_{1280}$|     |
|----:|----:|----------:|-----------:|-----------:|-------------------:|--------------------:|----:|
|   24|    1|  11477.142|   12812.267|   13498.800|            1.116329|             1.053584|     |
|   24|    2|   5140.682|    5522.981|    5716.434|            1.074367|             1.035027|     |
|   36|    1|  18026.082|   20628.184|   21959.832|            1.144352|             1.064554|     |
|   36|    2|   6066.399|    6645.775|    6936.168|            1.095506|             1.043696|     |
|   54|    1|  20281.816|   24528.202|   26713.847|            1.209369|             1.089107|     |
|   54|    2|   3909.330|    4435.478|    4699.338|            1.134588|             1.059489|     |
|   80|    1|  16767.333|   22066.527|   24828.648|            1.316043|             1.125172|     |
|   80|    2|   2028.907|    2341.954|    2499.358|            1.154294|             1.067210|     |

: Normalized Frobenius mass and adjacent-scale ratios.

</div>

The opposite trends are the central finite finding: the Frobenius mass grows on all 16 adjacent comparisons, while the trace-square envelope shrinks. The ratio $\sqrt{\operatorname{tr}(G^2)}/\operatorname{tr}(G)$ also decreases on every row, from a range of approximately $0.061$–$0.227$ at $X=640$ to $0.030$–$0.098$ at $X=2560$. The effective trace rank increases from roughly $19$–$270$ at $X=640$ to $103$–$1088$ at $X=2560$. These summaries describe spectral mass spreading; they do not prove that the largest eigenvalue decreases.

# Interpretation and claim firewall

The strongest positive result is mathematical and finite: the PSD Gram chain gives a strictly sharper valid source-level envelope than the Frobenius bound, and the trace-square identity is independently checked on an exact rational anchor. The large-panel certificate then shows that this sharper envelope behaves materially differently from the previous one across the declared panels.

The strongest obstruction is equally important. The computation does not certify the top eigenvalue. A decreasing upper envelope can coexist with a constant or increasing true norm, and the three panels do not establish a uniform law in $X$. Moreover, the prime-shell labels are still aggregated in $G$; no signed four-packet reassembly or arithmetic cancellation has been proved. The result therefore pays no fixed power and does not advance the Route-B endpoint.

The parent certificate is locked by repository SHA-256, and all large-panel entries are recomputed from the same literal formula. This is a same-engine finite diagnostic, not an external physical holdout. The Session-named Route-A and Route-B evaluator files were absent from the checkout, so the local route note and Bridge-B checker are fail-closed substitutes and no official evaluator pass is asserted.

# Conclusion and next gate

For the literal prime-shell operator, the finite inequality $$\frac1N\left\lVert A\beta\right\rVert_2^2
 \leq \frac{\sqrt{\operatorname{tr}((A^*A)^2)}}{N}\left\lVert \beta\right\rVert_2^2
 \leq \frac{\operatorname{tr}(A^*A)}{N}\left\lVert \beta\right\rVert_2^2$$ provides the correct next envelope after TPC-316. On $X=640,1280,2560$ it is interval-separated downward in all 16 adjacent comparisons, while the Frobenius envelope is upward in all 16. This is a real finite spectral compression and a useful warning against reading the Frobenius mass as the operator scale.

The next minimal question is to certify the actual top eigenvalue, or a higher trace-power ladder, while retaining the literal prime-shell arithmetic. Only after that step would it be meaningful to test whether any resulting operator estimate can interact with the signed Route-B reassembly.

#### Status.

This manuscript is a finite diagnostic release by Liang Wang (HUST). It does not prove the twin-prime conjecture or an equivalent asymptotic statement.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@book{montgomeryvaughan,
  author    = {Hugh L. Montgomery and Robert C. Vaughan},
  title     = {Multiplicative Number Theory I: Classical Theory},
  publisher = {Cambridge University Press},
  year      = {2007}
}

@book{iwankow,
  author    = {Henryk Iwaniec and Emmanuel Kowalski},
  title     = {Analytic Number Theory},
  series    = {American Mathematical Society Colloquium Publications},
  volume    = {53},
  publisher = {American Mathematical Society},
  year      = {2004}
}

@misc{tpc316,
  author = {Liang Wang},
  title  = {A Literal Finite $L^2$ Envelope for the Fresh Prime--Shell Operator},
  year   = {2026},
  note   = {TPC-316 project release, Huazhong University of Science and Technology}
}
```

<!-- SOURCE_BODY_END -->
