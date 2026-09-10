# **Conservative Completion Fibers:**\ **A Current-Schema Obstruction**\ **to Canonical Occurrence Recovery**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-154-conservative-completion-fiber-obstruction.pdf](../tpc-154-conservative-completion-fiber-obstruction.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-153 constructs a canonical cut-occurrence shadow but leaves the actual one-to-many occurrence lift unresolved. We determine whether the missing lift can nevertheless be recovered uniquely from the current schema. Over each partial occurrence we define the maximal free formal completion class constrained only by row separation, exact rational column conservation and inheritance of the sourced native tuple, source shift, physical normalization and formal-support status. This class contains two explicit global completions. The first has one child of weight $1$ over every source column; the second has two row-separated children of weights $1/2,1/2$. Both push forward to the same canonical shadow, while their per-column branch counts differ. Therefore branch multiplicity, and likewise the populated formal parent, zero-mode, stage and physical labels, do not descend to the current cut schema. This proves an $\mathrm{L0}$ schema nonidentifiability theorem and stops only the route that derives a canonical actual lift from the present artifacts alone. The constructed children are formal models, not occurrences on the unknown actual carrier; consequently the argument proves no actual-carrier impossibility and leaves an augmented theorem-backed route open. A deterministic certificate verifies the obstruction on all $2988$ production fibers and on one separately marked synthetic eligible-tail fiber.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

Let $$S_X:\mathbb C^{\mathcal C_X^{\rm ns}}\longrightarrow\mathbb C^{\mathcal O_X^{\rm cut}},
 \qquad S_Xe_c=e_{\iota(c)}$$ be the exact conservative cut-occurrence shadow of TPC-153 `\citep{WangTPC153}`. Its target row $\iota(c)$ stores every cut-sourced field and none of the unarchived downstream fields. TPC-143 showed that those downstream labels do not descend from the current cut records `\citep{WangTPC143}`. The present question is stronger and matrix-valued:

> Does the current schema determine how many row-separated occurrence children lie above each $\iota(c)$, their coefficients, and their downstream provenance?

We answer “no” relative to a precisely declared formal completion class. This is a statement about information contained in the present artifacts. It is not a statement that the mathematical actual carrier has two completions, or that no future theorem can identify one.

# The free conservative completion class

> **Definition: Formal completion over one shadow row** For $u=\iota(c)\in\mathcal O_X^{\rm cut}$, a finite formal completion is a nonempty row set $E_u$ with exact coefficients $\lambda_{e,u}\in\mathbb Q$ satisfying $$\sum_{e\in E_u}\lambda_{e,u}=1.
>  \label{eq:column}$$ Every $e\in E_u$ has its own row identifier and echoes the native tuple, source $h_0$, physical normalization and formal-support role of $u$. Fields absent from the cut schema may be populated with typed `FORMAL_ONLY` annotations. Such annotations carry no actual-provenance semantics.

> **Definition: Global free completion** A global formal completion is the disjoint union $$E=\bigsqcup_{u\in\mathcal O_X^{\rm cut}}E_u$$ and the matrix $$K:\mathbb C^{\mathcal O_X^{\rm cut}}\longrightarrow\mathbb C^E,
>  \qquad
>  Ke_u=\sum_{e\in E_u}\lambda_{e,u}e_e.$$ Let $q:E\to\mathcal O_X^{\rm cut}$ send every child in $E_u$ back to $u$, and extend it linearly by $q_*e_e=e_{q(e)}$. The class $\mathfrak F_{\rm free}(S_X)$ consists of all such completions.

> **Proposition: Exact forgetting identity** <span id="prop:forget" label="prop:forget">\[prop:forget\]</span> Every $K\in\mathfrak F_{\rm free}(S_X)$ satisfies $$q_*K=I_{\mathcal O_X^{\rm cut}},\qquad
>  q_*KS_X=S_X,\qquad
>  \mathbf 1_E^TK=\mathbf 1_{\mathcal O_X^{\rm cut}}^T.$$

> **Proof** For a basis vector $e_u$, $$q_*Ke_u
>  =\sum_{e\in E_u}\lambda_{e,u}e_u=e_u$$ by [\[eq:column\]](../main.tex#L113){reference-type="eqref" reference="eq:column"}. This proves the first two identities. Taking the sum of each matrix column proves the third.

The class is “maximal free” only in the following controlled sense: it imposes the identities literally visible at the cut-shadow interface and does not add an unarchived actual-support, canonical parent, stage or physical reconstruction theorem.

# Two inequivalent completions

> **Definition: Completion A** For every $u\in\mathcal O_X^{\rm cut}$, let $$E_u^A=\{e_u^A\},\qquad \lambda_{e_u^A,u}=1.$$ Denote the resulting global matrix by $K_A$.

> **Definition: Completion B** For every $u\in\mathcal O_X^{\rm cut}$, let $$E_u^B=\{e_{u,0}^B,e_{u,1}^B\},\qquad
>  \lambda_{e_{u,0}^B,u}
>  =\lambda_{e_{u,1}^B,u}=\frac12.$$ Denote the resulting global matrix by $K_B$.

Both completions populate typed formal values for the canonical parent and determinant edge, outer zero mode, physical group, reconstruction multiplier, transformation stage, source and target shift, affine consumer and endpoint token. Their field values are deterministic test tokens. They are not imported from TPC-136 and are never labeled theorem-backed.

> **Definition: Row-separated equivalence** Two completions over the same $\mathcal O_X^{\rm cut}$ are equivalent if there is a bijection between their row sets that preserves the forgetting target and every nonzero matrix coefficient. In particular, the number $$b_K(u):=\#\{e:q(e)=u,\ K_{e,u}\ne0\}$$ is an equivalence invariant.

> **Theorem: Completion-fiber nonuniqueness** <span id="thm:nonunique" label="thm:nonunique">\[thm:nonunique\]</span> The matrices $K_A,K_B$ both lie in $\mathfrak F_{\rm free}(S_X)$, and $$q_{A*}K_AS_X=q_{B*}K_BS_X=S_X.$$ They are not row-separated equivalent.

> **Proof** Their column sums are respectively $1$ and $\frac12+\frac12=1$, so [\[prop:forget\]](../main.tex#L139){reference-type="ref" reference="prop:forget"} applies. For every $u\in\mathcal O_X^{\rm cut}$, $$b_{K_A}(u)=1,\qquad b_{K_B}(u)=2.$$ Because $b_K(u)$ is preserved by every permitted row bijection, no equivalence can exist.

The use of positive rational weights makes the obstruction especially elementary. It does not depend on cancellation between different source columns, floating-point tolerance or signed reconstruction.

# What is and is not identifiable

Let $\mathfrak C(u)$ be the fiber of all free formal completions over one shadow row. A quantity $a$ is *identified by the shadow* only if it is constant on $\mathfrak C(u)$ for every $u$.

> **Corollary: Branch count does not descend** <span id="cor:branch" label="cor:branch">\[cor:branch\]</span> The row-separated branch count $b_K(u)$ is not identified by the current shadow schema.

> **Proof** gives values $1$ and $2$ in the same forgetting fiber.

> **Proposition: Downstream provenance does not descend** <span id="prop:labels" label="prop:labels">\[prop:labels\]</span> Within the declared free class, none of the following is determined by the shadow alone:
>
> 1.  a canonical-parent key or determinant-bin edge;
>
> 2.  an ordered zero-mode key or $Q_Z$ edge;
>
> 3.  a physical occurrence, physical group, cover or reconnection destination;
>
> 4.  a transformation-stage identifier, target shift or proof of shift preservation; and
>
> 5.  an affine-intercept crosswalk or endpoint-ledger token.

> **Proof** The construction assigns different typed formal annotations to the children of $K_A$ and $K_B$ while their pushforwards are equal. Each listed label therefore varies on a forgetting fiber. The standard fiber-constancy criterion rules out descent.

The native divisor coordinate $d_{\rm nat}$ is stored separately from the formal affine intercept $d_{\rm aff}$. Every test record sets their crosswalk status to `NOT_SOURCED`. Equality of the two symbols is not inferred from notation.

## The exact negative theorem

> **Theorem: Current-artifacts-only recovery obstruction** <span id="thm:obstruction" label="thm:obstruction">\[thm:obstruction\]</span> No rule whose output is required to be an invariant determined by the current cut-shadow data can recover the row-separated branch multiplicity, or the labels in [\[prop:labels\]](../main.tex#L244){reference-type="ref" reference="prop:labels"}, of an unknown actual occurrence lift. Accordingly, $$\boxed{
>  \mathsf{current\ artifacts\ only\ canonical\ actual\ lift}
>  =\textnormal{\textsc{stop-declared-route}}.}$$

> **Proof** Any invariant determined by the shadow must take the same value on all formal completions with that shadow. This contradicts \[[cor:branch](../main.tex#L233),[prop:labels](../main.tex#L244)\]. Thus the current data do not identify the requested output.

> **Remark: Arbitrary choice is not recovery** One can define a set-theoretic rule that always chooses Completion A. Such a convention is not a theorem-backed recovery of the actual lift: the current data contain no proposition making that choice correct.

# Why this does not prove impossibility

The formal class deliberately omits unknown actual-carrier constraints. A future theorem may restrict it to a smaller class, possibly a singleton. We have not proved that $K_A$ or $K_B$ lies on the actual arithmetic carrier, and we have not constructed two actual lifts.

> **Proposition: Scoped character of the obstruction** <span id="prop:scope" label="prop:scope">\[prop:scope\]</span> does not imply:
>
> 1.  nonexistence or nonuniqueness of the actual occurrence lift;
>
> 2.  failure of determinant–zero quotient compatibility;
>
> 3.  failure of physical grouping or fixed-shift commutation; or
>
> 4.  impossibility of an augmented theorem-backed construction.

> **Proof** Each assertion quantifies over the actual carrier or over extra downstream maps. The proof of [\[thm:obstruction\]](../main.tex#L273){reference-type="ref" reference="thm:obstruction"} quantifies only over the maximal current-schema free class. The quantifier domains are different.

This distinction is consistent with the compatibility and commutation contracts in TPC-144–146 `\citep{WangTPC144,WangTPC145,WangTPC146}`. Those contracts become evaluable only after literal source edges are supplied; formal labels cannot make their defect vectors zero.

# Executable certificate

The standard-library program

`experiments/tpc154_completion_fiber_obstruction.py`

reruns and source-locks TPC-153 under `CANONICAL_UTF8_LF_V2`. It emits one completion-fiber record for every partial production occurrence. For the committed archive it verifies $$\begin{array}{c|c|c}
 \text{fiber scope}&\#\text{fibers}&
       (\#K_A\text{ edges},\#K_B\text{ edges})\\ \hline
 \text{production FUM}&2988&(2988,5976)\\
 \text{synthetic L0 ETO}&1&(1,2).
 \end{array}$$ Every column of each completion sums exactly to $1$ in $\mathbb Q$, and every row-separated edge identifier is globally unique. The synthetic ETO fiber remains outside the production census.

Each edge contains the source native tuple, source $h_0$, physical normalization and formal-support role, together with typed formal parent, zero-mode, physical, stage, multiplier and affine-consumer fields. The validator rejects source deletion or duplication, synthetic-ETO omission, a cross-fiber edge, nonconservative weights, native/$h_0$/normalization drift, missing parent or stage data, active-support or actual-provenance promotion, an assumed $d_{\rm nat}=d_{\rm aff}$ crosswalk, canonical-choice promotion and a false $\mathrm{L2}$ claim.

\@P0.38P0.22Y@ Export & Status & Meaning\
Formal completion-fiber nonuniqueness & $\textnormal{\textsc{proved}}_{\mathrm{L0}}$ schema & Two conservative formal completions share the same pushforward and differ in branch count.\
Current-artifacts-only canonical actual lift & $\textnormal{\textsc{stop-declared-route}}$ & Current data cannot identify the actual completion.\
Augmented actual occurrence lift & $\textnormal{\textsc{not-testable}}$ & Required sourced crosswalk has not been supplied.\
Selected augmented route & Open & Not stopped by the formal nonuniqueness theorem.\

# Kill criteria and next object

The obstruction certificate fails if either completion loses exact column conservation, if the two alternatives no longer share a forgetting target, if their branch-count invariant agrees, or if any production fiber is omitted. Its scoped stop ceases to be the relevant route decision once a theorem-backed augmentation supplies and verifies the missing provenance; the formal free class must then be replaced by the smaller sourced class.

The first missing object remains a row-level cut-to-stage-to-parent-to-physical-occurrence crosswalk over every eligible-tail-open and frontier-unmapped source. It must include exact edge coefficients, all inherited fields, target shift and support status, plus cover and reconnection evidence. A verifier can certify a supplied witness, but neither TPC-153 nor the present paper can invent it.

This paper proves no actual active-support theorem, frontier $o(X)$ estimate, positive fixed-$h_0$ $\mathrm{L2}$ saving, endpoint below $1/400$, prime-pair lower bound or twin-prime theorem.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC136,
  author = {Wang, Liang},
  title  = {A Complete Cut Archive at the First Unsupported Carrier},
  year   = {2026},
  note   = {TPC-136 manuscript}
}

@misc{WangTPC143,
  author = {Wang, Liang},
  title  = {The Frontier Occurrence-Lift Contract},
  year   = {2026},
  note   = {TPC-143 manuscript}
}

@misc{WangTPC144,
  author = {Wang, Liang},
  title  = {Determinant--Zero Quotient Compatibility},
  year   = {2026},
  note   = {TPC-144 manuscript}
}

@misc{WangTPC145,
  author = {Wang, Liang},
  title  = {Physical Grouping and Fixed-Shift Commutation},
  year   = {2026},
  note   = {TPC-145 manuscript}
}

@misc{WangTPC146,
  author = {Wang, Liang},
  title  = {A Frontier Four-Map Completion Certificate},
  year   = {2026},
  note   = {TPC-146 manuscript}
}

@misc{WangTPC153,
  author = {Wang, Liang},
  title  = {The Canonical Cut-Occurrence Shadow},
  year   = {2026},
  note   = {TPC-153 manuscript}
}
```

<!-- SOURCE_BODY_END -->
