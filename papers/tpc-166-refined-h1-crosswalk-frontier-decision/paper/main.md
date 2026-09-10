# **Refining the H1 Crosswalk Frontier:**\ **Three Independent Production Roots after**\ **Archive Separation and Formal Gluing**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-166-refined-h1-crosswalk-frontier-decision.pdf](../tpc-166-refined-h1-crosswalk-frontier-decision.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-162 records the first missing structural object as the monolithic node $\mathsf H_{\rm mono}$. TPC-163–165 now reveal its internal dependency structure without constructing the production carrier. We freeze the TPC-162 pointer as historical fact and refine it by a source-locked acyclic graph.

Inside this monolithic-crosswalk sub-DAG, the graph has exactly three minimal $\mathsf{NOT\_TESTABLE}$ roots: $$\begin{gathered}
\mathsf{H1.source\_backed\_local\_occurrence\_edge\_family},\\
\mathsf{H1.actual\_active\_support\_certificate},\\
\mathsf{H1.canonical\_minimal\_representation\_certificate}.
\end{gathered}$$ The first root feeds overlap compatibility and formal local-to-global totality. Formal totality then joins the other two roots at a production occurrence witness, which feeds the historical monolithic crosswalk. The exact archived separation key of TPC-164 and the finite gluing theorem of TPC-165 are proved supporting nodes, not unresolved roots.

For work ordering, the local-edge family is selected as the refined first-child pointer. The full three-element antichain is nevertheless preserved: selection is not implication. TPC-163 still finds zero theorem-backed production local occurrence edges, so the verdict remains $\mathsf{NOT\_TESTABLE}$. No selected route is stopped, and no actual-carrier impossibility is inferred. These three roots are not the complete H1 blocker set: the full map clause still has nine zero-defect requirements and an independent occurrence registry, while the scalar-plus-ETO clause remains independently $\mathsf{NOT\_TESTABLE}$.

<!-- SOURCE_BODY_BEGIN -->

**Keywords:** fixed shift; occurrence provenance; dependency DAG; minimal blocker antichain; route decision.

# Historical pointer versus current refinement

TPC-162 freezes the current verdict $$\mathsf{Verdict}_{162}=\textnormal{\textsc{not-testable}}$$ and the first missing object $$\mathsf H_{\rm mono}:=
 \mathsf{H1.theorem\_backed\_occurrence\_provenance\_crosswalk}.
 \tag{1.1}\label{eq:historical}$$ This statement is correct at the interface resolution used there `\citep{WangTPC162}`. A later decomposition should not retroactively replace [\[eq:historical\]](../main.tex#L120){reference-type="eqref" reference="eq:historical"}: reproducible route histories require old pointers to remain interpretable against their own source locks.

TPC-163–165 provide new resolution:

1.  the frozen source corpus has no theorem-backed production actual-occurrence edge, and native triples collide `\citep{WangTPC163}`;

2.  a unique five-field minimum key separates every archived cut row `\citep{WangTPC164}`; and

3.  compatible local formal patches would glue uniquely with exact conservation, but no production patch is supplied `\citep{WangTPC165}`.

These facts justify a new child-level graph beneath $\mathsf H_{\rm mono}$.

## The complete H1 envelope remains outside this refinement

TPC-156 defines two sufficient clauses `\citep{WangTPC156}`. Write $$\mathcal D=
\{D_L,D_{QD},D_{QZ},D_G,D_P,D_{DZ},D_{GP},
  D_{\rm cover},D_{\rm rec}\}.$$ Then $$\begin{aligned}
\mathsf{Map}_{H1}
 &=
 \mathsf H_{\rm mono}\wedge
 \bigwedge_{D\in\mathcal D}(D=0)
 \wedge\mathsf{OccurrenceRegistryTotal},\\
\mathsf{Scalar}_{H1}
 &=
 \mathsf{CompleteFUM}_{o(X)}
 \wedge\mathsf{TheoremBackedETO},\\
\mathsf{H1Complete}
 &=\mathsf{Map}_{H1}\vee\mathsf{Scalar}_{H1}.
\end{aligned}
\tag{1.2}\label{eq:full-h1}$$ TPC-166 refines only the factor $\mathsf H_{\rm mono}$ in $\mathsf{Map}_{H1}$. The nine zero-defect conditions and the independent occurrence registry remain external requirements. The scalar-plus-ETO clause is a separate $\textnormal{\textsc{not-testable}}$ route and is not a child of $\mathsf H_{\rm mono}$. Therefore the antichain computed below must never be reported as the complete H1 minimal blocker antichain.

> **Definition: Non-retroactive refinement**<span id="def:refine" label="def:refine">\[def:refine\]</span> A refinement of a historical frontier node $H$ consists of:
>
> 1.  a source lock preserving $H$’s original identifier, status, and scope;
>
> 2.  a directed acyclic graph whose target is a new copy of $H$;
>
> 3.  typed child nodes whose conjunction supplies $H$; and
>
> 4.  an explicit statement that the historical record is not rewritten.

# The refined production DAG

We abbreviate: $$\begin{aligned}
\mathsf H_{\rm local}&=\mathsf{source\mbox{-}backed\ local\ occurrence\ edge\ family},\\
\mathsf H_{\rm support}&=\mathsf{actual\ active\ support\ certificate},\\
\mathsf H_{\rm canon}&=\mathsf{canonical/minimal\ representation\ certificate},\\
\mathsf H_{\rm overlap}&=\mathsf{local\ overlap\ bijection/cocycle},\\
\mathsf H_{\rm total}&=\mathsf{glued\ formal\ occurrence\ totality},\\
\mathsf H_{\rm witness}&=\mathsf{production\ occurrence\ witness}.
\end{aligned}$$ The dependency direction is “parent is prerequisite.” The full refined graph is: $$\begin{array}{ccl}
\mathsf H_{\rm local}&\longrightarrow&\mathsf H_{\rm overlap}\\
\{\mathsf H_{\rm local},\mathsf H_{\rm overlap},K_{164},G_{165}\}
 &\longrightarrow&\mathsf H_{\rm total}\\
\{\mathsf H_{\rm total},\mathsf H_{\rm support},\mathsf H_{\rm canon}\}
 &\longrightarrow&\mathsf H_{\rm witness}\\
\mathsf H_{\rm witness}&\longrightarrow&\mathsf H_{\rm mono},
\end{array}
\tag{2.1}\label{eq:dag}$$ where $K_{164}$ is the proved archived separation key and $G_{165}$ is the proved finite typed gluing theorem. The three nodes $\mathsf H_{\rm local},\mathsf H_{\rm support},\mathsf H_{\rm canon}$ have no parents. The nodes $K_{164},G_{165}$ are also parentless, but their status is $\textnormal{\textsc{proved}}$, so they are not blockers.

> **Definition: Minimal unresolved root antichain**<span id="def:antichain" label="def:antichain">\[def:antichain\]</span> For a target $H$ in a finite prerequisite DAG, take the ancestral subgraph of $H$. An unresolved root is a node of status $\textnormal{\textsc{not-testable}}$ having no $\textnormal{\textsc{not-testable}}$ parent in that subgraph. The set of all such roots is the *minimal unresolved root antichain*.

This definition removes descendants that are unavailable only because an earlier unresolved prerequisite is missing. It does not choose one root at the expense of independent roots.

# Exact three-root frontier

> **Theorem: Refined crosswalk-sub-DAG blocker antichain** <span id="thm:antichain" label="thm:antichain">\[thm:antichain\]</span> Within the source-locked DAG [\[eq:dag\]](../main.tex#L208){reference-type="eqref" reference="eq:dag"}, the minimal unresolved root antichain of $\mathsf H_{\rm mono}$ is exactly $$\mathcal A_{166}
>  =
>  \{\mathsf H_{\rm local},\mathsf H_{\rm support},\mathsf H_{\rm canon}\}.
>  \tag{3.1}\label{eq:antichain}$$ The nodes $\mathsf H_{\rm overlap},\mathsf H_{\rm total},\mathsf H_{\rm witness},\mathsf H_{\rm mono}$ are unresolved descendants and hence do not belong to $\mathcal A_{166}$.

> **Proof** The imported TPC-164 and TPC-165 audits give $$\operatorname{status}(K_{164})
>  =\operatorname{status}(G_{165})=\textnormal{\textsc{proved}}.$$ TPC-163 gives zero qualifying production local edges, and TPC-165 keeps formal totality, actual support, and canonical/minimality separate. Therefore $$\operatorname{status}(\mathsf H_{\rm local})
>  =\operatorname{status}(\mathsf H_{\rm support})
>  =\operatorname{status}(\mathsf H_{\rm canon})=\textnormal{\textsc{not-testable}}.$$ Each of these three has no unresolved parent, so all belong to the root antichain.
>
> The node $\mathsf H_{\rm overlap}$ has unresolved parent $\mathsf H_{\rm local}$. The node $\mathsf H_{\rm total}$ has unresolved parents $\mathsf H_{\rm local},\mathsf H_{\rm overlap}$. The node $\mathsf H_{\rm witness}$ has unresolved parents $\mathsf H_{\rm total},\mathsf H_{\rm support},\mathsf H_{\rm canon}$, and $\mathsf H_{\rm mono}$ has unresolved parent $\mathsf H_{\rm witness}$. Hence none of these descendants is minimal. The DAG contains no other nodes, proving [\[eq:antichain\]](../main.tex#L237){reference-type="eqref" reference="eq:antichain"}.

> **Remark: Not the full H1 antichain**<span id="rem:not-full" label="rem:not-full">\[rem:not-full\]</span> concerns only the ancestral sub-DAG of $\mathsf H_{\rm mono}$. Replacing $\mathsf H_{\rm mono}$ by its three roots inside [\[eq:full-h1\]](../main.tex#L163){reference-type="eqref" reference="eq:full-h1"} still leaves the nine defect nodes, occurrence-registry totality, and the independent scalar-plus-ETO clause. Their full-DAG minimality is not computed here.

> **Corollary: No single-root reduction**<span id="cor:no-single" label="cor:no-single">\[cor:no-single\]</span> Proving any one member of $\mathcal A_{166}$ does not, by the current dependency contract, prove either of the other two.

> **Proof** The three nodes are pairwise parent-independent in [\[eq:dag\]](../main.tex#L208){reference-type="eqref" reference="eq:dag"}. No imported theorem supplies a directed path between them.

# A selected pointer that preserves the antichain

For sequential work, a single display pointer is useful. We select $$\mathsf{FirstChild}_{166}=\mathsf H_{\rm local}
 \tag{4.1}\label{eq:selected}$$ because it is the first source-producing object on the local-to-global branch. If local edges are found, overlap maps become testable and the proved gluing theorem can be instantiated.

> **Proposition: Selection is not erasure**<span id="prop:selection" label="prop:selection">\[prop:selection\]</span> Equation [\[eq:selected\]](../main.tex#L292){reference-type="eqref" reference="eq:selected"} is an ordering convention for the next construction. The production blocker set remains the full $\mathcal A_{166}$ of [\[eq:antichain\]](../main.tex#L237){reference-type="ref" reference="eq:antichain"}.

> **Proof** The machine decision stores both fields independently: $$\begin{split}
> \mathsf{canonical\ selected\ representative}&=\mathsf H_{\rm local},\\
> \mathsf{full\ antichain\ preserved}
>  &= [\mathsf H_{\rm local},\mathsf H_{\rm support},\mathsf H_{\rm canon}].
> \end{split}$$ Its validator recomputes the antichain from the DAG and rejects any candidate that deletes $\mathsf H_{\rm support}$ or $\mathsf H_{\rm canon}$. Thus selection cannot change the mathematical dependency set.

Here “canonical selected representative” refers only to deterministic serialization and display order. It is not the missing $\mathsf H_{\rm canon}$ theorem.

# Production evidence and verdict

The source-locator census remains decisive at the first child: $$\#\mathcal E_{\rm local}^{\rm theorem\mbox{-}backed}=0
 \quad\text{in the frozen declared corpus}.
 \tag{5.1}\label{eq:zero-local}$$ Consequently no production local patch family exists in the current evidence set. The statuses are:

0.96\@Y P0.2@ **Object** & **Status**\
minimum archived separation key & $\textnormal{\textsc{proved}}$\
finite typed gluing theorem & $\textnormal{\textsc{proved}}$\
source-backed local occurrence edge family & $\textnormal{\textsc{not-testable}}$\
actual active-support certificate & $\textnormal{\textsc{not-testable}}$\
canonical/minimal representation certificate & $\textnormal{\textsc{not-testable}}$\
overlap cocycle and glued formal totality & $\textnormal{\textsc{not-testable}}$\
production occurrence witness and monolithic crosswalk & $\textnormal{\textsc{not-testable}}$\

> **Theorem: Current refined decision**<span id="thm:decision" label="thm:decision">\[thm:decision\]</span> Under the nine source locks of TPC-166, and only inside the historical monolithic-crosswalk sub-DAG, $$\boxed{\mathsf{Verdict}_{166}=\textnormal{\textsc{not-testable}}},
>  \qquad
>  \mathsf{FirstChild}_{166}=\mathsf H_{\rm local},
>  \qquad
>  \mathcal A_{166}
>  =\{\mathsf H_{\rm local},\mathsf H_{\rm support},\mathsf H_{\rm canon}\}.
>  \tag{5.2}\label{eq:decision}$$ The selected occurrence-augmented route is not stopped, and no actual-carrier impossibility is proved.

> **Proof** The verdict cannot be $\mathsf{GO}$ because each root in $\mathcal A_{166}$ is unresolved. It cannot be a route stop or impossibility verdict because the source census is closed-world and the formal gluing theorem leaves source augmentation open. Thus the typed result is $\textnormal{\textsc{not-testable}}$, with pointer and antichain given by \[[eq:selected](../main.tex#L292),[eq:antichain](../main.tex#L237)\].

# Why TPC-162 is not rewritten

There is no contradiction between $$\mathsf{FirstMissing}_{162}=\mathsf H_{\rm mono}
 \quad\text{and}\quad
 \mathsf{FirstChild}_{166}=\mathsf H_{\rm local}.$$ The first names the unresolved public interface at TPC-162 resolution. The second names one child after a later factorization. The certificate records $$\mathsf{historical\ pointer\ retroactively\ rewritten}=\mathsf{false}$$ and mutation-tests the opposite value. This provenance discipline allows later papers to refine a route without silently changing what an earlier source actually asserted.

# Reproducible DAG audit

The generator locks the TPC-162 snapshot/audit and both certificate/audit pairs from TPC-163–165, together with the TPC-156 full H1 contract. It validates:

1.  unique node identifiers and total parent references;

2.  acyclicity by depth-first topological traversal;

3.  exact node statuses and dependency lists;

4.  recomputation of the minimal unresolved root antichain;

5.  preservation of the crosswalk-sub-DAG scope and exclusion of the nine defects, independent registry, and scalar clause;

6.  preservation of the historical pointer;

7.  zero production local edges and the $\textnormal{\textsc{not-testable}}$ verdict.

Real mutations delete either independent root, rewrite the historical pointer, fabricate a production edge, promote the verdict to $\mathsf{GO}$, stop the route, introduce a dependency cycle, or select a representative outside the antichain. The same validator rejects each mutation.

# Next source-producing task

The refinement identifies what the next paper must actually deliver: not another global schema, but at least one theorem-backed local actual-occurrence edge family with:

1.  the five-field archived source address;

2.  canonical path and hash, theorem and formula locators, and a nonempty derivation tree;

3.  exact typed row weights and parent/stage/downstream payloads;

4.  an explicit statement of whether the result is merely formal or lies on the actual carrier.

A partial local theorem would be genuine forward progress even before total coverage. It would not close $\mathsf H_{\rm support}$ or $\mathsf H_{\rm canon}$; those remain parallel research programs.

# Conclusion

TPC-166 turns one opaque H1 blocker into a precise three-root frontier inside that blocker. Two supporting uncertainties are already closed: archived cuts have an exact lossless key, and compatible formal patches glue with exact conservation. The unresolved mathematics is now localized to source-backed local occurrence edges, actual active support, and canonical/minimal representation. The route remains open, the verdict remains $\textnormal{\textsc{not-testable}}$, and the next constructive target is smaller without being overstated. The complete H1 graph, including the external map-clause and scalar-clause requirements of [\[eq:full-h1\]](../main.tex#L163){reference-type="eqref" reference="eq:full-h1"}, remains for a later integration.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@unpublished{WangTPC162,
  author = {Wang, Liang},
  title  = {{MVP6} on the Actual-Carrier Endpoint Corridor},
  note   = {TPC-162 manuscript},
  year   = {2026}
}

@unpublished{WangTPC156,
  author = {Wang, Liang},
  title  = {The {H1} Occurrence-Crosswalk Route Decision},
  note   = {TPC-156 manuscript},
  year   = {2026}
}

@unpublished{WangTPC163,
  author = {Wang, Liang},
  title  = {Source-Locator Census for the {H1} Crosswalk},
  note   = {TPC-163 manuscript},
  year   = {2026}
}

@unpublished{WangTPC164,
  author = {Wang, Liang},
  title  = {An Exact Minimal Addressing Key for the Frozen {H1} Cut Archive},
  note   = {TPC-164 manuscript},
  year   = {2026}
}

@unpublished{WangTPC165,
  author = {Wang, Liang},
  title  = {Source-Backed Local-to-Global Gluing for Formal {H1} Occurrence Crosswalks},
  note   = {TPC-165 manuscript},
  year   = {2026}
}
```

<!-- SOURCE_BODY_END -->
