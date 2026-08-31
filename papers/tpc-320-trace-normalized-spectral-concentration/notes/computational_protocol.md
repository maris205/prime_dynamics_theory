# TPC-320 computational protocol

- Source intervals: \(I_X=\{X/2+1,\ldots,X\}\), for
  \(X=640,1280,2560\).
- Height: \(H=66\); shell:
  \(\mathcal S_Q=\{p\ {\rm prime}:Q<p\leq2Q\}\), with
  \(Q=24,36,54,80\).
- Kernel exponents: \(s=1,2\); total rows: \(3\cdot4\cdot2=24\).
- Concentration sizes: \(k=1,2,4,8,16\); adjacent transitions:
  \(2\cdot4\cdot2\cdot5=80\).
- Every row is accumulated in forward and reverse shell order.
- SciPy eigh reads the top 17 eigenvalues; NumPy eigvalsh supplies the
  full-spectrum path.  The independent checker uses a reversed einsum
  accumulation and a fresh full eigensolve.
- The declared literal bound is \(\lvert K\rvert\leq160\).  The finite guard
  combines binary64 entrywise error, solver spread, residual, and Weyl's
  inequality; quotient endpoints use \(F_k^-/T^+\) and \(F_k^+/T^-\).
- Stable rank, participation rank, and entropy are recomputed from the full
  spectrum and labeled observations.  No random input or external data is
  used.
- Normal and optimized Python runs are required to emit byte-identical
  deterministic check output.
