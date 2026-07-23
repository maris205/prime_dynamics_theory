# TPC-75: primal-dual completion certificates

This paper turns the analytic completion gate of TPC-73 and the direct
entry kernels of TPC-74 into an exact finite-dimensional optimization
problem.

## Main results

- The complete divisor-variation cost is exactly an \(\ell^1\)-norm
  \(\|A_DF\|_1\) of a finite linear analysis operator.
- The minimum cost over all completions of one primitive datum is attained
  and has the strong dual
  \[
  \gamma_D(k)=
  \max\{\operatorname{Re}\langle\lambda,k\rangle:
  A_D^*z=R^*\lambda,\ \|z\|_\infty\le1\}.
  \]
- Thus every low-cost construction has an exact alternative: a
  checkable dual obstruction witness.  The completion gauge is a quotient
  seminorm whose nullspace is \(R(\ker A_D)\).
- For the fixed post-\(q\) TPC-74 Hermitian row-pair family, independent completion classes
  have no hidden joint gain:
  \[
  \inf_{\boldsymbol F}\rho(P(\boldsymbol F))=\rho(Q^\gamma),
  \qquad Q^\gamma_{mn}=\gamma_{mn}.
  \]
- A genuine joint problem begins only when a declared \(q\)-compatible
  rule couples different row pairs.  The paper gives the exact
  fixed-weight primal and dual for every affine coupled rule at fixed
  finite stacked data.  Uniformity over a growing coefficient class
  remains a separate minimax problem.
- Every absolute-value completion majorant lies above the exact
  \(|H|\)-Perron floor.  A symmetric Hadamard example proves that this
  floor can remain order one while the signed operator norm tends to zero;
  failure of the completion certificate is therefore not failure of
  arithmetic cancellation.

## Claim boundary

The exact duality and quotient geometry are L0.  Attaching them to every
literal direct-entry kernel of the normalized missing-native Gram is L1.
No physical smallness of the optimum, Mertens saving, fixed-\(2\) result,
parity breaking, prime-pair estimate, or twin-prime theorem is claimed.

The archival PDF is `primal-dual-completion-certificates.pdf`.

## Build

Run `pdflatex main.tex`, `bibtex main`, and then `pdflatex main.tex`
twice.  The generated `main.pdf` is ignored; the archival PDF is tracked.
