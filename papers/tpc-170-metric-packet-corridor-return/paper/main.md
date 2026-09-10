# **Metric All-Prefix Return on Prescribed Determinant-Two Packet Corridors:\ Borel–Cantelli, Representative Invariance, and the Fixed-Atom Stop**

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](../main.tex)
- Preserved PDF: [tpc-170-metric-packet-corridor-return.pdf](../tpc-170-metric-packet-corridor-return.pdf)
- Bibliography source: [references.bib](../references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Artificial Intelligence and Automation,; Huazhong University of Science and Technology, Wuhan 430074, P.R. China; wangliang.f@gmail.com
- Source date: July 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`

## Abstract

We lift the single-cell maximal phase-$L^2$ theorem of TPC-169 to a prescribed countable corridor of determinant-two packets. The only uniformity cost is the explicit sum of packet energies. Borel–Cantelli then gives, for almost every fixed phase, simultaneous eventual control of every declared packet and every prefix. Under a dyadic ambient schedule, polylogarithmically many packets, and terminal scales at least the square root of the ambient scale, every power strictly below $1/4$ is admissible. We prove that all Bézout representatives for fixed $(a,s)$ are translations of the same coefficient packet and should be canonicalized rather than union-counted. Exact Abel summation returns the maximal estimate to literal weights. A fixed-atom example shows that almost-everywhere phase control cannot be promoted to a named physical phase.

<!-- SOURCE_BODY_BEGIN -->

**Keywords.** Borel–Cantelli; maximal Fourier sum; packet corridor; Abel summation; determinant two.

# Canonical determinant-two representatives

Fix coprime positive odd-product integers $a,s$ and let $$su-ad=2.$$ The apparent infinity of integer solutions does not create independent coefficient packets.

> **Lemma: Bézout representative invariance**<span id="lem:translate" label="lem:translate">\[lem:translate\]</span> Every second solution $(d',u')$ is uniquely of the form $$d'=d+sk,\qquad u'=u+ak,\qquad k\in\mathbb Z.
> \label{eq:representative}$$ Writing $$q=as,\quad t_{d}(z)=ad+qz,\quad
>  c_{d,u}(z)=\mu(d+sz)\mu(u+az),$$ one has $$t_{d'}(z)=t_d(z+k),\qquad
>  c_{d',u'}(z)=c_{d,u}(z+k).
> \label{eq:translation}$$ If a multiplier is translated covariantly by $\rho'(z)=\rho(z+k)$, then every corresponding additive-twist prefix differs by the single factor $\mathrm e(\alpha k)$.

> **Proof** Subtracting the two determinant equations gives $s(u'-u)=a(d'-d)$. Coprimality yields $d'-d=sk$ and $u'-u=ak$, proving [\[eq:representative\]](../main.tex#L80){reference-type="eqref" reference="eq:representative"}. Direct substitution gives [\[eq:translation\]](../main.tex#L91){reference-type="eqref" reference="eq:translation"}. With $w=z+k$, $$\rho'(z)\mathrm e(-\alpha z)
>  =\rho(w)\mathrm e\{-\alpha(w-k)\}
>  =\mathrm e(\alpha k)\rho(w)\mathrm e(-\alpha w).$$

Thus a packet registry must select one canonical representative for each fixed $(a,s)$. Counting all representatives as distinct would manufacture a false infinite union. The covariance condition on $\rho$ is essential; an unshifted coordinate multiplier need not describe the same physical packet.

# Prescribed packet energies

Let $X_n\to\infty$ be a prescribed ambient schedule. At level $n$, let $\mathcal P_n$ be a finite, explicit packet list. A packet $p$ consists of a canonical determinant-two fiber, a terminal scale $T_{n,p}$, and a bounded multiplier $\rho_{n,p}$. Let $L_{n,p}$ be the number of positive fiber points up to $T_{n,p}$, and put $$D_{n,p}=1+\lceil\log_2L_{n,p}\rceil.$$ For its ordered points $z_{n,p,j}$, define $$S_{n,p,k}(\alpha)=
 \sum_{j\le k}
 \mu(d+sz_{n,p,j})\mu(u+az_{n,p,j})
 \rho_{n,p}(z_{n,p,j})\mathrm e(-\alpha z_{n,p,j}),$$ $$G_{n,p}(\alpha)=
 \frac{q_{n,p}}{T_{n,p}}
 \max_{k\le L_{n,p}}|S_{n,p,k}(\alpha)|.$$ TPC-169 proves `\citep{WangTPC169}` $$\int_{\mathbb T}G_{n,p}^2
 \le V_{n,p},
\qquad
 V_{n,p}:=
 D_{n,p}^2\lVert\rho_{n,p}\rVert_\infty^2
 \left(
 \frac{q_{n,p}}{T_{n,p}}
 +\frac{q_{n,p}^2}{T_{n,p}^2}
 \right).
\label{eq:packetenergy}$$ No two packets are assumed to share a coefficient sequence. Uniformity is paid by the literal sum of [\[eq:packetenergy\]](../main.tex#L151){reference-type="eqref" reference="eq:packetenergy"}.

# Metric packet-corridor theorem

> **Theorem: Prescribed-corridor Borel–Cantelli**<span id="thm:bc" label="thm:bc">\[thm:bc\]</span> Let $\lambda_n>0$. If $$\sum_{n=1}^{\infty}
>  \lambda_n^{-2}
>  \sum_{p\in\mathcal P_n}V_{n,p}<\infty,
> \label{eq:summability}$$ then for Lebesgue-almost every fixed $\alpha\in\mathbb T$, there exists $n_0(\alpha)$ such that for all $n\ge n_0(\alpha)$, all $p\in\mathcal P_n$, and all $k\le L_{n,p}$, $$\frac{q_{n,p}}{T_{n,p}}
>  |S_{n,p,k}(\alpha)|
>  \le\lambda_n.
> \label{eq:eventual}$$

> **Proof** Let $$E_n=\{\alpha:\max_{p\in\mathcal P_n}G_{n,p}(\alpha)>\lambda_n\}.$$ The union bound, Chebyshev, and [\[eq:packetenergy\]](../main.tex#L151){reference-type="eqref" reference="eq:packetenergy"} give $$\operatorname{meas}(E_n)
>  \le\lambda_n^{-2}\sum_{p\in\mathcal P_n}V_{n,p}.$$ Thus $\sum_n\operatorname{meas}(E_n)<\infty$. The first Borel–Cantelli lemma, which requires no independence, implies that almost every $\alpha$ belongs to only finitely many $E_n$ `\citep{Durrett2019}`. This is exactly [\[eq:eventual\]](../main.tex#L173){reference-type="eqref" reference="eq:eventual"}.

The words “prescribed” and “fixed” are load-bearing. The packet lists must be fixed before the exceptional phases are read, and the same $\alpha$ is followed through the schedule. The resulting null set depends on that entire prescribed schedule; changing or enlarging the schedule requires paying the new packet energies and constructing the corresponding null set again.

# A positive-power dyadic corridor

> **Corollary: Every exponent below one quarter**<span id="cor:power" label="cor:power">\[cor:power\]</span> Suppose $$X_n=2^n,\qquad
>  \sqrt{X_n}\le T_{n,p}\le X_n,$$ $$q_{n,p}\ll(\log X_n)^\eta,\qquad
>  |\mathcal P_n|\ll(\log X_n)^C,\qquad
>  \lVert\rho_{n,p}\rVert_\infty\ll1$$ uniformly in declared packets. Then for every fixed $0<\delta<1/4$, [\[thm:bc\]](../main.tex#L158){reference-type="ref" reference="thm:bc"} applies with $$\lambda_n=X_n^{-\delta}.$$

> **Proof** Uniformly, $D_{n,p}=O(\log X_n)$, so $$\lambda_n^{-2}\sum_{p\in\mathcal P_n}V_{n,p}
>  \ll
>  (\log X_n)^{C+\eta+2}
>  X_n^{-1/2+2\delta}.$$ With $X_n=2^n$, this is a polynomial in $n$ times a geometric sequence of ratio tending to $2^{-(1/2-2\delta)}<1$. Hence [\[eq:summability\]](../main.tex#L164){reference-type="eqref" reference="eq:summability"} holds.

To obtain natural endpoint normalization, include dyadic terminal shells in the packet list. An endpoint $U\in[T_{n,p}/2,T_{n,p}]$ then satisfies $$\frac{q_{n,p}}U|S_{n,p,k}(\alpha)|
 \le2X_n^{-\delta}.$$ Only $O(\log X_n)$ shells are required, so this cost is absorbed by increasing $C$ by one. This produces simultaneous metric control throughout the *declared* endpoint corridor, not over an unregistered physical family.

# Exact Abel return

Let $w_1,\ldots,w_L\in\mathbb C$, set $$\Delta_iw=w_i-w_{i+1}\quad(i<L),\qquad
 \Delta_Lw=w_L,$$ and $$\operatorname{Var}_*(w)=\sum_{i=1}^L|\Delta_iw|.$$

> **Proposition: Metric weighted return**<span id="prop:abel" label="prop:abel">\[prop:abel\]</span> Whenever $G_{n,p}(\alpha)\le\lambda_n$, $$\frac{q_{n,p}}{T_{n,p}}
>  \left|\sum_{j=1}^{L}
>  b_j\mathrm e(-\alpha z_j)w_j\right|
>  \le\lambda_n\operatorname{Var}_*(w),
> \label{eq:abel}$$ where $b_j=c_{z_j}\rho(z_j)$. A prefix cutoff has $\operatorname{Var}_*(w)=1$.

> **Proof** Exact Abel summation gives $$\sum_{j=1}^Lb_j\mathrm e(-\alpha z_j)w_j
>  =
>  \sum_{i=1}^L
>  \left(\sum_{j\le i}b_j\mathrm e(-\alpha z_j)\right)\Delta_iw.$$ Bound every partial sum by $(T_{n,p}/q_{n,p})\lambda_n$ and sum absolute values. The prefix assertion is the one-atom identity of TPC-160 `\citep{WangTPC160}`.

Thus any source-locked literal weight with $\operatorname{Var}_*(w)\le X_n^\beta$, $\beta<\delta$, receives the metric saving $X_n^{-(\delta-\beta)}$. This is an interface, not a claim that the missing physical weight registry supplies the variation certificate.

# The fixed-atom stop

> **Proposition: Metric information does not select an atom** <span id="prop:atom" label="prop:atom">\[prop:atom\]</span> The Lebesgue-almost-everywhere conclusion of [\[thm:bc\]](../main.tex#L158){reference-type="ref" reference="thm:bc"}, viewed only as a measure statement, contains no control at a named fixed phase or at phases $\alpha_n$ selected separately at each scale.

> **Proof** A Lebesgue null set may contain any prescribed atom, so the almost-everywhere quantifier alone has no value at that atom. The coefficient-blind maximal framework makes this sharp: take $b_{n,j}=1$ and $\alpha_n=0$. At the terminal prefix, $$\frac1{L_n}\left|\sum_{j=1}^{L_n}b_{n,j}\mathrm e(-\alpha_nj)\right|=1$$ for every $n$. The single phase zero has Lebesgue measure zero and is therefore fully compatible with an almost-everywhere theorem. Allowing $\alpha_n$ to vary only makes the selector mismatch more pronounced.

The example proves a quantifier nonimplication for the general bounded-coefficient maximal framework, not a counterexample inside the literal Möbius packet class. It is not evidence that the literal Möbius coefficients have a large twist. Likewise, TPC-168’s finite-registry selector firewall forbids density-one promotion to a named registry phase `\citep{WangTPC168}`.

More generally, an uncontrolled atomic phase registry may place every one of its atoms inside the schedule-dependent null set at zero Lebesgue cost. Neither [\[thm:bc\]](../main.tex#L158){reference-type="ref" reference="thm:bc"} nor the packet-energy bound controls the mass of such a registry. This is a scoped *uncontrolled atomic registry obstruction*: it stops the metric-to-atomic transfer, not the direct additive-twist route and not any future source-locked registry with its own avoidance theorem.

# Route decision

TPC-170 has the exact program status $$\mathsf{PROVED\_L1\_ACTUAL\_CORE\_
 PHASE\_METRIC\_PACKET\_CORRIDOR}.$$ Its analytic and program axes are $$\begin{array}{c|c}
\text{axis}&\text{value}\\ \hline
\mathsf{analytic\_norm}&\mathsf{L2\_PHASE\_MAXIMAL\_BC}\\
\mathsf{program\_positive\_L2}&\mathsf{false}\\
\mathsf{fixed\_atom}&\mathsf{false}
\end{array}$$ It advances both parent-ready arithmetic doors along one new typed route: $$\begin{aligned}
 \text{direct additive twist}
 &\longrightarrow
 \text{phase-metric prescribed packet corridor},\\
 \text{bad atomic endpoint}
 &\longrightarrow
 \text{phase-metric all-prefix corridor}.\end{aligned}$$ The original fixed-phase nodes remain open. Closing either requires a source-locked production phase-metric crosswalk or a genuinely pointwise theorem. Neither Lebesgue-a.e. nor a registry average is a fixed atom.

# Reproducible audit and conclusion

The standard-library audit source-locks TPC-168/169, verifies [\[lem:translate\]](../main.tex#L76){reference-type="ref" reference="lem:translate"} with literal Möbius values and a covariantly translated multiplier, checks exact Abel summation, records the ratio-test exponent in [\[cor:power\]](../main.tex#L203){reference-type="ref" reference="cor:power"}, and realizes the fixed-atom stop. Executable bad-snapshot mutations reject undeclared packet uniformity, missing packet-energy unions, duplicate Bézout representatives, untranslated multipliers, $\delta\ge1/4$, and every $\mathsf{LEBESGUE\_AE}$-to-$\mathsf{FIXED\_ATOM}$ promotion.

The four-paper corridor has therefore moved forward without conflating norms. Direct twists and every terminal-shell prefix now have a positive-power metric theorem on explicit packet schedules. The surviving gap is no longer cancellation in that metric; it is the theorem-backed selection of the production phase, or a new pointwise arithmetic estimate. No physical endpoint is inferred from that unresolved selection.

# References (preserved BibTeX)

Bibliography source: references.bib

``` {.bibtex}
@misc{WangTPC160,
  author = {Wang, Liang},
  title  = {{Exceptional-Variation Abel Return:
             Literal Weights, Almost-Prefixes, and the Atomic
             All-Prefix Barrier}},
  year   = {2026},
  note   = {TPC-160 manuscript}
}

@misc{WangTPC168,
  author = {Wang, Liang},
  title  = {{Separated Phase Registries for Direct Core Twists:
             A Finite Large-Sieve Gate and a Selector Firewall}},
  year   = {2026},
  note   = {TPC-168 manuscript}
}

@misc{WangTPC169,
  author = {Wang, Liang},
  title  = {{One Phase-Exceptional Set for Every Atomic Prefix:
             A Dyadic Maximal Parseval Theorem on Determinant-Two
             Fibers}},
  year   = {2026},
  note   = {TPC-169 manuscript}
}

@book{Durrett2019,
  author    = {Durrett, Rick},
  title     = {Probability: Theory and Examples},
  edition   = {Fifth},
  publisher = {Cambridge University Press},
  year      = {2019}
}
```

<!-- SOURCE_BODY_END -->
