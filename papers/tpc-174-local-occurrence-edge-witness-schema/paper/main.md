# **A Minimal Source-Locked**\ **Local Occurrence-Edge Witness Contract**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-174-local-occurrence-edge-witness-schema.pdf](../tpc-174-local-occurrence-edge-witness-schema.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-173 finds no qualifying local actual-occurrence edge claim in the frozen TPC-133–172 theorem corpus. This does not remove the need for an exact acceptance interface. We define a minimal source-locked local-edge witness. Every edge has the five-field archived cut address, a distinct actual-occurrence identifier, an exact nonzero rational weight, edgewise fixed $h_0=2$, physical-normalization lineage, and source evidence resolving to a qualifying TPC-173 claim. Every declared local cut fibre is nonempty and has exact column sum one.

A deterministic verifier proves finite internal consistency for supplied records. It keeps source-backed local support separate from actual active support and canonical/minimal representation. The committed two-edge fixture has weights $1/3,2/3$ and is explicitly synthetic $\mathrm{L0}$ only. Since TPC-173 has zero qualifying claims, no production witness can currently instantiate the contract. The production status remains not-testable; no arithmetic $\mathrm{L2}$ conclusion is obtained.

<!-- SOURCE_BODY_BEGIN -->

# Source contract

Let $$\kappa(c)=(\ell(c),k(c),d_{\rm nat}(c),j_L(c),j_K(c))
\tag{1}\label{eq:key}$$ be the exact archived address supplied by TPC-164. It identifies a frozen cut row, not a downstream occurrence `\citep{WangTPC165,WangTPC173}`.

> **Definition: Local edge record**<span id="def:edge" label="def:edge">\[def:edge\]</span> A production local edge record contains $$(\kappa(c),o,\lambda,h_0,\nu,\mathcal S),
> \tag{2}\label{eq:edge}$$ where $o$ is an actual-occurrence identifier, $\lambda\in\mathbb Q\setminus\{0\}$, $h_0=2$, $\nu$ is the physical normalization, and $\mathcal S$ is the source bundle. The latter contains a TPC-173 qualifying claim ID, path, canonical hash, theorem locator, formula locator and an exactly matching nonempty derivation AST.

The edge ID is a deterministic digest of the ordered pair $(\kappa(c),o)$. Thus an archive address cannot silently become an occurrence identity.

# Local completeness

> **Definition: Covered local fibre**<span id="def:fibre" label="def:fibre">\[def:fibre\]</span> For a finite nonempty declared cut set $U$, every $c\in U$ has a finite nonempty edge family $E(c)$ satisfying $$\sum_{e\in E(c)}\lambda_e=1.
> \tag{3}\label{eq:conservation}$$ Every edge source lies in $U$, and edge and occurrence identifiers are globally unique inside the witness.

This is the local hypothesis required by the TPC-165 gluing theorem. It is not global coverage, actual active support, or a canonical-parent theorem.

# Finite verifier theorem

> **Theorem: Internal verifier soundness**<span id="thm:soundness" label="thm:soundness">\[thm:soundness\]</span> If the TPC-174 verifier accepts a supplied witness, then:
>
> 1.  all edge and occurrence identifiers are unique;
>
> 2.  every edge belongs to exactly one declared five-field cut address;
>
> 3.  every cut fibre is nonempty and satisfies [\[eq:conservation\]](../main.tex#L88){reference-type="eqref" reference="eq:conservation"} in exact rational arithmetic;
>
> 4.  fixed $h_0=2$ and physical normalization agree edgewise; and
>
> 5.  in production mode, every source record resolves exactly to a qualifying TPC-173 claim, including equality of the derivation AST.

> **Proof** The verifier parses exact integers and reduced fractions, reconstructs the canonical edge ID, and rejects duplicate identities. It groups edges by the ordered address [\[eq:key\]](../main.tex#L59){reference-type="eqref" reference="eq:key"}, checks nonempty coverage and computes each sum in $\mathbb Q$. Equality checks enforce $h_0$, normalization and the full source join. Closed root, edge and source field sets reject undeclared fields, and the complete claim-boundary record is fixed false. These are precisely the asserted finite predicates.

> **Proposition: No provenance or root promotion**<span id="prop:firewall" label="prop:firewall">\[prop:firewall\]</span> Verifier acceptance does not prove the mathematical truth of a cited external theorem, actual active support, canonical/minimal actual representation, or an arithmetic saving.

> **Proof** The verifier checks finite records and their source joins. It contains no proof kernel for the cited theorem, no nonzero physical-coefficient test, no representation theorem and no analytic estimate. These conclusions therefore do not follow.

# Synthetic nonvacuity and production state

The committed fixture declares one address and two distinct typed edge rows: $$\lambda_1=\frac13,\qquad \lambda_2=\frac23.$$ It passes every identity, typing and conservation check. Its evidence mode is `SYNTHETIC_L0_ONLY`; its source locators are deliberately null and its source ID is `SYNTHETIC_AXIOM_L0`. It is not a production claim.

> **Theorem: Current production verdict**<span id="thm:verdict" label="thm:verdict">\[thm:verdict\]</span> For the source-locked TPC-173 inventory, $$\boxed{
>  \#\mathcal Q_{173}=0,\qquad
>  \operatorname{Status}_{\rm production\ witness}=\textnormal{\textsc{not-testable}}.}
> \tag{4}\label{eq:verdict}$$

> **Proof** Production mode requires each edge source to occur in the TPC-173 qualifying-claim map. That map is empty. The synthetic fixture is rejected under production mode, so it cannot change the verdict.

# Claim firewall

The schema and verifier are finite $\mathrm{L0}$ interface results. They do not supply a production local occurrence family or close either parallel H1 root. No named fixed phase, positive fixed-$X$ $\mathrm{L2}$, strict $1/400$, prime-pair lower bound, or twin-prime theorem is established.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@article{WangTPC155,
  author  = {Liang Wang},
  title   = {A Theorem-Backed Occurrence Witness Contract},
  journal = {TPC Research Archive},
  year    = {2026},
  note    = {TPC-155}
}

@article{WangTPC165,
  author  = {Liang Wang},
  title   = {Source-Backed Local-to-Global Gluing for Formal H1 Occurrence Crosswalks},
  journal = {TPC Research Archive},
  year    = {2026},
  note    = {TPC-165}
}

@article{WangTPC173,
  author  = {Liang Wang},
  title   = {Production Source-Claim Inventory},
  journal = {TPC Research Archive},
  year    = {2026},
  note    = {TPC-173}
}
```

<!-- SOURCE_BODY_END -->
