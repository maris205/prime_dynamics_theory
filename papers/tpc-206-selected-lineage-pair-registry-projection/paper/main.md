# **A Source-Locked Selected-Lineage\ Pair-Registry Projection**\ Thirteen Fields, the First Missing $D$, and a Corpus-Wide Firewall

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-206-selected-lineage-pair-registry-projection.pdf](../tpc-206-selected-lineage-pair-registry-projection.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

We evaluate the 42-field pair-native registry contract of TPC-205 on one source-locked ordered lineage. Six uniquely selected TPC-133/134/136 records and four typed derivation nodes materialize exactly thirteen fields: $X,h_0,\delta,R,V,D_0,L,K,\alpha,\gamma,j,N_\alpha,N_\gamma$. The first unmaterialized field in contract order is the opened dyadic scale $D$, at index nine. The row divisor $d=1$ does not fill $D$; TPC-133’s truncation $Q=4$ maps to TPC-18’s $R=4$, not to its row scale $Q=LD$; and the native index $k=5$ is distinct from the dyadic scale $K=8$. Hence the explicit selected graph has no 42-field completion. This is a finite $\mathrm{L1}$ selected-lineage obstruction. It is not a corpus-wide maximality theorem, a production occurrence, a structural reopen, an $L2$ estimate, or a prime-pair theorem.

<!-- SOURCE_BODY_BEGIN -->

# Authorization, contract, and theorem scope

The authorized object is the finite theorem

`FINITE_SELECTED_LINEAGE_13_OF_42_PROJECTION_AND_`\
`FIRST_MISSING_D_THEOREM`.

Authorization is workflow input and not theorem evidence. The source snapshot is `42507087b774d9057ba3794468a4790bf93162d5`. TPC-205 separates 42 required fields into four blocks `\citep{WangTPC205}`:

0.92\@l r Y@ Block & Fields & Function\
identity and packet scope & 16 & physical scales, packet ID, source locator\
ordered pair & 10 & rows, targets, mask, coefficient, support and nonzero\
source and child & 12 & polarization, divisor child, inverse and resolved data\
normalization & 4 & source, linear, quadratic and target-return stages\

The pair is ordered; no swap quotient is licensed.

The theorem scope is the explicit graph $$\mathcal G_{103,107}
 =
 \{\text{six selected records}\}
 \cup
 \{\text{four typed derivation nodes}\}.$$ An external record may not be joined merely because it shares a numerical value. Semantic identity and the parent/upstream integrity chain are required. This scope is deliberately smaller than the full reachable Git closure.

# The selected source lineage

The two source rows are selected by the semantic IDs $$\begin{split}
 \alpha &: X=512\mid h_0=2\mid \ell=103\mid k=5\mid d=1,\\
 \gamma &: X=512\mid h_0=2\mid \ell=107\mid k=5\mid d=1.
\end{split}$$ Their unique diagnostic lines are 724 and 736 in the TPC-133 archive `\citep{WangTPC133}`. The corresponding TPC-134 tail paths occur uniquely at lines 2554 and 2602, with $$(j_L,j_K,D_0)=(6,3,0),$$ and the TPC-136 cut records occur at the same diagnostic lines `\citep{WangTPC134,WangTPC136}`. Both cuts are

`FRONTIER_UNMAPPED/NO_TAIL_ROOM`.

The certificate recomputes all six record hashes and the two row-to-path-to-cut parent/upstream chains.

The selected row archive is itself bound to the chosen TPC-133 manifest. The manifest has $X=512,h_0=2,\delta=1/4$; its certificate records 866 rows and pins the complete JSONL hash. Thus $\delta=1/4$ is a *chosen-manifest provenance lift*. It is neither recoverable uniquely from a selected row nor promoted to a cross-scale packet schedule.

# Four typed derivations and three notation firewalls

First, $$Q_{133}
 =\left\lfloor X^{1/2-\delta}\right\rfloor
 =\left\lfloor512^{1/4}\right\rfloor=4.$$ TPC-135 imports this quantity as the TPC-18 truncation parameter $$R_{18}=4$$ `\citep{WangTPC18,WangTPC135}`. This is a role-checked alias, not a same-letter substitution. The TPC-18 row scale remains $$Q_{18}=LD,$$ and is missing because $D$ is missing.

Second, TPC-134’s dyadic definitions give $$L=2^{j_L}=2^6=64,\qquad K=2^{j_K}=2^3=8.$$ Third, the native row relation uses lowercase $k$: $$k=dj,\qquad 5=1\cdot j,\qquad j=5.$$ Consequently, $$N_\alpha(j)=103\cdot1\cdot5+2=517,\qquad
 N_\gamma(j)=107\cdot1\cdot5+2=537.$$ These computations enforce the three firewalls $$Q_{133}\to R_{18}\ne Q_{18},\qquad
 d=1\ne D,\qquad
 k=5\ne K=8.$$

# Selected-graph closure

The ten graph nodes provide fields as follows.

0.96\@l Y@ Node class & Fields contributed to the selected closure\
two row records & $X,h_0,V,\alpha,\gamma$\
two path records & $D_0$\
two cut records & no new registry field; they close the provenance chain\
chosen-manifest node & $\delta=1/4$\
typed truncation node & $R=4$\
dyadic node & $L=64,K=8$\
native-target node & $j=5,N_\alpha=517,N_\gamma=537$\

> **Theorem: Selected-lineage projection and first missing field** <span id="thm:selected" label="thm:selected">\[thm:selected\]</span> The field closure of $\mathcal G_{103,107}$ has exactly thirteen of the 42 TPC-205 fields. In contract order they are $$\begin{gathered}
>  X,h_0,\delta,R,V,D_0,L,K,\\
>  \alpha,\gamma,j,N_\alpha(j),N_\gamma(j).
> \end{gathered}$$ The first missing field is $D$, at one-based index nine. No full 42-field completion exists inside this explicit selected graph.

> **Proof** The six record nodes are uniquely reselected and their integrity edges are recomputed. The four typed nodes apply exactly the derivations above. Taking the union of the fields emitted by these ten nodes gives the displayed list; duplicate row/path values agree exactly. Its cardinality is thirteen. Comparing the union with the fixed 42-field contract places $D$ first among the 29 absent fields. None of the graph’s nodes emits $D$, so no node-closed completion of this selected graph has all 42 fields.

The 29 absent fields split as $$8\ \text{identity/packet}
 +5\ \text{ordered-pair}
 +12\ \text{source/child}
 +4\ \text{normalization}.$$ The first group is $$D,J,Q,T,U_0,G_X^{\rm row}.$$ The remaining two are `packet_id` and `source_locator`. The ordered-pair block still lacks the evaluated joint mask, the full literal pair-coefficient AST, an actual-record relation attachment, formal support, and numeric nonzero status. All child fields and all four normalization stages remain absent. In particular, the archived label `nu_X` is not a scalar normalization.

# Why this is not a corpus-wide maximum

The TPC-32/TPC-93 comparison fixture contributes fourteen contract slots in its own derived $L0$ lineage `\citep{WangTPC32,WangTPC93}`. Its $(\alpha,\gamma,j)$, scales, evidence mode, and source identity differ from $\mathcal G_{103,107}$. It therefore cannot be spliced into the selected graph, but it also prevents any casual reading of thirteen as a global maximum.

> **Proposition: Corpus-wide firewall** TPC-206 proves neither a maximum partial-field count nor a full-join count over the 28-tip reachable Git closure. Both questions have status <span class="nodecor"><span class="smallcaps">not testable</span></span>. A proof would require a complete semantic candidate graph, including JSONL and formula-derived candidates, followed by componentwise field closure.

The frozen archive census contains 34 ref pairs, 28 unique tips, 328 commits, and 12,203 reachable objects. Under a strict RFC-8259 parser, 1,707 dot-JSON blobs parse and 17 files containing non-finite constants are rejected. This census is a reproducible context and reopen-trigger audit. It is not a semantic census of every JSONL or TeX formula and is not used in the proof of [\[thm:selected\]](../main.tex#L178){reference-type="ref" reference="thm:selected"}.

# Route state and machine boundary

The selected graph has no production pair ID, joint source locator, active mask, literal complete coefficient, pair-to-$\omega$ crosswalk, or global normalization return. Therefore:

|                                         |                                             |
|:----------------------------------------|--------------------------------------------:|
| `ACTIVE_PRODUCTION_PAIR_OCCURRENCE`     |  <span class="smallcaps">not testable</span>|
| `CORPUS_WIDE_MAXIMALITY`                |  <span class="smallcaps">not testable</span>|
| `SOURCE_LOCKED_PAIR_TO_OMEGA_CROSSWALK` |                                         FAIL|
| `GLOBAL_NORMALIZATION_RETURN`           |                                         FAIL|
| `H1_E_REPAIR`                           |                                         FAIL|

There is no fixed-atom credit, positive saving exponent, endpoint $1/400$ payment, or positive $L2$ result. The pair-native architecture reroute, both O161 parents, H1 architecture, and the global architecture remain open. Earlier route stops remain scoped; the new cell

`DECLARED_TPC206_SELECTED_103_107_LINEAGE_GRAPH_V1`\
`=STOP_SCOPED`

stops only implicit extension of this selected graph.

The machine release freezes 29 source locks against both the working tree and the source snapshot, rebuilds the ten-node/twelve-edge closure, checks the 42-row field ledger and 29 selected-graph blockers, and runs 76 mutation rows: 12 base, 52 semantic, and 12 strict bool/integer attacks. A checker that imports neither builder nor materializer independently rebuilds the source chains, archive census, selected closure, schemas, firewalls, and strict eleven-artifact manifest. The manifest is a repository review pin, not an external signature or theorem source.

# Conclusion

TPC-206 advances the pair-native route by replacing “zero production records” with a concrete source-locked obstruction on one ordered lineage: thirteen fields are present, $D$ is the first missing field, and all stronger claims remain fenced off. The natural next unnumbered audit is therefore a source-backed opened-$D$ attachment search for this selected lineage. It may create a later numbered paper only if a new theorem-backed edge survives the same type and normalization checks.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC18,
  author       = {Wang, Liang},
  title        = {{M{\"o}bius Tail Determinant Dispersion}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-18-mobius-tail-determinant-dispersion}}
}

@misc{WangTPC32,
  author       = {Wang, Liang},
  title        = {{The Matched Cutoff Frequency Gate}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-32-matched-cutoff-frequency-gate}}
}

@misc{WangTPC93,
  author       = {Wang, Liang},
  title        = {{The Literal Low-Window Affine Export}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-93-literal-low-window-affine-export}}
}

@misc{WangTPC133,
  author       = {Wang, Liang},
  title        = {{The Executable Native Entrance}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-133-executable-native-entrance}}
}

@misc{WangTPC134,
  author       = {Wang, Liang},
  title        = {{A Boundary-Complete Dyadic Prefix--Tail Archive}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-134-boundary-complete-dyadic-prefix-tail-archive}}
}

@misc{WangTPC135,
  author       = {Wang, Liang},
  title        = {{The TPC-17/TPC-18 Block Frontier}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-135-tpc17-tpc18-block-frontier}}
}

@misc{WangTPC136,
  author       = {Wang, Liang},
  title        = {{A Complete Native Cut Archive at the First Unsupported Carrier}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-136-complete-native-cut-archive}}
}

@misc{WangTPC205,
  author       = {Wang, Liang},
  title        = {{Pair-Native Post-TT-star Registry and Architecture-Reroute Interface}},
  year         = {2026},
  howpublished = {\url{https://github.com/maris205/prime_dynamics_theory/tree/main/papers/tpc-205-pair-native-post-ttstar-registry-interface}}
}
```

<!-- SOURCE_BODY_END -->
