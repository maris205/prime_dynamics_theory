# TPC147–149 conversion and bounded prerequisite audit

Updated 2026-09-09. Preserved source commit:
`ab23455ba941e5a14ded27d49de0e874aee811ac`. Three existing manuscripts only;
no new paper, original-source repair, theorem, or publication release.

## Mechanical evidence and limits

Preflight retains 289 math nodes and 50 raw displayed-equation blocks over
12 preserved PDF pages. Source locks and full abstract/body formula and
normalized-text roundtrips pass. Original hashes and automated heading
matches remain in each conversion record. Automatic section matches are
unique, which does not certify TeX/PDF synchronization or visual quality.

All three use root main.tex and an exact-basename original PDF. Reading
layers stay at paper/main.md; no source is copied or moved. Complete
invoked bibliographies are retained, not externally verified or formatted
into invented entries. No separate PROOF_PACKAGE.md is present.

The converter and maintenance helpers are unchanged. All 24 targeted
coverage/inventory/source-link tests pass in normal and optimized modes.
Neither full semantic verification nor reliable-full-md is earned.

## Independent original-source audit

Read-only task `tpc-maintenance-source-scope-147-149-20260909` completed
all required original text and full PDF-extraction reads. No required
original file or page remains unread; first fatal is NONE and the
supported level is SCOPED_ARCHIVE_REVIEW_ONLY. The nine complete README,
main.tex and references.bib texts total 1,336 raw LF characters and
43,659 bytes. The three PDFs total 12 pages and 1,222,500 bytes;
all 12 originals total 1,266,159 bytes. Discovery, including ignored
filenames, found no local TeX children, alternative paper/main.tex,
separate proof/derivation package or original notes/*.md.

All 12 originals matched baseline Git blobs by direct raw-byte and
SHA-256 equality, at start and finish. The unchanged canonical ledger
SHA-256 is
`41a2954c695858aa08adfa46696fdc0b140e47e0683fec4f217c44ca99e8b0d8`.
It contains only each paper's README, main.tex, references.bib and
exact-basename PDF, as repository-relative path, TAB, lowercase SHA-256
and LF, in bytewise path order equivalent to LC_ALL=C, with a final LF.
No ledger file was written. Binary PDF LF counts are not text-line counts.

HEAD and cached origin/main stayed at the declared commit; the index
stayed empty and the same nine declared tracked paths stayed dirty.
AGENTS.md was read completely and matched baseline bytes. Handoff hash
stayed `f8ee2801e45b26b080a406c7548aa852cfa865d3e24deb09f0d868ad147510e8`.
Untracked counts increased from 591 to 614, exactly the 20 authorized
reading-layer/record paths and three scope documents; no starting status
entry disappeared. Generated contents were not read. The primary owns
the broader pre-existing-untracked content check, not this source audit.
Cached remote equality is not an independent live-remote observation.

Actual command families were pwd, Git status/diff/rev-parse, sha256sum,
full AGENTS and restricted handoff reads, rg discovery/heading searches,
wc, complete numbered original-text reads, pdfinfo and complete
pdftotext -layout streams. Reported shell invocations exited zero;
compound-command component exits were not separately observed. An
oversized initial control display was recovered completely. In-memory
preservation audits exited zero at both endpoints, including all 26
captured git-show calls for 12 originals plus AGENTS at each endpoint.
No mandatory original read remains truncated. No source edit, network,
scientific script/JSON/schema review, reproduction, build or render ran.

## Original counts and complete manual PDF locations

| Original source | Text files / raw LF / bytes | PDF pages / bytes |
|---|---:|---:|
| [TPC147](../../papers/tpc-147-tt-periodic-residue-reassembly/main.tex) | 3 / 401 / 14,057 | 4 / 356,532 |
| [TPC148](../../papers/tpc-148-quotient-mobius-fiber-lift/main.tex) | 3 / 435 / 13,340 | 4 / 392,592 |
| [TPC149](../../papers/tpc-149-small-polylog-determinant-two-mobius-corridor/main.tex) | 3 / 500 / 16,262 | 4 / 473,376 |

Lines below refer to each linked root main.tex. Complete layout-text
reads use actual PDF page boundaries, not visual inspection. None of
these sources has subsection, subsubsection or paragraph sectioning.
Preambles, macro definitions and document endings were also read.

| Paper | Complete heading/page coverage and continuations |
|---|---|
| TPC147 | Title L41–48, abstract L53–73 and §1 The exact source contract L75–107: p1. §1 continuation/source estimate and Remark 1.1 L108–129, §2 An exact periodic residue partition L131–163 with Lemma 2.1/proof, and §3 Periodic reassembly without a census loss L165–200 with Theorem 3.1/opening proof: p2. §3 proof continuation L201–211, Corollary 3.2 Products of periodic masks L213–225, §4 What is and is not an l1 cost L227–260 with Proposition 4.1 No prefix promotion/proof, and §5 Certificate and claim boundary L262–297 with full table: p3. References L299–304: p4, one printed entry. Complete README L1–61 and bibliography L1–34 read. |
| TPC148 | Title L39–46, abstract L51–78 and §1 L80–125 with Definition 1.1, Theorem 1.2 Exact quotient recovery/proof and Remark 1.3: p1. §2 L127–179 with Theorem 2.1 Exact determinant-two Mobius lift/proof and Corollary 2.2, plus §3 L181–223 with distance definition, Lemma 3.1 Prime-level perturbation/proof and Proposition 3.2: p2. Proposition 3.2 proof L225–232, Lemma 3.3/proof L234–252, sourced distance L254–261, Corollary 3.4/proof L263–286, and §4 Scope and machine certificate L288–325: p3. References L327–332: p4, all four entries. Complete README L1–67 and bibliography L1–34 read. |
| TPC149 | Title L40–47, abstract L52–85 and §1 Inputs and notation L87–126: p1. §2 L128–195 with Proposition 2.1 One quotient-pair exceptional set/proof and Remark 2.2, plus §3 L197–230 with Lemma 3.1 Unique quotient-pair census/proof and opening Theorem 3.2: p2. Theorem 3.2 continuation/proof L231–278, §4 L280–308 with Proposition 4.1 Where the previous CRT costs went and all three items/proof, and §5 opening L310–319: p3. §5 continuation L320–335 with missing fields/NOT-TESTABLE/interval qualification, §6 Claim boundary L337–371 with full table, and references L373–378: p4, five printed entries. Complete README L1–72 and bibliography L1–48 read. |

## Bounded prerequisites and source qualifications

The following are attributed manuscript statements and archive-scope
qualifications, not independent proofs of the imported theorems. No
paper supplies a complete physical occurrence/outer-coefficient registry,
physical h0 attachment or paid strict-1/400 physical loss ledger.

- **TPC147:** main.tex L79–119 (pp1–2) retains the signed summand
  `(g1(n+h1)-delta_N)g2(n+h2)rho((n-b0)/Q)`, one-bounded multiplicative
  gi and delta_N=0 in the selected nonpretentious branch. Source shifts
  h1!=h2 do not identify physical h0; generic outer gamma_xi are not
  actual physical coefficients. The domain is N<n<=2N in one progression.
  X>=2, 1<=calligraphic-L<=log X, N in [sqrt(X),X] outside the local
  exceptional set, W<=L^c and b,hi=O(L^c) remain explicit. Reassembly
  requires Q,R>=1 and QR<=L^c (L140–210, p2). The local exceptional set
  depends on g1,g2,L and is selected before permitted moduli/residues/
  shifts; it has normalized logarithmic measure <<L^(-c), and is not the
  global affine-Liouville exceptional set (L92–129, pp1–2). Refinement
  preserves residue values rho(r), normalization W/N and native masses
  N/(QR), N/Q. R*N/(QR)=N/Q gives no residue-census exponent, but retains
  ||rho||_infinity and the outer weighted-mass ratio. Products pay their
  combined period corridor, rational phases require exact denominator
  absorption, and generic phases/nonperiodic physical weights remain
  excluded (L213–244, p3). No deterministic endpoint, arbitrary origin/
  interval, all-prefix estimate or fixed-X-power follows (L246–289, p3).
  The source distinguishes exact L0 partition from sourced good-scale
  arithmetic L1; neither is a complete physical theorem.
- **TPC148:** main.tex L82–179 (pp1–2) defines G_c at prime powers by
  (-1)^j below e_p=v_p(c) and mu(p^(j-e_p)) at/above it. The literal
  identities G_c(cm)=mu(m) and mu(D(z))mu(V(z))=G_a(t)G_s(t+2) retain
  Mobius signs and squarefree zeros. Here c,m>=1; a,s are positive odd
  coprime integers; D=d+sz,V=u+az are positive on the integer-z domain;
  t=ad+asz lies in the residue ad modulo as. This pointwise identity
  is not a prefix estimate, and shift two is not physical h0 attachment.
  Remaining packet coprimality, masks, physical weights and prefix factors
  are not removed. The squared pretentious-distance comparison uses
  prime weights 1/p, Y,Q>=2, |v|<=Y and character moduli q<=Q
  (L183–232, pp2–3), with loss at most 2*sum_(p<=Y,p||c)1/p.
  For Y=X^2, Q=(log X)^(1/125), c<=(log X)^A and fixed A>0, the stated
  prime-factor bound is o(log_2 X); the cited Liouville input gives
  (1/3-o(1))*log_2 X. Fixed 0<alpha<1/3 gives L=(log X)^alpha,
  uniformly for sufficiently large X depending on A (L234–286, p3).
  This paper supplies no correlation exceptional-set selection or N-range,
  no physical comparison mass and no physical loss payment. Its exact
  identities, unconditional comparison and sourced quantitative input
  concern the actual Mobius core, not a synthetic replacement; no
  squarefree cutoff/tail is needed for that core, while full H3/L2 and
  fixed-power credit remain excluded (L288–325, p3).
- **TPC149:** main.tex L89–126 (p1) retains mu(d+sz)mu(u+az)rho(z),
  equivalently G_a(t)G_s(t+2)rho(z). Positive a,s,R, integral d,u,
  coprime a,s, odd as and su-ad=2 accompany the domain
  N<ad+asz<=2N. As>0 preserves the arithmetic coordinate order but
  does not prove arbitrary physical-prefix control. Source h1=0,h2=2
  is explicit without a physical attachment (L177–186, p2). The corridor
  asR<=(log X)^eta0 and good N in [sqrt(X),X] hold for sufficiently
  large X; intercepts have no independent height cost. Source W=asR
  is distinct from the imported character modulus. Pair-dependent sets
  E_(a,s;X) are united into one local E_X^star, with no extra union over
  d,u,R,rho,residues or permitted shifts (L133–278, pp2–3). Normalization
  as/N uses natural block mass N/(as), while exceptional-set measure is
  logarithmic. With beta=alpha*c after a possible harmless decrease,
  pair census <=Q(1+log Q), 0<eta0<beta/4 and kappa0=beta/2, the stated
  union pays exponent eta0+o(1), leaving beta-eta0-o(1) exceptional
  saving. No R-census or squarefree-tail exponent appears, but
  ||rho||_infinity remains. Periodic masks/small rational phases are
  admissible; generic phases/nonperiodic physical weights are not.
  Occurrence fields/outer coefficient mass remain REQUIRED_MISSING;
  exceptional-window, deterministic-prefix, physical-weight and four-point
  returns remain unpaid (L280–371, pp3–4). The source claims actual-core
  arithmetic L1 progress while frontier consumption is NOT-TESTABLE;
  fixed-X-power credit is explicitly zero, not a full physical L2 result.

## Bibliography and preserved wording

TPC149 README L10–33 omits the explicit good-scale interval stated in
main.tex L150 and L236 (pp2–3). Main.tex L258–259 (p3) says the union
runs over all ordered pairs, while the sets were introduced for coprime
odd pairs at L135–142 (p2). The source's admissibility restrictions must
be retained; this wording alone is not an unrestricted-pair theorem.

The three complete bibliographies have 4, 4 and 6 entries, with 1, 4
and 5 printed respectively. TPC147 prints only TaoTeravainen2026;
TPC149 omits uncited WangTPC140. All three BibTeX sources record the
same Tao–Teravainen year 2026 and arXiv 2512.01739v2, metadata omitted
by the printed references. TPC148 bibliography L29–34 and TPC149 L36–41
shorten TPC147's original title; TPC149 L43–48 shortens TPC148's title.
These local variants are preserved, not independently reconciled.

Upstream theorem correctness, MRT equation (1.12), primorial/Mertens
estimates and cited out-of-scope frontier/carrier sources were not
verified. Finite certificate descriptions were read, not executed.
Independent original-proof validation, explicit wording reconciliation,
rendered-PDF QA and reliable-full Markdown semantic review remain open.

TPC418 STOP, arithmetic advance NO, fixed-power credit 0 and full Gate B
OPEN remain unchanged. No new research route or paper is authorized.
