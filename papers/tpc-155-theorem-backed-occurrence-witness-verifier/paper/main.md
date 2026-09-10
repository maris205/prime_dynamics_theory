# **A Theorem-Backed Occurrence Witness Contract:**\ **Exact Verification without Provenance Promotion**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-155-theorem-backed-occurrence-witness-verifier.pdf](../tpc-155-theorem-backed-occurrence-witness-verifier.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The first unresolved object in the source-locked frontier program is a conservative row-separated lift from every nonsoft cut path to fully typed downstream occurrences. The existing archive does not contain that lift. This paper answers the next narrower question: what finite evidence would be sufficient to verify a proposed lift without silently inventing its arithmetic provenance?

We define `OccurrenceWitnessV1`. Every occurrence row has one cut source and exact Gaussian-rational edge weight; every cut column must sum to one. The witness separately records native tuple, prescribed shift, physical normalization, three support namespaces, canonical parent, stage, local multiplier chain, determinant quotient, zero-mode quotient, physical grouping and downstream shift selector. Physical cover, hard-packet reconnection and the occurrence registry are three independent exports. A source identifier is required for every nontrivial field.

We prove that the finite contract is equivalent to column conservation for the induced sparse matrix, that its copied metadata gives exact intertwining identities, and that its edgewise shift test excludes aggregate cancellation. A deterministic standard-library verifier implements these statements with canonical UTF-8/LF source locks and mutation regressions. A two-cut, three-occurrence fixture exercises both eligible-tail and frontier-unmapped types and a genuine one-to-many column. It is explicitly synthetic $\mathrm{L0}$ evidence.

No production witness is supplied. Consequently the actual occurrence lift, determinant and zero-mode maps, physical grouping, downstream selector, physical cover, reconnection and occurrence registry all remain $\textnormal{\textsc{not-testable}}$. The positive result is a sound verification interface; it is not existence of the object it would verify and is not positive fixed-$X$-power arithmetic progress.

<!-- SOURCE_BODY_BEGIN -->

**Keywords:** occurrence lift; exact conservation; provenance witness; fixed shift; source lock; executable certificate.

# The exact verification problem

The nonsoft cut domain is $$\mathcal C_X^{\mathrm{ns}}=\mathcal C_X^{\mathrm{ETO}}\sqcup\mathcal C_X^{\mathrm{FUM}}.$$ Here ETO denotes `ELIGIBLE_TAIL_OPEN` and FUM denotes `FRONTIER_UNMAPPED`. The frozen finite archive used by TPC-143 has $0$ ETO rows and $2{,}988$ FUM rows `\citep{WangTPC143}`. The zero is a property of that fixture, not a theorem that ETO is asymptotically empty. Therefore every general contract in this paper retains both summands.

The desired object is a finite sparse matrix $$L_X:\mathbb C^{\mathcal C_X^{\mathrm{ns}}}\longrightarrow\mathbb C^{\mathcal O_X},
 \qquad \mathbf 1^T L_X=\mathbf 1^T.$$ whose rows are downstream occurrences. A single cut path may have several computational or physical occurrences. An occurrence row must have one recorded cut source: conservation by cancellation between unrelated sources is forbidden.

TPC-143–146 specify why downstream parent, determinant, zero-mode, group and selector labels do not descend from the cut archive alone `\citep{WangTPC143,WangTPC144,WangTPC145,WangTPC146}`. TPC-151 and MVP5 retain the actual lift as the first missing structural object `\citep{WangTPC151,WangTPC152}`. TPC-153 constructs the maximal source-backed partial cut-occurrence shadow, while TPC-154 proves that its conservative formal completion fiber is non-singleton `\citep{WangTPC153,WangTPC154}`. Thus current-artifacts-only canonical recovery is stopped, but the theorem-augmented actual-lift route remains open. We do not fill that gap by fabricated labels. Instead we make the acceptance condition for a future candidate exact and executable.

# Exact scalars and row separation

> **Definition: Exact scalar** An exact scalar is a pair $$z=(a/b)+i(c/d),\qquad a,c\in\mathbb Z,\quad b,d\in\mathbb N,$$ stored as two reduced fractions with positive denominators. Floating point values are invalid.

This representation allows signed and complex lift edges without changing the conservation rule. Let $s:\mathcal O_X\to\mathcal C_X^{\mathrm{ns}}$ assign to each occurrence its unique source cut, and let $\lambda_o$ be its lift edge weight. The matrix encoded by the rows is $$(L_X)_{o,c}=\lambda_o\,\mathbf 1_{\{s(o)=c\}}.
 \label{eq:matrix}$$

> **Theorem: Exact column criterion** <span id="thm:column" label="thm:column">\[thm:column\]</span> For the row-separated matrix in [\[eq:matrix\]](../main.tex#L163){reference-type="ref" reference="eq:matrix"}, $$\mathbf 1^T L_X=\mathbf 1^T
>  \quad\Longleftrightarrow\quad
>  \sum_{o:s(o)=c}\lambda_o=1
>  \quad\text{for every }c\in\mathcal C_X^{\mathrm{ns}}.$$

> **Proof** The $c$-th coordinate of $\mathbf 1^T L_X$ is the sum of the entries in column $c$. By row separation, exactly the rows with $s(o)=c$ contribute, giving the right side. The equalities are coordinatewise, so no cancellation involving another cut column can certify conservation.

> **Remark** The theorem neither requires $\lambda_o\ge0$ nor requires a one-to-one lift. For example $3/2$ and $-1/2$ form a valid two-row column. The verifier checks the sum in exact Gaussian-rational arithmetic.

# `OccurrenceWitnessV1`

## Domain and source registry

> **Definition: Witness domain** A witness has scope either `SYNTHETIC_L0_ONLY` or `PRODUCTION_CANDIDATE`. Its declared domain is exactly `ALL_NONSOFT_ETO_PLUS_FUM`. Each cut record contains: $$(\text{cut id},\text{terminal type},\text{native identity},
>    \text{source multiplier AST},m_c,
>    \text{support record},\text{source id}),$$ where $m_c$ is an exact sourced evaluation of the inherited cut multiplier. In production mode the source AST must equal the literal TPC-143 dyadic multiplier AST; the evaluation source must then justify the exact scalar used by the multiplier chain.

In production mode the cut ids and ETO/FUM types must equal the source-locked TPC-143 obligation domain. In synthetic mode the regression bundle must contain at least one row of each type. This second rule makes the empty-class policy executable rather than merely documentary.

Every source record has a unique identifier, theorem identifier, source class, artifact path and canonical hash. Production mode accepts only `SOURCE_LOCKED_THEOREM`; the path must stay inside the repository and its `CANONICAL_UTF8_LF_V2` hash must match. Synthetic mode uses `SYNTHETIC_AXIOM_L0`, for which artifact path and hash are null. Resolving an identifier proves referential integrity, not the mathematical truth of the named theorem.

## Native identity and support namespaces

The native identity is $$(\text{native id},(\ell,k,d_{\rm native}),h_0,
   \text{physical normalization},\text{weight source}).$$ It is copied literally from cut to every occurrence. The name $d_{\rm native}$ is intentional: it is not automatically the affine intercept $d$ used later.

Support has three distinct roles: $$\begin{split}
 &\texttt{FORMAL\_SUPPORT\_ENVELOPE},\\
 &\texttt{CANONICAL\_PARENT\_CARRIER},\\
 &\texttt{ACTUAL\_ACTIVE\_SUPPORT}.
\end{split}$$ The coefficient status is separately `UNDECIDED`, `PROVED_NONZERO` or `PROVED_ZERO`. An active-support row is accepted only with a nonzero status and a resolved source. All inherited cut records remain formal-envelope and undecided. Thus the verifier cannot turn a symbolic native coefficient into a nonzero physical coefficient by changing a label.

## Parent, stage and multiplier chain

For every occurrence $o$, the canonical-parent record contains:

1.  the key $(\alpha,\gamma,j)$, row ids, integer slopes and ordered targets $(x,y)$;

2.  content gcd, signed determinant numerator and exact determinant label;

3.  inverse-aggregation relation, computational and physical multiplicities;

4.  literal parent coefficient and determinant-bin edge; and

5.  a trusted source id.

The stage record identifies the source cut, target occurrence, source and target shift tags, selector domains, stage-matrix edge, local multiplier and source. Its target must be the current occurrence, not merely a group containing that occurrence.

The multiplier chain is $$M_o=m_{s(o)}\lambda_o\prod_{r=1}^{R(o)}\mu_{o,r}.$$ with each factor separately named, exactly represented and sourced. The stage multiplier and physical reconstruction multiplier must both appear among the factors. The recorded total is accepted only when it equals the right side exactly.

## The four downstream interfaces

The witness does not infer the four maps; it demands their occurrence-resolved data:

$Q_D$, determinant quotient

:   determinant-bin id, bin edge and exact label, agreeing with the canonical parent.

$Q_Z$, outer zero-mode quotient

:   outer affine key, ordered coordinate and rank, arithmetic sign, outer weight, factor allocation, content-remainder destination and zero-mode edge.

$G$, physical grouping

:   physical occurrence and group ids, exact reconstruction multiplier, inverse aggregation, cover class, reconnection destination and physical edge.

$P_{h_0}$, downstream selector

:   stage edge, source and target shift tags, source and target selector domains, and a literal edgewise fixed-$h_0$ preservation Boolean.

The affine record writes $$D(n)=d+sn,\qquad V(n)=u+an,\qquad \Delta=su-ad.$$ It must reproduce the parent’s signed determinant and must state `DISTINCT_SYMBOL_WITH_EXPLICIT_CROSSWALK` between $d_{\rm native}$ and $d$. Equality caused only by using the same letter is rejected.

# Three exports that cannot be merged

The occurrence witness is accompanied by three files with the same witness id and occurrence-id domain.

> **Definition: Separate exports** <span id="def:exports" label="def:exports">\[def:exports\]</span>
>
> 1.  The *physical-cover export* gives a cover atom, cover class, row-disjointness key, exact cover multiplier and source for each occurrence.
>
> 2.  The *reconnection export* gives a destination, exact reconnection multiplier, literal weight-sign-phase id and source for each occurrence.
>
> 3.  The *occurrence-registry export* gives cut, parent, stage, physical occurrence, group, native, support and exact ancestor closure for each occurrence.

Every supplied occurrence must occur exactly once in each export. The cover multiplier must equal the $G$-record reconstruction multiplier; the reconnection destination must equal the $G$-record destination; and the registry must reproduce the full row lineage. In this V1 *row-disjoint* cover contract, cover atoms and disjointness keys are unique. A later contract may admit a shared physical atom only through an explicit theorem-backed joint token and a corresponding no-double-charge rule; no such token is inferred here.

The committed export scope is `WITNESS_OCCURRENCE_ROWS_ONLY`, with `claim_full_production_carrier=false`. This distinction is essential: a complete export on a synthetic or incomplete supplied witness is not a complete physical cover of the unknown actual carrier.

# Soundness of the finite verifier

Let $\mathcal W$ be a supplied witness and let $\operatorname{Verify}(\mathcal W)$ denote acceptance by the executable checks above.

> **Theorem: Internal soundness** <span id="thm:soundness" label="thm:soundness">\[thm:soundness\]</span> If $\operatorname{Verify}(\mathcal W)=\textnormal{\textsc{pass}}$, then the induced map $$L_{\mathcal W}e_c
>    =\sum_{o:s(o)=c}\lambda_o e_o\qquad
>  \label{eq:induced-map}$$ is row-separated and exactly conservative. Every row has:
>
> 1.  identical native tuple, $h_0$ and physical normalization to its source cut;
>
> 2.  a resolved parent, stage and exact multiplier product;
>
> 3.  internally consistent $Q_D,Q_Z,G,P_{h_0}$ records;
>
> 4.  an explicit support role and coefficient-status field; and
>
> 5.  exactly one compatible record in each export of [\[def:exports\]](../main.tex#L319){reference-type="ref" reference="def:exports"}.

> **Proof** The parser rejects missing or duplicate cut and occurrence ids. Each occurrence contains one source-cut id and is inserted in exactly one column. Exact per-column summation and [\[thm:column\]](../main.tex#L167){reference-type="ref" reference="thm:column"} give conservation. The remaining statements are direct equality checks: native identity against its cut; parent determinant against $Q_D$ and the affine calculation; stage tags and domains against $P_{h_0}$; named multiplier factors against the recorded product; and exact occurrence-id covers plus field joins against the three exports.

> **Proposition: Metadata intertwining** <span id="prop:intertwining" label="prop:intertwining">\[prop:intertwining\]</span> Let $a$ be any scalar-valued cut field copied exactly to all occurrences above its source, and let $D_a^{\rm cut}$ and $D_a^{\rm occ}$ be the corresponding diagonal multiplication operators. Every accepted witness satisfies $$D_a^{\rm occ}L_{\mathcal W}
>    =L_{\mathcal W}D_a^{\rm cut}.$$ In particular this holds for $h_0$ and for any encoded scalar normalization label.

> **Proof** For a basis vector $e_c$, both sides equal $a(c)\sum_{s(o)=c}\lambda_oe_o$, because the occurrence value is required to equal the cut value.

> **Proposition: No hidden shift leakage** An accepted witness preserves the prescribed shift row by row. It cannot pass merely because cross-shift entries cancel in an aggregated matrix.

> **Proof** For each occurrence, source and target shift tags and selector domains must both equal the literal value constructed from that row’s $h_0$. The test precedes all aggregation. Therefore an edge that leaves the slice fails independently of every other edge, matching the row-separated criterion of TPC-145 `\citep{WangTPC145}`.

> **Theorem: Relative completeness** Within the declared finite schema, the verifier accepts exactly when all required records exist, all identifiers are total and unique, all trusted-source references resolve, all cross-record equalities hold, every cut column is conservative, and the three supplied exports are exact occurrence covers.

> **Proof** Soundness is [\[thm:soundness\]](../main.tex#L357){reference-type="ref" reference="thm:soundness"}. Conversely, the implementation is a finite conjunction of precisely the listed syntactic, arithmetic, referential and equality predicates. If they all hold, no rejection branch is reached.

# The provenance firewall

Internal soundness must not be confused with external arithmetic truth.

> **Theorem: No provenance promotion** <span id="thm:firewall" label="thm:firewall">\[thm:firewall\]</span> Acceptance of a production candidate proves neither:
>
> 1.  that a theorem named in its source registry is mathematically correct;
>
> 2.  that its occurrence set is the actual active-support carrier, unless that assertion is itself supplied by a valid external theorem; nor
>
> 3.  that the completed four maps yield an arithmetic saving.

> **Proof** The verifier reads finite files. Its source operation checks path, hash and identifier equality; it does not contain a proof checker for the mathematical statements in those files. Its support operation checks a typed source for a nonzero assertion but cannot derive that assertion from a symbolic coefficient. Finally, the contract contains no analytic estimate. Hence none of the three conclusions follows from acceptance alone.

> **Corollary** A positive production verification would establish a candidate $\mathrm{L1}_{\rm structural}$ carrier conditional on the imported provenance, not positive physical $\mathrm{L2}$. Independent mathematical audits of the sources and all later arithmetic gates would still be required.

# A non-vacuous synthetic certificate

The committed fixture has two cut columns and three occurrence rows.

\@P0.25 P0.23P0.14Y@ Cut & Type & Occurrence weights & Exact column sum\
`synthetic-cut-eto` & ETO & $1$ & $1$\
`synthetic-cut-fum` & FUM & $1/3,\ 2/3$ & $1$\

The FUM column is genuinely one-to-many. The three rows carry distinct affine determinant checks $5,13,2$. The fixture exercises formal-envelope, canonical-parent and active-support namespaces; the last is backed only by a source explicitly named `SYNTHETIC.SUPPORT.FIXTURE`. Stage and reconstruction factors are $2$ and $1/2$, so their downstream product is one while each factor remains visible.

> **Proposition: Synthetic certificate result** The generated fixture passes exact conservation, row separation, native/$h_0$/normalization intertwining, parent-stage-multiplier lineage, all four interface records and all three separate exports.

> **Proof** The two column sums are displayed in [\[tab:fixture\]](../main.tex#L482){reference-type="ref" reference="tab:fixture"}. The deterministic artifact reports three unique occurrence ids, and the verifier checks every remaining predicate in [\[thm:soundness\]](../main.tex#L357){reference-type="ref" reference="thm:soundness"}. All trusted records have synthetic rather than production source class.

This proposition establishes that the contract is satisfiable and that its one-to-many branch is executable. It says nothing about whether the current production archive admits such a completion.

# Current production verdict

The production-status artifact deliberately contains no witness path and no paths for the three exports. Its exact state is: $$\begin{array}{ll}
\texttt{partial\_shadow\_status}
  &=\texttt{PROVED\_L1\_STRUCTURAL},\\
\texttt{production\_witness\_present} & =\texttt{false},\\
\texttt{current\_production\_actual\_witness\_status}
  &=\textnormal{\textsc{not-testable}},\\
\texttt{occurrence\_lift\_candidate\_status}&=\textnormal{\textsc{not-testable}},\\
\texttt{QD\_status},\texttt{QZ\_status},
\texttt{G\_status},\texttt{P\_h0\_status}&=\textnormal{\textsc{not-testable}},\\
\texttt{physical\_cover\_status}&=\textnormal{\textsc{not-testable}},\\
\texttt{reconnection\_status}&=\textnormal{\textsc{not-testable}},\\
\texttt{occurrence\_registry\_status}&=\textnormal{\textsc{not-testable}}.
\end{array}$$

> **Theorem: Source-locked TPC-155 verdict** <span id="thm:verdict" label="thm:verdict">\[thm:verdict\]</span> For the canonical TPC-143–152 sources, $$\boxed{
>  \operatorname{Status}_{\rm verifier}=\textnormal{\textsc{pass}}_{\mathrm{L0}},
>  \qquad
>  \operatorname{Status}_{\rm production\ actual\ lift}=\textnormal{\textsc{not-testable}}.}$$ The refined missing artifact is the theorem-backed row-level cut-to-stage-to-parent-to-physical-occurrence provenance crosswalk needed to populate a production `OccurrenceWitnessV1` on every ETO and FUM cut path, together with separate complete physical-cover, reconnection and occurrence-registry exports.

> **Proof** The canonical source hashes and imported statuses pass. The schema, fixture, three exports and mutation suite are deterministically generated and verified. Conversely, the production declaration has no witness or export paths. By [\[thm:firewall\]](../main.tex#L444){reference-type="ref" reference="thm:firewall"}, the synthetic bundle cannot supply them. Hence the interface is proved and the actual object remains unavailable.

This is not a negative theorem saying that no actual occurrence lift exists. It says only that TPC-155 has received no theorem-backed production witness satisfying the contract.

# Mutation audit and kill criteria

The executable audit rejects the following classes of mutations:

1.  cut deletion, duplication, ETO omission and terminal-domain narrowing;

2.  occurrence deletion, duplication and an empty source column;

3.  failure of one cut column even when the sum over all columns is unchanged;

4.  floating-point or nonreduced exact fractions;

5.  native tuple, $h_0$, normalization, parent or stage drift;

6.  a multiplier total that does not equal the named factor product;

7.  $Q_D$/parent determinant mismatch, unresolved $Q_Z$ source, $G$-multiplier mismatch and downstream shift leakage;

8.  identification of $d_{\rm native}$ with the affine intercept by name alone;

9.  active-support promotion without a nonzero source;

10. deletion, duplication or cross-field drift in any one of the physical-cover, reconnection or registry exports;

11. promotion of the synthetic scope, production witness, actual map status, physical cover or positive-$\mathrm{L2}$ claim.

These tests give operational kill criteria.

Schema route fails

:   if a proposed witness omits either nonsoft type from the declared domain, lacks a unique row source, or cannot represent its coefficients exactly.

Conservation route fails

:   if any individual cut column does not sum exactly to one. Aggregate compensation by another cut is inadmissible.

Provenance route fails

:   if a parent, stage, multiplier, support or map field lacks a resolved theorem-backed production source.

Fixed-shift route fails

:   if even one occurrence edge changes its shift tag or leaves its literal $h_0$ selector domain.

Physical-completion route fails

:   if any supplied occurrence is absent from one of the three independent exports or if their joins disagree.

Failure of one candidate does not prove architecture infeasibility. It rejects that witness and leaves the augmented occurrence route open. A genuine impossibility verdict would require a separate theorem covering the full route universe.

# What the verifier enables next

Once a source-locked production bundle exists, the following questions become finite and testable:

1.  whether the actual $Q_D$ and $Q_Z$ quotient matrices have equal kernels on the completed occurrence space `\citep{WangTPC144}`;

2.  whether physical grouping commutes with the downstream $P_{h_0}$ selector row by row `\citep{WangTPC145}`;

3.  whether all components of the four-map defect vector vanish `\citep{WangTPC146}`; and

4.  whether the physical cover, final reconnection and independent registry are complete in the actual active-support scope.

The order matters. Abstract quotient or commutation theorems cannot be evaluated on an occurrence space that has not been supplied. Likewise, an internally complete cover of a formal support envelope does not establish the minimal active carrier. TPC-155 therefore turns a vague request for “more provenance” into an exact artifact boundary without moving an unknown Boolean to true.

#### Established.

The exact witness schema, column-conservation theorem, metadata intertwining, edgewise fixed-shift test, multiplier accounting, three-export separation, internal verifier soundness and synthetic non-vacuity are $\mathrm{L0}/\mathrm{L1}_{\rm structural}$ interface results.

#### Not established.

No production occurrence witness or actual active-support carrier is established. The same is true of the actual $Q_D,Q_Z,G,P_{h_0}$ maps, complete physical cover, reconnection, occurrence registry, positive fixed-$X$-power $\mathrm{L2}$ theorem and endpoint pass.

# Conclusion

The missing frontier occurrence lift is now accompanied by a precise acceptance contract. A future producer cannot obtain a pass by dropping ETO, aggregating away row leakage, renaming formal support as active, hiding a multiplier, merging cover with reconnection, or citing an unhashed source. Conversely, a fully sourced candidate can be checked with exact finite arithmetic.

This is a useful structural advance because it converts the next claim into a falsifiable certificate. It is intentionally not the claim itself. The source-locked production status remains $\textnormal{\textsc{not-testable}}$, and the next mathematical task is to construct the missing parent-stage-occurrence crosswalk rather than to promote the synthetic regression.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@unpublished{WangTPC143,
  author = {Wang, Liang},
  title  = {The Frontier Occurrence-Lift Contract},
  note   = {TPC-143 manuscript},
  year   = {2026}
}

@unpublished{WangTPC144,
  author = {Wang, Liang},
  title  = {A Kernel Test for Determinant and Zero-Mode Quotients},
  note   = {TPC-144 manuscript},
  year   = {2026}
}

@unpublished{WangTPC145,
  author = {Wang, Liang},
  title  = {Occurrence-Resolved Physical Grouping and Prescribed-Shift Commutation on the Frontier},
  note   = {TPC-145 manuscript},
  year   = {2026}
}

@unpublished{WangTPC146,
  author = {Wang, Liang},
  title  = {An Executable Four-Map Completion Certificate for Frontier Totalization},
  note   = {TPC-146 manuscript},
  year   = {2026}
}

@unpublished{WangTPC151,
  author = {Wang, Liang},
  title  = {Source-Locked Integration at the Frontier Occurrence Lift},
  note   = {TPC-151 manuscript},
  year   = {2026}
}

@unpublished{WangTPC152,
  author = {Wang, Liang},
  title  = {MVP5 at the Frontier Occurrence Lift},
  note   = {TPC-152 manuscript},
  year   = {2026}
}

@unpublished{WangTPC153,
  author = {Wang, Liang},
  title  = {The Canonical Cut-Occurrence Shadow: A Maximal Source-Backed Partial Lift and Its Exact Boundary},
  note   = {TPC-153 manuscript},
  year   = {2026}
}

@unpublished{WangTPC154,
  author = {Wang, Liang},
  title  = {Conservative Completion Fibers: A Current-Schema Obstruction to Canonical Occurrence Recovery},
  note   = {TPC-154 manuscript},
  year   = {2026}
}
```

<!-- SOURCE_BODY_END -->
