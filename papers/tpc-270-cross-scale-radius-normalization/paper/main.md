# Cross-Scale Endpoint-Normalized Radius in a Finite V59 Residual

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 27 August 2026
- Source repository commit: `6be994e34a06fda0de2ed0bcaa42ff3db716ffef`
- Converter: `source-markdown-audit-v2`

## Abstract

TPC-269 showed that a registered growing-cutoff proxy and a convex profile path still cross the quarter threshold, but it did not measure the size of the residual radius. We introduce the dimensionless finite observable $\mathsf{Xi}_{N,\theta}=(R_{N,\theta}^{2})^3/N^{10}$, equivalently $(R_{N,\theta}/N^{5/3})^6$, so that the endpoint-scale normalization is rational once the upstream interval for $R^2$ is certified. On the same source-compatible finite registry, four dyadic ratio intervals exhibit the separated pattern $\text{DROP--RISE--RISE--DROP}$: the ratio for $96\!\to\!192$ is above $23$, while that for $64\!\to\!128$ is below $1/4$. Three matched profile controls remain in $(1/2,3/4)$. This is a finite normalization audit and a scoped stability obstruction; it is not an asymptotic radius estimate, a power-saving theorem, or a twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Position and claim firewall

The TPC-266 typed compiler leaves the Schur residual radius as a separate lane. TPC-267 instantiated the literal prime-shell object at finite scale, and TPC-268 showed that declared finite cutoff changes can alter its quarter-sector classification. TPC-269 then used $z_N=\lfloor\log N\rfloor$ and an affine two-profile path, finding a finite profile flip. The remaining minimal question is a scale question: does the radius itself have a stable normalization on the same finite interface?

The status of this paper is

`NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT`.

The word “finite” is part of the claim. The registered scales are a diagnostic registry, not an asymptotic sequence with a proved source-level uniformity law. In particular, no observed ratio below or above one is promoted to an eventual lower or upper bound.

# The frozen finite residual

Let $N$ be one of the registered even scales and write $$\mathcal I_N=\{N/2+1,\ldots,N\}, \qquad
 \mathcal Q_Q=\{q:q\ \mathrm{prime},\ Q<q\leq 2Q\}.$$ The source and shifted-prime comparison are the finite objects used in TPC-269: $$\beta_N(t)=\frac{\Lambda(t)}{\log t}
 -\sum_{d\mid t,\ d^{400}\leq N^{133}}\mu(d),
 \qquad w_N(u)=\Lambda(u+2)-b_N^{(z_N)}(u),$$ where $z_N=\lfloor\log N\rfloor$ on the registry and $$b_N^{(z)}(u)=C_2^{(z)}1_{2\nmid u}
 \prod_{p\leq z}\frac p{p-1}
 \prod_{\substack{p\mid u\\p>z}}\frac{p-1}{p-2}.$$ As before, the value is zero when $u+2$ has a prime factor at most $z$, and the Euler product is enclosed by the finite tail protocol.

For $s=1,2$, let $$K_{H,s}(h)=\left(1+\frac{h^2}{H^2}\right)^{-s}$$ and retain the prime shell, unit masks, deleted diagonal, and centered residue factor in $$A_s(u,t)=1_{u\ne t}\sum_{q\in\mathcal Q_Q}qK_{H,s}(u-t)1_{q\nmid ut}
 \left(1_{u\equiv t\pmod q}-\frac1{q-1}\right).$$ For the base rows we use $\theta=0$, so $g_{N,0}=A_1\beta_N$. At three matched scales we also use the source-compatible finite mixture $$A_\theta=(1-\theta)A_1+\theta A_2, \qquad
 g_{N,\theta}=A_\theta\beta_N, \qquad \theta=1/2.$$

Partition $\mathcal I_N$ into four equal blocks and let $P_3$ be the orthogonal projection onto the three contrasts $$(1,1,-1,-1),\qquad (1,-1,0,0),\qquad (0,0,1,-1).$$ The residual product is $$R_{N,\theta}^2=\left\lVert (I-P_3)w_N\right\rVert^2
                  \left\lVert (I-P_3)g_{N,\theta}\right\rVert^2.$$ All non-logarithmic terms are rational on a finite row. The logarithms and the Euler constant use outward intervals with tail cutoff $P=50000$.

# Endpoint normalization

The endpoint budget in TPC-265 uses the baseline exponent $5/3$ for a radius lane. Directly taking $N^{5/3}$ would introduce an unnecessary algebraic number into a finite certificate. We instead define $$\mathsf{Xi}_{N,\theta}:=\frac{(R_{N,\theta}^2)^3}{N^{10}}.
 \tag{1}$$

> **Lemma: exact normalization identity** If $R_{N,\theta}^2>0$, then $$\mathsf{Xi}_{N,\theta}=\left(\frac{R_{N,\theta}}{N^{5/3}}\right)^6.$$ If $[r_-,r_+]$ is a positive outward interval for $R^2$, then $$\mathsf{Xi}\in\left[\frac{r_-^3}{N^{10}},\frac{r_+^3}{N^{10}}\right].
>  \tag{2}$$

> **Proof** The first identity follows from $R^6=(R^2)^3$ and $N^{10}=(N^{5/3})^6$, and the second follows because cubing is increasing on the positive half-line. Every endpoint in (2) is rational in the finite interval engine.

For positive intervals $[a_-,a_+]$ and $[b_-,b_+]$, the derived scale ratio uses $$\frac{[a_-,a_+]}{[b_-,b_+]}=
 \left[\frac{a_-}{b_+},\frac{a_+}{b_-}\right].
 \tag{3}$$ We study $D(a,b)=\mathsf{Xi}_{b,0}/\mathsf{Xi}_{a,0}$ for the four registered dyadic pairs, and compare $\mathsf{Xi}_{N,1/2}/\mathsf{Xi}_{N,0}$ at three scales.

# Certified finite result

The six base rows use $$(N,H,Q)=(64,15,4),(96,20,5),(128,24,5),
 (192,32,6),(256,38,6),(384,50,7).$$ The resulting $\mathsf{Xi}_{N,0}$ intervals are shown in Table [1](main.tex#L154){reference-type="ref" reference="tab:base"}; the stored radius-square intervals are inherited from the exact finite operator replay and are not floating-point point estimates.

<div id="tab:base">

|    N| $z_N$ |      $\mathsf{Xi}_{N,0}$ interval      |
|----:|:-----:|:--------------------------------------:|
|   64|   4   | \[8.81278791526e-7, 8.81449971308e-7\] |
|   96|   4   | \[4.95949095187e-7, 4.96030749164e-7\] |
|  128|   4   | \[2.04279432566e-7, 2.04322254881e-7\] |
|  192|   5   | \[1.18847779301e-5, 1.18871727315e-5\] |
|  256|   5   | \[1.46532173424e-6, 1.46559968348e-6\] |
|  384|   5   | \[9.54437330125e-6, 9.54594504625e-6\] |

: Base endpoint-normalized sixth-power intervals.

</div>

> **Theorem: finite cross-scale normalization audit** On the declared registry, the four dyadic ratios are
>
> |   $a\to b$   |          $D(a,b)$ interval         | finite classification |
> |:------------:|:----------------------------------:|:----------------------|
> |  64$\to$ 128 | \[0.231753859227, 0.231847466257\] | drop below $1/4$      |
> |  96$\to$ 192 |  \[23.9597604587, 23.9685339622\]  | rise above 16         |
> | 128$\to$ 256 |  \[7.17162080603, 7.17448479796\]  | rise above 7          |
> | 192$\to$ 384 | \[0.802913654645, 0.803207691586\] | drop below 1          |
>
> Thus the dyadic pattern is $$\mathrm{DROP\!-\!RISE\!-\!RISE\!-\!DROP}.$$ At the matched scales $N=96,128,256$, the profile ratios obey $$\begin{array}{c|c}
> N&\mathsf{Xi}_{N,1/2}/\mathsf{Xi}_{N,0}\\ \hline
> 96 &[0.632933594160,0.633142026033]\\
> 128 &[0.716167972521,0.716468259088]\\
> 256 &[0.600909229748,0.601137218046]
> \end{array}$$ and hence all lie strictly between $1/2$ and $3/4$.

> **Proof** The finite operator and projection are the frozen TPC-269 objects. The interval engine first certifies positive $R^2$, applies (2), and then applies (3) to the listed pairs. Every displayed classification is separated from its stated threshold. The independent checker recomputes the source, operator, projection, and normalization using a separate floating-point implementation; the stress audit checks the registry and all threshold inequalities.

The five adjacent base ratios give the supplementary pattern $\mathrm{DROP, DROP, RISE, DROP, RISE}$, with the largest finite rise at $128\to192$ (above 58). The profile controls are deliberately reported as ratios at the same scale: they quantify a finite profile effect without being mistaken for a cross-scale theorem.

# Interpretation and limits

Equation (1) is useful because it turns the radius question into a dimensionless positive quantity and makes cross-scale comparisons auditable. The main finite obstruction is not the absolute size of any one row; it is the coexistence of a large normalized rise and a strict normalized drop under one declared cutoff rule and one base profile family.

Four promotions are prohibited. First, the six scales do not establish an asymptotic sequence or a uniform source-level estimate. Second, a finite rise of $D(a,b)$ does not refute an eventual bound $R_N\ll N^{5/3-\delta}$, since its constant and onset are not fixed here. Third, a finite drop does not prove such a saving. Finally, the radius product is not an arithmetic $L^2$ estimate and does not reassemble the signed prime-shell packet in Gate B.

# Conclusion

TPC-270 adds the missing finite scale lens to the TPC-267–269 chain. The exact sixth-power normalization and positive interval ratios expose strong finite cross-scale variation, while matched profile controls remain in a separated subunit band. The next source-level task is to state and prove an explicit uniform radius upper bound with a declared power and clock. The actual V59 radius and phase, strict $1/400$ payment, arithmetic $L^2$, full Gate B, and the twin-prime conclusion remain open.

# References

9 G. H. Hardy and E. M. Wright, *An Introduction to the Theory of Numbers*, 6th ed., Oxford University Press, 2008. H. L. Montgomery and R. C. Vaughan, *Multiplicative Number Theory I: Classical Theory*, Cambridge University Press, 2007. L. Wang, “A growing-cutoff and convex-profile transfer audit for the V59 residual,” TPC-269 project release, 2026.

<!-- SOURCE_BODY_END -->
