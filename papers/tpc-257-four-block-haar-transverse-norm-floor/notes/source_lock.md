# TPC-257 source lock

The theorem inputs are frozen at the TPC-256 release commit.  The checker reads
these blobs with `git show`, so later handoff/documentation edits cannot alter
the inputs silently.

```text
baseline HEAD = e593b6f85ff16c0c8fc99474ba50e74af4a93b51
```

The complete SHA-256 matrix is embedded in both executable checkers.  The
locked roles are:

| Path | Role |
|---|---|
| `AGENTS.md` | repository release and synchronization protocol |
| `TPC_HANDOFF.md` | TPC-256 current theorem and route state at baseline |
| `research/tpc-big-road/bridge_b_literal_beta_haar_adjoint_asymptotic.md` | prior literal beta midpoint and adjoint asymptotic |
| `research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md` | exact diagonal and boundary normal form |
| `research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md` | coefficient-independent rank geometry |
| `papers/tpc-256-literal-beta-haar-adjoint-asymptotic/PROOF_PACKAGE.md` | prior quantifier and phase firewall |
| `papers/tpc-256-literal-beta-haar-adjoint-asymptotic/notes/source_lock.md` | prior source matrix |
| `research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md` | weighted shell input |
| `papers/tpc-233-critical-depth-row-mass-obstruction/notes/source_lock.md` | strong PNT input |

All new claims beyond those inputs are elementary four-block algebra, the
displayed second-order integral calculation, and the bounded-variation
extension of the already exact TPC-255 compiler.  Numerical samples carry no
proof credit.
