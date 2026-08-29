# TPC-299 computational protocol

1. Lock the TPC-298 code/result, TPC-295 target labels, and frozen TPC-268
   engine by normalized LF SHA-256 hashes.
2. Reconstruct the literal profile matrix and physical columns exactly over
   `Fraction`; form `V_k=A^T U_k` and `M_k=U_k^T U_k`.
3. Replay every least-squares prefix at 70 decimal digits and locate the
   first normalized RMS threshold `1/2`.
4. At each first threshold and at the full available prefix, solve the
   source-norm frontier by deterministic bisection on the KKT multiplier.
5. Independently rebuild physical columns source-first, recompute all
   prefix residuals and frontier values, and check interval containment.
6. Run exact small rational/analytic fixtures for active constraints,
   nested-budget monotonicity, infeasibility, and the zero-budget limit.
7. Require canonical JSON, provenance locks, normal/optimized agreement,
   empty standard error, and a warning-free embedded-font PDF.

No random seed, statistical confidence, asymptotic extrapolation, or
fixed-power credit enters the certificate.
