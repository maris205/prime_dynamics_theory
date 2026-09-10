# **Source-Backed Local-to-Global Gluing**\ **for Formal H1 Occurrence Crosswalks**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-165-source-backed-local-global-crosswalk-gluing.pdf](../tpc-165-source-backed-local-global-crosswalk-gluing.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The missing H1 occurrence crosswalk need not be discovered as one monolithic table. This paper proves the finite descent theorem needed to construct it from local patches. Let a finite family $\{U_i\}$ cover the archived cuts. Suppose each $c\in U_i$ has a finite nonempty local formal row family, and suppose exact typed, weight-preserving bijections identify the row families on pairwise overlaps. If the bijections satisfy the identity, inverse, and triple-overlap cocycle laws, the quotient of the disjoint union is a global formal row family. All preserved payloads descend uniquely; the result is unique up to the unique typed isomorphism commuting with the local maps. If each local column has exact rational weight one, then every global column also has exact weight one.

This theorem is formal and conditional. A synthetic two-patch fixture glues four local row copies to three global rows and verifies exact conservation, while a three-patch regression tests the cocycle nonvacuously. Neither fixture has production semantics. TPC-163 finds zero theorem-backed production actual-occurrence edges in the frozen declared corpus, so no production local patch system is currently available.

Most importantly, the paper separates three gates: formal occurrence totality, actual active support, and canonical/minimal representation. Local-to-global gluing can close only the first. It cannot promote a formal row to nonzero physical support or choose a canonical actual parent.

<!-- SOURCE_BODY_BEGIN -->

**Keywords:** fixed shift; finite descent; gluing; occurrence provenance; exact column conservation; proof interface.

# From a monolithic blocker to a descent problem

TPC-163 gives a source-locator contract and finds no qualifying production actual-occurrence edge in its frozen corpus `\citep{WangTPC163}`. TPC-164 nevertheless solves the archive-address problem: the unique minimum separating key in its eight-field dictionary is $$\kappa(c)=(\ell(c),k(c),d_{\rm nat}(c),j_L(c),j_K(c)).
 \tag{1.1}\label{eq:address}$$ This key does not create actual occurrences, but it lets independent local constructions refer to the same source cut unambiguously `\citep{WangTPC164}`.

The next structural question is therefore: $$\text{can compatible local row families be assembled without
 losing types or exact coefficients?}$$ The answer is yes, by an elementary finite quotient theorem. This does not solve the source problem; it isolates exactly which local data would suffice.

# Typed local patch system

> **Definition: Local formal row system**<span id="def:local" label="def:local">\[def:local\]</span> Let $\mathcal C$ be a finite set of archived cut addresses, and let $\{U_i\}_{i\in I}$ be a finite cover. For every $c\in U_i$, let $\mathcal R_i(c)$ be a finite nonempty set of local formal rows. A row $r\in\mathcal R_i(c)$ carries:
>
> 1.  an archived source address $\kappa(c)$;
>
> 2.  a typed payload $T_i(r)$;
>
> 3.  an exact weight $w_i(r)\in\mathbb Q$; and
>
> 4.  , in production use, a source record satisfying the path–hash–theorem–formula–derivation contract of TPC-163.
>
> Local column conservation means $$\sum_{r\in\mathcal R_i(c)}w_i(r)=1
>  \qquad(c\in U_i).
>  \tag{2.1}\label{eq:local-conservation}$$

The typed payload may contain a formal occurrence symbol, stage, parent, multiplier, and downstream target. The theorem treats those as data to be preserved; it does not assert that they are true of an actual carrier.

> **Definition: Descent datum**<span id="def:descent" label="def:descent">\[def:descent\]</span> For every $c\in U_i\cap U_j$, an overlap map is a bijection $$\phi_{ji,c}:\mathcal R_i(c)\longrightarrow\mathcal R_j(c)
>  \tag{2.2}\label{eq:overlap}$$ such that $$T_j(\phi_{ji,c}r)=T_i(r),\qquad
>  w_j(\phi_{ji,c}r)=w_i(r).
>  \tag{2.3}\label{eq:preserve}$$ The maps form a *descent datum* if $$\phi_{ii,c}=\mathrm{id},\qquad
> \phi_{ij,c}=\phi_{ji,c}^{-1},\qquad
> \phi_{ki,c}=\phi_{kj,c}\circ\phi_{ji,c}
> \tag{2.4}\label{eq:cocycle}$$ on every applicable pairwise or triple overlap.

# Local-to-global gluing theorem

> **Theorem: Finite typed gluing**<span id="thm:gluing" label="thm:gluing">\[thm:gluing\]</span> Let $(\mathcal R_i,T_i,w_i,\phi_{ji})$ be a local formal row system with descent datum. Then:
>
> 1.  there is a global finite nonempty row family $\mathcal R(c)$ for every $c\in\mathcal C$;
>
> 2.  each local family has a canonical bijection $\iota_{i,c}:\mathcal R_i(c)\to\mathcal R(c)$, and $\iota_{j,c}\phi_{ji,c}=\iota_{i,c}$;
>
> 3.  the payload and weight descend uniquely to functions $T:\mathcal R(c)\to\mathcal T$ and $w:\mathcal R(c)\to\mathbb Q$;
>
> 4.  the global object is unique up to the unique typed, weight-preserving isomorphism commuting with all $\iota_{i,c}$; and
>
> 5.  if [\[eq:local-conservation\]](../main.tex#L138){reference-type="eqref" reference="eq:local-conservation"} holds, then $$\sum_{r\in\mathcal R(c)}w(r)=1
>              \qquad(c\in\mathcal C).
>              \tag{3.1}\label{eq:global-conservation}$$

> **Proof** Fix $c\in\mathcal C$. Form the disjoint union $$D(c)=\coprod_{i:c\in U_i}\mathcal R_i(c).$$ Declare $(i,r)\sim(j,s)$ if $s=\phi_{ji,c}(r)$. Identity and inverse give reflexivity and symmetry, and the cocycle gives transitivity. Thus $\sim$ is an equivalence relation. Put $$\mathcal R(c)=D(c)/{\sim},\qquad
>  \iota_{i,c}(r)=[i,r].
>  \tag{3.2}\label{eq:quotient}$$
>
> For fixed $i,j$ containing $c$, the overlap bijection identifies each row of $\mathcal R_i(c)$ with exactly one row of $\mathcal R_j(c)$. Consequently every equivalence class has exactly one representative in each participating patch, and each $\iota_{i,c}$ is bijective. Equation [\[eq:preserve\]](../main.tex#L157){reference-type="eqref" reference="eq:preserve"} makes $$T([i,r])=T_i(r),\qquad w([i,r])=w_i(r)$$ well-defined. Uniqueness of these descended functions is immediate because the local maps are jointly surjective.
>
> If another global family $\mathcal R'(c)$ has compatible local bijections $\iota'_{i,c}$, define $$\Psi_c([i,r])=\iota'_{i,c}(r).$$ Compatibility makes $\Psi_c$ well-defined. It is the only map commuting with the local maps, and the same construction in reverse gives its inverse. This proves the stated unique isomorphism.
>
> Finally choose any $i$ with $c\in U_i$. Since $\iota_{i,c}$ is a weight-preserving bijection, $$\sum_{r\in\mathcal R(c)}w(r)
>  =\sum_{r\in\mathcal R_i(c)}w_i(r)=1,$$ which proves [\[eq:global-conservation\]](../main.tex#L190){reference-type="eqref" reference="eq:global-conservation"}.

> **Corollary: Matrix conservation**<span id="cor:matrix" label="cor:matrix">\[cor:matrix\]</span> Let $L_i$ send the basis vector $e_c$ to the exact weighted sum of local rows in $\mathcal R_i(c)$. Under the hypotheses of [\[thm:gluing\]](../main.tex#L171){reference-type="ref" reference="thm:gluing"}, the $L_i$ descend to a global matrix $L$, and $$\mathbf 1^{T}L=\mathbf 1^{T}.
>  \tag{3.3}\label{eq:matrix-conservation}$$

> **Proof** The overlap maps identify equal typed coefficients, so the columns descend. Equation [\[eq:global-conservation\]](../main.tex#L190){reference-type="eqref" reference="eq:global-conservation"} is exactly [\[eq:matrix-conservation\]](../main.tex#L244){reference-type="eqref" reference="eq:matrix-conservation"} column by column.

# Why the cocycle is indispensable

Pairwise compatibility alone does not force consistent identifications around a triple overlap. If $\phi_{31,c}\ne\phi_{32,c}\phi_{21,c}$, a row in patch $1$ gets two competing representatives in patch $3$. The binary relation generated by pairwise maps still has a quotient, but a chosen local map need no longer be injective into it; the asserted common row family can collapse. Thus the cocycle is exactly the condition used in the injectivity step of [\[thm:gluing\]](../main.tex#L171){reference-type="ref" reference="thm:gluing"}.

The audit tests this nonvacuously. A three-patch, two-row fibre uses identity maps on all overlaps. Swapping only the direct map from the first patch to the third preserves exact payloads, weights, and pairwise bijectivity, but violates the triangle equation. The validator rejects it.

# Synthetic nonvacuity certificate

The public sample uses $$U_1=\{c_1,c_2\},\qquad U_2=\{c_2,c_3\}.$$ Each local cut has one row of rational weight $1$. The two copies over $c_2$ have the same typed payload and are identified by the overlap bijection. Therefore: $$\begin{array}{c|c}
\text{quantity}&\text{value}\\
\hline
\text{cut count}&3\\
\text{patch count}&2\\
\text{local row copies}&4\\
\text{global formal rows}&3\\
\text{every local/global column sum}&1.
\end{array}$$ This demonstrates that the serialization and quotient algorithm are reachable. Every record is explicitly marked $\mathsf{SYNTHETIC\_REACHABILITY}$ with theorem semantics false.

# Three gates that gluing must not merge

> **Definition: Separated production gates**<span id="def:gates" label="def:gates">\[def:gates\]</span> For a proposed production carrier, define:
>
> 1.  $\mathsf{formal\ occurrence\ totality}$: every archived cut address has at least one globally glued formal row;
>
> 2.  $\mathsf{actual\ active\ support}$: every required row is an actual carrier occurrence with the required nonzero physical coefficient; and
>
> 3.  $\mathsf{canonical/minimal\ representation}$: an independent theorem selects or characterizes its canonical/minimal actual parent representation.

> **Proposition: No gate promotion**<span id="prop:no-promotion" label="prop:no-promotion">\[prop:no-promotion\]</span> can establish G1 from its local hypotheses. It does not imply G2 or G3.

> **Proof** The construction in [\[eq:quotient\]](../main.tex#L206){reference-type="eqref" reference="eq:quotient"} uses only finite sets, typed payload equality, bijections, and exact formal weights. It contains no predicate that embeds a row into the actual arithmetic carrier or proves its physical coefficient nonzero, so it cannot imply G2. It also imposes no equivalence or optimization theorem on actual parents, so it cannot imply G3. Synthetic systems satisfying all gluing hypotheses while declaring both actual predicates undecided give explicit models of the separation.

TPC-155’s witness verifier `\citep{WangTPC155}` checks a declared interface. Even a successful format and conservation check would not, by itself, make an unsourced active-support or canonicality statement true. Those fields require their own source-backed theorems.

# Current production evaluation

The imported source locks give:

0.9\@Y P0.28@ **Production object** & **Status**\
source-backed local actual-occurrence edges & $0$ in frozen corpus\
local patch family & $\textnormal{\textsc{not-testable}}$\
overlap bijections and cocycle & $\textnormal{\textsc{not-testable}}$\
formal occurrence totality & $\textnormal{\textsc{not-testable}}$\
actual active support & $\textnormal{\textsc{not-testable}}$\
canonical/minimal representation & $\textnormal{\textsc{not-testable}}$\

The formal gluing theorem is proved, but its production hypotheses are not currently instantiated. This is not a negative existence theorem. New source-backed local occurrence results could populate the interface.

#### Reproducible audit.

The generator source-locks TPC-163/164, recomputes the quotient and exact rational sums, and rejects real mutations of overlap, payload, weight, cocycle, evidence mode, production edges, and gate status.

# Conclusion

Compatible source-backed local patches can build a global formal H1 crosswalk with exact conservation. Producing the local actual edges, proving actual active support, and proving canonical/minimal representation remain three distinct tasks that the next decision must preserve as parallel roots.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@unpublished{WangTPC155,
  author = {Wang, Liang},
  title  = {A Theorem-Backed Occurrence-Witness Verifier},
  note   = {TPC-155 manuscript},
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
```

<!-- SOURCE_BODY_END -->
