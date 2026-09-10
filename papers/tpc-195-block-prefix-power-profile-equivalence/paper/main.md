# **Block and Cumulative Prefix Power Profiles: Exact Constants and the Truncation Tail**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-195-block-prefix-power-profile-equivalence.pdf](../tpc-195-block-prefix-power-profile-equivalence.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; Huazhong University of Science and Technology
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

All-scale dyadic block bounds and cumulative prefix bounds transfer in both directions with explicit sigma-dependent constants. If small blocks are unavailable, the leftover tail is a real loss and cannot be suppressed by notation. The classification is `DETERMINISTIC_REDUCTION_L1` and the verdict is `PROVED_BIDIRECTIONAL_POWER_PROFILE_TRANSFER`. No program-positive L2 claim or endpoint exponent credit is made.

<!-- SOURCE_BODY_BEGIN -->

# Target contract and source boundary

The target has six simultaneous axes: actual fixed-$h_0$ packet, source-locked named physical atom, every deterministic prefix, every deterministic scale, a fixed-$X$ power at that atom, and actual active support. The value $h_0=2$ is source-backed data only. Repository hashes are integrity locks, not theorem evidence. TPC-193’s declared seven-source corpus remains <span class="smallcaps">stop-scoped</span> `\citep{WangTPC193}`.

# Abstract sequence theorem

Let $0<\sigma<1$, $q>0$, and $A(T)=\sum_{1\le n\le T}a_n$. Write $\Delta(N)=A(2N)-A(N)$, with real endpoints interpreted by integer cutoffs.

> **Theorem: Power-profile transfer**<span id="thm:transfer" label="thm:transfer">\[thm:transfer\]</span> If, uniformly for all $N>0$, $$|\Delta(N)|\le {C\over q}N^{1-\sigma},$$ then $$|A(T)|\le {C\over q(2^{1-\sigma}-1)}T^{1-\sigma}.$$ Conversely, if $|A(T)|\le (C/q)T^{1-\sigma}$ for all $T$, then $$|\Delta(N)|\le {C\over q}(2^{1-\sigma}+1)N^{1-\sigma}.$$

> **Proof** Decompose $(0,T]$ into $(T/2^j,T/2^{j-1}]$, $j\ge1$, and sum the geometric series $\sum_{j\ge1}2^{-j(1-\sigma)}
> =(2^{1-\sigma}-1)^{-1}$. The reverse direction is the triangle inequality applied to $\Delta(N)=A(2N)-A(N)$. Under the stated real-endpoint step-function convention the telescoping is exact. An input stated only for integer $N$ requires a separate rounding ledger; it is not silently charged as one endpoint coefficient.

# Truncated range ledger

Suppose the block hypothesis starts only at $N\ge M$, and $|a_n|\le B$. The dyadic decomposition stops when its lower endpoint would fall below $M$. If $R$ is the remaining endpoint, then $R<2M$, so the raw tail is strictly less than $2BM$. After the direct normalization $q/T$, the safe additional charge is $${2qBM\over T}.$$ It is small only after a separate range relation makes it small. Thus the full theorem is not a license to identify a terminal block with a cumulative prefix, and the truncated theorem does not yield a fixed $X$-power for free. This deterministic transfer is distinct from the exceptional-shadow statement of TPC-159 `\citep{WangTPC159}`.

# Route consequence

TPC-194 provides the per-packet sequence but not the production schedule or an all-scale block estimate on it. The theorem above is therefore a ready deterministic edge, not endpoint credit.

# Loss, level and scope ledger

The smallest missing literal theorem is $$\texttt{ALL\_\allowbreak{}SCALE\_\allowbreak{}BLOCK\_\allowbreak{}POWER\_\allowbreak{}BOUND\_\allowbreak{}ON\_\allowbreak{}THE\_\allowbreak{}LITERAL\_\allowbreak{}PHYSICAL\_\allowbreak{}SEQUENCE}.$$ The next route is `APPLY_ONLY_AFTER_PRODUCTION_CROSSWALK`. No new method cell is stopped in this paper.

The named-atom exponent credit is $0$, while the endpoint requires a strict budget greater than $1/400$; the ledger is unpaid. Block sums are not cumulative prefixes, symbolic packet atoms are not named production atoms, phase $L^2$ and almost-everywhere statements are not pointwise evaluation, and scoped method failures are not theorem or architecture failures.

# Machine certificate

The adjacent canonical payload freezes the formula or finite witness, exact repository-source hashes, any explicitly non-hashed external locator record, six target axes, scoped stop, route state and claim firewall. Its recursive exact schema has closed objects, exact array positions and constant leaves. The checker recomputes the finite certificate and executes ten adversarial mutations.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC93,
  author={Wang, Liang}, title={Literal Low-Window Affine Export}, year={2026}}
@misc{WangTPC94,
  author={Wang, Liang}, title={Exact Content Resonance Ledger}, year={2026}}
@misc{WangTPC108,
  author={Wang, Liang}, title={Literal Generic Affine Mobius Dispersion}, year={2026}}
@misc{WangTPC127,
  author={Wang, Liang}, title={Determinant-Two Liouville Pullback}, year={2026}}
@misc{WangTPC130,
  author={Wang, Liang}, title={Fejer Four-Sign H3 Gate}, year={2026}}
@misc{WangTPC157,
  author={Wang, Liang}, title={Literal Weight Periodic Approximation}, year={2026}}
@misc{WangTPC159,
  author={Wang, Liang}, title={Dyadic Shadow Prefix Lifting}, year={2026}}
@misc{WangTPC192,
  author={Wang, Liang}, title={MVP9 Pointwise Frontier Route Decision}, year={2026}}
@misc{WangTPC193,
  author={Wang, Liang}, title={Literal Fixed-Atom Candidate Mechanism Gate}, year={2026}}
@misc{WangTPC200,
  author={Wang, Liang}, title={Four-Form Determinant Resonance Refinement}, year={2026}}
@misc{Menon2026,
  author={Menon, Siddarth},
  title={Improved Bounds for Multiplicative Functions in Almost All Short Intervals},
  year={2026}, eprint={2607.15574}, archivePrefix={arXiv},
  primaryClass={math.NT}}
```

<!-- SOURCE_BODY_END -->
