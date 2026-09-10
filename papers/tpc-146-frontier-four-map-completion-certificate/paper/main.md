# **An Executable Four-Map Completion**\ **Certificate for Frontier Totalization**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-146-frontier-four-map-completion-certificate.pdf](../tpc-146-frontier-four-map-completion-certificate.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

We assemble an exact, executable completion criterion for the first unsupported carrier after the TPC cut archive. The map route requires a conservative row-separated occurrence lift, total determinant and zero-mode quotients $Q_D,Q_Z$, a total physical grouping $G$, a total downstream prescribed-shift selector $P_{h_0}$, two compatibility squares, physical cover, exact reconnection and a complete occurrence registry. We encode these requirements by nine row-separated defects. Once the literal source matrices exist, all map-route clauses hold exactly when the defect vector is zero. Unknown components are not assigned the value zero. We retain the alternative allowed by the source-locked program: a theorem proving that the complete original-scale frontier sum is $o(X)$, together with a theorem-backed disposition of every eligible-tail path. The current artifacts satisfy neither disjunct. In particular, the proved cut-stage identity $P_{h_0}^{\rm cut}=I$ is not the missing downstream selector. The resulting verdict remains <span class="smallcaps">not-testable</span>, with the first internal missing node sharpened to $\mathsf{H1.frontier\_occurrence\_lift}$. The stopped result is only the current-schema-only implementation; both an augmented map route and a scalar-plus-eligible-tail route remain open.

<!-- SOURCE_BODY_BEGIN -->

# The disjunctive frontier contract

TPC-141 defines frontier totalization by two legitimate and independent routes `\citep{WangTPC141}`. The first route completes every literal downstream occurrence. The second proves a complete frontier estimate and separately disposes of the remaining eligible tail. We keep this disjunction explicit: $$\begin{split}
\mathsf{H1Complete}(X)
\quad\Longleftrightarrow\quad&
\mathsf{MapTotal}_{\rm ns}(X)\\
&{}\lor\bigl(
\mathsf{ScalarSoft}_{\rm FUM}(X)
\land\mathsf{ETOTotal}(X)\bigr).
\end{split}
\label{eq:disjunction}$$ Here $$\mathsf{ScalarSoft}_{\rm FUM}(X)$$ means a theorem, in the inherited physical normalization, proving $$S_{\rm front}(X)=o(X)$$ for the *complete* original frontier sum. A finite regression, fixed-data logarithmic shadow, or estimate on only one frontier class does not satisfy this clause.

The factor $\mathsf{ETOTotal}(X)$ requires total downstream maps on every eligible-tail-open path, or a separate theorem that makes their complete original-scale sum soft. It cannot be removed because one finite fixture happens to contain no such row.

The map domain is not merely the paths labeled frontier in one sample. Following TPC-136, it is the complete nonsoft set $$\mathcal C_X^{\rm ns}
 =
 \mathcal C_X^{\mathsf{ETO}}
 \sqcup
 \mathcal C_X^{\mathsf{FUM}}.
 \label{eq:domain}$$ The eligible prefix is already separated with a theorem source; the eligible tail and geometric frontier both remain in the downstream archive `\citep{WangTPC136}`.

# The literal map route

TPC-143 identifies the common first input as a conservative row-separated occurrence lift $$L_X:\mathbb C^{\mathcal C_X^{\rm ns}}
 \longrightarrow\mathbb C^{\mathcal O_X}$$ with $$\mathbf 1^TL_X=\mathbf 1^T
 \label{eq:Lconservation}$$ and exact native, shift and normalization lineage `\citep{WangTPC143}`. One cut path may split, so $L_X$ is not replaced by a single target label.

On the completed occurrence space, TPC-144 requires literal determinant and zero-mode maps $$Q_D,\qquad Q_Z$$ and tests their quotient compatibility by a coefficientwise intertwining or, for surjective maps, equality of kernels `\citep{WangTPC144}`. TPC-145 similarly requires a literal physical grouping and downstream selector $$G,\qquad P_{h_0}^{\rm down}$$ whose commuting square passes on the occurrence-resolved lift `\citep{WangTPC145}`.

The remaining physical clauses are:

1.  an exact cover of all physical occurrences, with no deletion or duplication;

2.  exact reconnection to the inherited hard-packet coefficient; and

3.  a complete occurrence registry for every cost used by the physical endpoint.

These are not consequences of the four map names. TPC-124 already shows that physical aggregation can hide a native residual `\citep{WangTPC124}`.

# The zero-defect vector

Let $M_X^{\rm ns}$ be the row-separated TPC-136 nonsoft matrix. On a candidate completed source bundle define: $$\begin{aligned}
D_L&:\ \text{conservation and metadata defect of }L_X,\\
D_{QD}&:\ \text{path-domain defect of }Q_D,\\
D_{QZ}&:\ \text{path-domain defect of }Q_Z,\\
D_G&:\ \text{path-domain defect of }G,\\
D_P&:\ \text{path-domain defect of }P_{h_0}^{\rm down},\\
D_{DZ}&:\ \text{coefficientwise determinant/zero intertwining defect},\\
D_{GP}&:\ \text{occurrence-level grouping/shift commutator},\\
D_{\rm cover}&:\ \text{physical occurrence-cover defect},\\
D_{\rm rec}&:\ \text{final reconnection defect}.\end{aligned}$$ For example, the domain component of a partial map $F$ is the row-separated matrix $$(I-P_{\operatorname{Dom}F})L_XM_X^{\rm ns}.$$ The determinant/zero component includes $$(JQ_D-Q_Z)L_XM_X^{\rm ns},$$ and the grouping/shift component includes $$(P_{\rm phys}G-GP_{\rm occ})L_XM_X^{\rm ns}.$$ The cover and reconnection components use the literal occurrence registry, not only their final scalar sums.

> **Definition: Certified zero** A defect component is a certified zero only when all of its exact source matrices, domains, multipliers, scopes and normalization fields are present and the displayed matrix is identically zero. A missing source is $\textnormal{\textsc{not-testable}}$, not zero.

Put $$\mathfrak D_X=
 (D_L,D_{QD},D_{QZ},D_G,D_P,D_{DZ},D_{GP},
 D_{\rm cover},D_{\rm rec}).
 \label{eq:defectvector}$$

> **Theorem: Four-map completion criterion** <span id="thm:criterion" label="thm:criterion">\[thm:criterion\]</span> Assume all literal source matrices and the complete occurrence registry exist. Then the map-route clauses above hold if and only if $$\boxed{\mathfrak D_X=0}
>  \label{eq:zero}$$ componentwise.

> **Proof** If the map route holds, occurrence-lift conservation gives $D_L=0$; path-totality gives the four domain defects zero; the two declared commuting diagrams give $D_{DZ}=D_{GP}=0$; and exact cover and reconnection give the final two zeros.
>
> Conversely, $D_L=0$ supplies the conservative metadata-faithful lift. Row separation makes each of the next four zero matrix defects equivalent to path-totality, as in TPC-136. The next two zeros are precisely the coefficientwise compatibility requirements. The last two certify complete physical coverage and reconnection. The assumed complete registry then attaches every map edge to one literal occurrence. These are all map-route clauses.

> **Remark: The theorem is executable, not self-populating** turns a complete source bundle into a decidable certificate. It does not create $L_X,Q_D,Q_Z,G$, or $P_{h_0}^{\rm down}$. In particular, no defect can be evaluated from its name.

# Two aggregation firewalls

> **Proposition: Scalar zeros do not certify $\mathfrak D_X=0$** <span id="prop:scalar" label="prop:scalar">\[prop:scalar\]</span> Replacing any row-separated component of $\mathfrak D_X$ by its all-ones row sum can produce a false zero.

> **Proof** Two omitted or leaking occurrence rows with entries $1$ and $-1$ have aggregate scalar zero while the row-separated defect has two nonzero rows. TPC-136 gives this example for domain totality, and TPC-145 gives the corresponding cross-shift example `\citep{WangTPC136,WangTPC145}`. The same construction applies to cover and reconnection occurrences.

> **Proposition: Cut selection does not erase $D_P$** <span id="prop:cutP" label="prop:cutP">\[prop:cutP\]</span> The proved equality $P_{h_0}^{\rm cut}=I$ does not certify $D_P=0$.

> **Proof** $P_{h_0}^{\rm cut}$ acts before the missing occurrence lift and all later physical stages. The defect $D_P$ acts on their source and target records. A later stage can send a selected cut record to an unselected downstream record without changing the earlier identity. Therefore the operators have different domains and proof obligations.

This is the exact distinction required by the prescribed-shift telescope of TPC-125 `\citep{WangTPC125}`.

# Source-locked current evaluation

The deterministic program `experiments/tpc146_frontier_completion_audit.py` imports the TPC-136 cut paths and TPC-143–145 certificates by content hash. Hashes have the status `INTEGRITY_ONLY`; exact record identities are not replaced by digests. It creates the nine components in [\[eq:defectvector\]](../main.tex#L212){reference-type="eqref" reference="eq:defectvector"}.

Every current component is `NOT_EVALUABLE`: its literal source matrix is absent. None is assigned a numerical zero. The scalar branch also has no theorem source. The audit rejects:

-   a frontier-only domain;

-   promotion of the empty finite eligible-tail sample;

-   substitution of $P_{h_0}^{\rm cut}$ for $D_P$;

-   a fabricated source or zero defect;

-   a fabricated scalar-soft theorem; and

-   a false totalization verdict.

The committed finite census is $$\#\mathcal C_X^{\rm ns}=2988,\qquad
 \#\mathcal C_X^{\mathsf{ETO}}=0,\qquad
 \#\mathcal C_X^{\mathsf{FUM}}=2988.$$ This is a regression fixture, not an asymptotic support theorem.

\@P0.34P0.22Y@ Certificate cell & Status & First missing content\
Occurrence lift $L_X$ & $\textnormal{\textsc{not-testable}}$ & Complete row-separated cut-to-occurrence edges.\
$Q_D,Q_Z$ & $\textnormal{\textsc{not-testable}}$ & Canonical parent and ordered outer records.\
$G,P_{h_0}^{\rm down}$ & $\textnormal{\textsc{not-testable}}$ & Physical occurrences and later shift-tagged stages.\
Cover/reconnection/registry & $\textnormal{\textsc{not-testable}}$ & Literal physical occurrence census.\
Frontier scalar $S_{\rm front}=o(X)$ & $\textnormal{\textsc{not-testable}}$ & Independent original-scale theorem.\
Remaining eligible-tail route & $\textnormal{\textsc{not-testable}}$ & Total maps or a complete eligible-tail soft theorem.\

# Verdict and claim boundary

> **Theorem: Current frontier completion verdict** <span id="thm:verdict" label="thm:verdict">\[thm:verdict\]</span> For the source-locked TPC-136 and TPC-143–145 artifacts, $$\boxed{
>  \mathsf{H1.frontier\_totalization}=\textnormal{\textsc{not-testable}},}$$ with $$\boxed{
>  \mathrm{first\ missing}
>  =
>  \mathsf{H1.frontier\_occurrence\_lift}.}$$ The current-schema-only totalization is a scoped $\textnormal{\textsc{stop-declared-route}}$ route. The occurrence-augmented map route and the frontier-scalar-plus-tail route remain $\textnormal{\textsc{open}}$.

> **Proof** The source manifests pass validation, so the snapshot is not invalid. No literal occurrence lift exists, hence the map route in [\[eq:disjunction\]](../main.tex#L91){reference-type="eqref" reference="eq:disjunction"} is $\textnormal{\textsc{not-testable}}$ before its four maps can be tested. No theorem source proves the complete original-scale frontier scalar is $o(X)$, and no source totalizes every possible eligible-tail path, so the second route is also $\textnormal{\textsc{not-testable}}$. Thus neither disjunct passes. TPC-143’s descent obstruction stops only derivation from the current schema; it supplies no witness against an augmented lift or a scalar-plus-tail theorem.

The result sharpens one structural pointer. It does not advance the route to a purely arithmetic frontier. No positive fixed-$h_0$ $\mathrm{L2}$ estimate, frontier $o(X)$ bound, physical cover, determinant/zero exponent pair, endpoint below $1/400$, parity breakthrough, prime-pair lower bound or twin-prime theorem is proved. If a future bundle supplies $L_X$, [\[thm:criterion\]](../main.tex#L216){reference-type="ref" reference="thm:criterion"} specifies the next exact tests without moving any unknown cost to zero.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC123,
  author = {Wang, Liang},
  title  = {A Literal Native-Atom Path Archive},
  year   = {2026},
  note   = {TPC-123 manuscript}
}

@misc{WangTPC124,
  author = {Wang, Liang},
  title  = {Provenance-Faithful Physical Reassembly},
  year   = {2026},
  note   = {TPC-124 manuscript}
}

@misc{WangTPC125,
  author = {Wang, Liang},
  title  = {Prescribed-Shift Intertwining through the Physical Archive},
  year   = {2026},
  note   = {TPC-125 manuscript}
}

@misc{WangTPC131,
  author = {Wang, Liang},
  title  = {End-to-End Endpoint Synthesis on the Literal Fixed-Shift Carrier},
  year   = {2026},
  note   = {TPC-131 manuscript}
}

@misc{WangTPC136,
  author = {Wang, Liang},
  title  = {A Complete Cut Archive at the First Unsupported Carrier},
  year   = {2026},
  note   = {TPC-136 manuscript}
}

@misc{WangTPC141,
  author = {Wang, Liang},
  title  = {Source-Locked Integration at the First Unsupported Carrier},
  year   = {2026},
  note   = {TPC-141 manuscript}
}

@misc{WangTPC142,
  author = {Wang, Liang},
  title  = {TPC-MVP4: A Source-Locked Route Decision after TPC-133--141},
  year   = {2026},
  note   = {TPC-142 manuscript}
}

@misc{WangTPC143,
  author = {Wang, Liang},
  title  = {The Frontier Occurrence-Lift Contract},
  year   = {2026},
  note   = {TPC-143 manuscript}
}

@misc{WangTPC144,
  author = {Wang, Liang},
  title  = {Determinant and Zero-Mode Quotients on a Frontier Lift},
  year   = {2026},
  note   = {TPC-144 manuscript}
}

@misc{WangTPC145,
  author = {Wang, Liang},
  title  = {Occurrence-Resolved Physical Grouping and Prescribed-Shift Commutation},
  year   = {2026},
  note   = {TPC-145 manuscript}
}
```

<!-- SOURCE_BODY_END -->
