# Schur Slack and Sign-Law Uniformity in a Normalized Prime-Shell Operator

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)

- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: Liang Wang; School of Mathematics and Statistics; Huazhong University of Science and Technology (HUST); Wuhan, China
- Source date: September 2026
- Source repository commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`
- Converter: `source-markdown-audit-v2`

## Abstract

We audit two possible weaknesses in a finite normalized operator certificate: whether its Schur envelope is nearly saturated, and whether computing the true spectrum only for the all-plus sign law is representative. On the three origins fixed by the preceding geometry-adversarial holdout, we compute true spectra for all four fixed sign laws at counts 256 and 512, producing 144 rows. The largest spectral/Schur ratio is 0.77628391453148915 and the largest spectral/Frobenius ratio is 0.62110877254133434. All 144 normalized spectra are below 0.64; all-plus wins 30 of 36 setting-wise comparisons and the mod-4 law wins 6. These are finite, scoped observations: they quantify envelope slack and law variation but do not imply a growing operator theorem, an arithmetic estimate, or a twin-prime result.

<!-- SOURCE_BODY_BEGIN -->

# Question and scope

TPC-359 transferred a finite normalized cap to a high-origin panel selected using unsigned geometry alone. Its Schur and Frobenius values were recorded for four laws, while true eigenvalues were computed for all-plus. The present paper closes that diagnostic gap on a smaller, explicitly frozen ladder. We ask whether the envelope is tight and whether a law-uniform spectral maximum is hidden by the all-plus restriction. The V59 source response is not used, and no Route-B arithmetic reassembly is attempted. The Session-named official evaluator files are absent, so local Bridge-B remains fail-closed evidence.

# Operator and finite protocol

For $I=[x,x+N-1]\cap\mathbb Z$, primes $Q<p\leq2Q$, and $s\in\{1,2\}$, we use the literal component $$B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
 \left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.
 \label{eq:block}$$ For each fixed sign law $\varepsilon$, let $A_\varepsilon=\sum_p\varepsilon_pB_p$. The unsigned geometry is $G_u=\sum_{p,t}B_p(u,t)^2$, and $$A_\varepsilon^\#=D_G^{-1/2}A_\varepsilon D_G^{-1/2},
 \qquad D_G=\operatorname{diag}(G_u).
 \label{eq:norm}$$ We inherit origins $(267175,261267,269074)$ from TPC-359 and use $N\in\{256,512\}$, $Q\in\{24,54,80\}$, $s\in\{1,2\}$, and four laws: all-plus, alternating-index, the prime mod-$4$ character, and half-split. This gives $3\cdot2\cdot3\cdot2\cdot4=144$ rows and 36 within-setting law comparisons.

# Finite envelope facts

For every finite real symmetric matrix $T$, $$\lVert\,\cdot\,\rVert_2{T}\leq S(T):=\max_u\sum_t|T(u,t)|,
 \qquad
 \lVert\,\cdot\,\rVert_2{T}\leq F(T):=\left(\sum_{u,t}|T(u,t)|^2\right)^{1/2}.
 \label{eq:envelope}$$ The inequalities are exact finite statements. We use the ratios $\rho_S=\lVert\,\cdot\,\rVert_2{T}/S(T)$ and $\rho_F=\lVert\,\cdot\,\rVert_2{T}/F(T)$ only as descriptive quantities for the declared matrices.

# Results

| law         |  $\lVert\,\cdot\,\rVert_2{T}_{\min}$|  $\lVert\,\cdot\,\rVert_2{T}_{\max}$|      mean|  $\max\rho_S$|  $\max\rho_F$|
|:------------|------------------------------------:|------------------------------------:|---------:|-------------:|-------------:|
| all-plus    |                             0.029948|                             0.627166|  0.182371|      0.776284|      0.621109|
| alternating |                             0.017474|                             0.048357|  0.030149|      0.491689|      0.173625|
| mod-$4$     |                             0.028434|                             0.072074|  0.043659|      0.586123|      0.247643|
| half-split  |                             0.021530|                             0.066150|  0.036456|      0.492854|      0.239863|

: Normalized spectral extrema and envelope ratios over 36 rows per law.

The largest ratio over all laws is $$\max\rho_S=0.77628391453148915,
 \qquad
 \max\rho_F=0.62110877254133434.
 \label{eq:ratios}$$ Thus, within this finite panel, the Schur envelope has at least 0.22371608546851085 relative slack at the most saturated row, while the Frobenius envelope has at least 0.37889122745866566. This does not mean that the same slack holds for larger origins or counts.

Every one of the 144 normalized spectra is below 0.64. In the 36 comparisons at fixed origin, count, shell, and exponent, all-plus is largest 30 times and the mod-4 character is largest 6 times; alternating-index and half-split never win. Consequently all-plus is a useful finite stress law, but the winner census itself rules out silently treating it as a universal proxy.

# Audits and claim firewall

The canonical certificate locks the TPC-355 base implementation and the TPC-359 code and certificate, records every matrix metric, and includes a rational $Q=4$ anchor on $[267205,267218]$. A separate reverse-shell checker rebuilds the prime sieve, literal masks, geometry, all four signed matrices, normalization, and all 144 spectra without importing the TPC-360 producer. A 14-mutation stress test rejects altered row census, law set, response flag, ratios, winner census, firewall, and payload hash. The local Bridge-B checker reruns these checks in normal and optimized modes with byte-identical output.

The maximum justified claim is therefore a numerically certified finite Schur-tightness and law-uniform audit. The exact envelope inequalities are proved only for finite matrices. Source-uniform arithmetic $L^2$, a growing masked-operator estimate, fixed-power credit, Route-B reassembly, and the twin-prime endpoint remain open.

# Conclusion

The finite normalized cap is not close to saturation by either elementary envelope on this panel, and the all-plus law captures the largest spectrum in most but not all settings. This identifies the next useful control: repeat the tightness ledger on an independently selected high-origin panel, keeping all four laws in the spectral audit. Nothing in this finite diagnostic pays an arithmetic loss.

`TPC360_ARITHMETIC_ADVANCE=NO`, `TPC360_FIXED_POWER_CREDIT=0`, `TPC360_FULL_GATE_B=OPEN`.

<!-- SOURCE_BODY_END -->
