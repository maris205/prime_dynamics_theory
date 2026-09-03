# TPC-372 derivation package

## 1. Common-normalization decomposition

For each inherited origin `a`, let `I_a=[a,a+2048)` and let
`T_{a,Q,beta}` be the normalized all-plus matrix formed from the literal
prime-shell operator and the full-window square-energy geometry.  Let
`P_0` be the fixed block mask

\[
 (P_0)_{ij}=1\quad\Longleftrightarrow\quad
 \left\lfloor i/256\right\rfloor=left\lfloor j/256\right\rfloor,
 \qquad 0\leq i,j<2048.
\]

TPC-372 defines

\[
 D=P_0\odot T,\qquad R=(1-P_0)\odot T,
 \qquad T=D+R.
\]

The same full-window geometry is used for `T`, `D`, and `R`; only the entries
are split.  Thus this decomposition does not introduce the normalization
change present in the TPC-371 block-local audit.

## 2. Finite inequalities

The identity `T=D+R` is exact at the finite matrix level.  For any operator
norm,

\[
 \|R\|_2\geq\|T\|_2-\|D\|_2,
 \qquad
 \|T\|_2\leq\|D\|_2+\|R\|_2.
\]

The certificate records the true symmetric spectral norms, Schur envelopes,
Frobenius norms, extremal eigenvalues, and the numerical reconstruction error.

## 3. Frozen panel and result

The panel contains all three inherited origins, all `Q` values
`512,2048,8192`, beta `0,2`, exponent one, and the inherited all-plus law:
`18` rows in total.  No component or row is selected by its observed norm.

For beta=2, the full matrix has six spectral-cap failures (the same high-`Q`
support as TPC-370), while the block-diagonal part has zero failures and the
off-block part has zero failures.  The block-diagonal beta=2 maximum is
`0.51702415681590108`; the off-block maximum is `0.26329369743038339`; the
full maximum is `0.71099989528234753`.  On each of the six failing rows,
the reverse triangle inequality certifies a positive required off-block
lower bound, ranging around `0.1936--0.1940` (the certificate retains every
row value).

Thus neither component alone crosses the cap on beta=2, yet their sum does.
This is a finite coherence/synergy observation, not a claim that the
off-block component is causally responsible.

## 4. Exact inherited anchor and scope

The anchor `[1010346,1010359)` at `Q=4`, exponent one, shell `{5,7}` is
inherited from TPC-371 and checked by exact rational arithmetic.  The
decomposition is scoped to the three origins, one count, three shell scales,
one law, and two beta values.  It proves no origin/window uniformity, growing
operator estimate, source-valid normalization, arithmetic `L2`, fixed-power
saving, prime-shell reassembly, Route-A/Route-B closure, or twin-prime result.
