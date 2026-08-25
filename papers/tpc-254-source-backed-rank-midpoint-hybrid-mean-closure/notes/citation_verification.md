# Citation Verification

The paper cites external works only for their typed upstream roles:

| citation | verified role in the frozen compiler | not claimed here |
|---|---|---|
| Ford--Maynard, *On the Theory of Prime-Producing Sieves*, arXiv:2407.14368 | prime-producing sieve architecture and upstream parameter order | does not prove the TPC-254 adjoint form |
| Bombieri, *On the Large Sieve* | classical Bombieri--Vinogradov input behind the source-backed prime-progression remainder | not used at the endpoint `gamma=1/2` |
| Montgomery--Vaughan, *The Large Sieve* | classical large-sieve background for the maximal Bombieri--Vinogradov route | not a fixed-Haar V59 theorem |
| Vaughan, *Sommes trigonométriques sur les nombres premiers* | upstream Type-I/Type-II decomposition context | not invoked to turn logarithmic saving into power saving |
| Iwaniec, *Rosser's Sieve* | upper/lower fundamental-lemma weights in the hybrid comparison compiler | not a proof of the literal adjoint lane |

The precise corollary used by TPC-254 is source-locked to
`research/tpc-big-road/fm_local_comparison_compiler.md` at SHA-256
`4f7537ff5a10d53634638afff508ee6e3401364dab7970852b327470918c644f`.
TPC-254 does not reprove maximal Bombieri--Vinogradov, the Rosser--Iwaniec
fundamental lemma, or the Ford--Maynard framework; it proves the deterministic
rank-child attachment after those inputs.

The internal TPC-253 predecessor is cited only for the exact rank-midpoint
Haar identity and adjoint orientation. Bibliographic metadata and external
links were inherited from the frozen compiler and already-used repository
bibliographies; no broader literature-absence claim is made.
