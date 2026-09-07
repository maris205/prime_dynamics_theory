# Profile-Prefix Shift Sensitivity in a\ Common-Ambient Prime-Shell Holdout

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST), Wuhan, China
- Source date: 29 August 2026
- Source repository commit: `ed725e6537012bd17a32d061d9d8e6dd3b253613`
- Converter: `source-markdown-audit-v2`

## Abstract

The finite common-ambient holdout of TPC-308 used one ordered source-profile prefix and found a residual budget/holdout discordance concentrated on the final $Q=70\to90$ transition. We test the smallest neighboring profile perturbation: in a fixed 19-prime cutoff pool, replace the 17-coordinate profile ladder by its one-step lower window (LOW), the original window (BASE), or its one-step upper window (HIGH). The physical rows, shell labels, alignment, overlap protocol, and binary exclusive-completion envelopes remain unchanged; each ladder’s feasible common prefix and frontier are recomputed. The exact finite protocol gives three source-backed windows, while a producer and independent NumPy replay reproduce 54 profile cases, 162 envelope observations, and 2106 candidate evaluations. BASE recovers TPC-308’s $13/3/2$, $11/2/5$, and $10/1/7$ agreement censuses at radii $0,1,2$. LOW and HIGH move strict discordances to earlier transitions and broaden the unresolved band; at radius two HIGH has no strict discordance while LOW and BASE retain one each. Thus the location and persistence of the finite obstruction are not invariant under these declared profile shifts. This is a finite model-selection obstruction, not a causal, asymptotic, arithmetic, or twin-prime theorem.

<!-- SOURCE_BODY_BEGIN -->

# Question and frozen parent object

TPC-308 put adjacent prime-shell pairs in a common union ambient operator, fit aligned directional targets on their overlap, and evaluated the exclusive pieces as withheld binary completions `\cite{tpc307,tpc308}`. Its completion envelope was deliberately useful as an adversarial stress axis, but it left a natural modeling question: does the observed final-transition discordance depend on the selected finite source-profile prefix?

We ask only the following bounded question:

> Does the budget/holdout class, and in particular the location of a strict discordance, survive a one-step source-backed shift of the 17-cutoff profile ladder?

The source interval is $I=[257,512]\cap\mathbb Z$, the height is $H=58$, the source comparison cutoff is $z=5$, and the shell spine is $Q=(50,60,70,90)$. We retain exponents $e\in\{1,2\}$ and overlap-fit tolerances $\tau\in\{0.25,0.5,0.75\}$. The literal source profile is $$\beta(v;z)=\lambda(v)-\sum_{d\mid v,\ d\le z}\mu(d),$$ with the prime-power term supplied by the locked TPC-268 engine `\cite{tpc302}`. The source-first target labels remain the physical-Gram-dependent labels of the parent construction; this inherited leakage is explicit below.

Let $$P=(2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67).$$ The three ordered profile ladders are the contiguous windows $$\begin{split}
 \mathrm{LOW}&=P[0:17]=(2,3,5,\ldots,53,59),\\
 \mathrm{BASE}&=P[1:18]=(3,5,7,\ldots,53,59,61),\\
 \mathrm{HIGH}&=P[2:19]=(5,7,11,\ldots,59,61,67).
 \end{split}                                                    \tag{1}$$ Each neighboring pair shares 16 of 17 coordinates, and BASE is exactly the TPC-308 ladder. We change no shell, label, or holdout row.

# Finite protocol and exact algebra

For a ladder $a$, let $B_a$ be the $256\times17$ matrix of profile values and $M_a=B_a^\mathsf{T}B_a$. For a union shell $U$, the physical matrix is $V_{U,a}$, and $V_{O,a}$ is its restriction to the overlap rows. The two overlap targets are aligned by the sign of their raw binary inner product. For target $t$ define $k(t,a)$ as the first ordered prefix whose least-squares residual is at most $\tau^2\|t\|_2^2$. We use the common prefix $$k_a=\max\{k(t_L,a),k(t_R,a)\}.                         \tag{2}$$ At this prefix the frontier coefficient minimizes source energy subject to the residual constraint. Denote its two source energies by $E_{L,a}$ and $E_{R,a}$. The primary budget ratio is the conservative interval for $E_{R,a}/E_{L,a}$; a secondary control retains the TPC-308 budget class while only changing the profile-induced predictions.

For a native exclusive binary target $h\in\{-1,+1\}^m$ and its fitted prediction $y$, define the finite completion ball and its loss envelope by $$\mathcal C_r(h)=\{h':d_H(h,h')\le r\},\qquad
 L_r^\pm(y,h)=\mathop{\mathrm{ext}}_{h'\in\mathcal C_r(h)}
       \frac1m\|y-h'\|_2^2.                                \tag{3}$$ The reported right-over-left interval is $$\left[\frac{L_r^-(y_R,h_R)}{L_r^+(y_L,h_L)},
        \frac{L_r^+(y_R,h_R)}{L_r^-(y_L,h_L)}\right].        \tag{4}$$ An interval wholly below $0.9$ is right-lower, one wholly above $1.1$ is left-lower, and all other intervals are unresolved.

> **Proposition: Finite window and prefix facts** The three sets in (1) are ordered 17-element contiguous subwindows of $P$; the least-squares residual over the first $k$ columns is nonincreasing in $k$; and the common prefix in (2), whenever both first-feasible indices exist, is feasible for both targets.

> **Proof** The window statements follow by direct indexing and the two adjacent intersections have size 16. The span of the first $k$ columns is contained in the span of the first $k+1$ columns, so the distance to a target cannot increase. Apply this separately to the two targets and take the larger first-feasible index.

> **Proposition: Finite completion and ratio facts** For binary $h$, enumerating subsets of at most $r$ flipped coordinates gives all elements of $\mathcal C_r(h)$ exactly once. Hence $$|\mathcal C_r(h)|=\sum_{j=0}^{\min(r,m)}\binom mj,$$ the enumerated extrema in (3) are exact, the lower and upper envelopes are monotone in $r$, and radius zero recovers the native target. If the losses and denominators are positive, (4) contains every finite completion ratio.

> **Proof** The unique difference set $\{j:h'_j\ne h_j\}$ is the flip subset; binary values force each changed coordinate to be $-h_j$. This proves the bijection and the binomial count. Inclusion of successive Hamming balls proves the envelope monotonicity, and the empty subset proves radius-zero recovery. For positive intervals, ordinary quotient bounds give (4), and the threshold classification follows immediately.

> **Remark** The completion ball is an adversarial finite diagnostic, not a probability law or a causal intervention. A common positive normalizer cancels from $(E_{R,a}/N_a)/(E_{L,a}/N_a)$, although the implementation still checks positivity and reports all three normalizers.

# Numerical implementation

The producer locks the TPC-308 code and canonical certificate, reconstructs the six union shells and their inherited labels, and builds the three profile matrices from the same literal-beta formula. It uses the vectorized float64 physical-row construction, a 70-digit frontier solve on decimalized entries, and relative-$10^{-5}$ padded output enclosures. For every ladder it runs all 18 cells (three transitions, two exponents, three tolerances) and all three radii. The exclusive cardinality pairs are $(2,5)$, $(2,4)$, and $(5,7)$, so the candidate totals are $108,558,1440$ across the three ladders at radii $0,1,2$.

The standalone checker does not import the TPC-309 producer. It reloads the TPC-268 engine and TPC-302 row certificate, rebuilds each profile ladder and physical matrix in NumPy, independently solves the frontier, enumerates every completion, and verifies the published enclosures with a relative $2\times10^{-3}$ replay slack. This supports numerical reproduction of the declared finite object, but not a directed-rounding certificate.

# Results

Table [1](main.tex#L188){reference-type="ref" reference="tab:agreement"} gives the primary profile-recomputed budget comparison. Each triple is (concordant, discordant, unresolved). BASE recovers the preceding TPC-308 path exactly at all three radii, while the neighboring ladders change both the feasible-prefix census and the agreement pattern.

<div id="tab:agreement">

| profile ladder |   $r=0$  |   $r=1$  |   $r=2$  |
|:--------------:|:--------:|:--------:|:--------:|
|       LOW      | $13/4/1$ | $10/2/6$ |  $8/1/9$ |
|      BASE      | $13/3/2$ | $11/2/5$ | $10/1/7$ |
|      HIGH      | $10/5/3$ | $5/0/13$ | $5/0/13$ |

: Primary agreement census by profile ladder and completion radius.

</div>

The associated primary source-budget counts at radius zero are LOW $11/6/1$, BASE $13/5/0$, and HIGH $9/7/2$ (right-lower, left-lower, unresolved). The holdout counts are respectively LOW $13/5/0$, BASE $13/3/2$, and HIGH $8/9/1$. Thus the HIGH shift creates five strict discordances at radius zero, while two profile-specific budget cells become unresolved before any completion perturbation is applied.

<div id="tab:discordance">

|  radius  | $50\to60$ | $60\to70$ | $70\to90$ |
|:--------:|:---------:|:---------:|:---------:|
|  $0$ LOW |     2     |     1     |     1     |
| $0$ BASE |     0     |     0     |     3     |
| $0$ HIGH |     2     |     2     |     1     |
|  $1$ LOW |     2     |     0     |     0     |
| $1$ BASE |     0     |     0     |     2     |
| $1$ HIGH |     0     |     0     |     0     |
|  $2$ LOW |     1     |     0     |     0     |
| $2$ BASE |     0     |     0     |     1     |
| $2$ HIGH |     0     |     0     |     0     |

: Strict discordances by transition; rows are (LOW, BASE, HIGH).

</div>

The table makes the obstruction concrete. The three BASE discordances at radius zero are all on the final transition and exponent one, as in TPC-308. Under LOW, none of those three is a strict discordance at the same location: the strict discordances redistribute across the earlier transitions, and the radius-two survivor is on $50\to60$. HIGH likewise moves strict discordances to the first two transitions and has no strict survivor at radius two. The finite observation is therefore neither location-stable nor uniformly surviving under the declared one-step profile shifts.

The secondary frozen-budget control reaches the same qualitative warning. It isolates the effect of changing fitted predictions while retaining the parent budget orientation, and it also changes the strict-discordance census. This confirms that the result is a sensitivity statement about the finite representation and holdout geometry, not evidence for a preferred causal direction.

# Interpretation and route status

The strongest positive result is a reproducible finite protocol in which the profile perturbation is explicit, source-backed, same-dimensional, and adjacent to the parent ladder. The strongest obstruction is that the BASE final-transition discordance is not invariant: LOW and HIGH relocate or erase strict discordances, while completion envelopes turn more cells unresolved. The natural open theorem would require a profile-independent preference or a principled profile-selection law; neither is present here.

The following boundaries are part of the result:

-   The labels inherit physical-Gram-dependent target-generation leakage from TPC-302; changing profile coordinates does not cure that leakage.

-   The three windows are a finite modeling choice, not an asymptotic family and not a probability distribution.

-   Float64 physical rows and padded decimal intervals are numerical replay, not directed-rounding certification.

-   No arithmetic $L^2$ estimate, fixed-power credit, uniform growing budget, full Route-B Gate B, causal identification, or twin-prime conclusion follows.

The Session-named `propose.md` and Route-A/Route-B evaluator files are absent from this checkout. No official evaluator pass is asserted; the local fail-closed evaluation is recorded in the project route note and Bridge-B checker. The next minimal question is to compare alternative holdout aggregation rules under the same profile shifts.

# Reproducibility

The canonical certificate is `results/tpc309_certificate.json`. The producer, independent replay, exact stress suite, theorem ledger, claim firewall, and Bridge-B checker are in the project directory. All empirical statements above are finite observations under the locked protocol and should not be extrapolated to growing $N$ or $Q$.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc302,
  author       = {Liang Wang},
  title        = {Source-First Growing-Shell Budget Gap Audit},
  year         = {2026},
  note         = {Local TPC-302 release in the prime-dynamics research repository}
}

@misc{tpc307,
  author       = {Liang Wang},
  title        = {A Common-Ambient Union-Shell Holdout for Transported Prime-Shell Labels},
  year         = {2026},
  note         = {Local TPC-307 release in the prime-dynamics research repository}
}

@misc{tpc308,
  author       = {Liang Wang},
  title        = {Adversarial Exclusive Completions for a Common-Ambient Prime-Shell Holdout},
  year         = {2026},
  note         = {Local TPC-308 release in the prime-dynamics research repository}
}
```

<!-- SOURCE_BODY_END -->
