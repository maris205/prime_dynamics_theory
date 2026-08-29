# TPC-298 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T298.1 | `min_c ||V_kc-b||^2=b^T(I-P_k)b` | `PROVED_EXACT_FINITE` | full-column-rank finite prefix |
| T298.2 | `r_k=sin(theta_k)` and `r_k^2+cos^2(theta_k)=1` | `PROVED_EXACT_FINITE` | finite Euclidean image |
| T298.3 | `range(V_k) subseteq range(V_{k+1})`, hence residual/angle monotonicity | `PROVED_EXACT_FINITE` | declared ordered ladder |
| T298.4 | every prefix rank is `min(k,|S|)` under both moduli | `NUMERICALLY_CERTIFIED_FINITE` | 18 rows, 1,380 edges |
| T298.5 | weighted half-RMS prefix fraction is at least `2/3` on 18/18 rows | `NUMERICAL_OBSERVATION` | threshold `1/2`, finite grid |
| T298.6 | all-positive half-RMS prefix dimension is at most 6 on 18/18 rows | `NUMERICAL_OBSERVATION` | threshold `1/2`, finite grid |
| T298.7 | last prefix reaches every registered finite target | `NUMERICALLY_CERTIFIED_FINITE` | rank equals shell size |
| T298.8 | arithmetic `L2`, Gate B, and twin-prime endpoint | `OPEN/NONE` | outside finite angle audit |
