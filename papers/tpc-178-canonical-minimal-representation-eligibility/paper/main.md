# **Eligibility Before Canonicality:**\ **Why an Archive Key Is Not a Physical Representative**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-178-canonical-minimal-representation-eligibility.pdf](../tpc-178-canonical-minimal-representation-eligibility.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-164 proves that the five-field key $(\ell,k,d_{\rm nat},j_L,j_K)$ is the unique smallest key separating 2,988 rows of one frozen cut archive. Its semantics are row addressing. A canonical or minimal physical representation requires an actual eligible carrier, a physical representation space, an equivalence relation, and a proved selector or cost theorem.

TPC-175–177 expose no source-backed eligible carrier. Consequently no physical equivalence class can be formed and no canonicality or minimality test can be run. Zero counterexamples on this empty domain do not prove a positive certificate. The audit is blocked by the empty carrier domain, while the H1 canonical/minimal representation root remains $\textnormal{\textsc{not-testable}}$. This is an $\mathrm{L1}$ interface obstruction, not physical arithmetic or program-positive $\mathrm{L2}$.

<!-- SOURCE_BODY_BEGIN -->

# Three notions that must not be merged

Let $\mathcal A$ be the frozen archive of TPC-164 and $$K_{\rm arc}(r)=(\ell,k,d_{\rm nat},j_L,j_K)                       \tag{1}$$ its minimal separating key. TPC-164 establishes $$K_{\rm arc}(r)=K_{\rm arc}(r')\quad\Longrightarrow\quad r=r'
 \qquad(r,r'\in\mathcal A).                                      \tag{2}$$ This is an exact finite theorem `\cite{WangTPC164}`.

An occurrence identifier would instead identify a production occurrence object across all valid descriptions. A canonical physical representative would select one element from an equivalence class of physical representations. Neither an occurrence space nor its equivalence relation appears in (1)–(2).

> **Proposition: Archive-address firewall** The injectivity and minimal field cardinality of $K_{\rm arc}$ do not imply that it is an occurrence identifier or a canonical/minimal physical representation.

> **Proof** The domain of (2) is $\mathcal A$, a finite set of archived rows. The desired domain is a physical representation space modulo a source-backed equivalence relation. No map between these domains, let alone a selector theorem, is supplied by (2). The implication is therefore absent rather than merely numerically untested.

# A positive representation contract

For an eligible physical carrier $c$, let $\mathcal R(c)$ be its representation space. A positive certificate must source-lock:

1.  a proved eligible actual carrier $c$;

2.  a nonempty physical representation set $\mathcal R(c)$;

3.  an equivalence relation $\sim_c$ preserving the literal physical contribution;

4.  either a selector $s(c)\in\mathcal R(c)$ with a uniqueness theorem, or a cost $J_c$ with an attained minimum;

5.  compatibility with literal coefficient, fixed-$h_0$, and normalization lineage.

For canonicality, one needs $$r\sim_c r'\quad\Longrightarrow\quad s([r])=s([r']).              \tag{3}$$ For minimality, one needs both existence and the claimed strength of $$J_c(r_\star)=\min_{r\in\mathcal R(c)}J_c(r).                     \tag{4}$$ An archive key may help store $r_\star$ after (3) or (4) is proved; it cannot prove them.

# Eligibility audit

TPC-175 supplies an empty source-backed local edge family. TPC-176 therefore has no eligible carrier, and TPC-177 correctly refuses to manufacture one through vacuous active support. Hence $$\mathcal C_{\rm elig}=\varnothing.                               \tag{5}$$

We classify representations only after carrier eligibility. The ledger is therefore $$\begin{array}{c|c}
\text{quantity}&\text{count}\\ \hline
\text{eligible physical carriers}&0\\
\text{physical representation classes formed}&0\\
\text{canonical representatives proved}&0\\
\text{minimal representatives proved}&0\\
\text{noncanonical counterexamples proved}&0 .
\end{array}                                                       \tag{6}$$

> **Theorem: TPC-178 eligibility verdict** The current representation audit has status $$\texttt{ELIGIBILITY\_BLOCKED\_EMPTY\_CARRIER\_DOMAIN}.           \tag{7}$$ It proves neither canonicality nor noncanonicality of a production carrier. The H1 representation root remains $\textnormal{\textsc{not-testable}}$.

> **Proof** By (5), there is no $c$ for which $\mathcal R(c)$, $\sim_c$, (3), or (4) can be instantiated. The zero counterexample count in (6) is vacuous, just as the zero positive count is. The correct classification is ineligibility of the current audit input, not a positive or negative physical theorem.

# What is preserved for a future nonempty family

The audit records the contract above rather than hard-coding the empty result as a permanent decision. If a future source inventory provides a proved carrier, the next audit must reject at least the following shortcuts:

0.96\@lY@ Shortcut & Missing theorem content\
use $K_{\rm arc}$ as a physical selector & no physical representation domain or equivalence relation\
choose the lexicographically first row & no invariance under physical equivalence\
minimize a formal archive cost & no proof that the cost controls the literal physical contribution\
declare uniqueness from hash identity & a hash locks bytes, not mathematical representation semantics\
declare success because no counterexample was tested & empty-domain absence has no existential content\

If canonicality eventually fails on an eligible carrier, the counterexample must be retained and the physical multiplicity or quotient cost quantified before the route is classified.

# Reproducible audit and claim boundary

The standard-library audit source-locks TPC-164, TPC-175, and TPC-177. It verifies the archive key exactly as an `ARCHIVE_ADDRESS`, recomputes (5)–(7), and mutation-tests all role boundaries. It rejects promotion of the archive key, promotion of zero counterexamples to canonicality, a fabricated eligible carrier, and any claim of program-positive $\mathrm{L2}$. Hashes carry integrity semantics only.

The audit consumes no named fixed phase, fixed physical $h_0=2$ arithmetic estimate, literal physical normalization, active support, deterministic endpoint, or endpoint slack. It therefore supplies no strict $1/400$, prime-pair, or twin-prime conclusion.

# Conclusion

Canonicality begins after eligibility, not before it. The only proved finite uniqueness here concerns addresses inside a frozen archive. With no source-backed actual carrier, the physical representation root remains $\textnormal{\textsc{not-testable}}$. TPC-179 integrates this result with the empty local-edge family and active-support vacuity firewall, while keeping the scoped extraction stop distinct from the global architecture status.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC164,
  author       = {Liang Wang},
  title        = {The Minimal Archived Separation Key:
                  Exact Row Addressing without Occurrence Semantics},
  year         = {2026},
  howpublished = {TPC-164 manuscript}
}

@misc{WangTPC166,
  author       = {Liang Wang},
  title        = {A Refined H1 Crosswalk Frontier:
                  Three Independent Production Roots},
  year         = {2026},
  howpublished = {TPC-166 manuscript}
}

@misc{WangTPC175,
  author       = {Liang Wang},
  title        = {The Maximal Source-Backed Local Occurrence Family
                  in the Frozen Production Corpus},
  year         = {2026},
  howpublished = {TPC-175 manuscript}
}

@misc{WangTPC177,
  author       = {Liang Wang},
  title        = {Actual Active Support on an Empty Eligible Family:
                  A Vacuity Firewall for the H1 Carrier Root},
  year         = {2026},
  howpublished = {TPC-177 manuscript}
}
```

<!-- SOURCE_BODY_END -->
