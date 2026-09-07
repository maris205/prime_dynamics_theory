# Prime-Shell Cancellation Depth:\ A Finite Signed Component Ledger for the Physical Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 28 August 2026
- Source repository commit: `c9f2a3559e421cb10eaf51c1268a03b838c5ed68`
- Converter: `source-markdown-audit-v2`

## Abstract

After separating the deleted diagonal from the centered residue block, the next unresolved interface in the literal twin-prime route is cancellation across the outer prime shell. We make that interface explicit. For every finite shell we define one physical off-diagonal component per prime and prove that the four-block scalar attachment is exactly additive over those components. We then audit a declared ladder of shells containing one through seven primes, six frozen source baselines, and two kernel exponents. The result is an independently replayable ledger of 84 rows and 336 component intervals. All 336 component intervals are separated from zero; 57 rows have mixed component signs. A conservative interval retention upper bound is below $1/2$, $1/4$, and $1/10$ in 31, 22, and 8 rows, respectively. Leaving out one prime reverses the nonzero shell sign in 48 events, while 12 single-prime remainders are exactly zero. These observations establish a finite cancellation-depth diagnostic and an exact reusable decomposition, not an asymptotic saving. The principal obstruction is now precise: the finite ladder has no canonical growing-shell measure, so uniform cancellation under growing shells and source controls remains open. No fixed-power credit, Gate-B pass, or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Question and contribution

The working twin-prime route studies a literal prime-shell operator attached to a finite source profile. A preceding control atlas showed that small changes in the height, cutoff, and shell endpoint can change the sign of the scalar attachment. A subsequent rank analysis showed that the centered residue block has a useful factorization before its physical diagonal is deleted, while the deleted-diagonal block is generically full rank. The diagonal-split ledger that followed isolated this correction `\cite{tpc284,tpc285,tpc286}`. The remaining natural question is: *does the physical scalar cancel across several prime components, and how deep is that cancellation on a controlled finite ladder?*

This paper addresses only that question. Its contributions are:

1.  a prime-by-prime definition of the physical output and an exact finite-shell additivity theorem;

2.  a conditional interval theorem that bounds signed shell mass relative to the unsigned mass of its separated components;

3.  a declared cardinality ladder with shells containing exactly one, two, three, four, five, six, and seven primes;

4.  a 84-row, 336-component numerical certificate with independent replay, optimized-interpreter replay, and hostile mutation tests;

5.  a route obstruction identifying the next missing theorem: uniform cancellation stability as both shell and source controls grow.

The distinction between exact structure and finite evidence is essential. We use `PROVED_EXACT` for the algebraic identities, `PROVED_CONDITIONAL` for the interval envelope, and `NUMERICALLY_CERTIFIED_FINITE` for the ledger counts. The declared ladder is a modeling choice, not an asymptotic sampling rule.

# The physical prime components

Let $I$ be a finite interval of integers and let $q$ be an odd prime. Put $$m_q(u)=\mathbf{1}_{q\nmid u},\qquad
 B_q(u,t)=m_q(u)m_q(t)
 \left(\mathbf{1}_{u\equiv t\pmod q}-\frac{1}{q-1}\right).
 \label{eq:block}$$ The physical convention deletes the diagonal of this block: $$D_q(u,t)=B_q(u,t)-\mathbf{1}_{u=t}B_q(u,u).
 \label{eq:deleted}$$ For an integer height $H>0$ and exponent $s\in\{1,2\}$, the frozen kernel is $$K_{H,s}(h)=\frac{H^{2s}}{(H^2+h^2)^s}.
 \label{eq:kernel}$$ For a finite shell $\mathcal S_Q=\{q:Q<q\leq 2Q,\ q\text{ prime}\}$ and a source vector $\beta$, define the physical component $$g_q(u)=\sum_{t\in I}qK_{H,s}(u-t)D_q(u,t)\beta(t),
 \qquad q\in\mathcal S_Q,
 \label{eq:component}$$ and the shell output $$g_{\mathcal S_Q}(u)=\sum_{q\in\mathcal S_Q}g_q(u).
 \label{eq:shell}$$ The explicit off-diagonal implementation used in the certificate skips $t=u$, as well as the two active-mask failures $q\mid u$ and $q\mid t$.

The scalar attachment is the same finite interface used by the earlier certificates. Partition $I$ into four consecutive equal blocks. If $w$ is the interval-valued source weight and $g$ is an output, write $$C(w,g)=\sum_{u\in I}w(u)g(u)
 -\sum_{r=1}^{3}\frac{W_r(w)G_r(g)}{d_r}.
 \label{eq:attachment}$$ Here the three contrasts are $(1,1,-1,-1)$, $(1,-1,0,0)$, and $(0,0,1,-1)$, with denominators $4b,2b,2b$ when a block has size $b$. Only linearity in $g$ is needed for the exact theorem; the interval-valued $w$ is handled by outward-rounded interval arithmetic in the finite audit.

# Exact shell additivity

> **Theorem: finite component decomposition** For every finite $I$ and finite prime set $\mathcal S$, every source vector $\beta$, and every fixed kernel, the outputs in [\[eq:component\]](main.tex#L109){reference-type="eqref" reference="eq:component"}–[\[eq:shell\]](main.tex#L114){reference-type="eqref" reference="eq:shell"} satisfy $$g_{\mathcal S}=\sum_{q\in\mathcal S}g_q.
>  \label{eq:output-add}$$ If $C(w,\cdot)$ is linear in its output argument, then $$C(w,g_{\mathcal S})=\sum_{q\in\mathcal S}C(w,g_q).
>  \label{eq:scalar-add}$$

> **Proof** For each fixed $u$, substitute [\[eq:component\]](main.tex#L109){reference-type="eqref" reference="eq:component"} into the right hand side of [\[eq:output-add\]](main.tex#L141){reference-type="eqref" reference="eq:output-add"}. The resulting sum is exactly the defining finite double sum for $g_{\mathcal S}(u)$. Since both $I$ and $\mathcal S$ are finite, no limiting rearrangement is involved. Applying linearity of $C(w,\cdot)$ gives $$C\left(w,\sum_{q\in\mathcal S}g_q\right)
>  =\sum_{q\in\mathcal S}C(w,g_q),$$ which proves the claim.

> **Remark** The theorem is deliberately elementary but important for the route. It permits a signed shell estimate to be decomposed into individual prime components without replacing the physical operator by an absolute-value majorant. It does not provide a bound for the signed sum.

# A certified retention envelope

Let $c_q=C(w,g_q)$ and $c_{\mathcal S}=C(w,g_{\mathcal S})$. Suppose interval computations provide valid enclosures $J_q=[\ell_q,u_q]$ and $J_{\mathcal S}=[\ell_{\mathcal S},u_{\mathcal S}]$. Assume each $J_q$ is separated from zero. Define $$\begin{aligned}
 m^-&=\sum_{q\in\mathcal S}\operatorname{dist}(0,J_q), &
 m^+&=\sum_{q\in\mathcal S}\max\{|\ell_q|,|u_q|\}, \\
 r^-&=\frac{\operatorname{dist}(0,J_{\mathcal S})}{m^+}, &
 r^+&=\frac{\max\{|\ell_{\mathcal S}|,|u_{\mathcal S}|\}}{m^-}.
 \label{eq:envelope}\end{aligned}$$

> **Proposition: conditional interval envelope** Under the stated enclosure and sign-separation assumptions, $$r^-\ \le\ \frac{|c_{\mathcal S}|}{\sum_{q\in\mathcal S}|c_q|}\ \le\ r^+.
>  \label{eq:retention}$$

> **Proof** For each component, interval inclusion and sign separation imply $$\operatorname{dist}(0,J_q)\le |c_q|\le\max\{|\ell_q|,|u_q|\}.$$ Summing gives $m^-\le\sum_q|c_q|\le m^+$, with $m^->0$. Likewise, inclusion of $c_{\mathcal S}$ in $J_{\mathcal S}$ gives $$\operatorname{dist}(0,J_{\mathcal S})\le |c_{\mathcal S}|
>  \le\max\{|\ell_{\mathcal S}|,|u_{\mathcal S}|\}.$$ Divide the lower numerator by $m^+$ and the upper numerator by $m^-$ to obtain [\[eq:retention\]](main.tex#L187){reference-type="eqref" reference="eq:retention"}.

The envelope is intentionally conservative. The component intervals share source-weight uncertainty, and the interval for the shell sum is computed directly rather than by asserting endpoint equality with the sum of component intervals. Thus a small $r^+$ is useful finite evidence of cancellation, but not a limiting proportion or a norm estimate.

# Declared ladder and finite protocol

The shell anchors and their exact prime contents are listed in Table [1](main.tex#L222){reference-type="ref" reference="tab:ladder"}. They were chosen solely to realize cardinalities one through seven while keeping the frozen source baselines unchanged.

<div id="tab:ladder">

| $Q$ |     $\mathcal S_Q$     | $|\mathcal S_Q|$ |
|:---:|:----------------------:|:----------------:|
|  3  |           $5$          |         1        |
|  4  |          $5,7$         |         2        |
|  9  |       $11,13,17$       |         3        |
|  10 |      $11,13,17,19$     |         4        |
|  16 |    $17,19,23,29,31$    |         5        |
|  22 |   $23,29,31,37,41,43$  |         6        |
|  27 | $29,31,37,41,43,47,53$ |         7        |

: Declared shell-cardinality ladder.

</div>

Each anchor is paired with the six frozen tuples $$(64,15,4,4),\ (96,20,5,4),\ (128,24,5,4),\quad
 (192,32,6,5),\ (256,38,6,5),\ (384,50,7,5),
 \label{eq:baselines}$$ where the entries are $(X,H,Q_0,z)$. The source interval is $I_X=(X/2,X]\cap\mathbb Z$; $Q_0$ and $z$ are source-control baseline parameters, while the shell anchor $Q$ is varied independently. Both $s=1$ and $s=2$ are evaluated. This gives $7\cdot6\cdot2=84$ rows and $$12(1+2+3+4+5+6+7)=336$$ prime components.

The producer uses exact rational arithmetic for the Möbius-derived source coefficient, the kernel, and the residue indicators. Comparison weights are interval-valued and outward rounded on the frozen grid. For every component and shell, the attachment interval is recomputed; the component-sum interval is checked to contain the directly computed shell interval. Leave-one-out remainders are then formed by summing all component output vectors except the omitted prime.

# Results: cancellation depth and sensitivity

The headline finite census is in Table [2](main.tex#L273){reference-type="ref" reference="tab:aggregate"}. All 336 component intervals are separated from zero, so the envelope proposition applies to every row. More than two thirds of the shell rows have mixed component signs, and the frequency remains high through the five-prime portion of the ladder.

<div id="tab:aggregate">

| Quantity                              |      Count|  Denominator|
|:--------------------------------------|----------:|------------:|
| Shell rows                            |         84|           84|
| Component intervals                   |        336|          336|
| Negative / positive components        |  175 / 161|          336|
| Negative / positive shell attachments |    52 / 32|           84|
| Mixed-sign component rows             |         57|           84|
| Retention upper $<1/2$                |         31|           84|
| Retention upper $<1/4$                |         22|           84|
| Retention upper $<1/10$               |          8|           84|
| Retention upper $<1/20$               |          5|           84|
| Leave-one-out same-sign events        |        276|          336|
| Leave-one-out nonzero sign flips      |         48|          336|
| Leave-one-out zero remainders         |         12|          336|

: Aggregate TPC-287 finite certificate.

</div>

Table [3](main.tex#L305){reference-type="ref" reference="tab:size"} resolves the cancellation depth by shell cardinality. The one-prime rows provide the expected no-cancellation baseline. The three- and four-prime rows are the most active part of this finite ladder; larger shells still contain mixed signs, but the threshold counts do not increase monotonically. That non-monotonicity is itself useful map information: shell cardinality alone is not a proxy for asymptotic gain.

<div id="tab:size">

| Cardinality |  Mixed|  $r^+<1/2$|  $r^+<1/4$|  $r^+<1/10$|
|:-----------:|------:|----------:|----------:|-----------:|
|      1      |      0|          0|          0|           0|
|      2      |      2|          1|          1|           1|
|      3      |     12|          7|          2|           1|
|      4      |     12|         10|          9|           4|
|      5      |     11|          6|          6|           2|
|      6      |      9|          4|          2|           0|
|      7      |     11|          3|          2|           0|

: Census by shell cardinality; each line has 12 rows.

</div>

The smallest certified upper retention in the registry occurs at $(X,H,Q,s)=(256,38,9,1)$ and is approximately $0.02397$ (the exact interval ratio is retained in the JSON certificate). This is a strong finite diagnostic, but its interpretation must be bounded by the protocol: it is one source baseline, one shell anchor, and one kernel exponent. The corresponding question for a growing, canonically selected shell is not answered.

The leave-one-out experiment gives a complementary view. For a shell with components $c_q$, omit one $q$ and recompute the scalar of $\sum_{p\ne q}g_p$. There are 48 nonzero sign reversals relative to the full shell sign. The 12 zero remainders are exactly the one-prime rows, where removing the sole component leaves zero. The remaining 276 events preserve the sign. Thus the finite sum is often genuinely signed, while its sign can also be sensitive to a single shell member.

# What this settles, and what it does not

The exact theorem settles the bookkeeping interface that was missing after the diagonal split: $$\text{physical shell}
 \longrightarrow
 \text{prime components}
 \longrightarrow
 \text{signed scalar sum}.$$ This structure is reusable in any later estimate that preserves signs. The finite ledger adds a concrete map of the terrain: multi-prime mixed signs are not a bookkeeping artifact, and cancellation can be deep on selected rows.

The strongest obstruction is equally concrete. The ladder is declared and finite, not a natural family indexed by a growing parameter. Source controls are frozen at six baselines, and the component intervals share uncertainty. Consequently the counts do not imply any of the following:

-   a uniform bound for shells with $Q\to\infty$;

-   a power saving for the literal arithmetic $L^2$ quantity;

-   a replacement of the full-rank physical blocks by low-rank centered blocks;

-   a positive density of cancellation rows, or a twin-prime theorem.

The next natural experiment is therefore not another isolated shell anchor. It is an adversarial stability study: enlarge the shell and source-control ranges together, retain the exact component ledger, and test whether any retention threshold survives. If it fails, the failure will locate the missing uniform hypothesis rather than be hidden by an absolute-value bound.

# Verification and claim firewall

The release contains a producer, an independent checker, a stress checker, and a Bridge-B wrapper. The producer locks the TPC-286 code and result and the frozen TPC-268 engine by normalized-LF SHA-256 hashes. The independent checker does not import the producer: it rebuilds prime shells by trial division, recomputes every physical component, and checks every serialized interval, sign, mass, ratio, and leave-one-out field. Ordinary and optimized Python replays produce the same pass output. The stress checker mutates the theorem, ladder, component prime, intervals, retention, leave-one-out flag, budget, provenance, and row census; all nine mutations are rejected.

The Session-named Route-A and Route-B evaluator files are absent from this checkout. The local route note therefore reports a fail-closed fallback and does not claim an official evaluator pass. The mathematical claim firewall for this paper is:

| Claim                                                     | Status             |
|:----------------------------------------------------------|:-------------------|
| $g_{\mathcal S}=\sum_qg_q$ and $C_{\mathcal S}=\sum_qC_q$ | EXACT              |
| Retention envelope under separated intervals              | CONDITIONAL        |
| -row / 336-component ledger and census                    | FINITE CERTIFICATE |
| Growing-shell cancellation stability                      | OPEN               |
| Literal arithmetic $L^2$ estimate                         | OPEN               |
| Fixed-power credit                                        | 0                  |
| Route-B Gate                                              | OPEN               |
| Twin-prime conclusion                                     | NONE               |

# Conclusion

TPC-287 converts the phrase “cross-prime cancellation” into a checked finite object. It proves the exact additive decomposition, supplies a safe retention envelope, and finds 57 mixed-sign rows and 8 rows with a retention upper bound below one tenth on the declared ladder. The same ledger records 48 nonzero leave-one-out sign reversals, showing that finite cancellation and finite sensitivity coexist.

The result is a map marker, not the destination. The reusable road segment is prime components $\to$ signed shell sum $\to$ interval retention envelope. The next obstruction to clear is uniformity under growing shells and source controls. Until that theorem is supplied, fixed-power credit remains zero and the twin-prime route remains open.

# Reproduction record

From the project directory, the essential commands are:

    cd papers/tpc-287-prime-shell-cancellation-depth
    P=code/tpc287_prime_shell_cancellation_certificate.py
    I=experiments/tpc287_independent_checker.py
    S=experiments/tpc287_cancellation_stress.py
    PYTHONDONTWRITEBYTECODE=1 python -B "$P" --check
    PYTHONDONTWRITEBYTECODE=1 python -O -B "$P" --check
    PYTHONDONTWRITEBYTECODE=1 python -B "$I"
    PYTHONDONTWRITEBYTECODE=1 python -O -B "$I"
    PYTHONDONTWRITEBYTECODE=1 python -B "$S"

The source interval is $I_X=(X/2,X]\cap\mathbb Z$. For a row with block size $b$, the three attachment normalizers are $4b,2b,2b$. Every finite quantity before decimal serialization is rational; source comparison intervals are outward-rounded. The JSON payload stores the full row ledger, so the aggregate counts in Tables [2](main.tex#L273){reference-type="ref" reference="tab:aggregate"} and [3](main.tex#L305){reference-type="ref" reference="tab:size"} can be audited without relying on the prose.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc284,
  author = {Liang Wang},
  title = {A Finite Control Atlas for Literal Twin-Prime Source Attachment},
  note = {TPC-284 in-repository research artifact, 2026}
}

@misc{tpc286,
  author = {Liang Wang},
  title = {A Diagonal-Deletion Attachment Ledger for the Literal Prime-Shell Operator},
  note = {TPC-286 in-repository research artifact, 2026}
}

@misc{tpc285,
  author = {Liang Wang},
  title = {Prime-Shell Residue Factorization and the Deleted-Diagonal Rank Obstruction},
  note = {TPC-285 in-repository research artifact, 2026}
}

@misc{tpc268,
  author = {Liang Wang},
  title = {Finite Cutoff Sensitivity Obstruction for the Literal Operator},
  note = {TPC-268 in-repository research artifact, 2026}
}
```

<!-- SOURCE_BODY_END -->
