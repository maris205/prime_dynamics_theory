# TPC220–224 conversion and bounded prerequisite audit

Updated 2026-09-08. Preserved source commit:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. Five existing manuscripts only;
no new paper, source repair, theorem, or publication release.

## Mechanical evidence and limits

The conversion preflight retains 300 math nodes and 56 raw displayed-equation
blocks over 17 preserved PDF pages. All five source locks and complete
abstract/body formula and normalized-text roundtrips pass. The per-paper
records retain exact source/PDF hashes, raw display catalogues, and original
source-line/PDF-heading candidates. TPC223 has one unresolved automatic
heading match; that limitation is not a missing manuscript section.

This is mechanical preservation, not a proof audit, numerical reproduction,
source/PDF synchronization certificate, or reliable full-content review.
Original manuscripts and historical numerical/release claims remain intact.
`reliable-full-md` remains unearned. The independent bounded source-reading
receipt is recorded separately below.

TPC418 retains arithmetic advance `NO`, fixed-power credit `0`, full Gate B
`OPEN`, and `NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`. This maintenance
does not reopen that route or create a paper number.

## Independent source-reading scope

Read-only task `tpc-maintenance-source-scope-220-224-20260908` returned
`SCOPED_ARCHIVE_REVIEW_ONLY`. It fully read 20 manuscript/package text files,
1,864 original LF-delimited lines, and all ten committed manuscript PDFs:
17 unique pages, or 34 pages counting both identical aliases. Each paper's
versioned main.pdf and paper.pdf are byte-identical; the converter selects
main.pdf. No local TeX child input was invoked or missing.

All 30 original text/PDF hashes matched the declared baseline Git blobs.
The sorted original-source hash-ledger digest is
`03d4b035dc044694de32e42844ee011f9a19436318b50bf79356001c822337ee`.
The reviewer changed no files and did not rerun the parent's conversion
checks or independently rehash the parent's preexisting untracked manifest.

TPC220–223 use inline thebibliography entries. Their separately preserved
references.bib files were also read and hashed but are not invoked by those
roots. TPC224 invokes its local references.bib. All text sources end in LF
and contain no CR. Initial/final HEAD and handoff matched the declared task
locks; the handoff snapshot was
`88419d30d9393710f7f3800972cef7baa787060f925985c5aa2e9a3b0c103b9d`.

## Per-paper premises and formula boundaries

| Paper | Original source anchors | Bounded qualification |
|---|---|---|
| TPC220 | [rows and cutoffs](../../papers/tpc-220-prime-ap-collision-crosswalk/paper/main.tex#L47); [crosswalk](../../papers/tpc-220-prime-ap-collision-crosswalk/paper/main.tex#L68); [collision/diagonal](../../papers/tpc-220-prime-ap-collision-crosswalk/paper/main.tex#L108) | Finite prime labels, H>0, unit q modulo h, primitive residues, literal floor cutoff, gcd(m,h)=1, and the original congruence mask. AP weights may be complex; cross-profile collision products retain the second-factor conjugate. Only diagonal reduction needs 2L<h. The global cutoff bound additionally uses q≤2Q, although the dyadic set is not separately defined locally. Raw residue sums supply no physical averaging or fixed-h0 identification. |
| TPC221 | [Gram definition](../../papers/tpc-221-collision-graph-schur-envelope/paper/main.tex#L57); [PSD/energy statement](../../papers/tpc-221-collision-graph-schur-envelope/paper/main.tex#L75); [Schur bound](../../papers/tpc-221-collision-graph-schur-envelope/paper/main.tex#L93) | Finite masked primitive rows, one profile, unit prime labels. Auxiliary Schur weights must be strictly positive; the printed maximum needs nonempty labels or a separate empty-set convention. PSD and an absolute Schur bound must not hide the complex energy-identification discrepancy below. Modulus h=5 in the finite saturation is not physical h0. |
| TPC222 | [Hilbert convention](../../papers/tpc-222-four-packet-cross-term-obstruction/paper/main.tex#L36); [polarization](../../papers/tpc-222-four-packet-cross-term-obstruction/paper/main.tex#L70); [trace](../../papers/tpc-222-four-packet-cross-term-obstruction/paper/main.tex#L94) | Four vectors in one complex Hilbert space, conjugate-linear-first inner product, and arbitrary complex coefficients. Polarization uses i^(-r)/4. Trace is an unsigned upper envelope; rank-one sharpness still needs an appropriate top-eigenspace coefficient. Abstract fixture phases do not supply canonical arithmetic signs, masks, clocks or physical normalization. |
| TPC223 | [three-line interface](../../papers/tpc-223-conditional-signed-reassembly-compiler/paper/main.tex#L63); [conditional theorem](../../papers/tpc-223-conditional-signed-reassembly-compiler/paper/main.tex#L87); [package interface](../../papers/tpc-223-conditional-signed-reassembly-compiler/PROOF_PACKAGE.md#L5) | All three channel/reassembly inputs must use the same literal object, clock and normalization. Nonnegative ledger parameters give the conditional upper-bound saving min(δ_AP,κ_pol)−λ_struct. Strict endpoint payment requires saving greater than 1/400, not equal to it; varying ledgers need a uniform positive gap. The compiler does not prove its own missing arithmetic/physical inputs. |
| TPC224 | [common family](../../papers/tpc-224-literal-two-channel-compatibility-audit/paper/main.tex#L97); [common-vector theorem](../../papers/tpc-224-literal-two-channel-compatibility-audit/paper/main.tex#L132); [package domain](../../papers/tpc-224-literal-two-channel-compatibility-audit/PROOF_PACKAGE.md#L44) | One common finite vector family, identical support/normalization in all channels, positive P,J for nontrivial sharpness, and positive denominators for ratios. The bound is E_all≤min(J E_AP,P E_pol)≤PJ/(P+J)(E_AP+E_pol). Its displayed residue/frequency family is not explicitly primitive, unlike TPC220. Common synthesis preserves inequalities but is not proved isometric to a physical-window norm. |

## Preserved discrepancies and source qualifications

### TPC221: complex Gram/energy convention

The [Gram](../../papers/tpc-221-collision-graph-schur-envelope/paper/main.tex#L57)
is Gamma_qq'=sum_a B_q(a) conjugate(B_q'(a)), but the
[energy identity](../../papers/tpc-221-collision-graph-schur-envelope/paper/main.tex#L75)
uses lambda* Gamma lambda for the norm of sum_q lambda_q B_q. Direct
expansion with that Gram gives lambda^T Gamma conjugate(lambda).
For the generic one-coordinate rows B=(1,i) and coefficients lambda=(1,i),
the row-sum energy is 0 but the printed quadratic form is 4. Real Gram data
avoid this mismatch; the theorem states unrestricted complex weights without
that restriction. The README/package also repeat the identity.

The Gram definition is on PDF page 1 and the energy theorem/proof on page 2.
This finite convention check is not a reproduction of a numerical artifact
or evidence about canonical physical rows. PSD and the absolute Schur
envelope remain separate from the printed energy identification. The parent
spot-checked both original definitions before archiving this qualification.

### TPC222: numbering and Rayleigh-quotient wording

The [package's “Theorem 3”](../../papers/tpc-222-four-packet-cross-term-obstruction/PROOF_PACKAGE.md#L18)
combines material that the PDF instead labels Corollary 3 (trace envelope)
and Theorem 4 (cross-term obstruction), both on page 2. Do not invent a PDF
Theorem 3 locator. The [abstract](../../papers/tpc-222-four-packet-cross-term-obstruction/paper/main.tex#L22)
calls c*Gc a Rayleigh quotient without normalizing c; the quotient requires
nonzero c and division by its squared norm. Later norm identities retain
the explicit conjugate-linear-first convention.

### TPC223: the interface reference names only its first equation

The [label](../../papers/tpc-223-conditional-signed-reassembly-compiler/paper/main.tex#L68)
sits on the first line of a three-equation alignment, so the theorem prints
“Assume (1)” on PDF page 2. Its proof and package need all of equations
(1)–(3): AP bound, polarized bound, and reassembly/identification. Equation
(1) alone does not imply the conclusion. The intended full interface is
recorded here without rewriting the original. The parent spot-checked the
label placement and the proof's use of all three inputs.

The review's small rational calculation checks the printed ledger values
11/1200, margin 1/150, compiled exponent 663/400 and target 1997/1200 only;
it does not reproduce a stored certificate or establish physical saving.

### TPC224: unresolved ratio normalization and package wording

The [source-surrogate table](../../papers/tpc-224-literal-two-channel-compatibility-audit/paper/main.tex#L203)
prints “sharp ratio” one in all nine rows although unit ratios are about
0.799. The [later stress-clock description](../../papers/tpc-224-literal-two-channel-compatibility-audit/paper/main.tex#L230)
normalizes a sharp ratio by dividing the unit ratio by PJ/(P+J). If Table 1
uses this same normalization, its displayed values are inconsistent: its
Q=11,P=3,J=4 row gives 0.799023/(12/7)=0.46609675, not one. A different
Table-1 denominator is not defined locally. Keep this as an unresolved
source/table qualification; no producer interpretation or corrected data
is inferred. The parent spot-checked both the table and stress-clock prose.

The [proof package](../../papers/tpc-224-literal-two-channel-compatibility-audit/PROOF_PACKAGE.md#L55)
has a second bare `qquad` without a backslash; the corresponding manuscript
prose does not. The [README](../../papers/tpc-224-literal-two-channel-compatibility-audit/README.md#L19)
calls the scalar min-to-sum inequality an identity, although equality need
not hold for arbitrary nonnegative inputs. These originals remain unchanged.

The manuscript's “any finite” label set allows P=0, whereas the package
requires positive P,J. Empty-label energy inequalities are trivial but do
not support the same nonzero aligned-ratio sharpness argument; retain P≥1
for that claim. A unit-factor failure generally requires PJ>P+J; P,J>2 is
sufficient but not exhaustive.

The [source-surrogate clock](../../papers/tpc-224-literal-two-channel-compatibility-audit/paper/main.tex#L189)
uses x=Q³,H=4Q²,h=4Q and four specified affine profiles. The separate stress
clock uses H=5Q,h=5, constant profiles and selected q≡1 mod 5 primes.
These are separate finite controls, not interchangeable V46 asymptotics or
canonical arithmetic sign patterns.

## Existing-PDF manual locators

One-based actual PDF pages apply equally to the two committed aliases.
Section starts follow numbered headings, not prose mentions. The source
lines below belong to the original paper/main.tex, not to a reading layer.

| Paper | Original section-start lines → PDF pages | Other locators |
|---|---|---|
| TPC220 | 37→1; 66→2; 98→2; 140→3; 164→3; 177→3 | Theorems 1–2: 2; Table 1 and References: 3. |
| TPC221 | 37→1; 73→2; 131→2; 163→3; 195→3 | Theorems 1–3: 2; Theorem 3 proof continues 3; Table 1 and References: 3. |
| TPC222 | 34→1; 68→2; 109→2; 138→3; 169→3 | Theorem 1: 1; Theorem 2, Corollary 3, Theorem 4: 2; Table 1 and References: 3. |
| TPC223 | 45→1; 61→1; 85→2; 122→2; 162→3; 180→3 | Section 2 continues 2; Remark 1 and Theorem 1: 2; Table 1: 3 although section 4 starts 2; References: 3. |
| TPC224 | 61→1; 95→2; 130→2; 187→3; 259→4; 290→4 | Theorem 3.1: 2, proof continues 3; Remark 3.2: 3; Table 1 floats onto 3 above the continued proof; Table 2: 4; References: 4–5. |

TPC223's manual supplement does not make its unresolved automatic heading
match unique. Text extraction is not rendered-page visual certification.

## Source-audit command evidence and exclusions

The reviewer reported 14 shell invocations, all exit 0: five discovery
commands and nine standard-library stdin programs for complete text reads,
source/blob hashing, PDF extraction, final metadata and bounded complex/
fraction checks. Ten pdfinfo and ten pdftotext stdout subprocesses exited 0
with empty stderr. A transport-truncated text response was followed by
complete rereads of the affected TPC223/TPC224 material. All final manuscript
diffs were empty; the index was empty and the same nine preexisting tracked
dirty-path names remained.

The handoff content inspection included lines 1–220 and 335–445, plus a
keyword scan with historical hits. This exceeded the assigned current-entry
content boundary; those historical lines were not used as scientific
evidence. Do not describe the inspection as perfectly range-confined.
The 433-versus-411 untracked-count change initially caused a coordination
hold; parent attribution to the 22 new maintenance files resolved it.
The parent separately verified preservation hashes; the source reviewer
did not independently repeat that manifest comparison.

No scientific producer/checker/certificate, broad test collection, TeX
build, PDF rendering, archive release, upstream scientific source or network
was invoked. Analytic citations and all historical certificate claims remain
unverified. AP dispersion, polarized cross-correlation, common physical
identification, fixed physical h0, zero/nonunit/fixed-atom transfer, growing
uniformity, arithmetic L2 and strict endpoint payment remain open.
