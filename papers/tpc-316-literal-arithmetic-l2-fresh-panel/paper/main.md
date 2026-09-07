# A Literal Finite $L^2$ Envelope for the Fresh Prime–Shell Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 30 August 2026
- Source repository commit: `b9723facc6f4c261e20e0d86513230e5351dfe4d`
- Converter: `source-markdown-audit-v2`

## Abstract

The preceding finite prime–shell audit left the source-level arithmetic $L^2$ interface open. We make that interface literal by treating the deleted-diagonal centered kernel as a matrix from every source coordinate to the $(p,u)$ output coordinates. Its Hilbert–Schmidt mass is reduced exactly to a signed-difference and residue-count sum over rational numbers. Hence a finite Frobenius inequality gives $\frac1N\left\lVert A\beta\right\rVert_2^2\leq
(\left\lVert A\right\rVert_{\rm HS}^2/N)\left\lVert \beta\right\rVert_2^2$. On the disjoint panels $I_{640}=\{321,\ldots,640\}$ and $I_{1280}=\{641,\ldots,1280\}$, we certify 16 rows and 80 coordinate probes with exact rational digests and independent replay. The normalized Hilbert–Schmidt upper envelope rises in all eight matched $(Q,s)$ rows when the scale changes from 640 to 1280, while its fresh-panel ratio to the strongest five-point coordinate lower witness exceeds 517 in every row. This is a finite literal $L^2$ envelope and a scoped obstruction to using that envelope as a decaying proxy. It is not a growing operator-norm theorem, arithmetic cancellation estimate, Route-B closure, or twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Question and route position

The TPC-315 release froze a menu of positive weights and moved the physical engine to a fresh source interval, but it deliberately did not claim the literal source-level $L^2$ estimate needed by the long route. The natural next question is more basic than prime-shell reassembly:

> What is the exact finite source-to-output operator behind the physical formula, and does its most immediate Hilbert–Schmidt envelope show a scale saving?

This question is related to the usual separation of Hilbert–Schmidt and spectral norms in analytic number theory; those norms are useful bookkeeping objects, not interchangeable asymptotic estimates `\cite{montgomeryvaughan,iwankow}`. We answer it for the locked finite engine and keep the two-panel comparison strictly finite. In particular, a rising Frobenius envelope does not prove that the true spectral norm rises, just as a finite upper bound cannot prove a future cancellation theorem.

# The literal source operator

For an even scale $X$, let $$I_X=\{X/2+1,\ldots,X\},\qquad N_X=|I_X|=X/2,$$ and let $$S_Q=\{p: p\text{ prime},\ Q<p\leq 2Q\}.$$ We use $H=66$, $Q\in\{24,36,54,80\}$, and $s\in\{1,2\}$. Define the matrix entry, for $p\in S_Q$ and $u,t\in I_X$, by $$K_{p,u,t}^{(Q,s,X)}=
 {\bf 1}_{t\neq u,\;p\nmid ut}\,p
 \frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left({\bf 1}_{u\equiv t\pmod p}-\frac1{p-1}\right).
 \label{eq:matrix-entry}$$ The literal operator is $$(A_{Q,s,X}\beta)_{p,u}=
 \sum_{t\in I_X}K_{p,u,t}^{(Q,s,X)}\beta_t,
 \qquad
 A_{Q,s,X}:\ell^2(I_X)\longrightarrow
 \ell^2(S_Q\times I_X).
 \label{eq:operator}$$ This is the same centered congruence gate and deleted diagonal as in the TPC-268 physical engine, but the source vector $\beta$ is now arbitrary. TPC-315 instead evaluated the image of one particular source coefficient vector and formed a Gram matrix among shell columns `\cite{tpc315}`.

Every entry in [\[eq:matrix-entry\]](main.tex#L81){reference-type="eqref" reference="eq:matrix-entry"} is rational. The shell cardinalities for the four anchors are $6,9,12,15$, so the output dimensions are finite and explicit. No logarithm, floating-point approximation, or source-weight choice enters this operator definition.

# Two exact finite identities

> **Proposition: Frobenius interface** For every finite vector $\beta$, $$\left\lVert A_{Q,s,X}\beta\right\rVert_2^2
>  \leq \left\lVert A_{Q,s,X}\right\rVert_{\operatorname{HS}}^2\left\lVert \beta\right\rVert_2^2,
>  \qquad
>  \frac1{N_X}\left\lVert A_{Q,s,X}\beta\right\rVert_2^2
>  \leq \frac{\left\lVert A_{Q,s,X}\right\rVert_{\operatorname{HS}}^2}{N_X}\left\lVert \beta\right\rVert_2^2.
>  \label{eq:frobenius}$$

> **Proof** Apply Cauchy–Schwarz to each output row: $$\left|\sum_t K_{p,u,t}\beta_t\right|^2
>  \leq \left(\sum_t|K_{p,u,t}|^2\right)
>        \left(\sum_t|\beta_t|^2\right).$$ Summing over $(p,u)$ gives the first inequality; division by $N_X>0$ gives the second.

The bound is useful only as an envelope. It does not assert that the right-hand side is close to the induced norm.

> **Lemma: Exact difference/residue count** Put $I_X=[L,U]\cap\mathbb Z$ and $N=U-L+1$. For a nonzero signed difference $\delta=u-t$, define $$J_\delta=[\max(L,L-\delta),\min(U,U-\delta)]\cap\mathbb Z,
>  \qquad m_\delta=|J_\delta|=N-|\delta|.$$ For a prime $p$, let $v_{\delta,p}$ count the pairs in $J_\delta$ for which both endpoints are nonzero modulo $p$. Then $$v_{\delta,p}=\begin{cases}
>  m_\delta-\#\{t\in J_\delta:t\equiv0\pmod p\},&p\mid\delta,\\[2mm]
>  m_\delta-\#\{t\in J_\delta:t\equiv0\pmod p\}
>  -\#\{t\in J_\delta:t\equiv-\delta\pmod p\},&p\nmid\delta.
>  \end{cases}
>  \label{eq:valid-count}$$ Consequently, $$\left\lVert A_{Q,s,X}\right\rVert_{\operatorname{HS}}^2
>  =\sum_{p\in S_Q}\sum_{0<|\delta|<N}
>  p^2\left(\frac{H^{2s}}{(H^2+\delta^2)^s}\right)^2
>  c_{\delta,p}^2v_{\delta,p},
>  \label{eq:hs-count}$$ where $$c_{\delta,p}^2=\begin{cases}(p-2)^2/(p-1)^2,&p\mid\delta,\\
>  1/(p-1)^2,&p\nmid\delta.
>  \end{cases}$$

> **Proof** Every pair with difference $\delta$ is uniquely parameterized by its $t$ in $J_\delta$. If $p\mid\delta$, the two endpoints have the same residue, so only residue zero is excluded and the centered factor is $(1-1/(p-1))=(p-2)/(p-1)$. Otherwise the endpoint residues zero and $-\delta$ are distinct, and the centered factor is $-1/(p-1)$. Squaring removes the sign. Summing the common kernel factor over the admissible pairs proves [\[eq:hs-count\]](main.tex#L153){reference-type="eqref" reference="eq:hs-count"}.

For a coordinate vector $e_t$, define its exact column energy $$C_t=\left\lVert A_{Q,s,X}e_t\right\rVert_2^2
 =\sum_{p\in S_Q}\sum_{u\in I_X}|K_{p,u,t}^{(Q,s,X)}|^2.
 \label{eq:column}$$ Since $\left\lVert e_t\right\rVert_2=1$, $$\left\lVert A_{Q,s,X}\right\rVert_{2\to2}^2\geq C_t.
 \label{eq:column-lower}$$ The certificate reports five such columns and chooses the largest by exact rational comparison. It never calls that five-point maximum the true maximum column energy.

# Exact protocol and finite results

The lower panel is $X=640$, with $I_{640}=\{321,\ldots,640\}$; the fresh panel is $X=1280$, with $I_{1280}=\{641,\ldots,1280\}$. For each row we evaluate [\[eq:hs-count\]](main.tex#L153){reference-type="eqref" reference="eq:hs-count"} using rational arithmetic. The five columns are the endpoint-inclusive offsets $$0,\quad \left\lfloor\frac{N-1}{4}\right\rfloor,\quad
 \left\lfloor\frac{N-1}{2}\right\rfloor,\quad
 \left\lfloor\frac{3(N-1)}{4}\right\rfloor,\quad N-1.$$ All exact values are sealed by numerator/denominator SHA-256 digests; decimal strings in the certificate are display views. The independent checker has a separate sieve, count implementation, direct small-panel mass replay, and direct column calculation.

Table [1](main.tex#L214){reference-type="ref" reference="tab:fresh"} gives the normalized five-point lower witness $L$ and the normalized Frobenius upper envelope $U$ on the fresh panel. The final column is $U/L$, not a condition number for the true operator.

<div id="tab:fresh">

|  $Q$|  $s$|  $L=C_{\rm probe}/N$|  $U=\left\lVert A\right\rVert_{\operatorname{HS}}^2/N$|    $U/L$|
|----:|----:|--------------------:|------------------------------------------------------:|--------:|
|   24|    1|            22.641661|                                           12812.266690|  565.871|
|   24|    2|             9.490073|                                            5522.980838|  581.975|
|   36|    1|            36.861146|                                           20628.183796|  559.619|
|   36|    2|            11.528590|                                            6645.774850|  576.461|
|   54|    1|            45.217512|                                           24528.202062|  542.449|
|   54|    2|             7.861723|                                            4435.477884|  564.187|
|   80|    1|            42.629523|                                           22066.526605|  517.635|
|   80|    2|             4.189095|                                            2341.953723|  559.060|

: Fresh-panel exact finite sandwich. Values are decimal views of rational quantities; all comparisons use the exact values.

</div>

The five-point witnesses are exact lower bounds for the induced norm, but the large gaps show that the Frobenius interface is loose at this resolution. Table [2](main.tex#L241){reference-type="ref" reference="tab:scale"} compares the normalized upper envelopes across the two panels.

<div id="tab:scale">

|  $Q$|  $s$|     $U_{640}$|    $U_{1280}$|  $U_{1280}/U_{640}$|
|----:|----:|-------------:|-------------:|-------------------:|
|   24|    1|  11477.141904|  12812.266690|            1.116329|
|   24|    2|   5140.681957|   5522.980838|            1.074367|
|   36|    1|  18026.082081|  20628.183796|            1.144352|
|   36|    2|   6066.399332|   6645.774850|            1.095506|
|   54|    1|  20281.815965|  24528.202062|            1.209369|
|   54|    2|   3909.330416|   4435.477884|            1.134588|
|   80|    1|  16767.332568|  22066.526605|            1.316043|
|   80|    2|   2028.906503|   2341.953723|            1.154294|

: Two-panel normalized Hilbert–Schmidt comparison.

</div>

All eight exact comparison ratios exceed one. This is a numerically certified finite observation, not an asymptotic monotonicity statement.

# Interpretation and route firewall

The positive result is now concrete: the literal finite matrix, rather than a typed hypothetical operator, has an exact source-level Frobenius interface. The difference-count identity also removes a practical computational obstacle; a full matrix need not be materialized to certify its Frobenius mass. This structure can be reused if a future argument supplies a sharper spectral or cancellation estimate.

The obstruction is equally important. On the declared two panels, the normalized Frobenius envelope rises in every matched row. On the fresh panel it is at least 517 times the strongest available coordinate lower witness. Thus the immediate envelope gives no negative-power credit and does not identify the scale of the true operator norm. The result does not say that a future arithmetic cancellation theorem is impossible; it says that such a theorem cannot be replaced by this Frobenius calculation.

The physical engine is inherited from TPC-268 and used on both panels, so the comparison is not externally independent. The source coordinates are also a finite modeling choice, and no canonical weight law is selected. The Session-named Route-A and Route-B evaluator files were absent from the checkout; the local route note and Bridge-B checker are fail-closed fallbacks. Accordingly, arithmetic Route-B advance remains `NO`, fixed-power credit is zero, full Gate B is `OPEN`, and no twin-prime conclusion is claimed.

# Conclusion and next gate

TPC-316 pays a finite literal $L^2$ interface: $$N^{-1}\left\lVert A\beta\right\rVert_2^2
 \leq (\left\lVert A\right\rVert_{\operatorname{HS}}^2/N)\left\lVert \beta\right\rVert_2^2,$$ with the coefficient on the right certified exactly by a residue-count formula. Sixteen rows and eighty coordinate probes are independently replayed. The normalized upper envelope rises in all eight two-panel pairs, and the fresh-panel upper/lower gap is large. The route therefore advances from a conditional $L^2$ interface to a literal finite envelope, but stops before any growing arithmetic claim.

The next minimal question is to replace the Frobenius envelope by a genuinely sharper growing operator estimate, or to expose an explicit arithmetic cancellation mechanism that controls the spectral norm while retaining the prime-shell and deleted-diagonal structure.

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

@misc{tpc315,
  author = {Liang Wang},
  title  = {Fresh-Source Replication and Weight-Order Obstruction in a Finite Prime--Shell Diagnostic},
  year   = {2026},
  note   = {TPC-315 project release, Huazhong University of Science and Technology}
}
```

<!-- SOURCE_BODY_END -->
