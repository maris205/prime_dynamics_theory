# **The Canonical Cut-Occurrence Shadow:**\ **A Maximal Source-Backed Partial Lift**\ **and Its Exact Boundary**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-153-canonical-cut-occurrence-shadow.pdf](../tpc-153-canonical-cut-occurrence-shadow.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The first unsupported object in the source-locked TPC route is a conservative, row-separated lift from every nonsoft cut path to its downstream occurrences. The existing archive does not contain those occurrences. We construct instead the strongest object that is literally determined by the archive: the canonical cut-occurrence shadow $$S_X:\mathbb C^{\mathcal C_X^{\rm ns}}
 \longrightarrow\mathbb C^{\mathcal O_X^{\rm cut}},
 \qquad S_Xe_c=e_{\iota(c)}.$$ There is exactly one shadow row for every eligible-tail-open or frontier-unmapped cut path. Thus $S_X$ is injective, row separated and exactly conservative, $\mathbf1^TS_X=\mathbf1^T$. It preserves the native tuple, prescribed shift, physical normalization, symbolic coefficient and cut multiplier, while keeping canonical-parent, stage, physical-occurrence and active-support fields absent. We prove a conditional pushforward property: every future actual occurrence lift that faithfully extends the cut data must forget to $S_X$. This universal property does not produce such a lift. The deterministic certificate reruns the TPC-143 source chain and contains $2988$ production rows, all frontier-unmapped. A separate eligible-tail fixture is marked synthetic $\mathrm{L0}$ only and never enters the production census. The result is structural $\mathrm{L1}$ progress, not a fixed-shift arithmetic saving.

<!-- SOURCE_BODY_BEGIN -->

# The exact input

The native, dyadic and cut archives of TPC-133–136 enumerate a literal packet through the first unsupported carrier `\citep{WangTPC133,WangTPC134,WangTPC135,WangTPC136}`. Their three terminal types are $$\mathsf{EPS},\qquad \mathsf{ETO},\qquad \mathsf{FUM}.$$ The already soft prefix rows $\mathsf{EPS}$ need no occurrence repair at this gate. The required nonsoft domain is $$\mathcal C_X^{\rm ns}=\mathcal C_X^{\mathsf{ETO}}\sqcup\mathcal C_X^{\mathsf{FUM}}.
 \label{eq:nonsoft-domain}$$ Neither summand may be omitted merely because it is empty in one finite fixture. TPC-143 attaches an explicit lift obligation to every element of $\mathcal C_X^{\rm ns}$, but correctly leaves every actual occurrence edge absent `\citep{WangTPC143}`.

For $c\in\mathcal C_X^{\rm ns}$, let $F_{\rm cut}(c)$ denote precisely the sourced data available at the cut:

1.  the cut, upstream-path and native identities;

2.  $X,h_0,Q,U,V$, the weight-source identifier and physical normalization;

3.  the native tuple $(\ell,k,d_{\rm nat})$;

4.  the native symbolic coefficient, native constraint witnesses and dyadic multiplier expressions; and

5.  the terminal type, block, boundary rule and formal-support status.

The subscript in $d_{\rm nat}$ is deliberate. No existing source identifies this divisor coordinate with a later affine intercept.

> **Definition: Support namespaces** The *formal support envelope* is the enumerated symbolic domain. A *canonical-parent carrier* requires a sourced inverse aggregation. The *actual active support* requires an exact nonzero coefficient certificate. We treat these as three different typed sets.

Every current nonsoft row lies in the first namespace. The other two are not inferred from a symbolic coefficient expression.

# The cut-occurrence shadow

> **Definition: Partial occurrence namespace** For each $c\in\mathcal C_X^{\rm ns}$, define $$\iota(c):=(c,F_{\rm cut}(c))$$ in a new typed namespace, and put $$\mathcal O_X^{\rm cut}:=\{\iota(c):c\in\mathcal C_X^{\rm ns}\}.$$ The identifier of $\iota(c)$ is derived deterministically from the literal cut-path identifier. It is called a *partial occurrence*; it is not an actual downstream occurrence.

> **Definition: Canonical shadow matrix** The cut-occurrence shadow is the linear map $$S_X:\mathbb C^{\mathcal C_X^{\rm ns}}\longrightarrow\mathbb C^{\mathcal O_X^{\rm cut}},
>  \qquad S_Xe_c=e_{\iota(c)}.
>  \label{eq:shadow}$$ Its only nonzero coefficient in column $c$ is the exact rational number $1$.

> **Theorem: Exact shadow identities** <span id="thm:shadow" label="thm:shadow">\[thm:shadow\]</span> The matrix $S_X$ is total on $\mathcal C_X^{\rm ns}$, injective and row separated. Moreover, $$\mathbf 1_{\mathcal O_X^{\rm cut}}^{T}S_X=\mathbf 1_{\mathcal C_X^{\rm ns}}^{T}.
>  \label{eq:shadow-conservation}$$ On every nonzero edge it intertwines the native tuple, source $h_0$, physical normalization, source path and formal-support status.

> **Proof** The rule $c\mapsto\iota(c)$ creates one distinct typed row for each literal source identifier, hence is injective and total. Each column contains one coefficient equal to $1$, proving [\[eq:shadow-conservation\]](../main.tex#L165){reference-type="eqref" reference="eq:shadow-conservation"}. The metadata statement follows because $F_{\rm cut}(c)$ is copied without reinterpretation from the corresponding source obligation.

> **Remark: Why the identity is useful but not the goal** An identity matrix can be trivial algebraically and still useful as a typed boundary object. Here it gives a lossless handoff point: any later construction must explain how one partial row branches into actual rows without changing the sourced column total. It does not explain that branching.

## Exact reconnection with the soft rows

Let $\mathcal N_X$ be the native-record set and write the conservative cut matrix as $$M_X^{\rm cut}=
 \begin{pmatrix}
 M_X^{\mathsf{EPS}}\\ M_X^{\rm ns}
 \end{pmatrix}.$$

> **Proposition: Shadow-level reconnection** <span id="prop:reconnection" label="prop:reconnection">\[prop:reconnection\]</span> The map $I_{\mathsf{EPS}}\oplus S_X$ satisfies $$\mathbf 1_{\mathsf{EPS}}^{T}M_X^{\mathsf{EPS}}
>  +\mathbf 1_{\mathcal O_X^{\rm cut}}^{T}S_XM_X^{\rm ns}
>  =\mathbf 1_{\mathcal N_X}^{T}.
>  \label{eq:reconnection}$$ This is an exact coefficient identity at the cut-shadow level.

> **Proof** Insert [\[eq:shadow-conservation\]](../main.tex#L165){reference-type="eqref" reference="eq:shadow-conservation"} into the cut-column identity $\mathbf 1_{\mathsf{EPS}}^{T}M_X^{\mathsf{EPS}}
> +\mathbf 1_{\mathcal C_X^{\rm ns}}^{T}M_X^{\rm ns}=\mathbf 1_{\mathcal N_X}^{T}$.

neither supplies physical cover nor proves that a symbolic column is nonzero. It only confirms that no cut-level coefficient was deleted by introducing the shadow.

# Universal pushforward property

The word “maximal” below refers to sourced cut fields, not to an unknown actual carrier.

> **Definition: Actual extension candidate** An actual extension candidate consists of a typed row set $\mathcal O_X^{\rm act}$, a row-separated matrix $$L_X:\mathbb C^{\mathcal C_X^{\rm ns}}\longrightarrow\mathbb C^{\mathcal O_X^{\rm act}},$$ and a forgetting map $q:\mathcal O_X^{\rm act}\to\mathcal O_X^{\rm cut}$. The map $q$ must erase only downstream fields and must retain all fields in $F_{\rm cut}$. Its linear pushforward is $$q_*e_o=e_{q(o)}.$$ The candidate lies over the cut shadow when, for all $c,c'\in\mathcal C_X^{\rm ns}$, $$\sum_{\substack{o\in\mathcal O_X^{\rm act}\\q(o)=\iota(c)}}(L_X)_{o,c'}
>  =\delta_{c,c'}.
>  \label{eq:fiber-conservation}$$

> **Theorem: Conditional universal property** <span id="thm:universal" label="thm:universal">\[thm:universal\]</span> Every actual extension candidate lying over the cut shadow satisfies $$q_*L_X=S_X.
>  \label{eq:universal}$$ Conversely, [\[eq:universal\]](../main.tex#L252){reference-type="eqref" reference="eq:universal"} is equivalent to the fiber identities [\[eq:fiber-conservation\]](../main.tex#L243){reference-type="eqref" reference="eq:fiber-conservation"}.

> **Proof** The coefficient of $e_{\iota(c)}$ in $q_*L_Xe_{c'}$ is the left-hand side of [\[eq:fiber-conservation\]](../main.tex#L243){reference-type="eqref" reference="eq:fiber-conservation"}. It equals $\delta_{c,c'}$, which is exactly the coefficient of $e_{\iota(c)}$ in $S_Xe_{c'}$. Reading the same argument backwards proves the converse.

> **Corollary: Conservation inherited from an actual lift** If $q_*L_X=S_X$, then $$\mathbf 1_{\mathcal O_X^{\rm cut}}^{T}q_*L_X=\mathbf 1_{\mathcal C_X^{\rm ns}}^{T}.$$ If, in addition, forgetting preserves the coefficient sum $\mathbf 1_{\mathcal O_X^{\rm cut}}^{T}q_*=\mathbf 1_{\mathcal O_X^{\rm act}}^{T}$, then $\mathbf 1_{\mathcal O_X^{\rm act}}^{T}L_X=\mathbf 1_{\mathcal C_X^{\rm ns}}^{T}$.

The existence of $q,L_X$, the number of rows in each fiber, and all actual edge coefficients remain hypotheses. Therefore [\[thm:universal\]](../main.tex#L248){reference-type="ref" reference="thm:universal"} is a compatibility condition for future work, not a construction of the missing lift.

# What remains deliberately absent

The partial row reserves, but does not populate, the following field groups:

1.  canonical parent, determinant fiber and $Q_D$ edge;

2.  ordered outer zero mode and $Q_Z$ edge;

3.  physical occurrence, physical group, cover and reconnection;

4.  transformation-stage identifier, exact later multiplier, source and target shift tags, and downstream selector edge; and

5.  the affine-corridor consumer fields and endpoint-ledger token.

The TPC-141 occurrence registry names administrative stages, but it does not give a row-level cut-to-stage-to-parent occurrence crosswalk `\citep{WangTPC141}`. It is therefore not used to manufacture these fields.

> **Proposition: No promotion by shadow construction** <span id="prop:no-promotion" label="prop:no-promotion">\[prop:no-promotion\]</span> Constructing $S_X$ proves none of the following:
>
> 1.  existence or uniqueness of an actual occurrence lift;
>
> 2.  actual one-to-many branch multiplicities;
>
> 3.  determinant, zero-mode, physical-group or downstream-shift totality;
>
> 4.  membership in actual active support; or
>
> 5.  an arithmetic estimate for the nonsoft scalar.

> **Proof** All five statements require fields erased by the map from a hypothetical actual extension to $\mathcal O_X^{\rm cut}$. The definition of $S_X$ uses only $F_{\rm cut}$, so none is a consequence of [\[eq:shadow\]](../main.tex#L153){reference-type="eqref" reference="eq:shadow"}.

# Executable finite certificate

The standard-library program

`experiments/tpc153_cut_occurrence_shadow.py`

reruns the TPC-143 generator, compares its logical UTF-8/LF obligations and certificate, and emits one shadow record per source obligation. The lock mode is `CANONICAL_UTF8_LF_V2`; hashes have integrity semantics only.

For the committed production fixture, $$\#\mathcal C_X^{\rm ns}=2988,\qquad
 \#\mathcal C_X^{\mathsf{ETO}}=0,\qquad
 \#\mathcal C_X^{\mathsf{FUM}}=2988.$$ All $2988$ source columns have one shadow row and exact column sum $1$. The validator rejects deletion, duplication, terminal relabeling, nonunit weight, $h_0$ or normalization drift, active support promotion, an invented downstream selector, an invented actual completion, and a false $\mathrm{L2}$ claim.

The production sample cannot exercise the $\mathsf{ETO}$ branch. A separate regression uses the TPC-135 block policy at $$X=2^{84},\quad R=2^{21},\quad V=2^{10},\quad
 (j_L,j_K)=(38,46),\quad D_0=2,$$ for which the policy classifies the block as eligible. This record is marked `SYNTHETIC_L0_ONLY`. It tests that the union [\[eq:nonsoft-domain\]](../main.tex#L99){reference-type="eqref" reference="eq:nonsoft-domain"} remains typed, but proves neither a current production $\mathsf{ETO}$ row nor asymptotic $\mathsf{ETO}$ existence.

\@P0.38P0.23Y@ Export & Status & Exact meaning\
$\mathsf{H1.cut\_occurrence\_shadow}$ & $\textnormal{\textsc{proved}}_{\mathrm{L1}}$ & Exact total conservative partial lift.\
$\mathsf{H1.frontier\_occurrence\_lift}$ & $\textnormal{\textsc{not-testable}}$ & Actual downstream rows and edge coefficients absent.\
Current-schema-only actual-lift derivation & $\textnormal{\textsc{stop-declared-route}}$ & A shadow cannot supply erased provenance.\
Selected augmented occurrence route & Open & A theorem-backed external crosswalk may extend the shadow.\

# Kill criteria and next artifact

The shadow subroute fails immediately if any nonsoft source lacks one partial row, if two source rows share a partial identifier, if a column sum differs from $1$, or if native, $h_0$, normalization or support metadata drift. Conversely, passing these checks must not be promoted to the actual lift.

The next required artifact is a theorem-backed, row-level cut-to-stage-to-parent-to-physical-occurrence crosswalk on every $\mathsf{ETO}$ and $\mathsf{FUM}$ source. It must include exact edge multipliers, native and $h_0$ lineage, physical normalization, support status, cover and reconnection. The source-locked route decision remains $\textnormal{\textsc{not-testable}}$ until that object or the separately typed scalar-plus-$\mathsf{ETO}$ alternative is supplied `\citep{WangTPC152}`.

This paper proves no frontier $o(X)$ estimate, positive fixed-$h_0$ $\mathrm{L2}$ saving, endpoint below $1/400$, prime-pair lower bound or twin-prime theorem.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC133,
  author = {Wang, Liang},
  title  = {An Executable Native Entrance for the TPC-15 Hard Packet},
  year   = {2026},
  note   = {TPC-133 manuscript}
}

@misc{WangTPC134,
  author = {Wang, Liang},
  title  = {A Boundary-Complete Dyadic Prefix--Tail Archive},
  year   = {2026},
  note   = {TPC-134 manuscript}
}

@misc{WangTPC135,
  author = {Wang, Liang},
  title  = {The Geometric Frontier of the TPC-17/18 Block Route},
  year   = {2026},
  note   = {TPC-135 manuscript}
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

@misc{WangTPC143,
  author = {Wang, Liang},
  title  = {The Frontier Occurrence-Lift Contract},
  year   = {2026},
  note   = {TPC-143 manuscript}
}

@misc{WangTPC152,
  author = {Wang, Liang},
  title  = {TPC-MVP5: A Source-Locked Route Decision at the Frontier Occurrence Lift},
  year   = {2026},
  note   = {TPC-152 manuscript}
}
```

<!-- SOURCE_BODY_END -->
