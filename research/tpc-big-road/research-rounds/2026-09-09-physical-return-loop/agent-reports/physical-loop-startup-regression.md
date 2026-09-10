# TPC_AGENT_RESULT_V1

task_id: `physical-loop-startup-regression`  
role: `tpc_release_qa`  
mode: `READ_ONLY_RESEARCH_AND_AUDIT`  
verdict: `PASS_CURRENT_STARTUP_SUITE_WITH_INHERITED_LIMITATIONS`  
proof_verdict: `FINITE_INTEGER_MODEL_SUPPORTED; PHYSICAL_TRANSFER_UNPAID`  
publication_GO: `NONE`  
files_changed: `[]`

The startup regression passes on the supplied new handoff baseline. The scoped TPC417/418 tracked scientific artifacts and wrapper remain identical to the unchanged HEAD underlying the preceding round. No repair, regeneration, build, synchronization, staging, publication, external upload, or subagent creation occurred.

## Execution evidence — diagnostics

I completely inspected all four invoked sources before execution:

- [Producer:1](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/code/tpc418_c1_shell_parity_envelope.py:1): standard-library imports; writing occurs only through the mutually exclusive `--write` branch at line 296. `--check` compares an in-memory reconstruction.
- [Independent checker:1](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/experiments/tpc418_independent_checker.py:1): reads certificates; no producer import or filesystem writing.
- [Stress checker:1](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/experiments/tpc418_adversarial_certificate_stress.py:1): mutations are in memory.
- [Wrapper:13](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py:13): hashes artifacts and executes only the six prescribed child checks.

Actual top-level commands, **both exit 0**, Python **3.12.3**:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py --check
```

Both returned exactly:

```text
TPC418_BRIDGE_CHECK=PASS fixtures=3 sigma=PASS independent=PASS stress=PASS paper_artifacts=PASS strict_firewall=PASS
```

Coverage is **8 distinct required command/mode forms**, implemented by **2 top-level wrapper executions plus 12 child executions**—14 suite-process executions, not eight separately issued top-level commands. Each wrapper executes producer, independent, and stress in normal and optimized modes. Success requires every child exit 0, empty child stderr, and matching normal/optimized stdout. See [wrapper:14](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py:14) and [current command list:952](/root/autodl-tmp/math_research3/prime_dynamics_theory/TPC_HANDOFF.md:952).

No TPC417 executable, broad pytest discovery, or unsafe TPC27–32 script was run.

## Scientific and validation boundaries

**First fatal mismatch:** none for the requested startup replay. For promotion to physical arithmetic, the first fatal mismatch remains **missing identification of literal physical coefficients, signs, masks, and outer \(q\)** with the alternating CRT model. Neither a model norm bound nor checker agreement supplies that identification.

**Strongest reproducibility objection:** inherited evidence remains shared. Both implementations regenerate shell/parity information but reuse TPC417’s large four-shell aggregate and matrix rows. This is not fresh independent recomputation of those rows. Sources: [producer:211](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/code/tpc418_c1_shell_parity_envelope.py:211), [independent:49](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/experiments/tpc418_independent_checker.py:49), and independent lines 74–81.

**Validator limitation retained:** the stress suite contains nine certificate mutations and two parser-rejection cases, not comprehensive schema or physical-contract validation. Its mutation list has no height mutation despite [protocol:11](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/notes/computational_protocol.md:11). Source inspection confirms that standalone `validate` does not enforce height or `PHYSICAL_H0`, and its `sigma_j in (-1,1)` comparison permits Boolean/integer equality. The preceding round’s accepted Boolean-sigma, changed-height, and physical-firewall probes remain explicitly **standalone-validator findings**, not demonstrated escapes through the complete hash-locked suite. [Stress:17](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/experiments/tpc418_adversarial_certificate_stress.py:17); [prior QA:66](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-multi-agent-recon/agent-reports/recon418-regression.md:66). Those extra probes were not rerun here.

**PDF limitation retained:** `paper_artifacts=PASS` means required-file presence and SHA-256 identity. It does not certify compilation, log semantics, text/fonts, rendering, or visual inspection. The wrapper actually requires both PDFs; the README’s “when they are available” wording is weaker than execution behavior. [Wrapper:8](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py:8).

**Proof assessment—my derivation from the inspected sources:** increasing amplitudes give the corrected block sign
\(\sigma_j=\epsilon_j(-1)^{n_j+1}\). Adjacent pairing and alternating odd-block signs support
\[
|A|\le B_*<3E+4\lceil O/2\rceil\le3K+1.
\]
The inherited star/bulk decomposition then supports the finite operator bound. [TPC418 proof:83](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md:83).

The prior domain caveats remain: integer \(Q_j\) is required; [proof:122](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md:122) unnecessarily states \(N<Q_j<p\), which some small fixtures violate. The sufficient condition \(|r-s|<N<p\) holds. This wording defect does not defeat the scoped bound.

**Closest existing result:** TPC417’s finite four-shell full-operator bound, explicitly inherited at [TPC417 proof:43](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-417-c1-four-shell-finite-operator-bound/PROOF_PACKAGE.md:43).

## Seven physical fields

1. **Literal object:** the inspected model uses zero-based alternating signs, amplitudes \(\alpha_i=p_i^3/[Q_i^2(p_i-1)]\), kernel \(T_d=H^2/(H^2+d^2)\), CRT assignments \(p_{\rm even}\mid o\), \(p_{\rm odd}\mid o+N\), and exact diagonal deletion. Its off-diagonal entries are \(M_{0r}=P_-T_r\), \(M_{rs}=-AT_{r-s}\) for interior coordinates. Physical coefficients and outer-\(q\) attachment are absent; the model star vector named \(q\) is not that outer label. [TPC417 main.tex:20](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-417-c1-four-shell-finite-operator-bound/paper/main.tex:20).
2. **Fixed shift:** physical \(h_0=2\) is not identified. Model height \(H\) is neither that shift nor a conductor.
3. **Domain/order:** disjoint complete prime shells, \(2Q_j\le Q_{j+1}\), increasing primes and global concatenation; coordinates \(r=0,\ldots,N-1\). No exact physical cumulative-prefix order is attached.
4. **Ranges:** integer \(Q_j\ge2,H\ge1\), \(N=4H\), finite \(K\ge1\), nonempty shells, \(L\ge2\), all selected \(p>N\). Replay heights: four-shell \(16,32,66,128\); small \(1,2,4\); mixed \(1\). Physical \(X,N,q\) ranges and their relationship to these parameters are unpaid. [Producer:26](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/code/tpc418_c1_shell_parity_envelope.py:26).
5. **Uniformity/exceptions:** explicit deterministic finite inequalities; this replay establishes no physical uniformity or exceptional-set theorem.
6. **Normalization:** \(Z=D^{-1/2}MD^{-1/2}\), with exact model row energies and \(V_-=\sum_{\rm odd}\alpha_i^2\). This is not an identified physical natural scale.
7. **Exponent budget:** the bound is \(2/(a_{\min}\sqrt H)+16B_*/V_-\). No complete physical reweighting, coverage, prefix, normalization, or loss ledger establishes strict \(\delta>1/400\); fixed-power credit remains zero.

Location: island **②**, a model operator subproblem relevant to image **Bridge A**. Neither analytic Gate A/B nor the dynamics/C bridge is closed. The new handoff reports two verified scoped model-growth regimes; its historical TPC418 tags must not negate those newer results. Their physical transfer remains unpaid, and their proofs were not reaudited in this task. [Handoff:15](/root/autodl-tmp/math_research3/prime_dynamics_theory/TPC_HANDOFF.md:15).

## Preservation and command record

Start/end:
`HEAD=origin/main=ab23455ba941e5a14ded27d49de0e874aee811ac`.

Control SHA-256 values matched the task at both endpoints:

```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
research/tpc-big-road/TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
```

Start/end status was byte-identical: **10 tracked dirty, 631 untracked, empty index**. No authorized parent additions were observed by the final check.

All **41 files** in the two paper directories had identical start/end SHA-256 manifests. The wrapper and preceding QA report also remained unchanged. Scoped tracked differences against HEAD were empty. Together with the preceding QA’s unchanged-HEAD/source record, this confirms no scoped tracked scientific-artifact change since that round. The four untracked `.aux`/`.log` files are verified unchanged **during this task**; their historical individual hashes were not published in the prior report.

Preservation commands all exited **0**:

```bash
git rev-parse HEAD origin/main
git --no-optional-locks status --porcelain=v1 --untracked-files=all
git --no-optional-locks diff --name-only
git diff --cached --name-only
git --no-optional-locks diff --name-only HEAD -- papers/tpc-418-c1-shell-parity-envelope papers/tpc-417-c1-four-shell-finite-operator-bound research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py
rg --files --hidden --no-ignore -0 papers/tpc-418-c1-shell-parity-envelope papers/tpc-417-c1-four-shell-finite-operator-bound | sort -z | xargs -0 sha256sum
```

The explicit control/wrapper/report `sha256sum`, scoped `git ls-files`/status, source-reading `sed`/`nl`/`wc`/`rg --files`, Python version, and process-status commands also exited 0.

Files read: required startup instructions/guide/handoff excerpts; four check sources; cited TPC417/418 proof/model/protocol/README files; prior QA report; runtime check dependencies. Other scoped artifacts were hashed only. External primary URLs: **none invoked**. ARS reproducibility guidance was applied inline and read-only; its 11 statistical-fallacy categories were considered inapplicable to this deterministic rational replay.

**No-GO boundary:** retain TPC418 as formal endpoint. This result authorizes no repair, numbered writer, gate closure, or arithmetic-advance claim.
