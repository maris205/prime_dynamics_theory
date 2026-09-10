# **An Exact Minimal Addressing Key**\ **for the Frozen H1 Cut Archive**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-164-minimal-archived-separation-key.pdf](../tpc-164-minimal-archived-separation-key.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-163 proves that the native triple $(\ell,k,d_{\rm nat})$ is not a row key for the $2988$-row frozen H1 cut archive: only $866$ triples occur, with $2122$ excess rows over native keys. We now solve the finite addressing problem exactly. For the declared field dictionary $$\mathcal F=
 \{\ell,k,d_{\rm nat},j_L,j_K,D_0,\mathsf{reason},\mathsf{type}\},$$ all $2^8-1=255$ nonempty subsets are tested on every production row. There is a unique separating subset of minimum cardinality: $$\kappa_{\min}=(\ell,k,d_{\rm nat},j_L,j_K).$$ Its cardinality is five, and it produces $2988$ distinct keys. There are respectively $1,3,3,1$ injective subsets of cardinalities $5,6,7,8$, and none of smaller cardinality.

This is an exact minimality theorem relative to the frozen field dictionary and archive. It is deliberately not called a canonical actual-occurrence representation: the archive contains shadows rather than a theorem-backed actual carrier, and the selected tuple says nothing about active support, parent minimality, or downstream multipliers. Its role is narrower and useful: it gives a lossless address on which future source-backed local occurrence patches can be defined and glued.

<!-- SOURCE_BODY_BEGIN -->

**Keywords:** fixed shift; finite archive; separation key; occurrence provenance; exhaustive certificate.

# The finite addressing question

TPC-153 gives each nonsoft cut path a unique shadow-row identifier `\citep{WangTPC153}`. TPC-163 then proves two facts `\citep{WangTPC163}`: the frozen declared corpus contains no source-locator-admissible actual-occurrence edge, and the projection $$c\longmapsto(\ell(c),k(c),d_{\rm nat}(c))
 \tag{1.1}\label{eq:native-projection}$$ is highly noninjective. The present task is not to infer the missing actual edges. It is to find the smallest already archived coordinate set that retains every distinct cut path.

> **Definition: Frozen rows and field dictionary**<span id="def:fields" label="def:fields">\[def:fields\]</span> Let $\mathcal C$ be the $2988$ distinct production cut paths in the canonical TPC-153 shadow archive. For $c\in\mathcal C$, define $$\begin{aligned}
> \ell(c),k(c),d_{\rm nat}(c)&:
>    &&\text{the exact native triple},\\
> j_L(c),j_K(c)&:
>    &&\text{the exact dyadic block indices},\\
> D_0(c)&:
>    &&\text{the archived prefix boundary},\\
> r(c)&:
>    &&\text{the archived frontier reason},\\
> \tau(c)&:
>    &&\text{\(\mathsf{PREFIX}\) or \(\mathsf{TAIL}\), recomputed from }
>        d_{\rm nat}(c)\le D_0(c).
> \end{aligned}$$ The ordered field dictionary is $$\mathcal F=(\ell,k,d_{\rm nat},j_L,j_K,D_0,r,\tau).
>  \tag{1.2}\label{eq:dictionary}$$ The derived value of $\tau$ must agree with the source-cut path identifier; disagreement invalidates the input.

> **Definition: Separating key**<span id="def:key" label="def:key">\[def:key\]</span> For a nonempty subset $S\subseteq\mathcal F$, let $$\kappa_S(c)=(f(c))_{f\in S},
>  \tag{1.3}\label{eq:projected-key}$$ where fields retain the order in [\[eq:dictionary\]](../main.tex#L128){reference-type="eqref" reference="eq:dictionary"}. We call $S$ *separating* if $\kappa_S$ is injective on $\mathcal C$. A *minimum archived separation key* is a separating subset of minimum cardinality.

This definition is representation-theoretically neutral. It asks only whether two archived cut paths receive the same tuple.

# Exhaustive theorem

> **Theorem: Unique minimum archived key**<span id="thm:minimal-key" label="thm:minimal-key">\[thm:minimal-key\]</span> Among the $255$ nonempty subsets of $\mathcal F$, the unique minimum-cardinality separating subset is $$S_{\min}=(\ell,k,d_{\rm nat},j_L,j_K).
>  \tag{2.1}\label{eq:min-key}$$ Its cardinality is $5$, and $$\#\kappa_{S_{\min}}(\mathcal C)=|\mathcal C|=2988.
>  \tag{2.2}\label{eq:injective}$$ No subset of at most four fields is separating. The complete numbers of separating subsets by cardinality are $$\begin{array}{c|rrrrrrrr}
>  |S|&1&2&3&4&5&6&7&8\\
> \hline
>  \#\{S:\kappa_S\text{ injective}\}&0&0&0&0&1&3&3&1.
> \end{array}
> \tag{2.3}\label{eq:injective-counts}$$

> **Proof** For each of the $2^8-1=255$ nonempty subsets $S$, the certificate constructs the exact tuple $\kappa_S(c)$ for all $c\in\mathcal C$ and stores $$\left(
>    |\kappa_S(\mathcal C)|,\
>    \max_v|\kappa_S^{-1}(v)|,\
>    |\mathcal C|-|\kappa_S(\mathcal C)|
>  \right).
>  \tag{2.4}\label{eq:stats}$$ It marks $S$ separating exactly when the first coordinate equals $2988$. The exhaustive list has no separating entry of size at most four, exactly one of size five, and that entry is [\[eq:min-key\]](../main.tex#L156){reference-type="eqref" reference="eq:min-key"}. Direct grouping gives [\[eq:injective\]](../main.tex#L161){reference-type="eqref" reference="eq:injective"}. Counting the remaining marked entries yields [\[eq:injective-counts\]](../main.tex#L171){reference-type="eqref" reference="eq:injective-counts"}.
>
> The computation is deterministic and integer/string exact. Default mode regenerates the full $255$-entry list; `–check` mode recomputes it and demands byte-identical outputs. The audit also recomputes all upstream canonical path–hash locks. Hence neither floating-point comparison nor random search enters the result.

> **Corollary: Necessity of both dyadic indices**<span id="cor:both" label="cor:both">\[cor:both\]</span> Neither $$(\ell,k,d_{\rm nat},j_L)
>  \quad\text{nor}\quad
>  (\ell,k,d_{\rm nat},j_K)$$ separates the archive.

> **Proof** These are four-field subsets and hence fail by [\[thm:minimal-key\]](../main.tex#L151){reference-type="ref" reference="thm:minimal-key"}. More precisely, their distinct-key counts are $1626$ and $1594$, respectively, and each has maximum multiplicity $2$.

# Quantifying the failed shortcuts

The exhaustive table also measures how much information each natural shortcut loses.

| **Fields**                     |  **Keys**|  **Excess**|  **Max. multiplicity**|
|:-------------------------------|---------:|-----------:|----------------------:|
| $(\ell,k,d_{\rm nat})$         |       866|        2122|                      4|
| $(\ell,k,d_{\rm nat},r)$       |      1068|        1920|                      4|
| $(\ell,k,d_{\rm nat},j_L)$     |      1626|        1362|                      2|
| $(\ell,k,d_{\rm nat},j_K)$     |      1594|        1394|                      2|
| $(\ell,k,d_{\rm nat},j_L,j_K)$ |      2988|           0|                      1|

The frontier reason improves the native triple only slightly. Either dyadic index halves the worst multiplicity, but both are necessary to separate all rows.

> **Proposition: Resolution of the TPC-163 collision**<span id="prop:four" label="prop:four">\[prop:four\]</span> For the four rows with native triple $(3,171,1)$, the key [\[eq:min-key\]](../main.tex#L156){reference-type="eqref" reference="eq:min-key"} takes the four values $$\begin{split}
> (3,171,1,1,7),\quad &(3,171,1,1,8),\\
> (3,171,1,2,7),\quad &(3,171,1,2,8).
> \end{split}$$

> **Proof** These values are read from the four production source-cut paths. The pair $(j_L,j_K)$ runs over $\{1,2\}\times\{7,8\}$, so the values are distinct.

# What “minimal” does and does not mean

There are three notions that must remain separate:

1.  **archive separation:** distinct frozen cut paths have distinct addresses;

2.  **actual occurrence identity:** rows refer to genuine downstream occurrences on an actual carrier;

3.  **canonical/minimal representation:** an independently proved equivalence or optimization principle selects one actual parent representation.

TPC-164 proves only the first. In particular, $\kappa_{\min}$ is not promoted to an occurrence identifier. It may be used as a source address in a later local patch, but such a patch must separately cite the theorem that produces its actual edge.

> **Proposition: Relative nature of minimality**<span id="prop:relative" label="prop:relative">\[prop:relative\]</span> The conclusion of [\[thm:minimal-key\]](../main.tex#L151){reference-type="ref" reference="thm:minimal-key"} is invariant under row ordering but depends on both $\mathcal C$ and $\mathcal F$. Adding a new primitive field or enlarging the production archive requires a new exhaustive certificate.

> **Proof** Injectivity depends only on equality classes of projected tuples, so permuting rows changes nothing. Adding a field creates new subsets not tested here; adding a row may create a collision in [\[eq:injective\]](../main.tex#L161){reference-type="eqref" reference="eq:injective"}. Thus neither enlargement is covered by the frozen theorem.

# Machine certificate and mutation audit

The certificate contains the entire $255$-subset table rather than only the winning tuple. This makes the negative part—no key of size at most four—independently recomputable. The audit performs the following adversarial modifications and runs the same validator:

-   drift an upstream source hash;

-   delete $j_L$ or $j_K$ from the selected key;

-   promote the archived key to an actual-occurrence identifier;

-   promote it to a canonical/minimal representation.

Every mutation is rejected. The last two tests enforce the mathematical boundary rather than merely the byte format.

# Interface to local-to-global construction

The new key supplies a clean domain for a local patch system. If $\{U_i\}$ covers $\mathcal C$, a future source-backed construction may describe local edge families $$\mathcal R_i(c),\qquad c\in U_i,$$ addressed by $\kappa_{\min}(c)$. On overlaps, exact bijections can then be asked to preserve source records, types, and coefficients. That local-to-global question is logically downstream of archive separation and upstream of actual active-support and canonical-minimality certificates.

# Conclusion

The archive-address ambiguity exposed by TPC-163 has an exact repair: retain both dyadic block indices together with the native triple. The repair is optimal among the eight declared archived fields and lossless on all $2988$ production cut paths. Because it is kept strictly at the archive layer, it creates a reliable interface for the next construction without pretending that the missing actual occurrence carrier has already been supplied.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@unpublished{WangTPC153,
  author = {Wang, Liang},
  title  = {A Canonical Cut--Occurrence Shadow Operator},
  note   = {TPC-153 manuscript},
  year   = {2026}
}

@unpublished{WangTPC163,
  author = {Wang, Liang},
  title  = {Source-Locator Census for the {H1} Crosswalk},
  note   = {TPC-163 manuscript},
  year   = {2026}
}
```

<!-- SOURCE_BODY_END -->
