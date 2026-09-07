# Outward-Rounded Profile-Budget Certificates on a New Finite Prime-Shell Panel

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
- Bibliography source: [references.bib](references.bib)
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: 30 August 2026
- Source repository commit: `abdb8bfb644f8d81c8d74b6ac609d88d191b913b`
- Converter: `source-markdown-audit-v2`

## Abstract

We close a finite analytic-interface gate left open by the preceding source–shell atlas. On the literal source interval $I=\{321,\ldots,640\}$, with $H=66$, prime shells $S_Q=\{p:Q<p\leq2Q\}$ for $Q\in\{24,36,54,80\}$, and kernel exponents $s\in\{1,2\}$, we construct the rational image of a 17-column source profile. For each of eight rows we identify the first profile prefix that can approximate the physical Gram-minimum sign target to normalized residual $1/2$. On that common prefix, exact rational ridge systems give feasible primal upper bounds and weak-dual lower bounds. A directed decimal-grid evaluator encloses every residual, objective, dual, ratio, and gap on the $10^{-36}$ grid. All eight weighted lower bounds exceed $5\times10^{-5}$ relative to the physical source norm, while all eight all-positive primal upper bounds are below $10^{-5}$. The result is an independently replayed finite certificate, not an external holdout, an arithmetic $L^2$ estimate, a growing-shell theorem, or a proof of the twin-prime conjecture.

<!-- SOURCE_BODY_BEGIN -->

# Question and route position

The prime-shell Bridge-B line has repeatedly separated finite physical structure from the arithmetic estimates needed for a theorem. The recent TPC-312 release moved the exact Gram/sign calculation to a new source panel, but explicitly left the profile-budget interface open `\cite{tpc312}`. This paper addresses that narrow question: can the native source cost be enclosed with a genuinely directed finite certificate?

We keep the physical engine, source interval, and target-generation rule fixed. The word “weighted” below refers to the TPC-312 Gram-minimum sign label; it is not a claim that this label is externally justified. This distinction is essential because choosing a target after seeing its physical Gram is source-first leakage.

# Finite profile model

For $t\in I$ and a profile cutoff $z$, set $$\beta_t^{(z)}=\frac{\mathbf 1_{t=p^a}}{a}
 -\sum_{\substack{d\mid t\\d\leq z}}\mu(d),
 \qquad
 z\in(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61).$$ The physical outputs $g_p(u)$ are those of the locked TPC-268/TPC-312 deleted-diagonal rational operator. If $A$ is the matrix whose columns are the output vectors and $U_k$ is the first $k$ profile columns, write $$W_k=A^{\mathsf T}U_k,\qquad M_k=U_k^{\mathsf T}U_k.$$ For a sign target $b\in\{-1,+1\}^{|S_Q|}$ and $R^2=\tau^2\|b\|_2^2$, the native profile budget is $$B_{k,\tau}(b)=\min_c\{c^{\mathsf T}M_kc:
             \|W_kc-b\|_2^2\leq R^2\}.                 \tag{1}$$ The source norm used for normalization is the exact physical $\|\beta\|_2^2$ from the locked engine, rather than a fitted floating-point surrogate.

# Rational primal–dual certificate

> **Proposition: Ridge dual lower bound** Assume $M_k$ is positive definite and let $\rho>0$. Define $$c_\rho=(W_k^{\mathsf T}W_k+\rho M_k)^{-1}W_k^{\mathsf T}b.$$ Then $$D_\rho(b)=
>  \frac{\|b\|_2^2-R^2-b^{\mathsf T}W_kc_\rho}{\rho}
>  \leq B_{k,\tau}(b).                                  \tag{2}$$ If $c_\rho$ is feasible, then $$D_\rho(b)\leq B_{k,\tau}(b)
>  \leq c_\rho^{\mathsf T}M_kc_\rho.                   \tag{3}$$

> **Proof** Use the Lagrangian $$L(c,\mu)=c^{\mathsf T}M_kc+
>  \mu(\|W_kc-b\|_2^2-R^2).$$ At $\mu=1/\rho$, stationarity is the displayed ridge system. Completing the square in $c$ gives (2) as the dual function value. Weak duality gives the left inequality in (3), and feasibility of $c_\rho$ gives the right one. All matrices and right-hand sides in this paper are rational, so the systems and inequalities are checked exactly over $\mathbb Q$.

For each row, we scan $k=1,\ldots,\min(|S_Q|,17)$ using exact least squares. The first feasible prefix for the TPC-312 minimum label is denoted $k^*$. The positive control is evaluated on that same $k^*$, avoiding a comparison that silently changes the profile dimension. The ridge parameters are fixed rational seeds, and are reduced by $999/1000$ only when exact feasibility requires it.

# Directed interval layer

The exact calculation is accompanied by a closed interval evaluator. For a rational $x$, its atomic enclosure is $$[\lfloor 10^{36}x\rfloor10^{-36},
   \lceil 10^{36}x\rceil10^{-36}].                    \tag{4}$$ For addition and subtraction we combine like endpoints; for multiplication and division we take the extrema of the four endpoint expressions. A square uses the endpoint containing zero when necessary. Division is accepted only when the denominator interval does not contain zero. Each operation is rounded again according to (4).

> **Lemma: Interval containment** Every interval produced by this evaluator contains the corresponding exact rational expression.

> **Proof** Atomic containment is the floor/ceiling definition. The endpoint rules are the standard inclusion rules for a closed interval under the four arithmetic operations; the nonzero-denominator condition makes division continuous on the operand rectangle. Rounding outward preserves inclusion. Induction on the finite expression tree proves the claim.

The independent replay recomputes the physical output formula, profile image, least-squares scans, ridge solution, exact scalar digests, and all six interval families. It does not import the producer or TPC-312’s producer module.

# Results

Table [1](main.tex#L164){reference-type="ref" reference="tab:main"} gives the common prefix and the resulting ratio enclosures. The lower ratio is the dual lower bound for the Gram-minimum target; the upper ratio is the feasible primal value for the all-positive control. The endpoints are outward-rounded, not confidence intervals.

<div id="tab:main">

|  $Q$|  $s$|  $k^*$|  $k^+_{\rm first}$|                  $D_\rho/\|\beta\|^2$|       $B^+_{\rm witness}/\|\beta\|^2$|
|----:|----:|------:|------------------:|-------------------------------------:|-------------------------------------:|
|   24|    1|      6|                  1|  $[4.8469605641,4.8469605642]10^{-4}$|  $[7.2890627631,7.2890627632]10^{-8}$|
|   24|    2|      4|                  1|  $[3.9650076013,3.9650076014]10^{-4}$|  $[1.3869245764,1.3869245765]10^{-7}$|
|   36|    1|      7|                  1|  $[9.8806509306,9.8806509307]10^{-5}$|  $[5.9389290927,5.9389290928]10^{-8}$|
|   36|    2|      7|                  1|  $[4.3960994502,4.3960994503]10^{-4}$|  $[1.1596823756,1.1596823757]10^{-7}$|
|   54|    1|     12|                  1|  $[5.9540989939,5.9540989940]10^{-5}$|  $[4.6318049889,4.6318049890]10^{-8}$|
|   54|    2|      8|                  1|  $[9.9387108544,9.9387108545]10^{-4}$|  $[1.1132162208,1.1132162209]10^{-7}$|
|   80|    1|     13|                  1|  $[1.2098557577,1.2098557578]10^{-4}$|  $[4.0920952988,4.0920952989]10^{-8}$|
|   80|    2|     12|                  2|  $[5.2587474247,5.2587474248]10^{-3}$|  $[9.4051662446,9.4051662447]10^{-8}$|

: Finite common-prefix budget certificate.

</div>

The first-feasible-prefix scans are exact: the preceding prefixes have residual square strictly greater than $\|b\|_2^2/4$, while the listed $k^*$ is feasible. The all-positive target is already feasible at $k=1$ in seven rows and at $k=2$ in the $(80,2)$ row; its common-prefix witness is therefore a conservative same-dimension comparison. Across all rows, the weighted dual lower interval lies above $1/20{,}000$, and the positive primal upper interval lies below $1/100{,}000$.

# Interpretation and limitations

The finite advance is specific but useful. It turns the previously float-replayed profile-budget interface into a rational primal–dual object with an explicit directed enclosure. It also shows that the separation seen in the new physical panel is not caused merely by an undecided threshold rounding: the two declared thresholds are separated in every row.

There are equally clear limits.

1.  The minimum label is chosen from the same physical Gram matrix. The certificate is consequently a source-first diagnostic, not a causal or predictive test.

2.  The source interval and shell rows are generated by the same locked finite engine. They are new coordinates within that engine, not an external physical holdout.

3.  A finite family of rational budgets supplies no uniform estimate as $x$ and the shell grow. In particular, it supplies no arithmetic $L^2$ bound and no fixed-power credit for the twin-prime route.

4.  The profile cutoff ladder, $\tau=1/2$, common-prefix rule, and rational ridge seeds are modeling choices. No external weighting law has been selected or justified.

Thus the next mathematically meaningful gate is an externally defensible weighting law tested on a genuinely fresh physical source interval. If that test fails, the present certificate remains an obstruction to treating the source-first finite separation as a global preference.

# Conclusion

TPC-313 proves a finite interface result: eight first-feasible profile prefixes and sixteen rational primal/dual witnesses are enclosed by an independently replayed $10^{-36}$ outward interval layer. The weighted lower and positive upper thresholds are strict on a common prefix in all eight rows. The result advances the Bridge-B audit by one well-defined gate while leaving external independence, canonical weighting, the growing budget theorem, arithmetic $L^2$, full Gate B, and the twin-prime conclusion open.

#### Route status.

The Session-named Route-A and Route-B evaluator files were not present in the checkout. The accompanying route note and Bridge-B checker are local, fail-closed fallbacks; no official evaluator pass is asserted.

# References (preserved BibTeX)

Bibliography source: paper/references.bib

``` {.bibtex}
@misc{tpc312,
  author       = {Liang Wang},
  title        = {A New Source--Shell Separation Atlas for a Finite Prime-Shell Diagnostic},
  year         = {2026},
  note         = {TPC-312 project in the prime-dynamics-theory repository}
}

@misc{tpc300,
  author       = {Liang Wang},
  title        = {Native Budget Dual Certificates for a Finite Prime-Shell Diagnostic},
  year         = {2026},
  note         = {TPC-300 project in the prime-dynamics-theory repository}
}
```

<!-- SOURCE_BODY_END -->
