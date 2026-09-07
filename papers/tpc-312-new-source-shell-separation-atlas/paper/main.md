# A New Source–Shell Separation Atlas for a Finite Prime-Shell Diagnostic

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 30 August 2026
- Source repository commit: `abdb8bfb644f8d81c8d74b6ac609d88d191b913b`
- Converter: `source-markdown-audit-v2`

## Abstract

We move a finite Bridge-B diagnostic to eight previously unused physical rows. The source interval is $I=\{321,\ldots,640\}$, the kernel height is $H=66$, and the prime shells are $S_Q=\{p:Q<p\leq 2Q\}$ for $Q\in\{24,36,54,80\}$, with exponents $s\in\{1,2\}$. All source coefficients, operator outputs, Gram entries, and sign energies are rational. An exhaustive Gray traversal after quotienting the global sign gives a unique minimum and a unique all-positive maximum in every row. The normalized minimum is below one and the all-positive value is above one in all eight rows. Moreover, along each four-anchor $Q$ spine the minimum strictly decreases and the positive value strictly increases; exponent two strengthens both chains. The result is an exact finite source–shell atlas and a useful new obstruction: the observed separation is reproducible inside the same engine, but it does not provide external independence, a canonical weight law, a uniform asymptotic budget, or a twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and route position

The preceding releases progressively attacked finite-instability concerns in the prime-shell Bridge-B route. TPC-309 shifted a profile window, TPC-310 showed that aggregation order changes the finite class, and TPC-311 found that a declared tolerance-slice rule reverses between calibration and confirmation on its locked parent atlas `\cite{tpc309,tpc310,tpc311}`. Its route clue was therefore specific: obtain new physical rows before making another global preference claim.

TPC-312 answers the smallest useful version of that request. We do not reweight the old atlas and do not import its sign labels. Instead, we fix a new source interval and a new shell spine, rebuild the literal physical outputs, and enumerate the sign geometry from the resulting Gram matrices. The word “new” is deliberately scoped: the rows use new indices and parameters within the same locked finite engine, not an externally collected sample.

# Finite operator and certificate

At scale $640$ the frozen source rule selects $U=7$. For $t\in I$ write $$\beta_t=\frac{\mathbf 1_{t=p^a}}{a}
 -\sum_{\substack{d\mid t\\d\leq U}}\mu(d).$$ For $p\in S_Q$ define the deleted-diagonal physical output $$g_p(u)=\sum_{\substack{t\in I,\ t\ne u\\p\nmid ut}}
 p\,\frac{H^{2s}}{(H^2+(u-t)^2)^s}
 \left(\mathbf 1_{u\equiv t\pmod p}-\frac1{p-1}\right)\beta_t.
 \tag{1}$$ The Gram matrix and normalized sign energy are $$G_{p,q}=\sum_{u\in I}g_p(u)g_q(u),\qquad
 R_Q(c)=\frac{c^\mathsf{T}G c}{\operatorname{tr}G},
 \quad c\in\{-1,+1\}^{S_Q}. \tag{2}$$ The lower value in the tables is $R_Q(c^-)$ and the upper value is $R_Q(c^+)$, where the extrema are taken modulo the global transformation $c\mapsto-c$.

The producer stores decimal renderings for readability, but also stores the SHA-256 digest of each reduced rational ratio. The independent checker rebuilds (1), clears denominators, enumerates the signs, and checks the exact ratio digests. It does not import the producer or TPC-288’s output routine.

# Finite facts

> **Lemma: Gram positivity** For every declared shell and every real vector $a$, $$a^\mathsf{T}Ga=\sum_{u\in I}\left(\sum_{p\in S_Q}a_pg_p(u)\right)^2\geq0.$$

> **Proof** Expand the square and interchange the two finite sums. This gives exactly the quadratic form in (2). Since all terms in (1) are rational, the identity also holds over the rational field.

> **Proposition: Finite sign enumeration** Fixing the first coordinate of $c$ to $+1$ represents every global-sign class, and the reflected Gray traversal visits exactly $2^{|S_Q|-1}$ classes.

> **Proof** Equation (2) is unchanged by $c\mapsto-c$. Exactly one of $c$ and $-c$ has first coordinate $+1$. The map $k\mapsto k\mathbin{\mathsf{xor}}(k>>1)$ is a bijection on the $m$-bit strings and adjacent images differ in one bit, so the incremental traversal visits all classes once.

> **Proposition: Finite ordering statement** Let $r^-_{Q,s}$ and $r^+_{Q,s}$ denote the exact minimum and positive-label ratios in this release. The certificate verifies $$r^-_{24,s}>r^-_{36,s}>r^-_{54,s}>r^-_{80,s},\qquad
>  r^+_{24,s}<r^+_{36,s}<r^+_{54,s}<r^+_{80,s}
>  \tag{3}$$ for $s=1,2$. It also verifies $r^-_{Q,2}<r^-_{Q,1}<1<r^+_{Q,1}<r^+_{Q,2}$ for each declared $Q$.

> **Proof** The producer and the independent replay compare the corresponding reduced integer fractions after exact denominator clearing. Each comparison in (3) has a strict nonzero cross-product difference; the certificate records the resulting order and the replay reconstructs it from (1).

# Results

The four shells have cardinalities $6,9,12,15$. Across both exponents this gives 84 shell targets and $$2(2^{5}+2^{8}+2^{11}+2^{14})=37\,440$$ global-sign classes. Every one of the eight Gram matrices has full rank modulo $1\,000\,000\,007$; the denominator-invertibility condition is checked before interpreting this as a rational full-rank certificate.

<div id="tab:rows">

|  $Q$|  $s$|  $|S_Q|$|  enumerated|   $r^-_{Q,s}$|    $r^+_{Q,s}$|
|----:|----:|--------:|-----------:|-------------:|--------------:|
|   24|    1|        6|          32|  0.5046844043|   2.7588516494|
|   24|    2|        6|          32|  0.4591169907|   2.7737466027|
|   36|    1|        9|         256|  0.4555424591|   3.8098670069|
|   36|    2|        9|         256|  0.3532719682|   4.5887285052|
|   54|    1|       12|        2048|  0.3255776085|   5.5005051240|
|   54|    2|       12|        2048|  0.1642611051|   8.6101405940|
|   80|    1|       15|       16384|  0.2204253917|   8.6831893234|
|   80|    2|       15|       16384|  0.0849742942|  13.5606805960|

: Exact finite sign extrema, shown as decimal renderings.

</div>

The smallest normalized minimum is the $(Q,s)=(80,2)$ row, while the largest positive value is also $(80,2)$. The corresponding minimizing sign vector is $$(+,+,+,+,-,+,+,-,-,-,-,-,-,+,+),$$ with the shell ordered increasingly. Its uniqueness is modulo the global negative vector. These facts are exact finite comparisons; the displayed decimals are not interval endpoints for a floating-point computation.

# What this does and does not establish

The new panel supplies a clean structural fact for the route: the physical operator’s sign landscape is not confined to the old source window. On this new finite spine, cancellation and amplification separate in opposite directions as the shell moves outward, and the stronger kernel exponent widens the separation. The modular-rank checks also rule out a trivial zero-dimensional explanation for these eight rows.

There are three essential limits. First, the target sign is selected by minimizing the same physical Gram matrix being diagnosed. This is the source-first leakage already identified in TPC-302, so the table is not a causal or predictive test. Second, the source and shell rows are generated by the same finite engine; “new” is not external independence. Third, exact finite ordering says nothing about a sequence of growing intervals or shells. No profile-budget frontier, directed-rounding enclosure, arithmetic $L^2$ estimate, fixed-power credit, or Gate-B passage is obtained here.

# Conclusion and next gate

TPC-312 establishes an exact, independently replayed new-source-shell atlas: all eight rows are full-rank, all eight have strict minimum-versus-positive separation, and both declared monotonicity chains hold. Its strongest obstruction is equally clear: finite sign separation alone cannot choose an external weighting law or turn a source-first target into an independent prediction. The next minimal gate is therefore to compute the profile-budget layer on these exact rows with outward-rounded intervals, keeping the physical sign certificate and the budget certificate separate.

#### Route status.

The Session-named Route-A and Route-B evaluator files were absent from the checkout. The included route note is local and fail-closed; this paper makes no official evaluator-pass claim and makes no claim about the twin-prime conjecture.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc309,
  author       = {Liang Wang},
  title        = {Profile-Prefix Shift Sensitivity in a Common-Ambient Prime-Shell Holdout},
  year         = {2026},
  note         = {TPC-309 project release, Huazhong University of Science and Technology}
}

@misc{tpc310,
  author       = {Liang Wang},
  title        = {Cross-Holdout Aggregation Order and Profile Robustness in a Prime-Shell Diagnostic},
  year         = {2026},
  note         = {TPC-310 project release, Huazhong University of Science and Technology}
}

@misc{tpc311,
  author       = {Liang Wang},
  title        = {Declared Stratification and Tolerance-Slice Holdout Replication},
  year         = {2026},
  note         = {TPC-311 project release, Huazhong University of Science and Technology}
}
```

<!-- SOURCE_BODY_END -->
