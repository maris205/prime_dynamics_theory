# **The Frontier Occurrence-Lift Contract:**\ **Field Descent, Lineage Completeness,**\ **and Schema Nonidentifiability**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-143-frontier-occurrence-lift-contract.pdf](../tpc-143-frontier-occurrence-lift-contract.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

The complete TPC cut archive reaches every eligible-tail and frontier path but does not yet reach the canonical determinant, ordered zero-mode, or physical occurrence archives. We identify the common missing object: a conservative row-separated occurrence lift $$L_X:\mathbb C^{\mathcal C_X^{\rm ns}}\longrightarrow
 \mathbb C^{\mathcal O_X}.$$ One cut path may have several downstream occurrences, so this object is a sparse matrix rather than a single-valued label map. We prove a field-descent criterion: a downstream label is determined by the current cut schema precisely when it is constant on every fiber of the forgetful completion map. The inherited cut-stage selector is therefore exactly $P_{h_0}^{\rm cut}=I$, but determinant bins, zero-mode order, physical groups, and the downstream shift selector do not descend from the current fields. This is a scoped nonidentifiability theorem for the present archive, not an impossibility result for an augmented construction. A deterministic audit binds every nonsoft cut path to an explicit lift obligation. The committed finite sample has $2988$ frontier paths and no eligible-tail path; that finite emptiness is not promoted to asymptotic totality. The new result is structural $\mathrm{L0}/\mathrm{L1}$ progress and supplies no positive fixed-shift arithmetic saving.

<!-- SOURCE_BODY_BEGIN -->

# The exact point reached by the cut archive

Fix the literal hard-packet scope $$\mathfrak s=(X,h_0,Q,U,V,W_{\rm id},\nu_{\rm phys})$$ and a native tuple $(\ell,k,d)$. TPC-133 enumerates every tuple in its certified support envelope; TPC-134 expands it into exact dyadic paths; and TPC-135–136 assign one of the terminal types $$\mathsf{EPS},\qquad \mathsf{ETO},\qquad \mathsf{FUM}$$ without deleting a path `\citep{WangTPC133,WangTPC134,WangTPC135,WangTPC136}`. They stand for eligible-prefix-soft, eligible-tail-open and frontier-unmapped. Put $$\mathcal C_X^{\rm ns}=\mathcal C_X^{\mathsf{ETO}}\sqcup
       \mathcal C_X^{\mathsf{FUM}}.$$ This is the required domain for every downstream map in TPC-136. Calling only the $\mathsf{FUM}$ rows “the domain” would silently delete the eligible tail.

The cut record stores its exact path identifiers, packet scope, native tuple, dyadic block, cutoff $D_0$, terminal reason, multiplier expression, $h_0$, and physical normalization. Joining on the exact scope and tuple recovers the TPC-133 coefficient expression. A SHA-256 value checks file integrity; it is not the mathematical identity.

> **Definition: Three support roles** The *formal support envelope* is the enumerated domain on which the symbolic packet is defined. A *canonical parent carrier* is obtained only after a theorem-backed inverse aggregation. The *actual active support* consists of the resulting records whose literal coefficients are certified nonzero. These roles are different typed sets.

The current cut archive is an envelope archive. A symbolic factor such as $r_Q(\ell k+h_0)$ may vanish. Conversely, an unevaluated coefficient is not an exact-zero certificate. We therefore retain every formal nonsoft path when testing map totality.

# The missing occurrence lift

> **Definition: Fully typed downstream occurrence** A downstream occurrence $o\in\mathcal O_X$ contains:
>
> 1.  an occurrence identifier, source and target record identifiers, stage identifier, and exact edge multiplier;
>
> 2.  the exact cut-path, native-tuple and packet-scope lineage;
>
> 3.  source and target shift tags and one inherited physical normalization;
>
> 4.  all content, mask, polarization, boundary and collision tags;
>
> 5.  canonical-parent, determinant-fiber and zero-mode fields when the corresponding maps are invoked; and
>
> 6.  physical group, cover, reconstruction and occurrence-registry fields when physical reassembly is invoked.

> **Definition: Occurrence lift** An occurrence lift is an exact sparse matrix $$L_X:\mathbb C^{\mathcal C_X^{\rm ns}}\longrightarrow\mathbb C^{\mathcal O_X}.$$ It is *row separated*: separate transformation paths remain separate rows even if they end at the same mathematical occurrence. It is *conservative* when $$\mathbf 1_{\mathcal O_X}^{T}L_X=\mathbf 1_{\mathcal C_X^{\rm ns}}^{T}.
>  \label{eq:conservation}$$ It is metadata-faithful when it intertwines the native tuple, $h_0$, and $\nu_{\rm phys}$ on every nonzero edge.

One cut path can split under polarization, content or physical reconstruction. Hence $L_X$ is not assumed to be a function. Its column sum can be one even when its individual entries are signed or complex. Equation [\[eq:conservation\]](../main.tex#L153){reference-type="eqref" reference="eq:conservation"} is a coefficientwise identity, not a bound on the associated arithmetic scalar.

> **Proposition: Exact extension of cut reconnection** <span id="prop:reconnection" label="prop:reconnection">\[prop:reconnection\]</span> Let $\mathcal N_X$ be the native-record set and let $M_X^{\rm cut}$ be the conservative TPC-136 cut matrix. After ordering its rows by terminal type, write $$M_X^{\rm cut}
>  =
>  \begin{pmatrix}
>   M_X^{\mathsf{EPS}}\\
>   M_X^{\rm ns}
>  \end{pmatrix},
>  \qquad
>  M_X^{\rm ns}:\mathbb C^{\mathcal N_X}\longrightarrow
>  \mathbb C^{\mathcal C_X^{\rm ns}}.$$ If [\[eq:conservation\]](../main.tex#L153){reference-type="eqref" reference="eq:conservation"} holds, then $$\mathbf 1_{\mathsf{EPS}}^TM_X^{\mathsf{EPS}}
>  +\mathbf 1_{\mathcal O_X}^TL_XM_X^{\rm ns}
>  =\mathbf 1_{\mathcal N_X}^T.
>  \label{eq:extended-reconnection}$$ Equivalently, adjoining the identity on the already soft rows gives $\widehat L_X=I_{\mathsf{EPS}}\oplus L_X$ and $\mathbf 1^T\widehat L_XM_X^{\rm cut}=\mathbf 1^T$. Thus the extended archive reconnects every native coefficient exactly. This conclusion neither identifies a physical occurrence nor estimates any nonsoft sum.

> **Proof** Multiply $\mathbf 1_{\mathcal O_X}^TL_X=\mathbf 1_{\mathcal C_X^{\rm ns}}^T$ by $M_X^{\rm ns}$, add the unchanged $\mathsf{EPS}$ contribution, and use the full TPC-136 column identity $\mathbf 1_{\mathsf{EPS}}^TM_X^{\mathsf{EPS}}
> +\mathbf 1_{\mathcal C_X^{\rm ns}}^TM_X^{\rm ns}=\mathbf 1_{\mathcal N_X}^T$.

# Field descent and nonidentifiability

Let $\widetilde{\mathcal O_X}_{\rm schema}$ be the maximal formal completion class constrained only by the fields and algebraic identities explicitly archived in the present contracts. In particular, it does not silently impose an unarchived actual-support condition. We include at least one formal completion above every cut row, and let $$\pi:\widetilde{\mathcal O_X}_{\rm schema}\longrightarrow\mathcal C_X^{\rm ns}$$ be the resulting surjective map that forgets every field absent from the current schema.

> **Theorem: Field-descent criterion** <span id="thm:descent" label="thm:descent">\[thm:descent\]</span> For a set $Y$ and a downstream label $\lambda:\widetilde{\mathcal O_X}_{\rm schema}\to Y$, the following are equivalent:
>
> 1.  there exists a label $\bar\lambda:\mathcal C_X^{\rm ns}\to Y$ satisfying $\lambda=\bar\lambda\circ\pi$;
>
> 2.  $\lambda$ is constant on every fiber $\pi^{-1}(c)$.
>
> The descended label $\bar\lambda$ is unique.

> **Proof** If $\lambda=\bar\lambda\circ\pi$, equal images under $\pi$ have equal $\lambda$-values. Conversely, define $\bar\lambda(c)=\lambda(o)$ for any $o\in\pi^{-1}(c)$. Fiber constancy makes the definition independent of the choice. Surjectivity gives both existence on all cut records and uniqueness.

> **Proposition: Schema-completion labels do not descend** <span id="prop:nondescend" label="prop:nondescend">\[prop:nondescend\]</span> On $\widetilde{\mathcal O_X}_{\rm schema}$, none of the literal determinant-bin label, canonical zero-mode record, physical group, or downstream shift lineage descends through $\pi$.

> **Proof** The cut schema contains no crosswalk to the canonical parent $t=(\alpha,\gamma,j)$ of TPC-95. For example, with the same forgotten cut record and $h_0=2,j=1$, two completion records may use slopes $$(m_\alpha,m_\gamma)=(3,1)
>  \quad\hbox{or}\quad(5,1).$$ Their target pairs are $(5,3)$ and $(7,3)$, and their normalized determinants are $2$ and $4$, respectively. Both values satisfy the displayed canonical integer formula, while the current cut fields distinguish neither completion.
>
> Likewise the present schema does not constrain an outer affine key, its ordered coordinate, a physical group identifier, or a later stage target shift. Two completion records can agree after forgetting those fields and disagree on any one of them. Each label therefore fails the fiber-constancy condition of [\[thm:descent\]](../main.tex#L218){reference-type="ref" reference="thm:descent"}. This proves nonidentifiability relative to the current schema-completion class. It is not a mathematical impossibility statement on the unknown actual carrier: proving that stronger statement would require two completions satisfying every actual-support constraint. A future theorem-backed $L_X$ can restrict the completion class and resolve the present ambiguity.

> **Remark: Why this is a scoped stop** stops the implementation that derives the four downstream maps from the present JSON labels alone. It does not stop a new analytic or algebraic construction of $L_X$, and it does not show that the complete frontier scalar is large.

# What the cut shift field does prove

Let $P_{h_0}^{\rm cut}$ be the coordinate selector on cut rows whose stored shift is the prescribed $h_0$.

> **Theorem: Exact cut-stage selector** <span id="thm:cutselector" label="thm:cutselector">\[thm:cutselector\]</span> On the complete TPC-136 cut archive, $$\boxed{P_{h_0}^{\rm cut}=I.}$$ This is a literal $\mathrm{L1}$ statement. It is not the downstream selector of TPC-125.

> **Proof** TPC-136 proves metadata intertwining for $h_0$ from every native column to every nonzero cut edge. The native packet is fixed at one prescribed $h_0$, so every cut row is selected.

A downstream selector requires shift tags on the source and target of every later stage and an exact proof that those stages intertwine the selectors `\citep{WangTPC123,WangTPC125}`. Copying $h_0$ into the cut metadata cannot certify a stage that has not been archived.

# Executable field obligations

The standard-library program `experiments/tpc143_frontier_lift_audit.py` joins every TPC-136 nonsoft path to TPC-133 by exact packet scope and native tuple. It emits one obligation record per path. Downstream fields are recorded as `REQUIRED_MISSING`; no placeholder label is inserted.

Before forming that join, the program independently reruns the TPC-133–136 deterministic generators and compares their logical UTF-8 text under the canonical LF convention. The older certificates bind some Windows CRLF byte serializations, so their raw hashes are reported explicitly as `LEGACY_RAW_HASH_STALE`; they are not silently accepted as current hashes. The new `CANONICAL_UTF8_LF_V2` lock passes only after the generated atoms, paths, frontier manifest, cut paths, downstream-map manifest, and all certificate fields other than those diagnosed EOL-only locks agree.

For future affine-correlation consumers, each occurrence contract also reserves typed fields for the two affine forms, determinant, coefficient height, residue class, ordered interval, periodic weight, coprimality/squarefree/content/prefix masks, coefficient $\ell^1$-mass, window identifier and endpoint-ledger token. These are obligations, not values inferred from the cut tuple.

The committed regression has $$\#\mathcal C_X^{\rm ns}=2988,\qquad
 \#\mathcal C_X^{\mathsf{ETO}}=0,\qquad
 \#\mathcal C_X^{\mathsf{FUM}}=2988.$$ This census describes one finite sample at $X=512$. Since the theoretical domain is the union $\mathsf{ETO}\sqcup\mathsf{FUM}$, the empty sample $\mathsf{ETO}$ set is never accepted as proof that the eligible tail is absent at growing scales.

\@P0.38P0.22Y@ Node & Status & Meaning\
$\mathsf{H1.cut\_shift\_selector}$ & $\textnormal{\textsc{proved}}_{\mathrm{L1}}$ & $P_{h_0}^{\rm cut}=I$.\
$\mathsf{H1.frontier\_occurrence\_lift}$ & $\textnormal{\textsc{not-testable}}$ & No conservative cut-to-occurrence matrix is archived.\
$Q_D,Q_Z,G,P_{h_0}^{\rm down}$ & $\textnormal{\textsc{not-testable}}$ & Their literal source fields and map edges are absent.\
Current-schema-only derivation & $\textnormal{\textsc{stop-declared-route}}$ & Stopped only by the scoped descent obstruction.\

The audit rejects a missing or duplicated path, a source-terminal relabeling, a frontier-only domain, a downstream-field promotion, a false arithmetic-nonzero or $\mathrm{L2}$ promotion, a fabricated occurrence edge, and promotion of $P_{h_0}^{\rm cut}$ to a downstream map. Default mode writes deterministic artifacts; `–check` is read-only.

# Claim boundary and next object

> **Theorem: Audited occurrence-lift verdict** <span id="thm:verdict" label="thm:verdict">\[thm:verdict\]</span> For the current TPC-133–136 source artifacts, $$\boxed{
>  \mathsf{H1.frontier\_occurrence\_lift}=\textnormal{\textsc{not-testable}}.}$$ The current schema alone cannot certify the four downstream labels, while the selected occurrence-augmented route remains open.

This paper proves no frontier $o(X)$ estimate, actual-carrier support theorem, determinant or zero-mode exponent, physical cover, downstream localization bound, endpoint below $1/400$, parity advance, prime-pair lower bound, or twin-prime theorem. Its positive content is an exact cut-stage selector and a necessary and sufficient field-descent test. The first object to build is the row-separated matrix $L_X$, not a collection of labels detached from their occurrence lineage.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC95,
  author = {Wang, Liang},
  title  = {Shared-Target Rigidity, Dominance Energy, and the Exact Native Census},
  year   = {2026},
  note   = {TPC-95 manuscript}
}

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

@misc{WangTPC142,
  author = {Wang, Liang},
  title  = {TPC-MVP4: A Source-Locked Route Decision after TPC-133--141},
  year   = {2026},
  note   = {TPC-142 manuscript}
}
```

<!-- SOURCE_BODY_END -->
