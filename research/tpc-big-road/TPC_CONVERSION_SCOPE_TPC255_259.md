# TPC255–259 conversion and bounded prerequisite audit

Updated 2026-09-07. Source lock:
`d1683c8f96ae1b86f2f9fcb9ba8318c9e1aaf3f6`. All five complete TeX
manuscripts, README files, proof packages, and external bibliography files
were read. Original scientific files, certificates, code, hand-edited
materials, and local build products remain unchanged.

## Conversion evidence

All five mechanical reading layers pass abstract/body formula-sequence and
normalized-text roundtrips: 584 math nodes and 158 raw-source display blocks
across 24 extracted PDF pages. Every source section has a unique heading-text
page match. All five external bibliographies are retained as full, hash-locked
BibTeX; unresolved citation commands remain explicit code. No converter
change was needed.

No independent bibliography verification, visual PDF certification, or proof
of PDF/TeX synchronization is claimed. No original producer, physical replay,
stress suite, or publication cascade was run. The checks below are independent
small rational/Gaussian-rational or symbolic examples, not reproductions of
the published 64-clock, 192-family, or prime-sampling experiments. The cited
PNT, Poisson, and hybrid H2 source theorems are retained as inherited inputs,
not independently re-proved by this maintenance pass.

## Per-paper formula and prerequisite review

| Paper | Source location | Bounded check and limit |
|---|---|---|
| TPC255 | [literal operator](../../papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/paper/main.tex#L58); [adjoint compiler](../../papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/paper/main.tex#L94); [unit masks](../../papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/paper/main.tex#L175) | The ordered split requires N≥2. Outer q, both unit masks, deleted diagonal, and kernel conjugation are retained. Complete-row zero requires the fixed smooth band-limited profile and H>2Q, not merely a finite test kernel or a centered row on a truncated interval. The returned diagonal is a term in an exact identity, not a nonvanishing theorem for the paired scalar. |
| TPC256 | [divisor layers](../../papers/tpc-256-literal-beta-haar-adjoint-asymptotic/paper/main.tex#L117); [curvature](../../papers/tpc-256-literal-beta-haar-adjoint-asymptotic/paper/main.tex#L162); [boundary estimates](../../papers/tpc-256-literal-beta-haar-adjoint-asymptotic/paper/main.tex#L292); [complex phase](../../papers/tpc-256-literal-beta-haar-adjoint-asymptotic/paper/main.tex#L341) | Divisor density cancels layer by layer between normalized consecutive child means, without Mertens cancellation. Prime powers contribute 1/k, not just a prime indicator. The fixed smooth profile supplies Schwartz decay; q<H is used in the first-moment estimate. Dominance chooses one fixed 0<epsilon<1/48 after the remainder bounds. Eventual negative real part does not make the scalar real or fix a principal-argument branch. |
| TPC257 | [four-block frame](../../papers/tpc-257-four-block-haar-transverse-norm-floor/paper/main.tex#L89); [curvature table](../../papers/tpc-257-four-block-haar-transverse-norm-floor/paper/main.tex#L188); [variation compiler](../../papers/tpc-257-four-block-haar-transverse-norm-floor/paper/main.tex#L211); [norm floors](../../papers/tpc-257-four-block-haar-transverse-norm-floor/paper/main.tex#L294) | All four blocks must be nonempty, equivalent here to N≥4. Balanced rank splitting supplies sizes comparable to x; arbitrary partitions need not. Variation is for the zero extension, including both outer jumps. Parseval gives exact projected energies, and projection inclusion gives a lower bound for the larger transverse output; neither is a full-vector upper bound. |
| TPC258 | [null direction](../../papers/tpc-258-source-frozen-transverse-null-direction/paper/main.tex#L323); [null theorem](../../papers/tpc-258-source-frozen-transverse-null-direction/paper/main.tex#L345); [conditional rate](../../papers/tpc-258-source-frozen-transverse-null-direction/paper/main.tex#L367) | Both displayed logarithm ratios exceed one, so LT is strictly positive. The direction uses fixed real coefficients and the same orthonormal frame at each clock. It cancels the limiting diagonal vector, not the exact finite output. A fixed linear combination of two little-oh errors remains little-oh; no fixed-power rate follows from that headline interface alone. The source's conditional refinement remains labeled conditional. |
| TPC259 | [hybrid interval input](../../papers/tpc-259-same-clock-null-coupling/paper/main.tex#L152); [rank-one identity](../../papers/tpc-259-same-clock-null-coupling/paper/main.tex#L206); [channel estimate](../../papers/tpc-259-same-clock-null-coupling/paper/main.tex#L237); [synthetic witness](../../papers/tpc-259-same-clock-null-coupling/paper/main.tex#L287) | The same actual w, beta, operator, profile, ordered blocks, and clock must be used in both factors. Freeze admissible finite K and fixed M before taking x large; constants and thresholds are not uniform in growing M or K. Unit z gives the conjugated projection coefficient. Orthogonality to z alone does not annihilate the residual pairing with A beta. The zero-diagonal witness is explicitly synthetic, not a literal prime-shell construction. |

## Preserved source issues and interface boundaries

### TPC255: reflected conjugation, period means, and nonzero wording

The [Poisson proof](../../papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/paper/main.tex#L127)
sets `phi(v)=conjugate(psi_+(-v))`, then identifies its kernel as
`conjugate(K_H(-h))`. For the same Fourier-transform convention used in
`K_H(h)=hat(psi_+)(h/H)`, direct substitution gives instead

```text
hat(conjugate(psi_+(-.)))(xi) = conjugate(hat(psi_+)(xi)),
hat(conjugate(psi_+))(xi)    = conjugate(hat(psi_+)(-xi)).
```

Thus the displayed profile actually supplies `conjugate(K_H(h))`, the kernel
needed by the defined adjoint row. The extra minus sign in the prose kernel
identification is not generally valid without evenness. The same wording
appears in [proof-package lines 36–40](../../papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/PROOF_PACKAGE.md#L36).
Both transforms still have support in the symmetric interval [-1,1], so this
local identification issue does not by itself refute the complete-row zero;
the inherited analytic theorem and its attachment are not independently
certified here. Neither original text is silently corrected.

The [proof-package unit-mask paragraph](../../papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/PROOF_PACKAGE.md#L60)
calls `−1/(q−1)` and `+1/(q−1)` the two period means. They are period
**sums**. The means are `−1/[q(q−1)]` and `+1/[q(q−1)]`, respectively.
The [manuscript](../../papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/paper/main.tex#L182)
correctly prints the sums and the additional 1/q in its zero-frequency
terms. For q=5, the first sum is −1/4 and its mean is −1/20. These quantities
must not be exchanged with the different normalization K_H(0)=integral psi=1.

The [README](../../papers/tpc-255-exact-adjoint-diagonal-boundary-compiler/README.md#L9)
says deleting the diagonal returns a nonzero local term. Read this as the
structural return, subject to its actual coefficient and domain: q=2 has
(q−2)/(q−1)=0, an empty shell has no return, and a beta pairing can cancel.
The manuscript abstract and README claim firewall explicitly do not prove
a nonzero scalar. That narrower boundary remains controlling.

### TPC256–257: exact rates, domains, and projection direction

The [TPC256 boundary exponent](../../papers/tpc-256-literal-beta-haar-adjoint-asymptotic/paper/main.tex#L325)
contains a literal extra comma, `x^{,1/3+2(21/32)-1/2+o(1)}`. It is retained,
not repaired. The arithmetic without that source punctuation is

```text
133/400 − 1/2 = −67/400,
1/3 + 2(21/32) − 1/2 = 55/48,
7/6 − 55/48 = 1/48.
```

The gap is before epsilon: the remainder-to-main ratio is
`x^(−1/48+epsilon) log^3 x`, which tends to zero only with a suitably fixed
epsilon. The kernel is fixed and smooth, not merely a function with compact
support on the profile side. The dyadic weighted-prime coefficient 9/2 uses
both the 3/2 shell integral factor and `log Q=(log x)/3`.

The [TPC257 divisor proof](../../papers/tpc-257-four-block-haar-transverse-norm-floor/PROOF_PACKAGE.md#L102)
mentions equal leading-width intervals. Exact layerwise density cancellation
does not require the two finite lengths to be equal: after division by p
and q, both leading densities are 1/d. Comparability to x is needed for the
stated asymptotic scale, not for that algebraic cancellation.

For a zero-extended step vector z, the elementary translation inequality
`sum_t |z(t+h)−z(t)| ≤ |h| TV(z)` records all jumps. It explains the
bounded-variation estimate without assuming that only the old midpoint
boundary survives. The three-dimensional frame is fixed in size; no
uniformity over a growing Haar family follows.

### TPC258–259: rate labels and an explicit retained residual

The [TPC258 rate marker](../../papers/tpc-258-source-frozen-transverse-null-direction/README.md#L67)
reads `CONDITIONAL_THEOREM_LOG_ONE_OVER_X`. Its actual mathematical
display is `S_x/log x + x^(55/48+epsilon)`, not `S_x/x`. Preserve the marker
literally but use the displayed formula to interpret its scale. This audit
does not promote or replace the released conditional theorem.

The formal error `1/sqrt(log x)` tends to zero while its ratio to any
`x^(−delta)` tends to infinity. This is an interface counterexample to
little-oh implying a fixed power; it is not an actual V59 output. Likewise,
arbitrary **fixed** logarithmic savings for w cannot be made polynomial by
selecting M=M(x) without a uniform theorem.

The [TPC259 finite-clock identity](../../papers/tpc-259-same-clock-null-coupling/paper/main.tex#L217)
says “every finite clock.” Its source-defined four-block z still requires
an admissible clock with nonempty blocks; it is not defined at N<4. The
algebra itself is valid for any finite-dimensional unit z. In the source
normalization, the exponent products check exactly:

```text
1/2 + 7/6 = 5/3,
1/2 + 55/48 = 79/48,
5/3 − 79/48 = 1/48.
```

The four-block input was traced to [TPC254's H2 statement](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/paper/main.tex#L77)
and [its m=1 extraction](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/paper/main.tex#L122):
the summands are nonnegative, the m=1 weight is one, and its maximum covers
every active consecutive interval before selecting any block. This is a
local source-contract comparison, not a re-proof of the upstream hybrid
comparison or its prime-progression inputs. The corresponding TPC259
source-marker checks were inspected only as provenance/schema checks, not
as an independent proof of the analytic assertion.

## Independent bounded checks actually executed

- A six-coordinate Gaussian-rational fixture on I={1,...,6}, split 3+3,
  with q in {3,5,7}, rational test h=±1/3, synthetic
  `beta(t)=(-1)^t/(t+1)`, and noneven nonreal kernel
  `K(d)=(1+i d/2)/(1+d^2)` for −3≤d≤4 and zero elsewhere checks all six
  adjoint coordinates, 15 unit-input jump rows, the conjugate pairing, and
  both diagonal formulas. Its pairing is
  `101869/2570400 + i 1552511/5140800`; its diagonal lane is `11099/5040`.
  The complete-row term is retained, not set to zero for this nonphysical
  finite-support kernel. PASS.
- Exact period sums/means and the diagonal coefficient were checked for
  q=2,3,5,7. This includes the zero q=2 diagonal. PASS.
- Five independent rank-frame sizes N=4,5,7,8,11 check weighted norms,
  orthogonality, zero mean, zero-extension variation, and translation bounds
  at h=−3,−1,1,4. Normalizing square roots are accounted for by their exact
  rational squares. Consecutive-interval divisor discrepancy bounds were
  checked at d=2,3,5,7. PASS.
- Symbolic evaluation of the three integrals using `y log y−y` verifies
  exactly the logarithm ratios 32/27, 3456/3125, and 884736/823543.
  Symbolic positive L1,L2 checks verify the unit null normalization and
  exact leading cross cancellation. No prime sample was used. PASS.
- An independent nonreal w,g example verifies the conjugated rank-one
  identity. The source's structural zero-diagonal witness was checked at
  lambda=−3,1/2,4; in each case the null channel is zero and the residual is
  the entire scalar lambda. These are synthetic checks only. PASS.
- All displayed rational exponent identities above were checked exactly.

Supplemental read-only sources remain byte-identical to the source commit:

| Source | SHA-256 |
|---|---|
| [TPC254 TeX, scoped H2/extraction excerpts](../../papers/tpc-254-source-backed-rank-midpoint-hybrid-mean-closure/paper/main.tex#L55) | `5d1bb10430c3f56e720e62c5d58a018a2c56d7b771eb815d4e8a1127555150a6` |
| [TPC259 provenance/marker and rank-domain code excerpts](../../papers/tpc-259-same-clock-null-coupling/code/tpc259_null_coupling_certificate.py#L46) | `053828e13ed92497593e360dc4bd2655f7b9f19a5845e1920ddd95a843f72b30` |

The source claims and route labels are preserved as historical author
statements. Mechanical preservation and these bounded checks do not certify
the complete manuscripts as independently semantically verified. No new
arithmetic advance, full-output estimate, fixed-power payment, or TPC419 is
created; the current TPC418 scientific stop remains unchanged.
