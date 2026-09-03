# TPC-371 derivation package

## 1. The finite block object

Let

\[
 I_{a,b}=\{a+256b,\ldots,a+256b+255\},\qquad b=0,\ldots,7,
\]

where `a` is one of the three inherited origins.  For a prime `p` in the
shell `Q<p<=2Q`, put

\[
 B_p(u,t)=p\frac{66^2}{66^2+(u-t)^2}
 \left(\mathbf 1_{p\mid u-t}-\frac1{p-1}\right)
 \mathbf 1_{u\ne t}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid t}.
\]

For `beta in {0,2}` and a declared sign law `epsilon`, define on one block

\[
 A_{a,b,Q,\beta,\epsilon}(u,t)=
 \sum_{Q<p\le 2Q}\epsilon_p\left(\frac pQ\right)^\beta B_p(u,t),
 \quad
 G_{a,b,Q,\beta}(u)=
 \sum_{Q<p\le2Q}\sum_{t\in I_{a,b}}
 \left[\left(\frac pQ\right)^\beta B_p(u,t)\right]^2.
\]

The normalized block matrix is

\[
 T_{a,b,Q,\beta,\epsilon}(u,t)=
 \frac{A_{a,b,Q,\beta,\epsilon}(u,t)}
 {\sqrt{G_{a,b,Q,\beta}(u)G_{a,b,Q,\beta}(t)}}.
\]

The certificate only includes blocks for which the displayed finite geometry
is positive; all 24 declared origin/block pairs pass this check for both beta
values and every shell anchor.

## 2. Exact finite facts

The block partition is an integer partition fixed independently of the
response.  Each entry of `G` is a finite sum of rational squares.  The
resulting matrices are symmetric by construction.  For any finite real
symmetric matrix `T`,

\[
 \|T\|_2\le \max_u\sum_t |T(u,t)|,
 \qquad
 \|T\|_2\le \|T\|_F.
\]

These are the only analytic inequalities used to interpret the recorded
finite envelopes.

## 3. Phase census

The complete panel has `576` rows.  The replay gives:

* beta `2`: `288` rows, zero spectral-cap violations and zero Schur-cap
  violations; the maximum normalized spectral value is
  `0.5536333251967529`;
* beta `0`: `288` rows, `72` spectral-cap violations and `72` Schur-cap
  violations; the maximum normalized spectral value is
  `1.4642797645332997`;
* the beta=2 block-local maximum is therefore below both working caps even
  though the TPC-370 full-window beta=2 panel has six high-Q/all-plus spectral
  failures.

The beta=0 violations are an all-plus control phase.  The beta=2 result is
not a proof that off-block terms are the sole source of the parent signal:
the local normalization changes when the domain changes.  It is a scoped
refutation of the stronger hypothesis that the parent failure is already
present in one independently normalized 256-point block.

## 4. Exact inherited anchor

The interval `[1010346,1010359)` at `Q=4`, exponent `1`, with shell `{5,7}`
is inherited from TPC-370.  It is checked by exact rational arithmetic for
both beta values and is not used to select a block or a main-panel response.

## 5. Scope

The statement is finite and scoped to three origins, one count, eight fixed
blocks per origin, three shell anchors, one exponent, four laws, and two beta
values.  It does not provide a growing operator bound, source-valid
normalization, source-uniform arithmetic `L2`, prime-shell reassembly,
fixed-power credit, Route-A/Route-B closure, or a twin-prime conclusion.
