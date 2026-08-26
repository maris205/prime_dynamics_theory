# Citation verification

The paper uses only source material already locked in the TPC-256 release.

| Input | Role | Local source |
|---|---|---|
| de la Vallée Poussin prime number theorem | `F(y)=Li(y)+O(y exp(-c sqrt(log y)))` | TPC-233 source lock |
| weighted prime-shell PNT | `B_Q=(9/2+o(1))x^(2/3)/log x` | V59/top-prime bridge |
| complete centered Poisson transference | vanishing complete alias and `H^2/q` first moment | V43 bridge |
| exact adjoint diagonal/boundary identity | TPC-255 normal form | TPC-255 bridge |
| ordered-rank Haar convention | coefficient-independent rank split | TPC-253 bridge |

No current web search was needed: the theorem inputs and their provenance are
already present in the repository and are frozen by `notes/source_lock.md`.
The new constants are evaluated by elementary integration and are proved in
the local proof package, not attributed to an external source.
