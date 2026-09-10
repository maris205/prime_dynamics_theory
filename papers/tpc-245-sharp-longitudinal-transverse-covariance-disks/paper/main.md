# Sharp Longitudinal–Transverse Covariance Disks

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [paper.pdf](paper.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology; Wuhan, China; liang.wang@hust.edu.cn
- Source date: August 25, 2026
- Source repository commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`
- Converter: `source-markdown-audit-v2`
- Included-source hashes, input order, and original-file line/page maps: [dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)

## Abstract

Fixing one longitudinal direction in a complex Hilbert space decomposes a covariance into a scalar center and a transverse remainder. We determine the exact feasible set when the two longitudinal moments and transverse energies are prescribed. With the inner product conjugate-linear in its first slot, the center is $c=\overline w b$ and the Cauchy radius is $r=(E_BE_W)^{1/2}$. In transverse dimension at least two the feasible set is the full closed disk $c+r\overline{\mathbb{D}}$; in dimension one it is the boundary circle $c+r\mathbb{T}$ when $r>0$ and a singleton when $r=0$; in dimension zero positive transverse energy is unrealizable. We derive sharp cancellation, minimum modulus, and phase-sector formulas. The result resolves the local structural question left by TPC-244, but a source-native block direction and the literal V59 two-lane attachment remain open. No arithmetic cancellation or twin-prime conclusion is claimed.

<!-- SOURCE_BODY_BEGIN -->

# Introduction

Suppose that two coefficient lanes contribute a local oriented covariance $\left\langle W,B\right\rangle$. Knowing the two norms alone gives only Cauchy–Schwarz. A more informative interface fixes a unit direction $u$, records the moments $b=\left\langle u,B\right\rangle$ and $w=\left\langle u,W\right\rangle$, and retains the remaining transverse energies. The resulting geometry is elementary but dimension-sensitive: two transverse directions fill a disk, whereas one transverse direction reaches only its boundary.

This distinction matters in the present twin-prime structural program. TPC-244 proved that a common outer block multiplier contributes through $|C_h|^2\left\langle w_h,b_h\right\rangle$, so its aggregate sign cannot control the same-block main covariance. The next local question is therefore whether longitudinal information forces, permits, or excludes cancellation inside $\left\langle w_h,b_h\right\rangle$. The exact answer is a translated disk, circle, singleton, or empty set according to transverse dimension and realizability.

Our maximum claim is structural L1. The theorem classifies all abstract vectors with fixed data; it does not assert that the actual arithmetic vectors range over that feasible set. In particular, no committed source currently defines the required one-dimensional block direction or attaches the literal V59 lanes to the common coefficient space.

# Source lock and object boundary

We use the convention that the inner product is conjugate-linear in the first slot. This fixes the longitudinal center as $\overline w b$, not $\overline b w$, and agrees with the oriented selected covariance transported by TPC-243.

TPC-244 explicitly identifies a within-block covariance as the next structural object. Its physical specialization is nevertheless conditional on a literal phasewise primitive two-lane attachment with common multiplier placement and payable coefficient norms. Those data are absent, so our $u,B,W$ are abstract.

TPC-219 contains an earlier longitudinal/transverse identity, but for a different object: its longitudinal space is the constant-prime-label subspace of $V^P$, generally of dimension $\dim V$. It is not a previously defined one-dimensional vector inside a TPC-244 primitive block. The relationship is therefore projection lineage, not literal object identity. This type boundary prevents a similarly named decomposition from being used as an arithmetic crosswalk.

# Exact covariance classification

Let $\mathcal{H}$ be a complex Hilbert space, let $u\in\mathcal{H}$ be a unit vector, and set $K=u^\perp$ and $m=\dim_{\mathbb{C}}K$. Fix $b,w\in\mathbb{C}$ and $E_B,E_W\ge0$. Let $\mathcal S$ contain every value $\left\langle W,B\right\rangle$ for vectors satisfying $$\left\langle u,B\right\rangle=b,\qquad \left\langle u,W\right\rangle=w,
 \qquad \left\lVert B\right\rVert^2-|b|^2=E_B,
 \qquad \left\lVert W\right\rVert^2-|w|^2=E_W.$$ Put $$c=\overline w b,\qquad r=\sqrt{E_BE_W}.$$

> **Theorem: Sharp feasible set**<span id="thm:classification" label="thm:classification">\[thm:classification\]</span> The feasible set is classified as follows.
>
> 1.  If $m\ge2$, then $\mathcal S=c+r\overline{\mathbb{D}}$.
>
> 2.  If $m=1$ and $r>0$, then $\mathcal S=c+r\mathbb{T}$.
>
> 3.  If $m=1$ and $r=0$, then $\mathcal S=\{c\}$.
>
> 4.  If $m=0$ and $E_B=E_W=0$, then $\mathcal S=\{c\}$. If $m=0$ and $E_B+E_W>0$, the data are unrealizable and $\mathcal S=\varnothing$.
>
> No finite-dimensionality or separability hypothesis is required.

The first branch includes $r=0$, when the displayed disk is a singleton. The one-dimensional branch is genuinely different: when both transverse energies are positive, fixed norms force equality in Cauchy–Schwarz and exclude every interior point.

# Proof of Theorem [\[thm:classification\]](sections/3_classification.tex#L17){reference-type="ref" reference="thm:classification"}

Define the orthogonal residuals $$B_{\perp}=B-bu,
 \qquad
 W_{\perp}=W-wu.$$ They lie in $K$, and Pythagoras gives $\left\lVert B_{\perp}\right\rVert^2=E_B$ and $\left\lVert W_{\perp}\right\rVert^2=E_W$. Orthogonality and the chosen sesquilinear convention give the exact identity $$\label{eq:split}
 \left\langle W,B\right\rangle=\overline w b+\left\langle W_{\perp},B_{\perp}\right\rangle.$$ Cauchy–Schwarz yields $$\label{eq:cauchy}
 \left\lvert \left\langle W_{\perp},B_{\perp}\right\rangle\right\rvert\le \sqrt{E_BE_W}=r,$$ so every feasible value lies in $c+r\overline{\mathbb{D}}$.

Assume first that $m\ge2$. If $r=0$, one transverse vector vanishes and the claim is immediate. Otherwise choose orthonormal $e_1,e_2\in K$. For any $q\in\mathbb{C}$ with $|q|\le r$, set $$W_{\perp}=\sqrt{E_W}\,e_1,
 \qquad
 B_{\perp}=\sqrt{E_B}\left(
       \frac{q}{r}e_1+
       \sqrt{1-\frac{|q|^2}{r^2}}e_2\right).$$ These vectors have the prescribed norms, and because the coefficient $q/r$ occurs in the linear second slot, $\left\langle W_{\perp},B_{\perp}\right\rangle=q$. Adding $bu$ and $wu$ realizes $c+q$ and fills the disk.

If $m=1$, choose a unit vector $e$ spanning $K$. For positive energies every admissible pair has the form $$W_{\perp}=\sqrt{E_W}\,\xi e,
 \qquad
 B_{\perp}=\sqrt{E_B}\,\eta e,
 \qquad |\xi|=|\eta|=1.$$ The transverse covariance is $r\overline\xi\eta$, which fills exactly the circle. If one energy is zero, it is zero. Finally, $m=0$ means $K=\{0\}$, so positive transverse energy is impossible and the zero-energy covariance is the center. This proves every branch.

# Cancellation margin and phase sector

> **Corollary: Exact cancellation criteria**<span id="cor:zero" label="cor:zero">\[cor:zero\]</span> If $m\ge2$, then $$\min_{z\in\mathcal S}|z|=\max\{|c|-r,0\},
>  \qquad 0\in\mathcal S\iff |c|\le r.$$ If $m=1$ and $r>0$, the minimum is $\bigl||c|-r\bigr|$ and zero is feasible if and only if $|c|=r$. Every realizable branch obeys $|\left\langle W,B\right\rangle|\ge\max\{|c|-r,0\}$.

This is the exact distance from the origin to the translated disk, circle, or singleton. It separates “cancellation is permitted by the moment data” from “cancellation occurs for the physical vectors.” Only the first statement is part of the present theorem.

> **Corollary: Sharp phase cone**<span id="cor:phase" label="cor:phase">\[cor:phase\]</span> Suppose $0\le r<|c|$. Every feasible nonzero covariance $z$ satisfies $$\left|\operatorname{Arg}(z\overline c)\right|
>  \le \arcsin(r/|c|).$$ The bound is sharp for the disk and for the nondegenerate one-dimensional circle.

To prove the claim, rotate so that $c=a>0$ and write $z=\rho e^{i\theta}$. The disk inequality becomes $$|z-a|^2=(\rho-a\cos\theta)^2+a^2\sin^2\theta\le r^2.$$ Because the disk misses zero, the principal angle is acute, and hence $|\theta|\le\arcsin(r/a)$. Equality occurs at either tangent point from the origin; those points lie on the boundary circle.

# Exact finite certificate

The machine certificate uses Gaussian-rational arithmetic and covers all dimension branches. A two-transverse-direction fixture fixes $E_B=4,E_W=9$ and realizes the center, a boundary point, and a strict interior point of the radius-six disk. A one-transverse-direction fixture checks four quarter phases on the radius-six circle and records that zero is not an interior option. Separate fixtures check the zero-radius singleton, the zero-dimensional realizability condition, and the sharp $3$–$4$–$5$ tangent geometry for a center of modulus five and radius three.

An independent implementation re-parses canonical JSON, rechecks five frozen source hashes, reconstructs all vectors, and rejects type, orientation, dimension, realizability, and arithmetic-promotion mutations. An exhaustive stress test checks $15{,}625$ ordered vector pairs in transverse dimension two and $625$ in dimension one. These computations are finite illustrations and do not replace the symbolic proof.

# Route consequence and boundary

TPC-244 reduced the orthogonal common-multiplier covariance to a nonnegative weighted sum of local covariances. Theorem [\[thm:classification\]](sections/3_classification.tex#L17){reference-type="ref" reference="thm:classification"} now gives the complete local uncertainty set once moments and transverse energies are supplied. The next structural operation is therefore a weighted Minkowski reassembly of these local disks, followed by comparison with the TPC-243 hard-window error.

Two source gates precede any physical use. First, the literal V59 $\beta,w$ lanes must be attached to one phasewise primitive coefficient space with their actual common or asymmetric multipliers and payable norms. Second, a source-native canonical direction or longitudinal projection must be defined inside each attached block. TPC-219 does not supply this second field: its constant-$q$ longitudinal subspace is a different object.

Accordingly, the maximum claim here is structural L1. We claim no arithmetic advance, no fixed-atom credit, no arithmetic L2 estimate, no payment of the strict $1/400$ endpoint, no full Gate B, and no twin-prime theorem.

# Conclusion

One longitudinal direction and two transverse energies determine an exact, dimension-sensitive covariance region. Two transverse directions fill the closed Cauchy disk; one fills only its boundary; zero permits no transverse energy. Exact cancellation margins and a sharp phase cone follow immediately but are not physical existence statements. The result closes the local Hilbert-geometry question and exposes the next honest bridge: source-native block projections, literal coefficient attachment, and weighted disk reassembly.

# Status ledger

| Field                           | Status                                                     |
|:--------------------------------|:-----------------------------------------------------------|
| Maximum claim                   | `PROVED_STRUCTURAL_L1_SHARP_COVARIANCE_DISKS`              |
| Dimension $\ge2$ feasible set   | proved exact closed disk                                   |
| Dimension $1$ feasible set      | proved exact circle or singleton                           |
| Dimension $0$ feasible set      | proved singleton or unrealizable                           |
| Minimum modulus and zero test   | proved exact and sharp                                     |
| Phase sector                    | proved sharp for $r<|c|$                                   |
| TPC-219 relationship            | projection lineage only; literal identity refuted in scope |
| Canonical block direction       | open                                                       |
| Literal V59 two-lane attachment | open                                                       |
| Arithmetic L2 / fixed atom      | none / zero                                                |
| Strict $1/400$ / full Gate B    | unpaid / open                                              |
| Twin-prime result               | none                                                       |

# Non-content font-mapping input (preserved command)

Original paper/main.tex line 8: glyphtounicode.tex, SHA-256 395e568c1f4db5e89013e6aa4aac22a668b543256a20b4349436070356870851. This audited PDF glyph-to-Unicode map is not manuscript content. Its command is retained without executing TeX or expanding the mapping table.

``` {.latex}
\input{glyphtounicode}
```

<!-- SOURCE_BODY_END -->
