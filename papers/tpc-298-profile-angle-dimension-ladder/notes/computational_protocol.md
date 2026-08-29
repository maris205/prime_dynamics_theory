# TPC-298 computational protocol

1. Lock the TPC-297 code/result, TPC-295 label result, and frozen TPC-268
   engine by normalized LF SHA-256 hashes.
2. Reconstruct the same 18 rows and physical columns with exact `Fraction`
   arithmetic; form each prefix image before 70-digit conversion.
3. Check every prefix rank modulo `1000000007` and `998244353`.
4. Solve each least-squares problem with 70-digit QR arithmetic, record
   residual, captured fraction, principal-angle sine/cosine, condition number,
   and the first half-RMS dimension.
5. Rebuild the physical columns independently by source-first accumulation in
   a separate checker and verify every stored interval and threshold count.
6. Run exact matrix fixtures for nesting, angle Pythagoras, threshold
   monotonicity, and rank-bookkeeping adversaries.
7. Run normal and optimized Python modes with `PYTHONDONTWRITEBYTECODE=1`,
   require empty stderr, canonical JSON, and a warning-free embedded-font PDF.

No random seed, statistical confidence, asymptotic extrapolation, or power
credit enters the certificate.
