# **Source-Locator Census for the H1 Crosswalk:**\ **Native-Key Collisions and the Absence of Production**\ **Occurrence Edges in the Frozen Corpus**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-163-source-locator-census-native-key-collision.pdf](../tpc-163-source-locator-census-native-key-collision.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The H1 branch of the fixed-shift program currently stops at a theorem-backed cut-to-occurrence provenance crosswalk. We turn that informal phrase into an auditable source-locator contract. A positive production edge must name a canonical source path and hash, an exact theorem locator, an exact formula locator, and a nonempty derivation abstract-syntax tree, while preserving the distinction between a formal shadow and an actual occurrence.

For the frozen declared TPC-153/154/155/156/161/162 corpus, the census contains $2988$ distinct cut paths, two qualifying positive shadow claims, and two formal-only scoped-obstruction claims. It contains no qualifying actual-occurrence edge in any of thirteen required semantic classes. Independently, the archive has only $866$ distinct native triples $(\ell,k,d_{\rm nat})$. Of these, $854$ collide; $2976$ rows lie in collision classes, and the excess over native keys is $2122$. The exact multiplicity distribution is $$\{1:12,\;2:220,\;4:634\}.$$ Consequently the native triple is not a row key for this archive.

Both conclusions are deliberately scoped. Zero qualifying edges in the frozen corpus is not a nonexistence theorem for actual occurrences, and failure of the native triple as an archive key is not a failure of every enriched occurrence representation. The next forced structural task is to identify the smallest archived separating key before attempting source-backed local occurrence patches.

<!-- SOURCE_BODY_BEGIN -->

**Keywords:** fixed shift; occurrence provenance; source locator; archive key; collision obstruction; proof audit.

# Why a source census is now necessary

TPC-153 constructs a conservative, row-separated map from every nonsoft cut path to a *partial shadow row* `\citep{WangTPC153}`. Its universal property says that any metadata-faithful actual completion must forget back to this shadow; it does not construct such a completion. TPC-154 constructs two inequivalent *formal* completions and thereby stops recovery from current artifacts alone; it explicitly leaves the augmented theorem-backed route open `\citep{WangTPC154}`. TPC-155 supplies a typed verifier, but its production witness is absent `\citep{WangTPC155}`. TPC-156 therefore identifies $$\mathsf{H1.theorem\_backed\_occurrence\_provenance\_crosswalk}
 \tag{1.1}\label{eq:first-missing}$$ as the first missing map object `\citep{WangTPC156}`. TPC-161 and TPC-162 preserve this blocker while integrating the arithmetic return side `\citep{WangTPC161,WangTPC162}`.

The phrase “theorem-backed” has two possible failure modes. First, a row may cite a file without identifying the mathematical statement or derivation that creates the edge. Second, a valid shadow theorem may be silently promoted to actual-occurrence semantics. The present paper closes both loopholes by defining the admissible evidence unit before counting it.

# Frozen corpus and evidence contract

> **Definition: Frozen declared corpus**<span id="def:corpus" label="def:corpus">\[def:corpus\]</span> The corpus $\mathcal C_{\mathrm{src}}$ consists of the canonically normalized UTF-8/LF versions of the following eleven production artifacts:
>
> 1.  the TPC-153 paper, certificate, and $2988$-row shadow archive;
>
> 2.  the TPC-154 paper, certificate, and formal-completion archive;
>
> 3.  the TPC-155 production status and verifier audit;
>
> 4.  the TPC-156 H1 route decision;
>
> 5.  the TPC-161 occurrence–return manifest; and
>
> 6.  the TPC-162 MVP6 snapshot.
>
> Every source is locked by its repository-relative path and SHA-256 digest. A digest is an integrity assertion only; it does not confer theorem semantics.

> **Definition: Source-locator admissibility**<span id="def:admissible" label="def:admissible">\[def:admissible\]</span> A positive production claim $e$ is *source-locator admissible* if its record contains:
>
> 1.  a canonical path $p(e)\in\mathcal C_{\mathrm{src}}$ and its recomputed canonical digest;
>
> 2.  an exact theorem locator that resolves in $p(e)$;
>
> 3.  an exact formula locator that resolves in $p(e)$;
>
> 4.  a nonempty derivation tree $A(e)$ specifying how the cited formula produces the claimed typed object; and
>
> 5.  a semantic class equal to the conclusion of that derivation.
>
> A shadow conclusion therefore cannot inhabit an actual-occurrence class merely by changing a status string.

The derivation tree is intentionally modest. It is not a proof assistant kernel. It records the operation, inputs, key fields, and exact coefficient so that an audit can reject empty provenance and semantic promotion. Full mathematical truth still resides in the cited source.

> **Definition: Actual H1 edge classes**<span id="def:classes" label="def:classes">\[def:classes\]</span> The production census checks the following thirteen classes: $$\begin{gathered}
> \mathsf{actual\ occurrence},\quad
> \mathsf{actual\ active\ support},\quad
> \mathsf{canonical/minimal\ parent},\\
> \mathsf{ordered\ stage},\quad
> \mathsf{exact\ multiplier},\quad
> Q_D,\ Q_Z,\ G,\ P_{h_0},\\
> \mathsf{native\ affine\ crosswalk},\quad
> \mathsf{physical\ cover},\quad
> \mathsf{reconnection},\quad
> \mathsf{occurrence\ registry}.
> \end{gathered}$$ These are actual-carrier classes. A partial shadow edge is not a member of any of them.

# Exact source-locator census

> **Theorem: Frozen-corpus edge census**<span id="thm:census" label="thm:census">\[thm:census\]</span> In $\mathcal C_{\mathrm{src}}$:
>
> 1.  exactly two shadow claims satisfy [\[def:admissible\]](../main.tex#L145){reference-type="ref" reference="def:admissible"}: the TPC-153 cut-to-shadow basis injection and its column-conservation identity, both with semantic class $$\mathsf{PROVED\_L1\_STRUCTURAL\_SHADOW\_ONLY};$$
>
> 2.  exactly two TPC-154 claims satisfy the source-locator contract: formal completion-fibre nonuniqueness and the current-artifacts-only recovery obstruction, both with class $$\mathsf{FORMAL\_ONLY/SCOPED\_OBSTRUCTION};$$
>
> 3.  none of these four claims has actual-occurrence semantics, and the number of source-locator-admissible production edges in every class of [\[def:classes\]](../main.tex#L167){reference-type="ref" reference="def:classes"} is zero.
>
> Thus the production actual-occurrence edge family is $$\mathcal E_{\rm occ}(\mathcal C_{\mathrm{src}})=\varnothing .
>  \tag{3.1}\label{eq:zero-edges}$$

> **Proof** The audit first recomputes all eleven path–digest locks. It then resolves both LaTeX labels for each positive TPC-153 claim and checks that its derivation tree is nonempty. The first tree is the basis injection $$e_c\longmapsto e_{\operatorname{shadow}(c)}
>  \quad\text{with coefficient }1,
>  \tag{3.2}\label{eq:shadow-map}$$ and the second applies the column-sum operation to [\[eq:shadow-map\]](../main.tex#L223){reference-type="ref" reference="eq:shadow-map"}. Their result types remain shadow-only.
>
> The audit next resolves the TPC-154 completion-fibre and obstruction theorems. Their derivations use two conservative formal completions with respectively one unit-weight child and two half-weight children. The source certificate explicitly records that neither completion is an actual-carrier lift and that only the current-artifacts-only recovery route is stopped. Their semantic class therefore remains $\mathsf{FORMAL\_ONLY/SCOPED\_OBSTRUCTION}$.
>
> Next the audit applies an explicit per-class mapping to the frozen production status, decision, manifest, and snapshot for the thirteen actual classes. TPC-155 records no production witness, and TPC-156/161/162 all retain [\[eq:first-missing\]](../main.tex#L114){reference-type="ref" reference="eq:first-missing"} as unavailable. No record supplies the required path, digest, two locators, derivation tree, and actual semantic class. Hence every class count is zero. Mutation tests verify that a fabricated edge, hash drift, a missing locator, an empty tree, and a shadow-to-occurrence promotion are each rejected.

> **Remark: Mapped census, not a future-schema scanner** The thirteen-class table is exhaustive only for the explicitly mapped fields of $\mathcal C_{\mathrm{src}}$. The program does not generically discover arbitrary fields added by a future schema. Any corpus or schema extension requires a new mapping and a regenerated certificate.

> **Remark: Closed-world scope**<span id="rem:closed" label="rem:closed">\[rem:closed\]</span> Equation [\[eq:zero-edges\]](../main.tex#L211){reference-type="eqref" reference="eq:zero-edges"} is a closed-world statement about $\mathcal C_{\mathrm{src}}$. It says $$\text{``no qualifying edge is declared in this frozen corpus,''}$$ not $$\text{``no actual occurrence edge exists in mathematics.''}$$ The latter would require a completeness theorem for the source universe, which is neither assumed nor proved.

# Native-key collision obstruction

Each shadow row has a unique source-cut path identifier and carries a native triple $$\kappa_{\mathrm{nat}}(c)=(\ell(c),k(c),d_{\rm nat}(c)).$$ One might hope to use $\kappa_{\mathrm{nat}}$ as the future occurrence-row address. The archive itself rules this out.

> **Theorem: Exact native collision census**<span id="thm:collision" label="thm:collision">\[thm:collision\]</span> For the $2988$ production cut paths in $\mathcal C_{\mathrm{src}}$, the map $$\kappa_{\mathrm{nat}}:\mathcal C\longrightarrow\mathbb Z^3
>  \tag{4.1}\label{eq:native-key}$$ has $866$ distinct values. Its fibre-size distribution is $$\#\{v:|\kappa_{\mathrm{nat}}^{-1}(v)|=m\}
>  =
>  \begin{cases}
>  12,&m=1,\\
>  220,&m=2,\\
>  634,&m=4,\\
>  0,&\text{otherwise}.
>  \end{cases}
>  \tag{4.2}\label{eq:distribution}$$ Consequently: $$\begin{aligned}
>  \#\{v:|\kappa_{\mathrm{nat}}^{-1}(v)|>1\}&=854,\\
>  \#\{c:|\kappa_{\mathrm{nat}}^{-1}(\kappa_{\mathrm{nat}}(c))|>1\}&=2976,\\
>  \sum_v\bigl(|\kappa_{\mathrm{nat}}^{-1}(v)|-1\bigr)&=2122.
> \end{aligned}
> \tag{4.3}\label{eq:collision-counts}$$ In particular, $\kappa_{\mathrm{nat}}$ is not a row key for the frozen archive.

> **Proof** Group the $2988$ distinct source-cut path identifiers by the exact integer triple [\[eq:native-key\]](../main.tex#L282){reference-type="eqref" reference="eq:native-key"}. The resulting multiplicity counter is [\[eq:distribution\]](../main.tex#L294){reference-type="eqref" reference="eq:distribution"}. The internal checks $$12+220+634=866,\qquad
>  12+2(220)+4(634)=2988$$ verify the number of keys and rows. Removing the $12$ singleton rows gives $2988-12=2976$ rows in collision classes. The excess is $$220(2-1)+634(4-1)=220+1902=2122.$$ Since a key must have singleton fibres, the final assertion follows.

> **Proposition: Explicit fourfold collision**<span id="prop:witness" label="prop:witness">\[prop:witness\]</span> The native triple $(3,171,1)$ has four distinct archived cut paths, distinguished by $$(j_L,j_K)\in\{1,2\}\times\{7,8\}.$$ Thus the collision in [\[thm:collision\]](../main.tex#L278){reference-type="ref" reference="thm:collision"} is not caused by duplicate row identifiers.

> **Proof** The four source-cut path identifiers in the production excerpt encode the four displayed pairs and are pairwise distinct, while their native triples agree exactly. The accompanying sample is copied from the production archive and is marked as an archive excerpt, not a synthetic or actual-occurrence witness.

# What the two theorems jointly imply

The two obstructions are logically different: $$\begin{array}{c@{\qquad}c}
 \mathcal E_{\rm occ}(\mathcal C_{\mathrm{src}})=\varnothing
 &
 \kappa_{\mathrm{nat}}\text{ is noninjective}
 \\[2pt]
 \text{evidence absence in a frozen corpus}
 &
 \text{exact combinatorial archive fact}.
\end{array}$$ The first blocks an evidence-complete production lift. The formal TPC-154 obstruction additionally rules out canonical recovery from the present shadow fields alone while leaving source augmentation open. The second blocks a tempting shortcut for addressing its rows. Neither prevents an enriched construction from succeeding.

> **Corollary: Required enrichment**<span id="cor:enrich" label="cor:enrich">\[cor:enrich\]</span> Any production crosswalk that represents all $2988$ archived cut paths by distinct rows must use an address strictly finer than $(\ell,k,d_{\rm nat})$, or supply an independently proved quotient theorem identifying every colliding path. No such quotient theorem is present in $\mathcal C_{\mathrm{src}}$.

> **Proof** This is the dichotomy between retaining distinct elements of a noninjective fibre and identifying them by a proved equivalence relation. The latter is absent by the source census.

# Reproducible certificate

The generator reads the upstream JSON/JSONL artifacts, recomputes canonical hashes and all counts, and serializes:

0.96\@P0.38Y@ **Artifact** & **Role**\
**Source census** & source locks, positive claims, thirteen-class census, and collision counts\
**Audit** & recomputation checks, semantic boundaries, and mutation regressions\
**Collision excerpt** & explicit fourfold production archive collision\

Default mode regenerates the artifacts. The `–check` mode recomputes them in memory and demands byte-for-byte equality. The audit performs real mutations: it changes the candidate object and then runs the same validators. It does not merely store expected Boolean values.

# Next forced object

Before constructing local occurrence patches, the archive needs a lossless addressing system. TPC-163 therefore leaves one immediate finite question: $$\text{which smallest subset of existing archived fields separates
 all \(2988\) source-cut paths?}$$ This is an exhaustive finite-key problem, not yet an actual occurrence, active-support, or canonical-minimality theorem. Solving it removes ambiguity from the later local-to-global gluing interface without overclaiming arithmetic progress.

# Conclusion

TPC-163 converts the H1 crosswalk blocker into two precise facts. The frozen declared corpus contains no theorem-backed actual occurrence edge under an explicit source-locator contract, and the native triple fails dramatically as an archive row key. At the same time, the paper preserves the correct open-world boundary: new source-backed occurrence mathematics may still supply the missing edges. The next step is therefore constructive—first refine the archive address, then formulate compatible local occurrence patches.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@unpublished{WangTPC153,
  author = {Wang, Liang},
  title  = {A Canonical Cut--Occurrence Shadow Operator},
  note   = {TPC-153 manuscript},
  year   = {2026}
}

@unpublished{WangTPC155,
  author = {Wang, Liang},
  title  = {A Theorem-Backed Occurrence-Witness Verifier},
  note   = {TPC-155 manuscript},
  year   = {2026}
}

@unpublished{WangTPC154,
  author = {Wang, Liang},
  title  = {A Conservative Completion-Fiber Obstruction},
  note   = {TPC-154 manuscript},
  year   = {2026}
}

@unpublished{WangTPC156,
  author = {Wang, Liang},
  title  = {The {H1} Occurrence-Crosswalk Route Decision},
  note   = {TPC-156 manuscript},
  year   = {2026}
}

@unpublished{WangTPC161,
  author = {Wang, Liang},
  title  = {Source-Locked Occurrence--Return Integration},
  note   = {TPC-161 manuscript},
  year   = {2026}
}

@unpublished{WangTPC162,
  author = {Wang, Liang},
  title  = {{MVP6} on the Actual-Carrier Endpoint Corridor},
  note   = {TPC-162 manuscript},
  year   = {2026}
}
```

<!-- SOURCE_BODY_END -->
