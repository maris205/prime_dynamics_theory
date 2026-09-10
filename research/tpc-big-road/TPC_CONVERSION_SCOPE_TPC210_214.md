# TPC210–214 conversion and bounded prerequisite audit

Updated 2026-09-08. Preserved source commit:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. Five existing manuscripts only;
no new paper, scientific source repair, theorem, or publication release.

## Mechanical evidence and limits

The conversion preflight retains 573 math nodes and 117 raw displayed-
equation blocks over 33 preserved PDF pages. All five source locks and full
abstract/body formula and normalized-text roundtrips pass. The original TeX,
invoked bibliography and PDF hashes, display catalogues and original-line/
PDF-heading candidates are retained in the per-paper conversion records.
TPC214 has one unresolved automatic heading match; it remains explicit.

TPC210–212 have no PROOF_PACKAGE.md. Existing source-lock, theorem-ledger and
route-evaluation notes provide bounded context, not substitute proof-package
or full semantic-verification receipts. Bibliographies are retained literally;
citation keys and theorem numbering are not reconstructed.

This is mechanical preservation, not numerical reproduction, source/PDF
synchronization certification, or reliable full-content review. The converter
and source-input helper are unchanged in this continuation. Independent
bounded source-reading evidence is recorded below.

TPC418 retains arithmetic advance `NO`, fixed-power credit `0`, full Gate B
`OPEN`, and `NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`. No source-location
or maintenance check reopens the research route or creates a paper number.

## Independent source-reading scope

Read-only task `tpc-maintenance-source-scope-210-214-20260908` returned
`SCOPED_ARCHIVE_REVIEW_ONLY`, with no fatal mismatch and no changed files.
It fully read 26 manuscript text files, 3,595 original LF-delimited lines:
five READMEs, five complete TeX roots, five invoked bibliographies, nine
permitted notes for TPC210–212, and two proof packages for TPC213–214.
No local TeX child is invoked. All five derivation packages are absent.
The nine notes are limited source context, not substitute proof packages.

All 31 original manuscript text/PDF files matched baseline Git blobs.
Only paper/paper.pdf is versioned in each directory; no main.pdf alias was
assumed. All five preserved PDFs were completely extracted once, 33 pages.
The sorted 31-file manuscript hash-ledger digest is
`46d8129d1b239d27d678624999331b32025061dbc6bc89202b7c1a22ef1b4da8`.
Serialization is SHA-256, two spaces, repository-relative path and LF,
sorted by path. Initial/final HEAD matched the declared commit and the
worktree handoff matched the task lock
`cdeb2f3cbac97aa98037ad138681826195734d35a6aa1a793393417b78ccde03`.

## Per-paper premises and formula boundaries

| Paper | Original source anchors | Bounded qualification |
|---|---|---|
| TPC210 | [finite realization](../../papers/tpc-210-poisson-profile-realizability/paper/main.tex#L107); [alignment](../../papers/tpc-210-poisson-profile-realizability/paper/main.tex#L201); [polarization](../../papers/tpc-210-poisson-profile-realizability/paper/main.tex#L249) | Prime q>2, finite dimension N=q−1, counting-space projection, unit divisors and independent Schwartz packets. Alignment needs squarefree divisors and a centered vector; the displayed energy ratio additionally needs a nonzero denominator. The packet realization is finite and does not impose canonical arithmetic profiles or a growing norm bound. |
| TPC211 | [CRT source](../../papers/tpc-211-product-coupled-euler-gram/paper/main.tex#L109); [normalization](../../papers/tpc-211-product-coupled-euler-gram/paper/main.tex#L155); [dual endpoint](../../papers/tpc-211-product-coupled-euler-gram/paper/main.tex#L469) | Distinct odd active primes, every one above z, CRT counting inner product and local Fourier factor 1/p. Endpoint cancellation requires a complete packet with at least two primes. The Gram-dual endpoint needs a fixed complex inner-product convention and supplies neither arithmetic identification nor uniform norm control. |
| TPC212 | [selector](../../papers/tpc-212-truncated-boundary-emitter/paper/main.tex#L145); [occupancy operator](../../papers/tpc-212-truncated-boundary-emitter/paper/main.tex#L301); [weighted collision](../../papers/tpc-212-truncated-boundary-emitter/paper/main.tex#L318) | Finite nonempty-prime-subset selector and integer incidence coefficients. Reciprocal formulas need unit q modulo d. Full rank/alignment needs nonzero occupancy rows. Unit weights are a fixture; an incidence operator and its output on the all-ones vector are distinct objects. |
| TPC213 | [common source](../../papers/tpc-213-physical-profile-cross-gram/paper/main.tex#L126); [package orthogonality](../../papers/tpc-213-physical-profile-cross-gram/PROOF_PACKAGE.md#L47); [detailed proof](../../papers/tpc-213-physical-profile-cross-gram/PROOF_PACKAGE.md#L112) | One finite common support, source, corrections and emitter rows; unnormalized positive-exponent Fourier transform. The scalar pullback is bilinear and must be distinguished from the Hermitian Gram. Simplified orthogonality is on complete periods, with the relevant rational frequency difference times the period integral. |
| TPC214 | [dilation hypotheses](../../papers/tpc-214-mobius-frequency-clusters/paper/main.tex#L112); [zero axis](../../papers/tpc-214-mobius-frequency-clusters/paper/main.tex#L162); [cluster theorem](../../papers/tpc-214-mobius-frequency-clusters/paper/main.tex#L186) | Finite squarefree family, one common unit-q set, height and emitter function, and integer cutoffs. Use the common family period L, not separate pair periods. Omitting reduced denominator h=1 requires the additional zero-axis hypothesis; complex emitter rows require conjugation in cross products. |

## Preserved source discrepancies and qualifications

### TPC210–211: lattice, ratios, and complex conventions

- TPC210 has literal bare `qquad` at [line 111](../../papers/tpc-210-poisson-profile-realizability/paper/main.tex#L111),
  also extracted on PDF page 2. Its [lattice wording](../../papers/tpc-210-poisson-profile-realizability/paper/main.tex#L149)
  says distinct points of one residue lattice are exactly one apart; that
  spacing applies to consecutive points. Its [isolation proof](../../papers/tpc-210-poisson-profile-realizability/paper/main.tex#L177)
  cites 2rho_q<1, but the relevant cross-residue spacing is 1/q; the specified
  rho_q=1/(4q) supplies the stronger comparison actually needed.
- TPC210's [alignment statement](../../papers/tpc-210-poisson-profile-realizability/paper/main.tex#L201)
  permits a zero centered vector or empty family but displays an energy
  ratio without a positive-denominator restriction. Its polarization uses
  a linear-first convention, and its later [M notation](../../papers/tpc-210-poisson-profile-realizability/paper/main.tex#L288)
  has no locally fixed normalization.
- TPC211's [prime hypotheses](../../papers/tpc-211-product-coupled-euler-gram/paper/main.tex#L109)
  give z<p_1 without explicitly ordering the primes; every active prime must
  remain above z. Its [dual system](../../papers/tpc-211-product-coupled-euler-gram/paper/main.tex#L469)
  cannot treat complex inner-product convention/conjugation as harmless.
  The following source limitation explicitly leaves arithmetic realization
  and growing norm control open.

### TPC212: occupancy output versus operator norm

The [README](../../papers/tpc-212-truncated-boundary-emitter/README.md#L26)
defines an incidence operator E_d but assigns it the ordered-collision norm.
The [manuscript](../../papers/tpc-212-truncated-boundary-emitter/paper/main.tex#L301)
distinguishes that operator from N_d=E_d applied to the all-ones vector:
the collision count is the squared norm of N_d, not generally the squared
operator norm. The parent spot-checked both definitions before archiving
this discrepancy.

The README also omits the two-prime condition present in the manuscript.
The [emitter description](../../papers/tpc-212-truncated-boundary-emitter/paper/main.tex#L313)
calls mu(d)log(d)/d nonzero in an earlier general d≥2 setting; squarefreeness
is required. A later [integer-d selector notation](../../papers/tpc-212-truncated-boundary-emitter/paper/main.tex#L491)
needs the explicit S-to-d_S identification from the original subset selector.

### TPC213: complete-period orthogonality and inherited scalar

The [package summary](../../papers/tpc-213-physical-profile-cross-gram/PROOF_PACKAGE.md#L47)
claims a geometric sum vanishes for every noninteger alpha, omitting the
condition L alpha is integral. Its [detailed proof](../../papers/tpc-213-physical-profile-cross-gram/PROOF_PACKAGE.md#L112)
supplies that condition for alpha=r/d−s/e. Thus the proof's rational-period
setting and the overbroad summary are distinct; the parent checked both.

The [TPC211 bibliography title](../../papers/tpc-213-physical-profile-cross-gram/paper/references.bib#L10)
differs from TPC211's original title. Identifying abstract source vectors
with the intended residual also needs TPC211's retained 1/log u factor;
symbol matching does not establish that attachment.

### TPC214: zero-axis premise, conjugation, and profile class

The [cluster theorem](../../papers/tpc-214-mobius-frequency-clusters/paper/main.tex#L186)
invokes only the dilation lemma's hypotheses, yet its proof deletes h=1
using a [zero-axis corollary](../../papers/tpc-214-mobius-frequency-clusters/paper/main.tex#L162)
that additionally requires every q<H. The package records that requirement;
the theorem's assumption line does not. This is an omitted local hypothesis,
not a source repair or a new physical cancellation statement.

The [pairwise expansion](../../papers/tpc-214-mobius-frequency-clusters/paper/main.tex#L223)
omits conjugation of B_e(s), although complex profiles are allowed. It needs
a real-valued restriction or the Hermitian conjugate factor. The parent
spot-checked both the zero-axis dependency and the printed cross product.

The [README](../../papers/tpc-214-mobius-frequency-clusters/README.md#L89)
and [conclusion](../../papers/tpc-214-mobius-frequency-clusters/paper/main.tex#L347)
call (1+t²)^−2 Schwartz. Its algebraic t^−4 decay is not Schwartz decay;
the fixture section correctly calls it smooth and even. The finite rational
profile and original prose are preserved, not silently replaced.

## Existing-PDF manual locators

One-based physical pages; section ranges include continuation text. All
abstracts and claim-level paragraphs are on page 1. The preserved source
for each paper is paper/paper.pdf.

| Paper | Numbered sections in order | Subsections/theorems and supplements |
|---|---|---|
| TPC210 | 1–2, 2, 2–3, 3–4, 4, 5, 5, 5–6 | Theorem 3.1/Remark 3.2: 3; Proposition 4.1: 3, proof through 4; Proposition 5.1: 4; table: 5; References: 6. |
| TPC211 | 1–2, 2–3, 3–4, 4–5, 5–6, 6–7, 7, 7 | Proposition 2.1: 3; Theorem 3.1: 3, proof through 4; Remark 3.2/Lemma 4.1: 4; Theorem 4.2: 4–5; Proposition 5.1/Theorem 6.1: 6; table: 7; References: 8. |
| TPC212 | 1–2, 2–4, 4–5, 6–7, 7, 7–8 | Subsections 2.1: 2–4; 2.2: 4; 3.1: 4–5; 4.1: 6; 4.2: 6–7; 5.1/5.2: 7. Lemma 2.1/Theorem 2.2: 3; Example 2.3/Proposition 2.4/Remark 2.5: 4; Lemma 3.1/Proposition 3.2/Remark 3.3: 5; table: 6; References: 8. |
| TPC213 | 1–2, 2–3, 3, 4, 4–5, 5–6, 6 | Subsections 2.1: 2–3; 5.1: 4–5; 5.2: 5. Theorem 2.1/Remark 2.2/Proposition 3.1/Corollary 3.2: 3; Theorems 4.1/4.2/Corollary 4.3/Remark 4.4: 4; table: 5; References: 6. |
| TPC214 | 1–2, 2, 3, 4, 4–5, 5, 5 | Lemma 2.1/Corollary 2.2: 2; Theorem 3.1/Corollary 3.2: 3; Proposition 4.1/Remark 4.2 and table: 4; References: 5. |

TPC210,211,214 have no numbered subsections. TPC214's one automatic heading
ambiguity remains explicit; a manual locator does not make it a unique
automatic match. TPC212 labels in unnumbered displays at original TeX lines
260,268,356,362,367 reuse printed (2.4)/(3.2) references on pages 4–6;
those are not unique equation-number locators. Conjugation marks are not
reliably recovered by text extraction, and no rendered-page QA is claimed.

## Commands, exclusions, and stop

Scoped Git tree/blob/hash comparisons, sha256sum, line counts, complete
numbered text reads, bounded source searches and pdftotext stdout extractions
all exited 0. An initial uppercase directory-navigation search exited 1
with no matches; the lowercase search succeeded. No failed source-lock or
PDF extraction check occurred. AGENTS was fully read and handoff content
reads stayed within the assigned lines 1–45 and 425–462.

TPC211 retains schematic outer −H, inner mu(d)log(d)/d, profile psi(Hm/dq),
reciprocal mask, nonzero integer cutoff and divisor band, plus 1/log u.
This does not identify the complete canonical physical coefficient, signs,
masks or outer labels. A printed +2 shift is not an independently locked
physical h0, and TPC210's N=q−1 is a finite dimension, not a growing clock.

No scientific module/test, producer/certificate, TeX build, PDF render,
network, upstream proof record, Git mutation or file write was invoked by
the reviewer. Parent maintenance changes were acknowledged, not audited.
Uniform physical X/N/q domains, exceptions, actual shell/support, common
clock, four-packet attachment, (q−2) subtraction, block reassembly and strict
1/400 loss remain unpaid. Reliable full-content/semantic review is unearned.
